"""Chạy tutor trên toàn bộ dataset -> results.jsonl (kèm latency, tokens, chi phí).

Cách dùng:  python3 eval/run_eval.py [dataset.jsonl]
Mặc định đọc dataset.jsonl ở root repo; nếu chưa có thì copy data/dataset.example.jsonl làm mẫu.
Chạy TUẦN TỰ (không song song) để dễ đọc log và tránh vượt rate limit.

Tracing (bài lab yêu cầu): đặt BRAINTRUST_API_KEY hoặc LANGSMITH_API_KEY trong .env —
mỗi câu hỏi sẽ được log thành một trace trong project "ai-evaluation" (xem lại tool
calls, tokens, cost trên app.braintrust.dev / smith.langchain.com). Không có key thì
bỏ qua lặng lẽ. Chi tiết trong README.md mục Tracing.
"""
import json, os, sys, time
from pathlib import Path

import requests

# tutor.py nằm ở tutor/ (khu vực sản phẩm) — thêm vào sys.path để import được
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tutor"))

import tutor
import tracing

# --- Tracing (tuỳ chọn): Braintrust hoặc LangSmith, log mỗi câu thành 1 trace
_tracer = tracing.init_tracer()

# Bảng giá USD / 1M tokens (input, output) — theo platform constants.ts
PRICING = {"deepseek-v4-flash": (0.44, 1.32), "gpt-4o-mini": (0.15, 0.60)}
TARGET = os.environ.get("EVAL_TARGET", "vlearn").strip().lower()

def estimate_cost_usd(model, usage):
    """Ước tính chi phí 1 lượt chạy; model lạ (chưa có giá) thì trả None."""
    short = model.split("/")[-1]
    if short not in PRICING:
        return None
    p_in, p_out = PRICING[short]
    return round((usage.get("prompt_tokens", 0) * p_in
                  + usage.get("completion_tokens", 0) * p_out) / 1_000_000, 8)

def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _p041_chat_url():
    """Return the Nova chat endpoint, allowing a full endpoint override for deployments."""
    explicit_url = os.environ.get("P041_CHAT_URL", "").strip()
    if explicit_url:
        return explicit_url
    base_url = os.environ.get("P041_BASE_URL", "http://localhost:8000").rstrip("/")
    return base_url + "/api/v1/assistant/chat"


def call_p041(row):
    """Run one text-chat scenario against the authenticated Nova/P-041 assistant API.

    The eval-kit report expects the tutor-like fields ``answer``, ``sources`` and
    ``followup_questions``. Nova's API uses a different response contract, so this
    adapter keeps its full response in ``raw_content``/``p041`` and maps the visible
    reply into that common report shape.
    """
    token = os.environ.get("P041_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Thiếu P041_ACCESS_TOKEN. Đăng nhập P-041 và đặt JWT access token vào .env.")

    metadata = row.get("metadata") or {}
    payload = {
        "message": row["input"],
        "history": metadata.get("p041_history") or [],
        "current_page": metadata.get("p041_current_page")
                        or os.environ.get("P041_CURRENT_PAGE", "dashboard"),
        "timezone": os.environ.get("P041_TIMEZONE", "Asia/Bangkok"),
    }
    timeout_s = float(os.environ.get("P041_TIMEOUT_S", "60"))
    started_at = time.perf_counter()
    response = requests.post(
        _p041_chat_url(),
        json=payload,
        headers={"Authorization": "Bearer " + token},
        timeout=timeout_s,
    )
    latency_s = round(time.perf_counter() - started_at, 3)
    response.raise_for_status()
    data = response.json()

    actions = data.get("suggested_actions") or []
    sources = []
    for action in actions:
        for source in action.get("sources") or []:
            sources.append({
                "doc_id": source.get("source_type", "p041"),
                "section_id": source.get("source_id", ""),
                "quote": source.get("quote", ""),
                "title": source.get("title", ""),
                "provenance": source.get("provenance", ""),
            })

    output = {
        "scope": "p041_chat",
        "answer": data.get("response", ""),
        "sources": sources,
        "followup_questions": [],
    }
    meta = {
        "raw_content": json.dumps(data, ensure_ascii=False),
        "latency_s": latency_s,
        "provider": data.get("provider"),
        "model": data.get("model"),
        "llm_succeeded": data.get("llm_succeeded"),
        "suggested_actions": actions,
        "conversation_id": data.get("conversation_id"),
    }
    return output, meta

def main():
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else "dataset.jsonl"
    if not os.path.exists(dataset_path):
        sys.exit("Không thấy %s. Tạo bằng: cp data/dataset.example.jsonl dataset.jsonl"
                 % dataset_path)
    if TARGET not in ("vlearn", "p041"):
        sys.exit("EVAL_TARGET chỉ nhận 'vlearn' hoặc 'p041'.")
    if TARGET == "vlearn" and not tutor.get_api_key():
        sys.exit("Chưa có API key cho model %s.\n"
                 "Tạo file .env trong thư mục eval-kit (xem .env.example), ví dụ:\n"
                 "  DEEPSEEK_API_KEY=sk-...   (cho model deepseek/*)\n"
                 "  OPENAI_API_KEY=sk-...     (cho model openai/*)\n"
                 "rồi chạy lại." % tutor.MODEL)

    rows = read_jsonl(dataset_path)
    if TARGET == "p041":
        if not os.environ.get("P041_ACCESS_TOKEN", "").strip():
            sys.exit("Thiếu P041_ACCESS_TOKEN trong .env. Xem .env.example để cấu hình Nova/P-041.")
        print("Dataset: %d câu | target: Nova/P-041 | endpoint: %s" % (len(rows), _p041_chat_url()))
    else:
        print("Dataset: %d câu | model: %s" % (len(rows), tutor.MODEL))
    results, total_cost, t_start = [], 0.0, time.time()

    for i, row in enumerate(rows, 1):
        q = row["input"]
        print("[%d/%d] %s ... " % (i, len(rows), q[:60]), end="", flush=True)
        rec = {"scenario_id": row.get("scenario_id") or row.get("id") or "row-%d" % i,
               "input": q,
               "expected_scope": row.get("expected_scope"),
               "metadata": row.get("metadata") or {}}
        slide = (row.get("metadata") or {}).get("slide")
        if slide:
            rec["slide"] = slide  # giữ lại để judge/report chấm theo đúng bối cảnh
        try:
            if TARGET == "p041":
                output, meta = call_p041(row)
                cost = None
                rec.update(output=output, raw_content=meta["raw_content"],
                           latency_s=meta["latency_s"], cost_usd=cost,
                           p041={k: v for k, v in meta.items() if k not in ("raw_content", "latency_s")})
            else:
                output, meta = tutor.call_tutor(q, slide=slide)
                cost = estimate_cost_usd(tutor.MODEL, meta["usage"])
                rec.update(output=output, raw_content=meta["raw_content"],
                           retrieved=meta["retrieved"], latency_s=meta["latency_s"],
                           usage=meta["usage"], cost_usd=cost)
            total_cost += cost or 0
            _tracer.log_run(  # log trace: input, output, tool calls, tokens, cost
                name="tutor-run",
                inputs={"question": q, "slide": slide,
                        "target": TARGET,
                        "model": meta.get("model") if TARGET == "p041" else tutor.MODEL},
                outputs=output,
                metadata={"steps": meta.get("steps"), "scenario_id": rec["scenario_id"],
                          "target": TARGET},
                metrics={**({k: v for k, v in meta.get("usage", {}).items()
                             if isinstance(v, (int, float))}),
                         "latency_s": meta["latency_s"],
                         **({"cost_usd": cost} if cost else {})},
            )
            if TARGET == "p041":
                print("ok (%.1fs, model=%s, llm=%s)" % (
                    meta["latency_s"], meta.get("model") or "?", meta.get("llm_succeeded")))
            else:
                print("ok (%.1fs, %s tok, $%s)" % (
                    meta["latency_s"], meta["usage"].get("total_tokens", "?"),
                    "%.6f" % cost if cost is not None else "?"))
        except Exception as e:  # lỗi 1 câu không được làm chết cả batch
            rec.update(error=str(e))
            print("LỖI: %s" % e)
        results.append(rec)

    with open("results.jsonl", "w", encoding="utf-8") as f:
        for rec in results:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("\nXong: ghi %d dòng vào results.jsonl | tổng %.1fs | chi phí ~$%.6f"
          % (len(results), time.time() - t_start, total_cost))
    if _tracer.backend:
        _tracer.flush()
        print("Đã log %d trace lên %s (project '%s')."
              % (len(results), _tracer.backend,
                 os.environ.get("BRAINTRUST_PROJECT") or os.environ.get("LANGSMITH_PROJECT")
                 or "ai-evaluation"))
    print("Bước tiếp: python3 eval/judge.py (chấm tự động) hoặc python3 eval/report.py (xem report)")

if __name__ == "__main__":
    main()

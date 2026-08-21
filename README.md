# Track 1 Day 21 — AI Evaluation

## Thông tin cá nhân và nhóm

- Học viên: **Nguyễn Minh Quân**
- Mã học viên: **2A202601478**
- Sản phẩm được đánh giá: **VLearn AI Tutor**
- Nhóm: Nguyễn Minh Quân, Vũ Đình Huy, Đào Văn Đạt
- Eval Pack dùng chung: mã nguồn trong `eval/`, `tutor/`, `tests/` và `data/`
- Trace: [Braintrust project](https://www.braintrust.dev/app/Henry%20Ng/p/track1-day21-2A202601478/logs)

## Sáu phase và artifact

| Phase | Quyết định | Artifact chính |
| --- | --- | --- |
| 1. Coverage | Chọn 25 scenarios có in-scope, ambiguous, out-of-scope, high-risk và adversarial. | `deliverables/evidence/dataset-v1.jsonl` |
| 2. Human baseline | Ba thành viên chấm độc lập trước khi chốt nhãn vàng. | `labels-*-v3.csv`, `agreement-v3.txt`, `labels-v3-final.csv` |
| 3. Rubric & routing | Tách code checks, LLM assist và expert review theo mức độ xác định được của tiêu chí. | `deliverables/REPORT.md` mục 3–4 |
| 4. Calibration | Calibrate riêng groundedness và follow-up; groundedness chưa đủ tin để auto-gate. | `judge-prompt-*`, `verdicts-*`, summary files |
| 5. Gate | Chốt threshold trước candidate tiếp theo; đọc scorecard theo slice. | `thresholds-v4.md`, `scorecard-v3.md`, `code-checks-v4.txt` |
| 6. Verdict | Hold candidate v3 vì quote và scope chưa đạt ngưỡng critical. | `deliverables/REPORT.md` mục 7 |

## Đóng góp của tôi

Tôi chấm độc lập 25 output của tutor, ghi lý do pass/fail/uncertain trong nhãn cá nhân, tham gia chốt evidence và kiểm tra cấu trúc bài nộp. Tôi cũng thiết lập project Braintrust cá nhân, kiểm tra tracing và tổng hợp report cá nhân dựa trên evidence của nhóm.

## Verdict của nhóm

**HOLD — không ship candidate v3.** Quote nguyên văn đạt 80% và scope đúng kỳ vọng đạt 84%, đều thấp hơn threshold 96%. Groundedness judge không ổn định qua ba vòng calibration, vì vậy chỉ được dùng làm LLM assist, không phải auto-gate.

## Áp dụng cho dự án thực tế

Với dự án P-041, tôi sẽ xác định slices có rủi ro trước khi viết test, giữ version cho mọi input/output, chấm độc lập trước khi dùng LLM judge, và chỉ ship sau khi threshold được chốt trước có evidence theo từng slice.

## Chạy lại Eval Pack

```powershell
python eval\run_eval.py
python eval\code_checks.py
python eval\report.py
```

Không commit `.env` hoặc API key. Data thô và quyết định được lưu trong `deliverables/`.

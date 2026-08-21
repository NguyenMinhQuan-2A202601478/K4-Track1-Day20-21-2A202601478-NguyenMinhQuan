# Evidence index

Mỗi phase phải có đầu vào, đầu ra và quyết định tương ứng trong `REPORT.md`. Không ghi đè artifact cũ: một run mới phải có version mới.

| Phase | Input | Output thô | Quyết định/evidence |
| --- | --- | --- | --- |
| 1 | `dataset-v1.jsonl` | — | Coverage ghi trong REPORT mục 1–2. |
| 2 | `results-v3.jsonl` | `labels-quan-v3.csv`, `labels-huy-v3.csv`, `labels-dat-v3.csv` | `agreement-v3.txt`, `labels-v3-final.csv`. |
| 3 | Các nhãn bất đồng Phase 2 | — | Rubric và routing trong REPORT mục 3–4. |
| 4 | `judge-prompt-grounded-v*.md`, `judge-prompt-followup-v*.md` | `verdicts-grounded-v*.jsonl`, `verdicts-followup-v*.jsonl` | Các summary và analysis calibration. |
| 5 | `thresholds-v4.md` | `code-checks-v4.txt` | `scorecard-v3.md`. |
| 6 | Toàn bộ evidence trên | — | Verdict HOLD trong REPORT mục 7. |

`braintrust-link.md` trỏ tới trace của các run tutor/judge. `results.jsonl`, `labels.csv` và `verdicts.jsonl` ở root chỉ là scratch; chỉ snapshot có version trong thư mục này mới là evidence nộp bài.

# Code checks v1 — 25 outputs

Lệnh chạy: `python eval/code_checks.py`.

| Check | Pass | Fail |
|---|---:|---:|
| `schema_valid` | 25 | 0 |
| `citation_exists` | 25 | 0 |
| `quote_verbatim` | 20 | 5 |

Các case fail `quote_verbatim`: `eval-v3-06-trace`, `eval-v3-09-code-vs-judge`,
`eval-v3-10-code-checks`, `eval-v3-16-expert-evidence`, `eval-v3-18-monitoring`.

Diễn giải: mọi output đều đúng contract và trỏ tới nguồn tồn tại, nhưng năm quote
không xuất hiện nguyên văn trong section được cite. Đây là tín hiệu fail của code
check; khi chốt nhãn vàng, con người vẫn cần xem answer có bám nguồn về mặt ngữ nghĩa
hay không.

# Groundedness judge v2 — calibration analysis

Nguồn dữ liệu: `labels-grounded.csv` (14 pass, 2 fail, 9 uncertain) và
`verdicts-grounded-v2.jsonl`.

## Confusion matrix

Hàng là judge, cột là nhãn groundedness của người.

| Judge \ Human | pass | fail | uncertain |
|---|---:|---:|---:|
| pass | 14 | 1 | 8 |
| fail | 0 | 1 | 1 |
| uncertain | 0 | 0 | 0 |

- Agreement: **15/25 = 60%**.
- Nhận đúng pass: **14/14 = 100%**.
- Bắt đúng fail: **1/2 = 50%**.
- Nhận đúng uncertain: **0/9 = 0%**.
- Verdict ngoài contract: **0** (v1 có 1 case `out_of_scope`).

## So với v1

| Chỉ số | v1 | v2 |
|---|---:|---:|
| Agreement | 52% | 60% |
| Nhận đúng pass | 11/14 | 14/14 |
| Bắt đúng fail | 1/2 | 1/2 |
| Nhận đúng uncertain | 1/9 | 0/9 |
| Verdict ngoài contract | 1 | 0 |

## Kết luận

V2 sửa được contract verdict và giảm false fail cho các case pass, nhưng judge trở nên
quá dễ: cho pass 8/9 case mà nhãn người là uncertain, đồng thời vẫn bỏ sót
`eval-v3-10-code-checks` là fail. Agreement tăng không đồng nghĩa judge đáng tin hơn.

Vòng tiếp theo cần ưu tiên tăng khả năng nhận `uncertain`: thêm 2–3 near-miss có
evidence gián tiếp/lạc đề, quy tắc “khi claim chính chưa có source trực tiếp thì chọn
uncertain”, và giữ ví dụ fail `eval-v3-10` để judge không chỉ nhìn thấy source liên
quan chung chung rồi cho pass.

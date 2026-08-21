# Scorecard v3 — baseline trước candidate v4

## Tổng quan

| Chỉ số | Kết quả |
|---|---:|
| Human final pass | 12/25 = 48% |
| Human final fail | 3/25 = 12% |
| Human final uncertain | 10/25 = 40% |
| Tổng cost | $0.021926 |
| Latency trung bình | 5.11 giây |
| P95 latency | 6.63 giây |
| Tổng token | 124,809 |

## Code checks v4

| Check | Kết quả |
|---|---:|
| `schema_valid` | 25 pass / 0 fail |
| `citation_exists` | 25 pass / 0 fail |
| `quote_verbatim` | 20 pass / 5 fail |
| `scope_matches_expected` | 21 pass / 4 fail |
| `in_scope_has_sources` | 25 pass / 0 fail |

## Slice breakdown theo nhãn human final

| Slice | N | Pass | Fail | Uncertain |
|---|---:|---:|---:|---:|
| In-scope | 19 | 8 | 1 | 10 |
| Out-of-scope | 4 | 3 | 1 | 0 |
| Unclear | 2 | 1 | 1 | 0 |
| Representative | 11 | 4 | 1 | 6 |
| Challenge | 6 | 3 | 1 | 2 |
| High-risk | 6 | 4 | 0 | 2 |
| Risk high | 13 | 6 | 1 | 6 |
| Risk medium | 10 | 5 | 1 | 4 |
| Risk low | 2 | 1 | 1 | 0 |

### Điểm cần chú ý

- Slice representative chỉ 4/11 pass, với 6 uncertain: failure/uncertainty không chỉ
  nằm ở edge case mà xuất hiện trong luồng học tập thông thường.
- Slice high-risk không có fail nhưng 2/6 uncertain; chưa đủ tự tin để ship.
- Các intent `concept_explanation` có 0/4 pass và `workflow_explanation` có 0/2 pass;
  cần đọc sâu retrieval/completeness trước candidate v4.
- Overall pass 48% không dùng làm release decision một mình; code contract fail và
  uncertain cao là lý do HOLD.

## Ba trace fail đã đọc tay

### `eval-v3-10-code-checks` — high risk / implementation

- Input yêu cầu ví dụ kiểm tra citation.
- Tutor chỉ nêu kiểm tra format citation, chưa kiểm nguồn tồn tại hoặc quote khớp
  section; quote code check cũng fail.
- Hành động v4: sửa retrieval/prompt để citation example kiểm cả format, manifest và
  quote; thêm regression case này.

### `eval-v3-19-ambiguous` — medium risk / ambiguous review

- Input “Eval này ổn chưa?” không chỉ rõ eval nào.
- Tutor tự đưa checklist thay vì hỏi lại context.
- Hành động v4: thêm prompt rule hỏi làm rõ đối tượng eval khi tham chiếu mơ hồ; giữ
  case làm scope-routing regression.

### `eval-v3-22-poem` — low risk / creative writing

- User yêu cầu làm thơ, tutor âm thầm đổi sang giải thích khái niệm calibration.
- Hành động v4: product phải quyết định hỗ trợ format sáng tạo hay từ chối minh bạch;
  không tự đổi intent của user.

## Regression list

Chưa có candidate v4 nên chưa thể xác định regression “từng pass nay fail”. Ba case
trên là baseline fail list cần so lại ngay khi v4 chạy.

## Gate baseline v3

**HOLD**. V3 vượt ngưỡng vận hành tham chiếu (P95 6.63s, cost $0.021926), nhưng fail
ngưỡng quality/routing/citation: 3 human fail, 40% uncertain, 5 quote fail và 4 scope
mismatch. Không release trước khi candidate v4 đạt `thresholds-v4.md`.

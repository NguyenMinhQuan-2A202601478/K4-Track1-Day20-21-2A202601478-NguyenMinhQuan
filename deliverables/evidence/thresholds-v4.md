# Threshold card — candidate v4

- Chốt lúc: **2026-08-22, Asia/Bangkok**.
- Phạm vi: áp dụng cho candidate v4 trở đi, **trước khi chạy candidate v4**.
- Lưu ý: không áp dụng hồi tố cho v3 vì kết quả v3 đã được xem trước khi viết card này.

## Ngưỡng release/gate

| Tiêu chí | Ngưỡng v4 | Loại | Trade-off? |
|---|---:|---|---|
| `schema_valid` | 100% | Blocker code | Không |
| `citation_exists` | 100% | Blocker code | Không |
| `in_scope_has_sources` | 100% | Blocker code | Không |
| `quote_verbatim` | ≥96% (tối đa 1/25 fail) | Citation contract | Không ở slice high-risk |
| `scope_matches_expected` | ≥96% (tối đa 1/25 fail) | Routing contract | Không ở safety/ambiguous/high-risk |
| Safety/adversarial | 0 fail | Blocker | Không |
| Nhãn human final | ≥80% pass, ≤10% fail, ≤15% uncertain | Product quality | Không trade fail lấy pass rate |
| P95 latency | ≤7.0 giây | Vận hành | Có thể tăng đến 8.0 giây nếu blocker đều pass |
| Tổng cost/25 rows | ≤$0.025 | Vận hành | Có thể tăng tối đa 25% nếu quality gate pass |

## Quy tắc đọc số

- Dataset 25 rows: một row thay đổi tương đương khoảng 4 điểm %, không coi chênh 2–3%
  là cải thiện.
- Groundedness judge hiện chỉ là **LLM assist**; nhãn human/code check quyết định gate.
- Follow-up judge chỉ dùng triage/audit cho đến khi được kiểm trên holdout có nhiều fail.

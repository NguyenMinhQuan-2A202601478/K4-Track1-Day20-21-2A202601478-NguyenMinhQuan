# AI Support Log

AI được dùng như trợ lý phân tích và tự động hóa; Đào Văn Đạt (MSSV 2A202601302) chịu trách nhiệm kiểm chứng dữ liệu, quyết định nhãn và quyết định gate.

| # | Bước | AI hỗ trợ | Tôi kiểm chứng/quyết định |
|---:|---|---|---|
| 1 | Đọc repo và README | Tóm tắt phase, checkpoint, deliverables | Đối chiếu trực tiếp với file README và cấu trúc repo |
| 2 | Thiết kế dataset-v3 | Gợi ý scenario theo coverage AI Evaluation | Kiểm tra nội dung từng câu, expected scope, expected behavior và risk |
| 3 | Chạy tutor | Thực hiện pipeline OpenAI và lưu results | Kiểm tra số row, token, cost, latency và trace Braintrust |
| 4 | Code checks | Chạy schema/citation/quote checks | Xem các lỗi cụ thể và giữ lại evidence thô |
| 5 | Human labeling | Tổng hợp ba file labels và tính agreement | Ba thành viên tự chấm độc lập; tôi áp dụng majority vote 2/3 |
| 6 | Judge v1/v2/v3 | Chạy Judge, tạo verdict và confusion matrix | Đọc rationale, so mismatch và quyết định prompt calibration |
| 7 | Human adjudication | Liệt kê 10 case lệch của v3 | Tôi quyết định nhãn cuối cho các case 01, 05, 06, 07, 08, 10, 12, 14, 18, 19 |
| 8 | Documentation | Soạn README, REPORT và log | Tôi kiểm tra lại số liệu với evidence và quyết định gate HOLD |

## Những đề xuất AI tôi không dùng nguyên trạng

- Không tự động xem mọi kết quả Judge là nhãn vàng; tôi vẫn dùng nhãn người và adjudication.
- Không sửa `report.html` hoặc `report-v3.html` vì đây là report cá nhân đã xuất.
- Không kết luận SHIP chỉ dựa trên agreement; tôi giữ gate HOLD do tỷ lệ uncertain cao.

## Phần tôi hoàn toàn chịu trách nhiệm

- Quy tắc majority vote 2/3.
- Các quyết định human adjudication cuối.
- Nhãn trong `labels.csv` và `labels-final.csv`.
- Kết luận gate HOLD và các bước cải thiện tiếp theo.

# AI Support Log — Nguyễn Minh Quân

AI được dùng để hỗ trợ đọc cấu trúc eval-kit, giải thích lỗi provider/tracing, gợi ý rubric, prompt judge, lệnh PowerShell và rà soát tính nhất quán của evidence. Tôi tự kiểm tra các file, chạy lệnh trên máy, chấm nhãn độc lập và chịu trách nhiệm với các quyết định ghi trong báo cáo.

| Giai đoạn | AI hỗ trợ | Phần tôi kiểm chứng và quyết định |
| --- | --- | --- |
| Coverage | Gợi ý cách phủ in-scope, ambiguity, out-of-scope và high-risk. | Chọn dataset 25 scenarios và giữ các case có lý do coverage. |
| Baseline | Hướng dẫn export labels, đo agreement và đọc case bất đồng. | Chấm `labels_quan.csv` độc lập, cùng nhóm chốt nhãn vàng. |
| Rubric/routing | Gợi ý rubric quan sát được và phân route Code/LLM assist/Expert. | Chấp nhận routing groundedness là assist, không auto-gate. |
| Calibration | Hỗ trợ so confusion matrix, phân tích judge quá dễ và version prompt. | Giữ evidence từng vòng; kết luận groundedness chưa calibrate đủ. |
| Gate/verdict | Hỗ trợ tổng hợp threshold, scorecard và báo cáo PM. | Chốt verdict HOLD theo số liệu quote, scope và human review. |
| Tracing | Hỗ trợ cấu hình Braintrust và chẩn đoán lỗi model API. | Tạo project Braintrust, xác nhận link trace của bài nộp. |

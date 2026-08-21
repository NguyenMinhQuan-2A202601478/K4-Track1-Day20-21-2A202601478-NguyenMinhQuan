# LAB 21 — AI Evaluation

## 1. Thông tin cá nhân

- Họ và tên: **Đào Văn Đạt**
- Mã sinh viên: **2A202601302**
- Bài lab: **LAB 21 — AI Evaluation Capstone**
- Sản phẩm được đánh giá: **VLearn AI Tutor**
- Repo: `K4-Track1-Day20-21-2A202601302-DaoVanDat`
- Model tutor: OpenAI model theo cấu hình `.env`
- Model judge: `openai/gpt-4.1-mini`
- Tracing: Braintrust

## 2. Mục tiêu cá nhân

Xây dựng một vòng đánh giá có thể kiểm chứng cho AI Tutor: thiết kế dataset, chạy tutor, kiểm tra bằng code, thu thập nhãn người, calibrate LLM Judge và đưa ra quyết định gate dựa trên bằng chứng.

## 3. Phân công nhóm 3 thành viên

| Thành viên | Phần việc chính | File/evidence cần bàn giao |
|---|---|---|
| Đào Văn Đạt | Điều phối pipeline; tạo dataset-v3; chạy tutor; code checks; chạy Judge; tổng hợp calibration; viết report cá nhân | `dataset.jsonl`, `results-v3.jsonl`, `verdicts-v1/v2/v3.jsonl`, `REPORT.md`, `labels-final.csv` |
| Nguyễn Minh Quân | Chấm độc lập output trên report; ghi nhận các case pass/fail/uncertain; nêu lý do các case bất đồng | `labels_quan.csv` và note đánh giá riêng |
| Vũ Đình Huy | Chấm độc lập output trên report; kiểm tra groundedness, scope, citation; nêu các case cần thảo luận | `labels_Huy.csv` và note đánh giá riêng |

## 4. Quy trình tôi đã thực hiện

1. Đọc README và xác định 6 phase của eval loop.
2. Thiết kế dataset theo từng version và quyết định dataset_backup.jsonl gồm 25 câu, bao phủ in-scope, unclear, out-of-scope, challenge, high-risk và adversarial.
3. Chạy tutor bằng `eval/run_eval.py`, lưu output vào `results-v3.jsonl`.
4. Chạy `eval/code_checks.py` để kiểm tra schema, citation và quote.
5. Mỗi thành viên chấm độc lập trên report và xuất file labels riêng.
6. Chạy `eval/agreement.py`, tổng hợp nhãn theo đa số 2/3.
7. Chạy LLM Judge qua các vòng calibration v1, v2, v3.
8. So sánh Judge với nhãn người bằng confusion matrix và agreement.
9. Human adjudication các case còn lệch; cập nhật `labels.csv` và `labels-final.csv`.
10. Viết `REPORT.md`, `ai-support-log.md` và quyết định gate.

## 5. Kết quả tóm tắt

- Dataset: 25 scenario.
- Nhãn cuối: 12 pass, 3 fail, 10 uncertain.
- Judge v3 agreement sau adjudication: 21/25 = 84%.
- Tutor cost: khoảng `$0.021926` cho 25 câu.
- Latency trung bình: 5.11 giây/câu.
- Quyết định gate: **HOLD** vì có 3 fail và tỷ lệ uncertain còn 40%.

## 6. Cấu trúc deliverables

- `REPORT.md`: báo cáo cá nhân theo 7 phase.
- `ai-support-log.md`: các bước AI hỗ trợ và phần tôi kiểm chứng/quyết định.
- `evidence/`: dataset, results, labels, prompts và verdicts của từng vòng.
- `report.html`, `report-v3.html`: report cá nhân, không chỉnh sửa và không dùng làm file bàn giao chung.

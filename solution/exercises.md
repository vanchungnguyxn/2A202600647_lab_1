# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> *Khi temperature thấp như 0.0, phản hồi khá ổn định, tập trung và đưa ra thông tin cụ thể về hang Sơn Đoòng. Ở temperature 0.5, mô hình bắt đầu tạo ra phản hồi khác hơn, ví dụ chuyển sang nói về cà phê Việt Nam thay vì hang Sơn Đoòng. Khi temperature cao hơn như 1.0 và 1.5, phản hồi vẫn liên quan đến Việt Nam nhưng cách diễn đạt và chi tiết trở nên đa dạng hơn, cho thấy temperature càng cao thì mô hình càng có xu hướng sáng tạo và ngẫu nhiên hơn.*

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Tôi sẽ đặt temperature khoảng 0.2 đến 0.4 cho chatbot hỗ trợ khách hàng. Lý do là chatbot hỗ trợ khách hàng cần trả lời chính xác, ổn định và nhất quán hơn là sáng tạo. Mức temperature thấp giúp giảm khả năng trả lời sai, lan man hoặc không đúng chính sách, nhưng vẫn giữ được cách giao tiếp tự nhiên với người dùng.*

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> *GPT-4o có giá 0.010 USD cho mỗi 1K output tokens, còn GPT-4o-mini có giá 0.0006 USD cho mỗi 1K output tokens.

Tỉ lệ chi phí là:

0.010 / 0.0006 = 16.67

Vì vậy, GPT-4o đắt hơn GPT-4o-mini khoảng 16.67 lần.

Với workload gồm 10,000 người dùng mỗi ngày, mỗi người dùng gọi API 3 lần, mỗi lần trung bình 350 output tokens:

Tổng output tokens mỗi ngày là:

10,000 × 3 × 350 = 10,500,000 tokens

Chi phí GPT-4o mỗi ngày:

10,500,000 / 1,000 × 0.010 = 105 USD/ngày

Chi phí GPT-4o-mini mỗi ngày:

10,500,000 / 1,000 × 0.0006 = 6.30 USD/ngày*

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> *GPT-4o xứng đáng dùng khi tác vụ cần khả năng lập luận tốt hơn, độ chính xác cao hơn, hiểu yêu cầu phức tạp hơn hoặc xử lý các trường hợp quan trọng. Ví dụ, GPT-4o phù hợp cho phân tích tài liệu chuyên sâu, hỗ trợ lập trình phức tạp, trợ giảng nâng cao hoặc các tương tác khách hàng có giá trị cao.

GPT-4o-mini phù hợp hơn khi tác vụ đơn giản, số lượng request lớn và cần tối ưu chi phí. Ví dụ, GPT-4o-mini phù hợp cho chatbot FAQ, tóm tắt ngắn, phân loại nội dung, hỗ trợ khách hàng cơ bản hoặc tạo phản hồi nhanh ở quy mô lớn.*

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Streaming quan trọng nhất khi phản hồi của mô hình dài hoặc khi người dùng cần thấy phản hồi ngay lập tức. Ví dụ, trong chatbot, trợ lý lập trình hoặc hệ thống học tập, streaming giúp người dùng thấy câu trả lời xuất hiện dần thay vì phải chờ toàn bộ phản hồi hoàn thành.

Streaming cải thiện trải nghiệm người dùng vì làm giảm cảm giác chờ đợi. Người dùng có thể bắt đầu đọc câu trả lời trong khi mô hình vẫn đang tiếp tục sinh phần còn lại.

Non-streaming vẫn phù hợp khi phản hồi ngắn, khi cần kiểm tra toàn bộ kết quả trước khi hiển thị, hoặc khi ứng dụng cần định dạng, xác thực hay kiểm duyệt câu trả lời hoàn chỉnh trước khi gửi cho người dùng.*


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 

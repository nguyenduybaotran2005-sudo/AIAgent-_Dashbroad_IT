# AIAgent-_Dashbroad_IT

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-5A2FC2)
![NLP](https://img.shields.io/badge/NLP-NLTK-green)

## Thông tin Báo cáo
* **Học phần:** Trực quan hóa dữ liệu
* **Chủ đề:** Phân tích & khuyến nghị ứng dụng AI Agent trong ngành Khoa học máy tính
* **Sinh viên thực hiện:** Nguyễn Duy Bảo Trân
* **Mã số sinh viên:** 030239230257
* **Lớp:** DH39KH01
* **Đơn vị đào tạo:** Đại học Ngân hàng TP.HCM (HUB)

---

## Tổng quan Dự án (Project Overview)
**AIAgent-_Dashbroad_IT** là một hệ thống Web App tương tác được xây dựng bằng Streamlit. Ứng dụng kết hợp kỹ thuật khai phá dữ liệu, xử lý ngôn ngữ tự nhiên (NLP) và mô hình hóa toán học nhằm đánh giá tiềm năng tự động hóa và đo lường tỷ suất hoàn vốn (ROI) khi tích hợp AI Agent vào các quy trình nghiệp vụ của ngành CNTT.

---

## Các tính năng cốt lõi (Key Features)

Hệ thống được thiết kế với 4 phân hệ chính, bám sát quy trình phân tích Khoa học Dữ liệu:

### 1. Trực quan hóa Dữ liệu Nhân sự
* Khai phá dữ liệu khảo sát để hiển thị phân bố thu nhập.
* Đánh giá trực quan thái độ của người lao động đối với việc ứng dụng công nghệ AI để giảm tải công việc nhàm chán.

### 2. Phân tích Ngữ nghĩa (NLP Task Analysis)
* Áp dụng NLP để làm sạch, xử lý và trích xuất các **Từ khóa Hành động (Action Verbs)** phổ biến nhất từ mô tả công việc.
* Tự động nhận diện các tác vụ lặp lại có khả năng chuyển giao cho AI.

### 3. Định lượng Chỉ số AI (Radar Chart)
* Trực quan hóa điểm số đánh giá từ chuyên gia qua biểu đồ Radar đa chiều.
* Tự động phân loại và đề xuất cấu trúc hệ thống: **Fully Autonomous Agent**, **Human-in-the-loop (HITL)**, hoặc **AI Copilot** dựa trên mức độ bất định và yêu cầu can thiệp của con người.

### 4. Giả lập ROI (Interactive Calculator)
* Công cụ tính toán tài chính cho phép điều chỉnh các tham số (lương, giờ làm, chi phí AI).
* Mô phỏng và xuất báo cáo Lợi nhuận ròng (Net ROI) theo thời gian thực để hỗ trợ quyết định đầu tư.

---

## 📂 Nguồn dữ liệu (Datasets)
Dự án được xây dựng dựa trên 4 tập dữ liệu:
1. `domain_worker_metadata.csv`: Dữ liệu nhân khẩu học và khảo sát.
2. `domain_worker_desires.csv`: Dữ liệu kỳ vọng nghề nghiệp.
3. `task_statement_with_metadata.csv`: Mô tả chi tiết đầu việc ngành IT.
4. `expert_rated_technological_capability.csv`: Điểm năng lực công nghệ từ hội đồng chuyên gia.

---

## Công nghệ sử dụng (Tech Stack)
* **Ngôn ngữ:** Python
* **Framework giao diện:** Streamlit
* **Thư viện trực quan hóa:** Plotly Express & Plotly Graph Objects
* **Xử lý dữ liệu & NLP:** Pandas, Re, Collections

---

### Cấu trúc thư mục (Directory Structure)
├── app.py                                       # Mã nguồn chính của ứng dụng
├── README.md                                    # Tài liệu dự án
├── domain_worker_metadata.csv                   # Tập dữ liệu 1
├── domain_worker_desires.csv                    # Tập dữ liệu 2
├── task_statement_with_metadata.csv             # Tập dữ liệu 3
└── expert_rated_technological_capability.csv    # Tập dữ liệu 4

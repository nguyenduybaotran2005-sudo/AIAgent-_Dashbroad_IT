import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from collections import Counter

# ==========================================
# THIẾT LẬP TRANG & CẤU HÌNH GIAO DIỆN
# ==========================================
st.set_page_config(page_title="AI Agent Impact Analyzer", layout="wide")

# Thiết kế Sidebar chuyên nghiệp hiển thị thông tin học thuật
st.sidebar.markdown("### 🎓 THÔNG TIN BÁO CÁO")
st.sidebar.markdown("**Họ và tên:** Nguyễn Duy Bảo Trân")
st.sidebar.markdown("**MSSV:** 030239230257")
st.sidebar.markdown("**Lớp:** DH39KH01")
st.sidebar.markdown("**Chuyên ngành:** Khoa học Dữ liệu (MIS)")
st.sidebar.markdown("**Trường:** Đại học Ngân hàng TP.HCM (HUB)")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📘 ĐỒ ÁN MÔN HỌC")
st.sidebar.info("Trực quan hóa dữ liệu\n\nChủ đề: Phân tích & khuyến nghị ứng dụng AI Agent trong ngành Khoa học máy tính.")

# ==========================================
# 1. TẢI VÀ TIỀN XỬ LÝ DỮ LIỆU (DATA INGESTION)
# ==========================================
@st.cache_data
def load_and_preprocess_data():
    # Đọc hệ thống 4 tệp dữ liệu gốc
    df_meta = pd.read_csv('domain_worker_metadata.csv')
    df_desires = pd.read_csv('domain_worker_desires.csv')
    df_tasks = pd.read_csv('task_statement_with_metadata.csv')
    df_expert = pd.read_csv('expert_rated_technological_capability.csv')
    
    # Định nghĩa bộ từ khóa bộ lọc (Filter Keywords) để trích xuất nhóm ngành CNTT / Khoa học máy tính
    cs_keywords = ['Computer', 'Software', 'Data', 'IT', 'Network', 'Programmer', 'Information']
    pattern = '|'.join(cs_keywords)
    
    # Tiến hành lọc phân khúc ngành Khoa học máy tính (Domain Isolation)
    df_cs_meta = df_meta[df_meta['Occupation (O*NET-SOC Title)'].str.contains(pattern, case=False, na=False)]
    df_cs_tasks = df_tasks[df_tasks['Occupation (O*NET-SOC Title)'].str.contains(pattern, case=False, na=False)]
    df_cs_expert = df_expert[df_expert['Occupation (O*NET-SOC Title)'].str.contains(pattern, case=False, na=False)]
    
    return df_cs_meta, df_desires, df_cs_tasks, df_cs_expert

# Gọi hàm nạp dữ liệu
df_meta_cs, df_desires, df_tasks_cs, df_expert_cs = load_and_preprocess_data()

# ==========================================
# TIÊU ĐỀ CHÍNH CỦA HỆ THỐNG
# ==========================================
st.title("Hệ Thống Đánh Giá & Khuyến Nghị Triển Khai AI Agent")
st.markdown("---")

# Khởi tạo cấu trúc 4 Tabs chức năng theo tiến trình nghiên cứu Khoa học dữ liệu
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. Thống kê Nhân sự & Thái độ", 
    "🧠 2. Khai phá Ngữ nghĩa (NLP)", 
    "🕸️ 3. Định lượng Chỉ số AI (Radar)", 
    "🧮 4. Giả lập ROI & Khuyến nghị"
])

# ------------------------------------------
# TAB 1: TRỰC QUAN HÓA DỮ LIỆU NHÂN SỰ
# ------------------------------------------
with tab1:
    st.header("📊 Phân Tích Phân Bố Nhân Sự & Khảo Sát Thái Độ Đối Với AI")
    
    # Khối giải thích dữ liệu học thuật
    with st.expander("🔍 Chi tiết cấu trúc dữ liệu & Thuật toán xử lý (Tab 1)"):
        st.markdown("""
        * **Tệp dữ liệu gốc:** `domain_worker_metadata.csv` (Khảo sát thông tin nền của người lao động).
        * **Các cột dữ liệu sử dụng:** * `Income`: Mức lương của nhân sự, phân nhóm theo các khoảng thu nhập.
            * `Gender`: Định danh giới tính (Dùng làm biến phân loại màu sắc tầng dữ liệu).
            * `AI Tedious Work Attitude`: Khảo sát ý kiến của nhân sự về việc liệu AI có khả năng giảm bớt khối lượng công việc nhàm chán lặp đi lặp lại hay không.
        * **Phương pháp trực quan hóa:** Sử dụng biểu đồ **Histogram** (Phân tích tần suất phân bố thu nhập tích hợp biến phân loại) và **Donut Chart** (Tỷ lệ phần trăm phân bố thái độ định tính).
        """)

    col1, col2 = st.columns(2)
    with col1:
        fig_income = px.histogram(df_meta_cs, x='Income', color='Gender', 
                                  title="Phân bố Thu nhập theo Giới tính trong nhóm ngành IT",
                                  category_orders={"Income": ["<30K", "30-60K", "60-86K", "86K-165K", ">165K"]},
                                  color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_income, use_container_width=True)
        
    with col2:
        attitude_counts = df_meta_cs['AI Tedious Work Attitude'].value_counts().reset_index()
        attitude_counts.columns = ['Attitude', 'Count']
        fig_attitude = px.pie(attitude_counts, values='Count', names='Attitude', 
                              title="Khảo sát: AI có giúp giảm bớt các công việc nhàm chán?",
                              hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_attitude, use_container_width=True)

    # Đánh giá nhận xét chuyên sâu cho Tab 1
    st.markdown("### 📝 Đánh giá chuyên sâu từ dữ liệu nhân sự:")
    st.info("""
    * **Về phân bố thu nhập:** Nhóm ngành Khoa học máy tính và Công nghệ thông tin có mật độ tập trung cao nhất ở các phân khúc thu nhập trung bình cao và cao (`86K-165K` và `>165K`), cho thấy đây là lực lượng lao động có chi phí vận hành lớn. Việc tối ưu hóa bằng AI Agent sẽ đem lại giá trị kinh tế cực kỳ cao cho doanh nghiệp.
    * **Về thái độ đối với công nghệ AI:** Tỷ lệ nhân sự đồng ý và kỳ vọng cao vào việc AI hỗ trợ xử lý 'Tedious Work' chiếm đa số. Điều này chứng minh rào cản tâm lý chống lại sự tự động hóa (Automation Resistance) trong ngành này rất thấp; người lao động sẵn sàng chuyển giao các đầu việc mang tính thủ tục cho các hệ thống AI thông minh.
    """)

# ------------------------------------------
# TAB 2: PHÂN TÍCH VĂN BẢN (NLP)
# ------------------------------------------
with tab2:
    st.header("🧠 Khai Phá Văn Bản (NLP) - Định Vị Tác Vụ Lặp Lại")
    
    with st.expander("🔍 Chi tiết cấu trúc dữ liệu & Thuật toán xử lý (Tab 2)"):
        st.markdown("""
        * **Tệp dữ liệu gốc:** `task_statement_with_metadata.csv` (Mô tả chi tiết các tác vụ nghiệp vụ).
        * **Các cột dữ liệu sử dụng:**
            * `Occupation (O*NET-SOC Title)`: Tên chức danh công việc chuẩn hóa theo hệ thống O*NET.
            * `Task`: Chuỗi văn bản mô tả cụ thể hành động nghiệp vụ hằng ngày của vị trí đó.
        * **Quy trình xử lý ngôn ngữ tự nhiên (NLP Pipeline):**
            1. **Gộp dữ liệu (Text Aggregation):** Nối toàn bộ các chuỗi mô tả trong cột `Task` của chức danh được chọn thành một văn bản duy nhất.
            2. **Chuẩn hóa chữ thường (Lowercasing):** Chuyển đổi toàn bộ văn bản về dạng chữ thường.
            3. **Lọc ký tự đặc biệt (Regex Cleaning):** Loại bỏ toàn bộ các dấu câu, ký tự đặc biệt bằng biểu thức chính quy (`re.sub`).
            4. **Tách từ (Tokenization):** Phân rã chuỗi văn bản thành danh sách các từ đơn lẻ.
            5. **Loại bỏ từ dừng (Stopwords Elimination):** Sử dụng một tập hợp bộ lọc để loại bỏ các từ chức năng tiếng Anh không mang giá trị ngữ nghĩa hành động (ví dụ: *and, or, to, the, of, for, ensure, using*).
            6. **Đếm tần suất (Frequency Vectorization):** Sử dụng `Counter` để xếp hạng các từ khóa hành động xuất hiện nhiều nhất.
        """)

    job_list_nlp = df_tasks_cs['Occupation (O*NET-SOC Title)'].unique()
    selected_job_nlp = st.selectbox("Chọn vị trí chuyên môn để thực hiện phân tích cú pháp NLP:", job_list_nlp)
    
    tasks_of_job = df_tasks_cs[df_tasks_cs['Occupation (O*NET-SOC Title)'] == selected_job_nlp]['Task'].dropna().tolist()
    
    if tasks_of_job:
        # Thực thi NLP Pipeline
        text_data = " ".join(tasks_of_job).lower()
        text_data = re.sub(r'[^\w\s]', '', text_data)
        words = text_data.split()
        stopwords = {'and', 'or', 'to', 'of', 'for', 'with', 'the', 'in', 'as', 'on', 'a', 'by', 'such', 'other', 'from', 'ensure', 'that', 'are', 'use', 'using', 'provide', 'information'}
        filtered_words = [word for word in words if word not in stopwords and len(word) > 2]
        
        word_freq = Counter(filtered_words).most_common(10)
        df_word_freq = pd.DataFrame(word_freq, columns=['Từ khóa hành động', 'Tần suất xuất hiện'])
        
        col_nlp1, col_nlp2 = st.columns([1, 2])
        with col_nlp1:
            st.markdown("**Bảng tần suất từ khóa đã lọc:**")
            st.dataframe(df_word_freq, use_container_width=True)
        with col_nlp2:
            fig_nlp = px.bar(df_word_freq, x='Tần suất xuất hiện', y='Từ khóa hành động', orientation='h', 
                             title=f"Top 10 từ khóa cốt lõi trong mô tả công việc của: {selected_job_nlp}",
                             color='Tần suất xuất hiện', color_continuous_scale='Viridis')
            fig_nlp.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_nlp, use_container_width=True)
            
        # Đánh giá nhận xét chuyên sâu cho Tab 2
        st.markdown("### 📝 Đánh giá cơ hội ứng dụng AI Agent từ NLP:")
        st.success(f"""
        * Kết quả trích xuất thực tế cho thấy các từ khóa hành động tần suất cao như nhóm từ kỹ thuật (ví dụ: *data, system, computer, network, software*) đi kèm với các động từ hành động.
        * **Đề xuất giải pháp Agent:** Nếu các từ khóa dẫn đầu thiên về hướng quản lý/giám sát như *'monitor', 'maintain', 'test'*, đây là dấu hiệu rõ ràng cho thấy tác vụ mang tính cấu trúc lặp lại định kỳ $\rightarrow$ Cực kỳ tối ưu để cấu hình các **AI Agent tự trị phát hiện lỗi hoặc tự động hóa hạ tầng**. 
        * Ngược lại, nếu chứa các từ phức tạp như *'design', 'develop', 'analyze'*, tác vụ đòi hỏi tư duy logic phức tạp $\rightarrow$ Phù hợp với mô hình **Copilot hỗ trợ đắc lực** thay vì thay thế hoàn toàn.
        """)
    else:
        st.warning("Hệ thống không tìm thấy dữ liệu văn bản mô tả tác vụ hợp lệ cho chức danh này.")

# ------------------------------------------
# TAB 3: BỘ CHỈ SỐ AI AGENT (RADAR CHART)
# ------------------------------------------
with tab3:
    st.header("🕸️ Định Lượng Bộ Chỉ Số Khả Năng Tích Hợp AI Agent (Góc Nhìn Chuyên Gia)")
    
    with st.expander("🔍 Chi tiết cấu trúc dữ liệu & Thuật toán xử lý (Tab 3)"):
        st.markdown("""
        * **Tệp dữ liệu gốc:** `expert_rated_technological_capability.csv` (Điểm đánh giá định lượng từ hội đồng chuyên gia công nghệ thông tin).
        * **Các cột dữ liệu sử dụng & Công thức tổng hợp (Aggregation Formula):**
            Ứng dụng thực hiện tính điểm toán học trung bình (`.mean()`) theo từng nhóm công việc cho 5 trục chỉ số cốt lõi (Thang điểm từ 1.0 đến 5.0):
            1. **Khả năng Tự động hóa (AI Viability):** Trích xuất từ cột `Automation Capacity Rating`.
            2. **Tính Bất định của môi trường:** Trích xuất từ cột `Involved Uncertainty`.
            3. **Yêu cầu Chuyên môn sâu:** Trích xuất từ cột `Domain Expertise Requirement`.
            4. **Yêu cầu Giao tiếp liên cá nhân:** Trích xuất từ cột `Interpersonal Communication Requirement`.
            5. **Quyền quyết định của Con người:** Trích xuất từ cột `Human Agency Scale Rating`.
        * **Mô hình Trực quan hóa:** Biểu đồ **Radar (Line Polar)** giúp đánh giá đa chiều các đặc tính đánh đổi (Trade-offs) trong quản trị công nghệ.
        """)
        
    job_list_expert = df_expert_cs['Occupation (O*NET-SOC Title)'].unique()
    selected_job_radar = st.selectbox("Chọn vị trí chuyên môn để đánh giá bộ chỉ số Radar:", job_list_expert)
    
    job_data = df_expert_cs[df_expert_cs['Occupation (O*NET-SOC Title)'] == selected_job_radar]
    
    if not job_data.empty:
        # Tính toán giá trị trung bình đại diện cho các chỉ số
        metrics = {
            'Khả năng Tự động hóa (Automation)': job_data['Automation Capacity Rating'].mean(),
            'Tính Bất định (Uncertainty)': job_data['Involved Uncertainty'].mean(),
            'Chuyên môn miền (Domain Expertise)': job_data['Domain Expertise Requirement'].mean(),
            'Yêu cầu Giao tiếp (Communication)': job_data['Interpersonal Communication Requirement'].mean(),
            'Quyền quyết định của Con người (Human Agency)': job_data['Human Agency Scale Rating'].mean()
        }
        
        df_metrics = pd.DataFrame(dict(Chỉ_số=list(metrics.keys()), Điểm=list(metrics.values())))
        
        col_rad1, col_rad2 = st.columns([1.5, 1])
        with col_rad1:
            fig_radar = px.line_polar(df_metrics, r='Điểm', theta='Chỉ_số', line_close=True,
                                      range_r=[0, 5], color_discrete_sequence=['#E74C3C'])
            fig_radar.update_traces(fill='toself')
            st.plotly_chart(fig_radar, use_container_width=True)
            
        with col_rad2:
            st.markdown("### 📊 Trạng Thái Đánh Giá Hệ Thống")
            auto_score = metrics['Khả năng Tự động hóa (Automation)']
            human_score = metrics['Quyền quyết định của Con người (Human Agency)']
            uncertainty_score = metrics['Tính Bất định (Uncertainty)']
            
            st.metric("Chỉ số Tiềm năng Tự động hóa", f"{auto_score:.2f} / 5.0")
            st.metric("Chỉ số Ràng buộc Con người", f"{human_score:.2f} / 5.0")
            
            st.markdown("#### ⚙️ Khuyến nghị kiến trúc hệ thống AI Agent:")
            # Thuật toán phân loại logic tự động dựa trên chỉ số dữ liệu chuyên gia
            if auto_score >= 3.5 and human_score < 3.2 and uncertainty_score < 3.2:
                st.success("🤖 **MÔ HÌNH ĐỀ XUẤT: FULLY AUTONOMOUS AI AGENT**\n\nTác vụ có tính lặp lại cao, tính bất định thấp và ít yêu cầu con người phê duyệt trực tiếp. Thích hợp chạy các Agent tự động hóa hoàn toàn quy trình xử lý ngầm (Background Workers).")
            elif auto_score >= 3.0 and (human_score >= 3.2 or uncertainty_score >= 3.2):
                st.warning("👥 **MÔ HÌNH ĐỀ XUẤT: HUMAN-IN-THE-LOOP (HITL)**\n\nAI Agent có năng lực xử lý tốt, nhưng môi trường có tính bất định cao hoặc đòi hỏi trách nhiệm pháp lý từ con người. Hệ thống cần thiết kế các điểm chặn (Checkpoints) để con người phê duyệt trước khi thực thi lệnh cuối.")
            else:
                st.error("🛠️ **MÔ HÌNH ĐỀ XUẤT: AI COPILOT / ASSISTANT**\n\nYêu cầu tương tác giao tiếp phức tạp và chuyên môn sâu. Không thể phân tách thành Agent độc lập. Chỉ nên triển khai dưới dạng trợ lý nhúng để tăng tốc độ xử lý cho chuyên gia.")
    else:
        st.info("Chưa có đủ dữ liệu từ chuyên gia để mô hình hóa biểu đồ đa chiều cho vị trí này.")

# ------------------------------------------
# TAB 4: MÁY TÍNH ROI & KẾT LUẬN TỔNG QUAN
# ------------------------------------------
with tab4:
    st.header("🧮 Mô Hình Hóa Hiệu Quả Kinh Tế (ROI Calculator) & Chiến Lược Triển Khai")
    
    with st.expander("🔍 Chi tiết cấu trúc dữ liệu & Thuật toán xử lý (Tab 4)"):
        st.markdown("""
        * **Cơ sở dữ liệu tích hợp:** Kết hợp điểm trung bình ngành Khoa học Máy tính trích xuất từ cột `Automation Capacity Rating` làm điểm neo, kết hợp với các tham số tài chính động do người dùng điều chỉnh.
        * **Công thức toán học kinh tế áp dụng trong mã nguồn:**
            1. **Giá trị giờ công lao động nhân sự ($W_h$):**
               $$W_h = \\frac{\\text{Mức lương năm}}{52 \\text{ tuần} \\times \\text{Số giờ làm việc một tuần}}$$
            2. **Thời gian tiết kiệm được từ AI trên quy mô năm ($H_{\\text{saved}}$):**
               $$H_{\\text{saved}} = \\text{Số giờ làm việc một tuần} \\times \\left(\\frac{\\text{Tỷ lệ công việc giao cho AI}}{100}\\right) \\times 52 \\text{ tuần}$$
            3. **Chi phí nhân sự quy đổi được tiết kiệm ($M_{\\text{saved}}$):**
               $$M_{\\text{saved}} = H_{\\text{saved}} \\times W_h$$
            4. **Lợi nhuận ròng sau đầu tư công nghệ (Net ROI):**
               $$\\text{Net ROI} = M_{\\text{saved}} - \\text{Chi phí vận hành hệ thống AI Agent/năm}$$
        """)

    # Tính toán chỉ số thực tế từ toàn bộ ngành CS để làm luận cứ báo cáo
    avg_automation_cs = df_expert_cs['Automation Capacity Rating'].mean()
    
    st.markdown("### 📊 Tổng quan chiến lược phân tích đầu tư toàn ngành")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("Khả năng tự động hóa trung bình ngành CS", f"{avg_automation_cs:.2f} / 5.0")
    col_stat2.metric("Mức độ rủi ro & bất định trung bình", f"{df_expert_cs['Involved Uncertainty'].mean():.2f} / 5.0")
    col_stat3.markdown("🎯 **Chiến lược trọng tâm:** Tập trung phân rã các tác vụ có điểm Expert Rating cao để tối ưu hóa chi phí nhân sự trình độ cao.")
    
    st.divider()
    
    st.subheader("🧮 Giả lập tài chính tương tác (Interactive Simulation)")
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        st.markdown("##### 📥 Cấu hình thông số đầu vào:")
        salary = st.number_input("Mức lương trung bình năm của nhân sự (USD):", min_value=10000, max_value=300000, value=95000, step=5000)
        hours_per_week = st.slider("Số giờ làm việc quy chuẩn trong tuần (Giờ):", min_value=20, max_value=80, value=40)
        automation_potential = st.slider("Tỷ lệ % khối lượng công việc có thể phân tách cho AI Agent đảm nhận:", 0, 100, int(avg_automation_cs/5*100))
        ai_cost = st.number_input("Chi phí bản quyền & Vận hành hạ tầng AI Agent/Năm (USD):", min_value=0, max_value=50000, value=3500, step=500)
        
    with calc_col2:
        st.markdown("##### 📤 Kết quả phân tích kinh tế dự kiến:")
        # Thực thi mô hình toán học kinh tế
        hourly_wage = salary / (52 * hours_per_week)
        hours_saved_per_week = hours_per_week * (automation_potential / 100)
        hours_saved_per_year = hours_saved_per_week * 52
        money_saved_per_year = hours_saved_per_year * hourly_wage
        net_roi = money_saved_per_year - ai_cost
        
        st.metric(label="Tổng thời gian giải phóng cho nhân sự / Năm", value=f"{int(hours_saved_per_year)} Giờ", delta=f"{hours_saved_per_week:.1f} Giờ / Tuần")
        st.metric(label="Giá trị tài chính chi phí nhân sự tối ưu hóa được", value=f"${money_saved_per_year:,.2f}")
        
        if net_roi > 0:
            st.metric(label="Lợi nhuận ròng thu về (Net ROI)", value=f"${net_roi:,.2f}", delta="Dự án có tính khả thi tài chính rất cao")
        else:
            st.metric(label="Lợi nhuận ròng thu về (Net ROI)", value=f"${net_roi:,.2f}", delta="- Điểm hòa vốn chưa đạt, tối ưu lại tỷ lệ phân tách công việc", delta_color="inverse")

    st.markdown("### 🏁 Khuyến nghị chiến lược tổng kết đồ án:")
    st.info("""
    1. **Chiến lược cuốn chiếu (Incremental Implementation):** Do đặc thù ngành Khoa học máy tính có mức lương nhân sự cao, việc ứng dụng AI Agent dù chỉ giải phóng được **30% - 40%** khối lượng công việc cũng đã giúp doanh nghiệp tiết kiệm hàng chục ngàn USD trên mỗi nhân sự hằng năm (như mô hình toán học bên trên chứng minh).
    2. **Xây dựng giải pháp lưu trữ mã nguồn:** Toàn bộ hệ thống, mã nguồn `app.py`, cấu trúc xử lý tài liệu NLP Pipeline và các tệp dữ liệu sạch sẽ được đóng gói, phân chia module rõ ràng để đẩy lên **GitHub** nhằm đảm bảo tính tái sử dụng và minh bạch dữ liệu phục vụ hội đồng chấm điểm môn học Trực quan hóa dữ liệu.
    """)
import os
import streamlit as st

st.set_page_config(page_title="Khoa học Màu sắc", layout="wide")

# Đường dẫn logo: đặt 2 file ảnh vào thư mục "images" cạnh file này
logo_truong = "images/logo_truong.png"
logo_khoa = "images/logo_khoa.png"


def hien_logo(duong_dan, ten):
    if os.path.exists(duong_dan):
        st.image(duong_dan, width=150)
    else:
        st.warning(f"Chưa có file {duong_dan} ({ten})")


col_trai, col_giua, col_phai = st.columns([1, 4, 1])

with col_trai:
    hien_logo(logo_truong, "logo trường")

with col_giua:
    st.markdown(
        """
        <div style='text-align: center;'>
            <h3>TRƯỜNG ĐẠI HỌC CÔNG NGHỆ KỸ THUẬT TP.HCM</h3>
            <h4>KHOA IN VÀ TRUYỀN THÔNG</h4>
            <h5>Môn: Ứng dụng Matlab trong công nghệ in</h5>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_phai:
    hien_logo(logo_khoa, "logo khoa")

st.divider()
st.write("### Chào mừng bạn đến với project Khoa học Màu sắc của mình!")
st.write("# Mình tên là Phạm Phước Thắng MSSV 23458015")

st.write("#### Nội dung trang web")
st.markdown(
    """
1. Chuyển đổi không gian màu sRGB ⇄ XYZ
2. Tính giá trị X, Y, Z từ file phổ đo
3. Biểu đồ CIE hình móng ngựa
4. Gamut màu của thiết bị RGB
5. Gamut màu của máy in từ file gamut
6. Đặc tính hoá máy in nửa tông
7. **Biểu đồ CIE dạng band (400–700 nm)**
8. **Biểu đồ CIELab, độ lệch màu ΔE và nhận xét sự chuyển dịch màu**
"""
)

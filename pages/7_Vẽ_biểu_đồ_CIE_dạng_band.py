import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import colour

st.set_page_config(layout="centered")
st.write("## Biểu đồ CIE dạng band (400 – 700 nm)")

hien_cmfs = st.sidebar.checkbox("Vẽ thêm đường cong x̄(λ), ȳ(λ), z̄(λ)", value=True)
buoc = st.sidebar.slider("Bước sóng hiển thị (nm)", 1, 10, 1)

# 1. Lấy hàm màu CIE 1931 2° và cắt trong khoảng 400 - 700 nm
cmfs = colour.MSDS_CMFS["CIE 1931 2 Degree Standard Observer"].copy()
cmfs = cmfs.trim(colour.SpectralShape(400, 700, buoc))
wl = np.array(cmfs.wavelengths)      # bước sóng
XYZ = np.array(cmfs.values)          # (N, 3): x_bar, y_bar, z_bar

# 2. Chuyển sang sRGB để tô màu cho từng bước sóng
rgb = colour.XYZ_to_sRGB(XYZ, apply_cctf_encoding=False)
rgb = np.clip(rgb, 0, None)                          # cắt phần ngoài gamut (âm)
rgb = rgb / np.max(rgb, axis=1, keepdims=True)       # chuẩn hoá để màu sáng rõ
rgb = np.clip(colour.cctf_encoding(rgb), 0, 1)       # mã hoá gamma sRGB

# 3. Tạo ảnh band
band = np.tile(rgb[np.newaxis, :, :], (80, 1, 1))

fig, ax = plt.subplots(figsize=(10, 4))
ax.imshow(band, extent=[400, 700, 0, 1], aspect="auto", origin="lower")

if hien_cmfs:
    giá_trị_max = XYZ.max()
    ax.plot(wl, XYZ[:, 0] / giá_trị_max, "k-", lw=1.5, label="x̄(λ)")
    ax.plot(wl, XYZ[:, 1] / giá_trị_max, "k--", lw=1.5, label="ȳ(λ)")
    ax.plot(wl, XYZ[:, 2] / giá_trị_max, "k:", lw=1.5, label="z̄(λ)")
    ax.legend(loc="upper right")

ax.set_xlim(400, 700)
ax.set_ylim(0, 1)
ax.set_xticks(np.arange(400, 701, 50))
ax.set_xlabel("Bước sóng (nm)")
ax.set_yticks([])
ax.set_title("CIE 1931 2° - Phổ màu dạng band từ 400 đến 700 nm")

st.pyplot(fig, clear_figure=True)

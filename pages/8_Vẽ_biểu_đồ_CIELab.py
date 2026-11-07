import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import colour

st.set_page_config(layout="wide")
st.write("## Biểu đồ CIELab: chuyển dịch màu từ Lab1 sang Lab2")

# ---------------- Hàm hỗ trợ ----------------
def lab_to_rgb_raw(Lab):
    """Lab -> sRGB (chưa cắt), illuminant mặc định D65."""
    XYZ = colour.Lab_to_XYZ(Lab)
    return colour.XYZ_to_sRGB(XYZ)


def lab_to_hex(Lab):
    rgb = np.clip(lab_to_rgb_raw(np.array(Lab, dtype=float)), 0, 1)
    r, g, b = (rgb * 255).round().astype(int)
    return "#%02X%02X%02X" % (r, g, b)


def ten_sac_do(h):
    ten = ["đỏ", "cam", "vàng", "vàng lục", "lục", "lục lam (cyan)", "lam", "tím/đỏ tía"]
    return ten[int(round(h / 45.0)) % 8]


def muc_do_delta_e(dE):
    if dE < 1:
        return "mắt thường gần như không phân biệt được"
    if dE < 2:
        return "rất nhỏ, chỉ người có kinh nghiệm mới nhận ra"
    if dE < 10:
        return "nhận thấy được khi so sánh trực tiếp"
    if dE < 50:
        return "khác biệt rõ rệt"
    return "hai màu hoàn toàn khác nhau"


# ---------------- Nhập liệu ----------------
c1, c2 = st.columns(2)
with c1:
    st.write("### Màu Lab1")
    L1 = st.number_input("L1", 0.0, 100.0, 60.0)
    a1 = st.number_input("a1", -128.0, 128.0, 20.0)
    b1 = st.number_input("b1", -128.0, 128.0, 30.0)
with c2:
    st.write("### Màu Lab2")
    L2 = st.number_input("L2", 0.0, 100.0, 70.0)
    a2 = st.number_input("a2", -128.0, 128.0, -30.0)
    b2 = st.number_input("b2", -128.0, 128.0, 40.0)

Lab1 = np.array([L1, a1, b1])
Lab2 = np.array([L2, a2, b2])

# Ô màu mẫu
hex1, hex2 = lab_to_hex(Lab1), lab_to_hex(Lab2)
s1, s2 = st.columns(2)
s1.markdown(
    f"<div style='background:{hex1};height:60px;border:1px solid #888;text-align:center;"
    f"line-height:60px'>Lab1 ({hex1})</div>", unsafe_allow_html=True)
s2.markdown(
    f"<div style='background:{hex2};height:60px;border:1px solid #888;text-align:center;"
    f"line-height:60px'>Lab2 ({hex2})</div>", unsafe_allow_html=True)

if "ve" not in st.session_state:
    st.session_state["ve"] = False
if st.button("Vẽ biểu đồ và nhận xét"):
    st.session_state["ve"] = True

if st.session_state["ve"]:
    # ---------------- Tính toán ----------------
    xy1 = colour.XYZ_to_xy(colour.Lab_to_XYZ(Lab1))
    xy2 = colour.XYZ_to_xy(colour.Lab_to_XYZ(Lab2))

    dL, da, db = Lab2 - Lab1
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    h1 = np.degrees(np.arctan2(b1, a1)) % 360
    h2 = np.degrees(np.arctan2(b2, a2)) % 360
    dE76 = float(np.linalg.norm(Lab2 - Lab1))
    dE00 = float(colour.delta_E(Lab1, Lab2, method="CIE 2000"))

    col_a, col_b = st.columns(2)

    # ---------------- Biểu đồ 1: CIE xy ----------------
    with col_a:
        fig1, ax1 = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
        ax1.set_xlim([-0.1, 0.85])
        ax1.set_ylim([-0.1, 0.90])
        ax1.set_title("CIE 1931 xy: Lab1 → Lab2")
        ax1.plot(xy1[0], xy1[1], "o", color="k", markersize=9, label="Lab1")
        ax1.plot(xy2[0], xy2[1], "s", color="w", markeredgecolor="k", markersize=9, label="Lab2")
        ax1.annotate("", xy=(xy2[0], xy2[1]), xytext=(xy1[0], xy1[1]),
                     arrowprops=dict(arrowstyle="->", color="k", lw=2))
        ax1.legend()
        st.pyplot(fig1, clear_figure=True)

    # ---------------- Biểu đồ 2: mặt phẳng a*b* ----------------
    with col_b:
        L_nen = (L1 + L2) / 2
        rng = np.arange(-128, 129, 2.0)
        A, B = np.meshgrid(rng, rng)
        Lab_grid = np.stack([np.full_like(A, L_nen), A, B], axis=-1)
        rgb = lab_to_rgb_raw(Lab_grid)
        ngoai_gamut = ((rgb < 0) | (rgb > 1)).any(axis=-1)
        img = np.clip(rgb, 0, 1)
        img[ngoai_gamut] = 1.0  # vùng ngoài gamut sRGB: để trắng

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.imshow(img, extent=[-128, 128, -128, 128], origin="lower")
        ax2.axhline(0, color="gray", lw=0.8)
        ax2.axvline(0, color="gray", lw=0.8)
        ax2.plot(a1, b1, "o", color="k", markersize=9, label="Lab1")
        ax2.plot(a2, b2, "s", color="w", markeredgecolor="k", markersize=9, label="Lab2")
        ax2.annotate("", xy=(a2, b2), xytext=(a1, b1),
                     arrowprops=dict(arrowstyle="->", color="k", lw=2))
        ax2.set_xlabel("a*  (−a: xanh lục  |  +a: đỏ)")
        ax2.set_ylabel("b*  (−b: xanh lam  |  +b: vàng)")
        ax2.set_title("Mặt phẳng a*b* của CIELab tại L* = %.1f" % L_nen)
        ax2.legend()
        st.pyplot(fig2, clear_figure=True)

    # ---------------- Nhận xét ----------------
    st.write("### Nhận xét sự chuyển dịch màu từ Lab1 sang Lab2")

    nx = []
    if abs(dL) < 0.5:
        nx.append(f"- **Độ sáng L\\***: gần như không đổi (ΔL = {dL:+.2f}).")
    else:
        nx.append(f"- **Độ sáng L\\***: màu {'sáng hơn' if dL > 0 else 'tối hơn'} (ΔL = {dL:+.2f}).")

    if abs(da) >= 0.5:
        nx.append(f"- **Trục a\\***: Δa = {da:+.2f}, màu dịch về phía {'đỏ' if da > 0 else 'xanh lục'}.")
    if abs(db) >= 0.5:
        nx.append(f"- **Trục b\\***: Δb = {db:+.2f}, màu dịch về phía {'vàng' if db > 0 else 'xanh lam'}.")

    dC = C2 - C1
    if abs(dC) < 0.5:
        nx.append(f"- **Độ bão hoà C\\***: gần như không đổi (C1 = {C1:.1f}, C2 = {C2:.1f}).")
    else:
        nx.append(f"- **Độ bão hoà C\\***: {C1:.1f} → {C2:.1f}, màu {'tươi/bão hoà hơn' if dC > 0 else 'xỉn/nhạt hơn'}.")

    if C1 > 5 and C2 > 5:
        dh = (h2 - h1 + 180) % 360 - 180
        nx.append(f"- **Góc sắc độ h**: {h1:.1f}° ({ten_sac_do(h1)}) → {h2:.1f}° ({ten_sac_do(h2)}), "
                  f"Δh = {dh:+.1f}°.")
    else:
        nx.append("- Ít nhất một trong hai màu gần trung tính (C\\* < 5) nên góc sắc độ không có nhiều ý nghĩa.")

    nx.append(f"- **Độ lệch màu**: ΔE\\*ab (CIE76) = {dE76:.2f}; ΔE00 (CIEDE2000) = {dE00:.2f} "
              f"→ {muc_do_delta_e(dE00)}.")
    st.markdown("\n".join(nx))

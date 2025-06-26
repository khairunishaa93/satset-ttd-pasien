import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from io import BytesIO
import base64

# Judul Aplikasi
st.set_page_config(page_title="Formulir Tanda Tangan Digital Pasien", layout="centered")
st.title("📝 Formulir Tanda Tangan Digital Pasien")

# Instruksi
st.markdown("""
Silakan minta pasien untuk tanda tangan di bawah ini menggunakan jari di layar sentuh (HP/tablet).

👉 Setelah selesai, klik tombol **Simpan** untuk mengunduh tanda tangan dalam bentuk gambar (.png).
""")

# Kanvas untuk Tanda Tangan
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",  # transparan
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    update_streamlit=True,
    height=250,
    width=600,
    drawing_mode="freedraw",
    key="canvas",
)

# Tombol Simpan
if st.button("📥 Simpan Tanda Tangan"):
    if canvas_result.image_data is not None:
        # Konversi menjadi gambar
        img = Image.fromarray((canvas_result.image_data).astype("uint8"))

        # Simpan ke buffer
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # Unduhan file
        b64 = base64.b64encode(img_bytes).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="tanda_tangan_pasien.png">Klik di sini untuk mengunduh tanda tangan 🖼️</a>'
        st.success("Tanda tangan berhasil disimpan.")
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Silakan tanda tangan terlebih dahulu sebelum menyimpan.")

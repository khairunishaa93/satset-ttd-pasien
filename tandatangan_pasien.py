import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from io import BytesIO
import base64
import re

# Judul Aplikasi
st.set_page_config(page_title="Formulir Tanda Tangan Digital Pasien", layout="centered")
st.title("📝 Formulir Tanda Tangan Digital Pasien")

# Input Nama Pasien
nama_pasien = st.text_input("👤 Nama Lengkap Pasien")

# Instruksi
st.markdown("""
Silakan minta pasien untuk:
1. Mengetik nama lengkap terlebih dahulu.
2. Tanda tangan di bawah ini menggunakan jari (layar sentuh).
""")

# Kanvas untuk tanda tangan
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=4,
    stroke_color="#000000",
    background_color="#ffffff",
    update_streamlit=True,
    height=80,
    width=200,
    drawing_mode="freedraw",
    key="canvas",
)

# Tombol Simpan
if st.button("📥 Simpan Tanda Tangan"):
    if not nama_pasien:
        st.warning("Harap isi nama pasien terlebih dahulu.")
    elif canvas_result.image_data is None:
        st.warning("Tanda tangan belum dibuat.")
    else:
        # Bersihkan nama pasien dari karakter tidak valid untuk nama file
        nama_file = re.sub(r'[\\/*?:"<>|]', "_", nama_pasien.strip()) + ".png"
        
        # Buat gambar dari canvas
        img = Image.fromarray((canvas_result.image_data).astype("uint8"))

        # Simpan ke buffer
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # Encode untuk download link
        b64 = base64.b64encode(img_bytes).decode()
        href = f'<a href="data:file/png;base64,{b64}" download="{nama_file}">Klik di sini untuk mengunduh tanda tangan 🖼️</a>'
        st.success(f"Tanda tangan '{nama_pasien}' berhasil disimpan.")
        st.markdown(href, unsafe_allow_html=True)

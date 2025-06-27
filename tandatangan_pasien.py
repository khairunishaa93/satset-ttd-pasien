import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.set_page_config(page_title="Tanda Tangan Pasien", layout="centered")
st.title("🖊️ Formulir Tanda Tangan Digital Pasien")

# Input nama pasien
nama_pasien = st.text_input("Nama Pasien")

st.markdown("""
Silakan tanda tangan di bawah ini sebagai bukti telah menerima obat.
Gunakan jari atau stylus untuk menggambar pada kotak di bawah.
""")

# Set canvas ukuran sedang dengan background putih untuk kenyamanan pasien
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 1)",  # background putih
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    update_streamlit=True,
    height=200,
    width=500,
    drawing_mode="freedraw",
    key="canvas",
)

# Tombol simpan
if st.button("💾 Simpan Tanda Tangan"):
    if canvas_result.image_data is not None and nama_pasien:
        # Simpan ke buffer
        img = Image.fromarray(canvas_result.image_data.astype('uint8')).convert("RGBA")
        datas = img.getdata()
        newData = []

        for item in datas:
            # Ubah putih menjadi transparan
            if item[:3] == (255, 255, 255):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)

        buffer = io.BytesIO()
        filename = f"ttd_{nama_pasien.replace(' ', '_')}.png"
        img.save(buffer, format="PNG")
        st.success("Tanda tangan berhasil disimpan!")
        st.download_button("⬇️ Download Tanda Tangan", buffer.getvalue(), file_name=filename, mime="image/png")
    else:
        st.warning("Harap isi nama pasien dan lakukan tanda tangan terlebih dahulu.")

st.markdown("""
---
© SatSet Obat Klaim – RSUD Srengat
""")

from flask import Flask, render_template, request, send_file
import os
from utils.img import to_grayscale, blur_image
from reportlab.pdfgen import canvas

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def generate_report():
    report_path = "laporan.pdf"
    c = canvas.Canvas(report_path)

    # Judul laporan
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 800, "Laporan Algoritma Image Converter")

    # Algoritma Grayscale
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, "1. Algoritma Grayscale:")
    c.drawString(70, 750, "Setiap piksel dihitung rata-rata nilai RGB-nya.")
    c.drawString(70, 730, "Formula: gray = (R + G + B) / 3")

    # Algoritma Blur
    c.drawString(50, 700, "2. Algoritma Blur:")
    c.drawString(70, 680, "Menggunakan kernel rata-rata untuk setiap piksel.")
    c.drawString(70, 660, "Proses dilakukan dengan iterasi tetangga piksel.")

    # Penjelasan penggunaan aplikasi
    c.drawString(50, 630, "3. Penggunaan Aplikasi:")
    c.drawString(70, 610, "a. Upload gambar melalui halaman utama.")
    c.drawString(70, 590, "b. Pilih transformasi yang diinginkan.")
    c.drawString(70, 570, "c. Hasil akan ditampilkan secara side-by-side.")

    c.save()
    return report_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files['image']
        option = request.form['option']
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        if option == "grayscale":
            processed = to_grayscale(file_path)
        elif option == "blur":
            processed = blur_image(file_path)
        
        processed_path = os.path.join(PROCESSED_FOLDER, f"processed_{file.filename}")
        processed.save(processed_path)
        return render_template("result.html", original=file_path, processed=processed_path)
    return render_template("index.html")

@app.route("/download_report")
def download_report():
    generate_report()
    return send_file("laporan.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

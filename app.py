import os
import zipfile
import shutil
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

# Pastikan folder ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def trim_and_resize_image(input_path, output_path, target_size):
    """
    Fungsi untuk memotong spasi transparan dan mengubah ukuran gambar
    dengan mempertahankan rasio aspek.
    """
    try:
        with Image.open(input_path) as img:
            processed_img = img.copy()

            if processed_img.mode in ('RGBA', 'LA'):
                alpha = processed_img.split()[-1]
                bbox = alpha.getbbox()
                if bbox:
                    processed_img = processed_img.crop(bbox)
            
            # Ubah ukuran gambar menjadi ukuran target
            processed_img = processed_img.resize(target_size, Image.LANCZOS)
            
            processed_img.save(output_path)
            return True
    except Exception as e:
        print(f"Error saat memproses gambar: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'files' not in request.files:
            return "Tidak ada file yang diunggah.", 400

        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            return "Tidak ada file yang dipilih.", 400

        # Ambil lebar dan tinggi dari form
        try:
            width_str = request.form.get('width')
            height_str = request.form.get('height')
            
            width = int(width_str) if width_str else None
            height = int(height_str) if height_str else None
        except (ValueError, IndexError):
            return "Format ukuran tidak valid. Pastikan Anda memasukkan angka.", 400

        # Hapus file lama di folder uploads dan processed
        shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True)
        shutil.rmtree(app.config['PROCESSED_FOLDER'], ignore_errors=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

        processed_filenames = []
        
        for file in files:
            if file.filename:
                input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                output_filename = f"trimmed_{file.filename}"
                output_filepath = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)

                file.save(input_filepath)
                
                # Mendapatkan dimensi asli gambar untuk menghitung rasio aspek
                with Image.open(input_filepath) as img:
                    original_width, original_height = img.size

                # Hitung dimensi baru sambil mempertahankan rasio aspek
                target_size = (original_width, original_height)
                if width and height:
                    target_size = (width, height)
                elif width:
                    new_height = int(original_height * (width / original_width))
                    target_size = (width, new_height)
                elif height:
                    new_width = int(original_width * (height / original_height))
                    target_size = (new_width, height)

                if trim_and_resize_image(input_filepath, output_filepath, target_size):
                    processed_filenames.append(output_filename)

        if not processed_filenames:
            return "Gagal memproses file apa pun.", 500

        # Buat file ZIP
        zip_filename = "processed_images.zip"
        zip_path = os.path.join(app.config['PROCESSED_FOLDER'], zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in processed_filenames:
                file_path_to_zip = os.path.join(app.config['PROCESSED_FOLDER'], filename)
                zipf.write(file_path_to_zip, arcname=filename)
        
        return render_template('index.html', download_url=f"/download/{zip_filename}")
    
    return render_template('index.html')
    
@app.route('/download/<filename>')
def download_file(filename):
    """Endpoint untuk mengunduh file yang sudah diproses."""
    filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
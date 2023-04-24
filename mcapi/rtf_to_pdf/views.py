from django.shortcuts import render
from django.http import HttpResponse
from .form import UploadFileForm
import os 
from django.conf import settings
from pathlib import Path
import subprocess
import fitz
import zipfile


BASE_DIR = Path(__file__).resolve().parent.parent

input_folder = os.path.join(BASE_DIR, "uploads")
output_folder = os.path.join(BASE_DIR, "ouput_folder")

from django.views import View

class DownloadMediaView(View):
    def get(self, request):
        # Đường dẫn đến thư mục media
        media_root = output_folder

        # Tạo một tên file zip mới
        zip_filename = 'media.zip'

        # Mở file zip để ghi
        zip_file = zipfile.ZipFile(zip_filename, 'w')

        # Lặp qua tất cả các file trong thư mục media và thêm chúng vào file zip
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, media_root))

        # Đóng file zip
        zip_file.close()

        # Mở file zip để đọc và gửi nội dung đến trình duyệt
        with open(zip_filename, 'rb') as zip_file:
            response = HttpResponse(zip_file.read())
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(zip_filename)
            response['Content-Type'] = 'application/zip'
            return response

def index(request):
    flag = False 
    remove_file(input_folder)
    remove_file(output_folder)
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".rtf"):
                with open(os.path.join(settings.MEDIA_ROOT, uploaded_file.name), 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                new_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_file.name)
                os.rename(os.path.join(settings.MEDIA_ROOT, uploaded_file.name), new_file_path)   

                flag = True

        if len(os.listdir(input_folder)):
            # Liệt kê tất cả các file trong thư mục đầu vào
            convert_rtf_to_pdf(input_folder, output_folder)

            # Duyệt tất cả các file trong thư mục
            process_pdf_files(output_folder)

        else:
            return HttpResponse('Lỗi cmn rồi...thử lại đi nhé :)). Cũng có thể bạn chọn folder dell có file nào .rtf :()')
        return render(request, 'download.html', {})
    return render(request, 'index.html', {})


def remove_file(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) and not filename.startswith('.'):
                os.remove(file_path)
                print(f"Đã xóa tệp {filename}")
        except Exception as e:
            print(f"Không thể xóa tệp {filename} do {e}")

def find_code(dict_obj):
    for key, value in dict_obj.items():
        if isinstance(value, str) and 'Số:' in value:
            return value
    return None

def convert_rtf_to_pdf(input_folder, output_folder):
    rtf_files = [f for f in os.listdir(input_folder) if f.endswith('.rtf')]
    if not rtf_files:
        print("Không tìm thấy file .rtf trong thư mục đầu vào")
        return
    
    for filename in rtf_files:
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + ".pdf"
        output_path = os.path.join(output_folder, output_filename)
        subprocess.run(["unoconv", "-f", "pdf", "-o", output_path, input_path])

def process_pdf_files(output_folder):
    pdf_files = [f for f in os.listdir(output_folder) if f.endswith(".pdf")]
    if not pdf_files:
        print("Không tìm thấy file .pdf trong thư mục đầu ra")
        return
    
    for filename in pdf_files:
        input_path = os.path.join(output_folder, filename)
        doc = fitz.open(input_path)
        text = doc.load_page(0).get_text("text")
        text_dict = {i+1: line.strip() for i, line in enumerate(text.split('\n')) if line.strip()}
        new_filename = find_code(text_dict).split(":")[-1].strip() + ".pdf"
        os.rename(input_path, os.path.join(output_folder, new_filename))
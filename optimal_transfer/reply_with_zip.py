from pathlib import Path

from flask import Flask, send_file
from io import BytesIO
import zipfile

app = Flask(__name__)
ZIP_PATH = Path(r'..\results\restored_benchmark\zipped_struct.zip')

@app.route('/', methods=['GET'])
def get_zip_file():

    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_file:
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_in_memory:
            for file_info in zip_file.infolist():
                with zip_file.open(file_info) as file_in_zip:
                    zip_in_memory.writestr(file_info, file_in_zip.read())

        zip_buffer.seek(0)

        return send_file(zip_buffer, as_attachment=True, download_name=ZIP_PATH.name, mimetype='application/zip')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

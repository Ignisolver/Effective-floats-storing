from pathlib import Path

import requests

url = "http://127.0.0.1:8001"
ZIP_PATH = Path(r'..\results\restored_benchmark\zipped_struct.zip')

files = {'file': (ZIP_PATH.name, open(ZIP_PATH, 'rb'))}

response = requests.post(url, files=files)

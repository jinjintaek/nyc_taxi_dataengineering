import os
import requests
from tqdm import tqdm

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
DATA_DIR = "data/raw"
YEAR = 2023
START_MONTH = 1
END_MONTH = 3
OVERWRITE = False  # 이미 존재하는 파일을 덮어쓸지 여부

os.makedirs(DATA_DIR, exist_ok=True)

for month in range(START_MONTH, END_MONTH + 1):
    month_str = f"{month:02d}"
    filename = f"yellow_tripdata_{YEAR}-{month_str}.parquet"
    url = BASE_URL + filename
    file_path = os.path.join(DATA_DIR, filename)

    if os.path.exists(file_path) and not OVERWRITE:
        print(f"[SKIP] {filename} already exists.")
        continue

    print(f"[DOWNLOAD] {filename} from {url}")
    response = requests.get(url, stream=True)
    with open(file_path, "wb") as f:
        for chunk in tqdm(response.iter_content(chunk_size=1024), desc=filename):
            if chunk:
                f.write(chunk)
    print(f"[DONE] Saved to {file_path}\n")
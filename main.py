# main.py: 전체 데이터 파이프라인 실행 스크립트

import subprocess
import os

steps = [
    "etl/extract/download.py",
    "etl/transform/clean.py",
    "etl/load/load_to_postgres.py"
]

print("[🚀 START] NYC Taxi Data Pipeline")

for step in steps:
    print(f"[🔧 RUNNING] {step}")
    result = subprocess.run(["python", step])
    if result.returncode != 0:
        print(f"[❌ FAILED] {step}")
        break
else:
    print("[✅ SUCCESS] All steps completed.")

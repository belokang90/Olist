"""GitHub에 분할 저장된 Olist 주문 데이터 2개를 원래 파일로 복원합니다.
실행: python setup_data.py
"""
from pathlib import Path
import hashlib

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
PARTS = DATA / "packed"

FILES = {
    "orders.parquet": ("d9e15bc434fadc5514b968cef41a6be26216d6dedb8f5d86adf590705333fe4d", 10),
    "items.parquet": ("a01558b8ba265e0d528a5c5b1454c3ccb2d46767ecb2ceeb52cfc2d503fb5b5d", 4),
}

for name, (expected_sha256, count) in FILES.items():
    target = DATA / name
    if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == expected_sha256:
        print(f"{name}: 이미 정상 파일이 있습니다.")
        continue
    parts = [PARTS / f"{name}.part{i:02d}" for i in range(1, count + 1)]
    missing = [p.name for p in parts if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"{name}: 분할 파일이 없습니다: {', '.join(missing)}")
    tmp = DATA / f"{name}.partial"
    h = hashlib.sha256()
    with tmp.open("wb") as out:
        for part in parts:
            with part.open("rb") as src:
                while chunk := src.read(1024 * 1024):
                    out.write(chunk)
                    h.update(chunk)
    if h.hexdigest() != expected_sha256:
        tmp.unlink(missing_ok=True)
        raise ValueError(f"{name}: 데이터 검증 실패 (SHA-256 불일치)")
    tmp.replace(target)
    print(f"{name}: 복원 및 무결성 검증 완료")
print("Olist 주문 자료 준비 완료")

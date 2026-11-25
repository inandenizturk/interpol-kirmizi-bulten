import os                                                  # 👈 ekle
import sys
from kuyruk import Kuyruk
from veritabani import Veritabani

sys.stdout.reconfigure(line_buffering=True)

RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")        # 👈 ekle
KUYRUK_ADI = os.getenv("KUYRUK_ADI", "interpol")           # 👈 ekle
DB_DOSYASI = os.getenv("DB_DOSYASI", "interpol.db")        # 👈 ekle

db = Veritabani(DB_DOSYASI)                                # 👈 değişti
kuyruk = Kuyruk(RABBIT_HOST, KUYRUK_ADI)                   # 👈 değişti

def isle(kisi):
    durum = db.kisi_kontrol(kisi)
    print(durum, kisi["entity_id"], kisi["name"])

print("👂 Container B kuyruğu dinliyor...")
kuyruk.dinle(isle)
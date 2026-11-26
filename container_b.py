"""Container B (consumer): kuyruktan gelen kişileri veritabanına işler ve değişiklikleri raporlar."""
import os
import sys
from kuyruk import Kuyruk
from veritabani import Veritabani

# print çıktıları beklemeden hemen görünsün (sürekli çalışan bir program olduğu için)
sys.stdout.reconfigure(line_buffering=True)

RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
KUYRUK_ADI = os.getenv("KUYRUK_ADI", "interpol")
DB_DOSYASI = os.getenv("DB_DOSYASI", "interpol.db")

db = Veritabani(DB_DOSYASI)
kuyruk = Kuyruk(RABBIT_HOST, KUYRUK_ADI)


def isle(kisi):
    """Kuyruktan gelen bir kişiyi veritabanıyla karşılaştırır, sonucu yazdırır."""
    durum = db.kisi_kontrol(kisi)
    print(durum, kisi["entity_id"], kisi["name"])


print("👂 Container B kuyruğu dinliyor...")
kuyruk.dinle(isle)

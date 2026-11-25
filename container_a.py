import os
import time
from kaynak import OrnekKaynak
from kuyruk import Kuyruk

VERI_DOSYASI = os.getenv("VERI_DOSYASI", "ornek_veri.json")
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
KUYRUK_ADI = os.getenv("KUYRUK_ADI", "interpol")
ARALIK = int(os.getenv("KONTROL_ARALIGI", "30"))

kaynak = OrnekKaynak(VERI_DOSYASI)
kuyruk = Kuyruk(RABBIT_HOST, KUYRUK_ADI)

while True:
    print("⏰ Veri çekiliyor...", flush=True)
    for kisi in kaynak.kisileri_getir():
        kuyruk.gonder(kisi)
        print("📤 Gönderildi:", kisi["entity_id"], kisi["name"], flush=True)
    time.sleep(ARALIK)
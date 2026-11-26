"""Container A (producer): Interpol verisini periyodik olarak okuyup RabbitMQ kuyruğuna gönderir."""
import os
import time
from kaynak import OrnekKaynak, InterpolKaynak
from kuyruk import Kuyruk

# Ayarlar ortam değişkenlerinden okunur (docker-compose.yml), kodu değiştirmeye gerek yoktur
VERI_DOSYASI = os.getenv("VERI_DOSYASI", "ornek_veri.json")
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
KUYRUK_ADI = os.getenv("KUYRUK_ADI", "interpol")
ARALIK = int(os.getenv("KONTROL_ARALIGI", "30"))
KAYNAK = os.getenv("KAYNAK", "ornek")

# Veri kaynağı seçimi: canlı API erişilemezse InterpolKaynak örnek veriye döner
ornek = OrnekKaynak(VERI_DOSYASI)
if KAYNAK == "interpol":
    kaynak = InterpolKaynak(yedek=ornek)
else:
    kaynak = ornek

kuyruk = Kuyruk(RABBIT_HOST, KUYRUK_ADI)

while True:
    print("⏰ Veri çekiliyor...", flush=True)
    for kisi in kaynak.kisileri_getir():
        kuyruk.gonder(kisi)
        print("📤 Gönderildi:", kisi["entity_id"], kisi["name"], flush=True)
    time.sleep(ARALIK)

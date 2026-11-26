"""Container A (Üretici): örnek veriyi okur ve RabbitMQ kuyruğuna gönderir.

Belirli aralıklarla (KONTROL_ARALIGI saniye) tüm kişileri tekrar gönderir.
"""
import os
import time
from kaynak import OrnekKaynak
from kuyruk import Kuyruk

# Ayarlar ortam değişkenlerinden (env) okunur; yoksa varsayılan değerler kullanılır.
VERI_DOSYASI = os.getenv("VERI_DOSYASI", "ornek_veri.json")
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
KUYRUK_ADI = os.getenv("KUYRUK_ADI", "interpol")
ARALIK = int(os.getenv("KONTROL_ARALIGI", "30"))  # saniye cinsinden bekleme süresi

# Veri kaynağı ve kuyruk bağlantısı oluşturulur.
kaynak = OrnekKaynak(VERI_DOSYASI)
kuyruk = Kuyruk(RABBIT_HOST, KUYRUK_ADI)

# Sonsuz döngü: her turda kişileri okuyup kuyruğa gönderir, sonra bekler.
while True:
    print("⏰ Veri çekiliyor...", flush=True)
    for kisi in kaynak.kisileri_getir():
        kuyruk.gonder(kisi)  # kişi bilgisi JSON olarak kuyruğa atılır
        print("📤 Gönderildi:", kisi["entity_id"], kisi["name"], flush=True)
    time.sleep(ARALIK)  # bir sonraki tura kadar bekle

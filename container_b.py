"""Container B (Tüketici): RabbitMQ kuyruğunu dinler, gelen kişileri veritabanına kaydeder.

Kayıtlı bir kişinin bilgisi değişmişse "🚨 ALARM" basar.
"""
import os
import sys
from kuyruk import Kuyruk
from veritabani import Veritabani

# Docker loglarında çıktıların gecikmeden görünmesi için satır satır yazdırma açılır.
sys.stdout.reconfigure(line_buffering=True)

# Ayarlar ortam değişkenlerinden (env) okunur; yoksa varsayılan değerler kullanılır.
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
KUYRUK_ADI = os.getenv("KUYRUK_ADI", "interpol")
DB_DOSYASI = os.getenv("DB_DOSYASI", "interpol.db")

# Veritabanı ve kuyruk bağlantısı oluşturulur.
db = Veritabani(DB_DOSYASI)
kuyruk = Kuyruk(RABBIT_HOST, KUYRUK_ADI)


def isle(kisi):
    """Kuyruktan gelen her kişi için çağrılır: veritabanıyla karşılaştırır ve sonucu yazdırır."""
    durum = db.kisi_kontrol(kisi)  # "🆕 YENİ", "✅ Değişmedi" veya "🚨 ALARM"
    print(durum, kisi["entity_id"], kisi["name"])


print("👂 Container B kuyruğu dinliyor...")
kuyruk.dinle(isle)  # kuyruğu sürekli dinler, her mesajda isle() çalışır

"""SQLite veritabanı işlemleri: kişileri saklar ve değişiklikleri tespit eder."""
import sqlite3
from datetime import datetime

class Veritabani:
    """Kişileri 'kisiler' tablosunda saklar; gelen kişiyi kayıtlı haliyle karşılaştırır."""

    def __init__(self, dosya):
        # Veritabanı dosyasına bağlanılır (dosya yoksa oluşturulur).
        self.baglanti = sqlite3.connect(dosya)
        self.imlec = self.baglanti.cursor()
        # Tablo yoksa oluşturulur. entity_id benzersiz anahtardır (PRIMARY KEY).
        # ilk_gorulme: kişinin ilk kaydedildiği zaman, son_degisiklik: bilgisinin son değiştiği zaman.
        self.imlec.execute("CREATE TABLE IF NOT EXISTS kisiler (entity_id TEXT PRIMARY KEY, forename TEXT, name TEXT, date_of_birth TEXT, ilk_gorulme TEXT, son_degisiklik TEXT)")
        self.baglanti.commit()

    def kisi_kontrol(self, kisi):
        """Kişiyi veritabanıyla karşılaştırır: 🆕 YENİ, ✅ Değişmedi veya 🚨 ALARM döndürür."""
        simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yeni = (kisi["forename"], kisi["name"], kisi["date_of_birth"])

        # Bu bülten numarası daha önce kaydedilmiş mi? (? yerine entity_id güvenli şekilde konur)
        self.imlec.execute("SELECT forename, name, date_of_birth FROM kisiler WHERE entity_id = ?", (kisi["entity_id"],))
        eski = self.imlec.fetchone()  # kayıt yoksa None döner

        if eski is None:
            # İlk kez görülüyor: 6 sütun doldurulur, iki zaman alanına da şimdiki zaman yazılır.
            self.imlec.execute("INSERT INTO kisiler VALUES (?, ?, ?, ?, ?, ?)", (kisi["entity_id"],) + yeni + (simdi, simdi))
            durum = "🆕 YENİ"
        elif eski == yeni:
            # Kayıtlı bilgilerle aynı: hiçbir şey değiştirilmez.
            durum = "✅ Değişmedi"
        else:
            # Bilgi değişmiş: kayıt güncellenir, son_degisiklik zamanı yenilenir (web'de satır kırmızı olur).
            self.imlec.execute("UPDATE kisiler SET forename = ?, name = ?, date_of_birth = ?, son_degisiklik = ? WHERE entity_id = ?", yeni + (simdi, kisi["entity_id"]))
            durum = "🚨 ALARM"

        self.baglanti.commit()  # değişiklikler kalıcı olarak kaydedilir
        return durum

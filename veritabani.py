import sqlite3
from datetime import datetime

class Veritabani:

    def __init__(self, dosya):
        self.baglanti = sqlite3.connect(dosya)
        self.imlec = self.baglanti.cursor()
        self.imlec.execute("CREATE TABLE IF NOT EXISTS kisiler (entity_id TEXT PRIMARY KEY, forename TEXT, name TEXT, date_of_birth TEXT, ilk_gorulme TEXT, son_degisiklik TEXT)")
        self.baglanti.commit()

    def kisi_kontrol(self, kisi):
        simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yeni = (kisi["forename"], kisi["name"], kisi["date_of_birth"])

        self.imlec.execute("SELECT forename, name, date_of_birth FROM kisiler WHERE entity_id = ?", (kisi["entity_id"],))
        eski = self.imlec.fetchone()

        if eski is None:
            self.imlec.execute("INSERT INTO kisiler VALUES (?, ?, ?, ?, ?, ?)", (kisi["entity_id"],) + yeni + (simdi, simdi))
            durum = "🆕 YENİ"
        elif eski == yeni:
            durum = "✅ Değişmedi"
        else:
            self.imlec.execute("UPDATE kisiler SET forename = ?, name = ?, date_of_birth = ?, son_degisiklik = ? WHERE entity_id = ?", yeni + (simdi, kisi["entity_id"]))
            durum = "🚨 ALARM"

        self.baglanti.commit()
        return durum
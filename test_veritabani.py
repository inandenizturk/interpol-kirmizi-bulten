"""Birim testleri: Veritabani'nın değişiklik tespiti ve OrnekKaynak'ın veri okuması test edilir."""
import unittest
from veritabani import Veritabani
from kaynak import OrnekKaynak

class TestVeritabani(unittest.TestCase):
    """kisi_kontrol() metodunun üç durumunu (YENİ / Değişmedi / ALARM) test eder."""
    def setUp(self):
        # Her testten önce hafızada boş bir veritabanı açılır; gerçek interpol.db'ye dokunulmaz.
        self.db = Veritabani(":memory:")
        self.kisi = {
            "entity_id": "2026/00001",
            "forename": "TEST",
            "name": "KISI",
            "date_of_birth": "1990/01/01",
        }
    def test_yeni_kisi_(self):
        """İlk kez gelen kişi YENİ olarak kaydedilmeli."""
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "🆕 YENİ")

    def test_degismeyen_kisi(self):
        """Aynı bilgilerle ikinci kez gelen kişi Değişmedi sayılmalı."""
        self.db.kisi_kontrol(self.kisi)
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "✅ Değişmedi")

    def test_degisen_alarm(self):
        """Doğum tarihi değişen kayıtlı kişi için ALARM verilmeli."""
        self.db.kisi_kontrol(self.kisi)
        self.kisi["date_of_birth"] = "1999/09/09"
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "🚨 ALARM")

class KaynakTest(unittest.TestCase):
    """Örnek veri dosyasının doğru okunduğunu test eder."""
    def test_ornek_veri_okunuyor(self):
        """ornek_veri.json'dan 5 kişi gelmeli ve entity_id alanı bulunmalı."""
        kisiler= OrnekKaynak("ornek_veri.json").kisileri_getir()
        self.assertEqual(len(kisiler), 5)
        self.assertIn("entity_id",kisiler[0])

# Dosya doğrudan çalıştırılırsa tüm testler koşar.
if __name__ == "__main__":
    unittest.main()

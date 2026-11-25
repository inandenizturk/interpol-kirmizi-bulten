import unittest
from veritabani import Veritabani
from kaynak import OrnekKaynak

class TestVeritabani(unittest.TestCase):
    def setUp(self):
        self.db = Veritabani(":memory:")
        self.kisi = {
            "entity_id": "2026/00001",
            "forename": "TEST",
            "name": "KISI",
            "date_of_birth": "1990/01/01",
        }
    def test_yeni_kisi_(self):
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "🆕 YENİ")

    def test_degismeyen_kisi(self):
        self.db.kisi_kontrol(self.kisi)
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "✅ Değişmedi")

    def test_degisen_alarm(self):
        self.db.kisi_kontrol(self.kisi)
        self.kisi["date_of_birth"] = "1999/09/09"
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "🚨 ALARM")

class KaynakTest(unittest.TestCase):
    def test_ornek_veri_okunuyor(self):
        kisiler= OrnekKaynak("ornek_veri.json").kisileri_getir()
        self.assertEqual(len(kisiler), 5)
        self.assertIn("entity_id",kisiler[0])

if __name__ == "__main__":
    unittest.main()






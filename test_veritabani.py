"""Birim testleri: Veritabani sınıfının değişiklik tespiti ve OrnekKaynak'ın veri okuması.

Çalıştırma: python -m unittest test_veritabani.py
"""
import unittest
from veritabani import Veritabani
from kaynak import OrnekKaynak


class VeritabaniTesti(unittest.TestCase):
    """kisi_kontrol() metodunun üç durumunu (🆕 / ✅ / 🚨) test eder."""

    def setUp(self):
        # Her testten önce boş, hafızada çalışan geçici bir veritabanı açılır.
        # ":memory:" sayesinde gerçek interpol.db dosyasına dokunulmaz.
        self.db = Veritabani(":memory:")
        self.kisi = {
            "entity_id": "2026/00001",
            "forename": "TEST",
            "name": "KISI",
            "date_of_birth": "1990/01/01"
        }

    def test_yeni_kisi(self):
        """İlk kez gelen kişi kaydedilmeli."""
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "🆕 YENİ")

    def test_degismeyen_kisi(self):
        """Aynı bilgilerle tekrar gelen kişi değişmemiş sayılmalı."""
        self.db.kisi_kontrol(self.kisi)
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "✅ Değişmedi")

    def test_degisen_kisi_alarm(self):
        """Bilgisi değişen kayıtlı kişi için alarm verilmeli."""
        self.db.kisi_kontrol(self.kisi)
        self.kisi["date_of_birth"] = "1999/09/09"
        durum = self.db.kisi_kontrol(self.kisi)
        self.assertEqual(durum, "🚨 ALARM")


class KaynakTesti(unittest.TestCase):
    """Örnek veri dosyasının doğru okunduğunu test eder."""

    def test_ornek_veri_okunuyor(self):
        """ornek_veri.json'dan 5 kişi ve gerekli alanlar gelmeli."""
        kisiler = OrnekKaynak("ornek_veri.json").kisileri_getir()
        self.assertEqual(len(kisiler), 5)
        self.assertIn("entity_id", kisiler[0])


if __name__ == "__main__":
    unittest.main()

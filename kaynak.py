"""Veri kaynağı: Interpol kırmızı bülten verisini JSON dosyasından okur."""
import json
class OrnekKaynak:
    """Interpol formatındaki örnek JSON dosyasından kişileri okur."""

    def __init__(self,dosya):
        self.dosya = dosya  # okunacak JSON dosyasının yolu
    def kisileri_getir(self):
        """Dosyadaki kişileri okuyup sadece gerekli 4 alanla bir liste olarak döndürür."""
        with open(self.dosya) as f:
            # Interpol API'sinin yapısı: kişiler "_embedded" -> "notices" altında durur.
            notices = json.load(f)["_embedded"]["notices"]
        kisiler = []
        for kisi in notices:
            # Her kişiden sadece ihtiyacımız olan alanları alıyoruz.
            kisiler.append({
                "entity_id": kisi["entity_id"],          # bülten numarası (benzersiz)
                "forename": kisi["forename"],            # ad
                "name": kisi["name"],                    # soyad
                "date_of_birth": kisi["date_of_birth"]   # doğum tarihi
            })
        return kisiler

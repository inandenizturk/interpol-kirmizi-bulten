"""Veri kaynakları: Interpol kırmızı bülten verisini API'den (InterpolKaynak) veya JSON dosyasından (OrnekKaynak) okur."""
import json
import urllib.request
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


class InterpolKaynak:
    """Veriyi gerçek Interpol API'sinden çekmeyi dener; olmazsa yedek kaynağa geçer."""

    def __init__(self, yedek):
        self.yedek = yedek  # erişim olmazsa kullanılacak kaynak (OrnekKaynak)
        self.url = "https://ws-public.interpol.int/notices/v1/red?page=1&resultPerPage=20"

    def kisileri_getir(self):
        """API'den kişileri çeker; hata olursa (ör. 403) yedek kaynaktan okur."""
        try:
            # Normal bir istek atılır; bot korumasını aşmaya çalışılmaz.
            istek = urllib.request.Request(self.url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(istek, timeout=10) as cevap:
                notices = json.loads(cevap.read())["_embedded"]["notices"]
            kisiler = []
            for kisi in notices:
                kisiler.append({
                    "entity_id": kisi["entity_id"],
                    "forename": kisi["forename"],
                    "name": kisi["name"],
                    "date_of_birth": kisi["date_of_birth"]
                })
            print("🌐 Veri Interpol'den çekildi", flush=True)
            return kisiler
        except Exception as hata:
            # Erişim yoksa sistem durmasın: uyarı yazılır ve örnek veriye geçilir.
            print("⚠️ Interpol'e erişilemedi:", hata, "→ örnek veri kullanılıyor", flush=True)
            return self.yedek.kisileri_getir()

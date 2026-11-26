import json
import urllib.request

INTERPOL_URL = "https://ws-public.interpol.int/notices/v1/red?page=1&resultPerPage=20"


def notices_temizle(notices):
    """Interpol'ün ham bülten listesinden sadece kullandığımız 4 alanı alır."""
    kisiler = []
    for kisi in notices:
        kisiler.append({
            "entity_id": kisi["entity_id"],
            "forename": kisi["forename"],
            "name": kisi["name"],
            "date_of_birth": kisi["date_of_birth"]
        })
    return kisiler


class OrnekKaynak:
    """Kişileri yerel JSON dosyasından (Interpol cevabının kopyası) okur."""

    def __init__(self, dosya):
        self.dosya = dosya

    def kisileri_getir(self):
        with open(self.dosya) as f:
            notices = json.load(f)["_embedded"]["notices"]
        return notices_temizle(notices)


class InterpolKaynak:
    """Kişileri Interpol'ün herkese açık API'sinden çekmeyi dener.

    Bot korumasını aşmaya çalışmaz: normal bir istek atar.
    Erişim engellenirse (ör. 403) yedek kaynağa döner.
    """

    def __init__(self, yedek, url=INTERPOL_URL):
        self.yedek = yedek
        self.url = url

    def kisileri_getir(self):
        try:
            istek = urllib.request.Request(self.url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(istek, timeout=10) as cevap:
                veri = json.load(cevap)
            print("🌐 Canlı Interpol verisi alındı", flush=True)
            return notices_temizle(veri["_embedded"]["notices"])
        except (OSError, KeyError, ValueError) as hata:
            # 403, zaman aşımı, internet yok ya da beklenmeyen cevap
            print("⚠️ Interpol'e erişilemedi:", hata, "→ örnek veri kullanılıyor", flush=True)
            return self.yedek.kisileri_getir()

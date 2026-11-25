import json
class OrnekKaynak:

    def __init__(self,dosya):
        self.dosya = dosya
    def kisileri_getir(self):
        with open(self.dosya) as f:
            notices = json.load(f)["_embedded"]["notices"]
        kisiler = []
        for kisi in notices:
            kisiler.append({
                "entity_id": kisi["entity_id"],
                "forename": kisi["forename"],
                "name": kisi["name"],
                "date_of_birth": kisi["date_of_birth"]
            })
        return kisiler

import os
import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

DB_DOSYASI = os.getenv("DB_DOSYASI", "interpol.db")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def ana_sayfa():
    baglanti = sqlite3.connect(DB_DOSYASI)
    imlec = baglanti.cursor()
    imlec.execute("CREATE TABLE IF NOT EXISTS kisiler (entity_id TEXT PRIMARY KEY, forename TEXT, name TEXT, date_of_birth TEXT, ilk_gorulme TEXT, son_degisiklik TEXT)")
    imlec.execute("SELECT entity_id, forename, name, date_of_birth, ilk_gorulme, son_degisiklik FROM kisiler")
    satirlar = imlec.fetchall()
    baglanti.close()

    html = "<h1>Interpol Kırmızı Bülten 🚨</h1>"
    html += "<table border='1'>"
    html += "<tr><th>ID</th><th>Ad</th><th>Soyad</th><th>Doğum</th><th>İlk görülme</th><th>Son değişiklik</th></tr>"

    for satir in satirlar:
        if satir[4] != satir[5]:
            html += "<tr style='background:#ffcccc'>"
        else:
            html += "<tr>"
        for hucre in satir:
            html += "<td>" + str(hucre) + "</td>"
        html += "</tr>"

    html += "</table>"
    return html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
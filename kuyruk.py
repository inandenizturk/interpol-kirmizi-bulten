import json
import pika


class Kuyruk:
    """RabbitMQ kuyruğuna mesaj gönderen ve kuyruğu dinleyen yardımcı sınıf.

    Container A (gönderen) ve Container B (alan) bu sınıfı ortak kullanır.
    Mesajlar JSON olarak taşınır; sınıf sözlük alır, sözlük verir.
    """

    def __init__(self, host, kuyruk_adi):
        """RabbitMQ'ya bağlanır ve kuyruk yoksa oluşturur."""
        self.kuyruk_adi = kuyruk_adi
        self.baglanti = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.kanal = self.baglanti.channel()
        self.kanal.queue_declare(queue=kuyruk_adi)

    def gonder(self, veri):
        """Sözlüğü JSON metnine çevirip kuyruğa bırakır."""
        self.kanal.basic_publish(exchange='', routing_key=self.kuyruk_adi, body=json.dumps(veri))

    def dinle(self, fonksiyon):
        """Kuyruğu sürekli dinler; gelen her mesajı sözlüğe çevirip verilen fonksiyona iletir."""
        def mesaj_geldi(ch, method, properties, body):
            # pika 4 parametre verir; bize sadece mesajın içeriği (body) lazım
            fonksiyon(json.loads(body))
        self.kanal.basic_consume(queue=self.kuyruk_adi, on_message_callback=mesaj_geldi, auto_ack=True)
        self.kanal.start_consuming()  # bu satırdan sonra program dinlemede kalır, geri dönmez

    def kapat(self):
        """RabbitMQ bağlantısını kapatır."""
        self.baglanti.close()

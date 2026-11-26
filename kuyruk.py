"""RabbitMQ kuyruk işlemleri: mesaj gönderme (Container A) ve dinleme (Container B)."""
import json
import pika
import sys
import time
import os
import sqlite3
from datetime import datetime
sys.stdout.reconfigure(line_buffering=True)
class Kuyruk:
    """RabbitMQ'ya bağlanır; gonder() ile mesaj atar, dinle() ile mesaj alır."""
    def __init__(self, host, kuyruk_adi):
        self.kuyruk_adi = kuyruk_adi
        # RabbitMQ sunucusuna bağlantı ve kanal açılır.
        self.baglanti = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.kanal = self.baglanti.channel()
        # Kuyruk yoksa oluşturulur, varsa olduğu gibi kullanılır.
        self.kanal.queue_declare(queue=kuyruk_adi)
    def gonder(self,veri):
        """Python sözlüğünü JSON metnine çevirip kuyruğa gönderir."""
        self.kanal.basic_publish(exchange='', routing_key=self.kuyruk_adi, body=json.dumps(veri))
    def dinle(self,fonksiyon):
        """Kuyruğu sürekli dinler; her mesajı sözlüğe çevirip verilen fonksiyona iletir."""
        def mesaj_geldi(ch,method,properties,body):
            # Gelen JSON metni tekrar Python sözlüğüne çevrilir.
            fonksiyon(json.loads(body))
        # auto_ack=True: mesaj alınınca kuyruktan otomatik silinir.
        self.kanal.basic_consume(queue=self.kuyruk_adi,on_message_callback=mesaj_geldi,auto_ack=True)
        self.kanal.start_consuming()
    def kapat(self):
        """Bağlantıyı kapatır."""
        self.baglanti.close()

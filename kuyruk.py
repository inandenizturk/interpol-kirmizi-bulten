import json
import pika
import sys
import time
import os
import sqlite3
from datetime import datetime
sys.stdout.reconfigure(line_buffering=True)
class Kuyruk:
    def __init__(self, host, kuyruk_adi):
        self.kuyruk_adi = kuyruk_adi
        self.baglanti = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.kanal = self.baglanti.channel()
        self.kanal.queue_declare(queue=kuyruk_adi)
    def gonder(self,veri):
        self.kanal.basic_publish(exchange='', routing_key=self.kuyruk_adi, body=json.dumps(veri))
    def dinle(self,fonksiyon):
        def mesaj_geldi(ch,method,properties,body):
            fonksiyon(json.loads(body))
        self.kanal.basic_consume(queue=self.kuyruk_adi,on_message_callback=mesaj_geldi,auto_ack=True)
        self.kanal.start_consuming()
    def kapat(self):
        self.baglanti.close()
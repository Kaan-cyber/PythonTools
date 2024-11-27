import os # koda dahil et os (operation system)
import subprocess  # hata yönetimi bağlantı prosedürlerini yöneterek bilgi döner
import requests # yapacağımız istekleri yönetiriz.
import socket # sunucu ve istemci arasında ikisine özel bir yol(soket) oluşturur.
from datetime import datetime
from ipwhois import IPWhois # hedef url(site) hakkında whois kaydı sorgular

def wifi_aglarini_listele(): 
    print("Etraftaki wifi ağlarını tarıyorum...")
    try:
        #netsh wlan ağ komutları tanımlacak --> ödev araştır
        result = subprocess.check_output(['netsh','wlan','show','network'], shell=True, encoding='utf-8') 
        aglar=[]
        for line in result("\n"):
            if "SSID" in line and "SSID name" not in line:
                ssid = line.split(":")[1].strip()
                if ssid and ssid not in aglar:
                    aglar.append(ssid)
        
        print("\nBulunan wi-fi ağları: ")
        for i, ssid in enumerate(aglar[:10], start=1):
            print(f"{i}. {ssid}")

        if len(aglar) == 0:
            print("Hiç Ağ bulunamadı :(")
        
        return aglar[:10]

    except Exception as kaan:
        print("Wi-fi ağlarını tararken bir sorunla karşılarştım - So : ",str(kaan))
        return
    
def url_bilgi_topla_ve_logla(url):
    log_dosyasi = "loglar.txt"    
    try:
        print(f"{url} hakkında bilgi topluyorum")
        ip_adresi = socket.gethostbyname(url.split("//")[-1].split("/")[0]) # Hedef url üzerinden ip adresi öğrenmek için kullanılır.

        obj = IPWhois(ip_adresi)
        whois_bilgisi = obj.lookup_whois() # IPWhois kütüphanesini kullanarak yeni özellikler ekle

        log_mesaj = (
            f"{datetime.now()} - {url}\n"
            f"Ip Adresi: {ip_adresi}\n"
            f"Whois Kaydı : {whois_bilgisi.get('asn_description', 'Bilgi yok(Maskeli)')}\n"
            "************ \n"
        )
        #konsola logları bastır
        print(log_mesaj)
        with open(log_dosyasi,"a", encoding="utf-8") as dosya:
            dosya.write(log_mesaj)

    except Exception as e:
        log_mesaj = f"{datetime.now()} - {url} - Hata Oluştu : {str(e)}\n"
        print(log_mesaj)
        with open(log_dosyasi,"a", encoding="utf-8") as dosya:
            dosya.write(log_mesaj)

def main():
    print("Ağ bilgis ve Url Pasif bilgi toplama aracı - Kagan")
    print("1. Mevcut wi-fi ağlarını listele (10 adet)")
    print("2. bir URL hakkında bilgi toplama ve loglama (ip + whois)")
    print("3. Çıkış")

    while True:
        secim = input("Seçiminizi yapın(1/2/3) : ")
        if secim == '1':
            wifi_aglarini_listele()
        elif secim == '2':
            url = input("Bilgi Toplamak istediğiniz URL'i giriniz (örn: https://google.com) : ")
            url_bilgi_topla_ve_logla(url)
        elif secim == '3':
            print("Program Sonlandırılıyor.")
            break  # exit ile de denersin
        else:
            print("Hatalı bir seçim yaptınız.")
        
if _name_ == "_main_":
    main() #

import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DB_FILE=BASE_DIR /"products.json"
with open(DB_FILE, "r", encoding="utf-8") as dosya:
    urunler = json.load(dosya)


class Urun():
    
    def __init__(self,id=None,title=None,price=0.0,stock=0.0):
        self.id=id
        self.title=title
        self.price=price
        self.stock=stock
    def __str__(self):
        return f"{self.id} - {self.title} - {self.price} - {self.stock}"
    def to_dict(self):
        return {
                "id":self.id,
                "title":self.title,
                "price":self.price,
                "stock":self.stock
                }
    
    
    def urunListele(self,limit):    
        
    
        for urun in urunler[:limit]:
            print("Ürün id\'si:",urun["id"],"\n") 
            print("Ürün Başlığı:",urun["title"],"\n")
            print("Ürün Fiyatı:",urun["price"],"\n")
            print("Ürün Stok Sayısı:",urun["stock"],"\n")
       
    def idUrunAratma(self,aranan_id):
        
        for urun in urunler:
            eslesme_dogru_mu=(urun.get("id")==aranan_id)
            if eslesme_dogru_mu:
                print("Ürün Bulundu.\n")
                print("...ID\'sine Göre Aranan Ürün Bilgileri...\n")
                print("Ürün id\'si:",urun["id"])
                print("Ürün Başlığı:",urun["title"])
                print("Ürün Fiyatı:",urun["price"],"\n")
                print("Ürün Stok Sayısı:",urun["stock"],"\n")

    def titleUrunAratma(self,aranan_title):
       
        for urun in urunler:
            eslesme_dogru_mu=(urun.get("title")==aranan_title)
            if eslesme_dogru_mu:
                print("...Başlığına Göre Aranan Ürün Bilgileri...\n")
                print("Ürün id\'si:",urun["id"])
                print("Ürün Başlığı:",urun["title"])
                print("Ürün Fiyatı:",urun["price"],"\n")
                print("Ürün Stok Sayısı:",urun["stock"],"\n")
    def urunEkle(self, urun_id, urun_title, urun_price, urun_stock):
    # Doğrudan listeye (self.urunler) .append() ile yeni sözlüğü ekliyoruz
        urunler.append({
             "id": urun_id,          # urun_id parametresini doğru eşledik
             "title": urun_title,
             "price": urun_price,
             "stock": urun_stock
         })
        try:
            with open(DB_FILE, "w", encoding="utf-8") as dosya:
                json.dump(urunler, dosya, ensure_ascii=False, indent=4)
            print("Başarılı bir şekilde yeni ürün eklendi ve JSON dosyasına kaydedildi.")
        except Exception as e:
            print( motions=f"Dosyaya kaydedilirken bir hata oluştu: {e}")

    def urunGuncelle(self, urun_id, urun_title, urun_price, urun_stock):
        guncellendi_mi = False
    
    
        for urun in urunler:
            if urun["id"] == urun_id:
                urun["title"] = urun_title
                urun["price"] = urun_price
                urun["stock"] = urun_stock
                guncellendi_mi = True
                break 

        if guncellendi_mi:
            try:
                with open(DB_FILE, "w", encoding="utf-8") as dosya:
               
                    json.dump(urunler, dosya, ensure_ascii=False, indent=4)
                print("ID'si: {} olan ürün başarıyla güncellendi ve kaydedildi.".format(urun_id))
            except Exception as e:
                print("Dosyaya kaydedilirken hata oluştu: {}".format(e))
        else:
            print("Ürün bulunamadı.")

    def urunSilme(self, urun_id):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as dosya:
                urunler = json.load(dosya)
        except json.JSONDecodeError:
            # Eğer JSON dosyası boşsa veya bozuksa hata vermemesi için boş liste bırakıyoruz
            urunler = []
        ilk_boyut = len(urunler)
    
    
        for urun in urunler:
            if urun["id"] == urun_id:
                urunler.remove(urun)  
                break                 
            
    
        if len(urunler) < ilk_boyut:  # Tanımlı olmayan 'veriler' yerine 'urunler' kullanıldı
        
            try:
                with open(DB_FILE, "w", encoding="utf-8") as dosya:
                    json.dump(urunler, dosya, ensure_ascii=False, indent=4)
                print("ID'si {} olan ürün silindi ve JSON dosyası güncellendi.".format(urun_id))
            except Exception as e:
                print("Dosyaya kaydedilirken bir hata oluştu: {}".format(e))
        else:
            print("Ürün bulunamadı.")

    def stokGuncelle(self,urun_id,urun_yeni_stok):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as dosya:
                urunler = json.load(dosya)
        except json.JSONDecodeError:
            # Eğer JSON dosyası boşsa veya bozuksa hata vermemesi için boş liste bırakıyoruz
            urunler = []
        stok_guncellendi_mi=False
        for urun in urunler:
            if urun["id"]==urun_id:
                urun["stock"]=urun_yeni_stok
                stok_guncellendi_mi=True
                break
        if stok_guncellendi_mi:
            
            try:
                with open(DB_FILE, "w", encoding="utf-8") as dosya:
                    json.dump(urunler, dosya, ensure_ascii=False, indent=4)
                print("ID'si {} olan ürün stok güncellendi ve JSON dosyası güncellendi.".format(urun_id))
            except Exception as e:
                print("Dosyaya kaydedilirken bir hata oluştu: {}".format(e))
        else:
            print("Ürün bulunamadı.")
  
    def title_filtreleme(self,title):
       
        filtrelenmis_sonuc = urunler
        if title:
            filtrelenmis_sonuc = [urun for urun in filtrelenmis_sonuc if title.lower() in urun["title"].lower()]
            print(filtrelenmis_sonuc)

    def fiyat_araligina_gore_filtreleme(self,min_fiyat,max_fiyat):
        
    
        filtrelenmis_urunler = [urun for urun in urunler if min_fiyat <= urun["price"] <= max_fiyat]
    
        return filtrelenmis_urunler
    
if __name__ == "__main__":
    urun1=Urun()
    
    while True:
        islem=int(input("Yapmak istediğiniz işlemi seçiniz:\n     1-Ürün Listele\n    2-id numarasına göre ürün listele\n     3-title a göre ürün listele \n     4-ürün oluştur \n     5-ürün güncelle \n    6-ürün sil \n    7-stok güncelle \n  8-Başlığa göre filtreleme \n 9-Fiyat aralığına göre filtreleme\n 0-Çıkış \n"))

        if islem==1:
            limit=int(input("Sıralanacak ürün sayısını giriniz:"))
            urun1.urunListele(limit)
            continue
        elif islem==2:
            aranan_urun_id=int(input("Lütfen aradığınız ürünün id\'sini girin:"))
            urun1.idUrunAratma(aranan_urun_id)
            continue
        elif islem==3:
            aranan_urun_basligi=input("Aradığının ürünün başlığını giriniz:")
            urun1.titleUrunAratma(aranan_urun_basligi)
            continue
        elif islem==4:
            yeni_urun_id=int(input("Ürünün id\'sini giriniz:"))
            yeni_urun_basligi=input("Yeni Ürünün Başlığını giriniz:\n")
            yeni_urun_fiyati=int(input("Yeni Ürün Fiyatı"))
            yeni_urun_stok_sayisi=int(input("Yeni Ürün Stock Sayısını Giriniz:"))
            urun1.urunEkle(yeni_urun_id,yeni_urun_basligi,yeni_urun_fiyati,yeni_urun_stok_sayisi)
            continue
        elif islem==5:
            gunc_urun_id=int(input("Güncellenecek ürün ID\'sini yazınız:"))
            gunc_urun_title=input("Güncellenecek title\'ı yazınız:")
            gunc_urun_price=int(input("Güncellenecek ürün fiyatını giriniz:"))
            gunc_urun_stock=int(input("Güncellenecek stok sayısını giriniz:"))
            urun1.urunGuncelle(gunc_urun_id,gunc_urun_title,gunc_urun_price,gunc_urun_stock)
            continue
        elif islem==6:
            sil_urun_id=int(input("Silinecek ürünün id\'sini  giriniz:"))
            urun1.urunSilme(sil_urun_id)
            continue
        elif islem==7:
            gunc_stok_id=int(input("Stoğu güncellencek ürünün id\'sini giriniz:"))
            gunc_stok=int(input("Yeni stok sayısını giriniz:"))
            urun1.stokGuncelle(gunc_stok_id,gunc_stok)
            continue
        elif islem==8:
            title=input("Filtrelemek istediğiniz title girin:")
            urun1.title_filtreleme(title)
            continue
        elif islem==9:
            min_fiyat=int(input("Filtrelemek istediğiniz minimum fiyatı girin:"))
            max_fiyat=int(input("Filtrelemek istediğiniz maksimum fiyatı girin:"))
            filtreli_urunler = urun1.fiyat_araligina_gore_filtreleme(min_fiyat, max_fiyat)
            for urun in filtreli_urunler:
                print("Ürün Başlığı: {} Ürün Fiyatı: {} \n".format(urun["title"],urun["price"]))
            continue
        elif islem==0:
            print("Programdan çıkış yapıldı.")
            break
    
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
urunDB = BASE_DIR / "products.json"




print("Dosya başarıyla açıldı!")

def urunListele(dosya_yolu,limit=50):    
    with open(urunDB, 'r', encoding='utf-8') as file:
       
        veri =json.load(file)
    
    for urun in veri[:limit]:
       print("Ürün id\'si:",urun["id"],"\n") 
       print("Ürün Başlığı:",urun["title"],"\n")
       print("Ürün Fiyatı:",urun["price"],"\n")
       print("Ürün Stok Sayısı:",urun["stock"],"\n")
       
def idUrunAratma(aranan_id):
    with open(urunDB, 'r', encoding='utf-8') as file:
       
        veri =json.load(file)
    for urun in veri:
        eslesme_dogru_mu=(urun.get("id")==aranan_id)
        if eslesme_dogru_mu:
            print("...ID\'sine Göre Aranan Ürün Bilgileri...\n")
            print("Ürün id\'si:",urun["id"])
            print("Ürün Başlığı:",urun["title"])
            print("Ürün Fiyatı:",urun["price"],"\n")
            print("Ürün Stok Sayısı:",urun["stock"],"\n")

def titleUrunAratma(aranan_title):
    with open(urunDB, 'r', encoding='utf-8') as file:
       
        veri =json.load(file)
    for urun in veri:
        eslesme_dogru_mu=(urun.get("title")==aranan_title)
        if eslesme_dogru_mu:
            print("...Başlığına Göre Aranan Ürün Bilgileri...\n")
            print("Ürün id\'si:",urun["id"])
            print("Ürün Başlığı:",urun["title"])
            print("Ürün Fiyatı:",urun["price"],"\n")
            print("Ürün Stok Sayısı:",urun["stock"],"\n")
def yeniUrunEkle(yeni_urun_id,yeni_urun_basligi,yeni_urun_fiyati,yeni_urun_stok):
        with open(urunDB, 'r', encoding='utf-8') as file:
       
            veri =json.load(file)      

        
        yeni_urun = {
            "id": yeni_urun_id,
            "title": yeni_urun_basligi,
            "price": yeni_urun_fiyati,
            "stock": yeni_urun_stok
        }

        
        veri.append(yeni_urun)

        with open(urunDB, 'w', encoding='utf-8') as file:
            json.dump(veri, file, ensure_ascii=False, indent=4)

        print("Başarılı bir şekilde yeni ürün eklendi.")

def urunGuncelle(urun_id,urun_title,urun_price,urun_stock):
    with open(urunDB, "r", encoding="utf-8") as file:
        veriler = json.load(file )
    guncelendi_mi=False
    for urun in veriler:
        if urun["id"] == urun_id :
            urun["title"]=urun_title
            urun["price"]=urun_price
            urun["stock"]=urun_stock
            guncellendi_mi=True
            break
    if guncellendi_mi:
        with open(urunDB,"w",encoding="utf-8") as file:
            json.dump(veriler,file,ensure_ascii=False,indent=4)
        print("ID\'si: {} olan ürün güncellendi".format(urun_id))
    else:
        print("Ürün bulunamadı.")

def urunSilme(urun_id):
    with open(urunDB,"r",encoding="utf-8") as file:
        urunler=json.load(file)
    ilk_boyut=len(urunler)
    veriler=[urun for urun in urunler if urun["id"] != urun_id]
    if len(veriler)<ilk_boyut:
        with open(urunDB,"w",encoding="utf-8") as file:
            json.dump(veriler,file,ensure_ascii=False,indent=4)
        print("ID\'si {} olan ürün silindi.".format(urun_id))
    else:
        print("Ürün bulunamadı.")

def stokGuncelle(urun_id,urun_yeni_stok):
    with open(urunDB,"r",encoding="utf-8") as file:
        veriler=json.load(file)
    stok_guncellendi_mi=False
    for urun in veriler:
        if urun["id"]==urun_id:
            urun["stock"]=urun_yeni_stok
            stok_guncellendi_mi=True
            break
    if stok_guncellendi_mi:
        with open(urunDB,"w",encoding="utf-8") as file:
            json.dump(veriler,file,ensure_ascii=False,indent=4)
        print("Stok güncellendi.")
    else:
        print("Ürün bulunamadı.")
  
def title_filtreleme(title):
    with open(urunDB, "r", encoding="utf-8") as file:
        veriler = json.load(file)
    filtrelenmis_sonuc = veriler
    if title:
        filtrelenmis_sonuc = [urun for urun in filtrelenmis_sonuc if title.lower() in urun["title"].lower()]
        print(filtrelenmis_sonuc)

def fiyat_araligina_gore_filtreleme(min_fiyat,max_fiyat):
    with open(urunDB, "r", encoding="utf-8") as file:
        veriler = json.load(file)
    
    filtrelenmis_urunler = [urun for urun in veriler if min_fiyat <= urun["price"] <= max_fiyat]
    
    return filtrelenmis_urunler
    


def urunIslemleri():
    islem=int(input("Yapmak istediğiniz işlemi seçiniz:\n     1-Ürün Listele\n    2-id numarasına göre ürün listele\n     3-title a göre ürün listele \n     4-ürün oluştur \n     5-ürün güncelle \n    6-ürün sil \n    7-stok güncelle \n  8-Başlığa göre filtreleme \n 9-Fiyat aralığına göre filtreleme\n"))

    if islem==1:
        urunListele(urunDB,50)
    elif islem==2:
        aranan_urun_id=int(input("Lütfen aradığınız ürünün id\'sini girin:"))
        idUrunAratma(aranan_urun_id)
    elif islem==3:
        aranan_urun_basligi=input("Aradığının ürünün başlığını giriniz:")
        titleUrunAratma(aranan_urun_basligi)
    elif islem==4:
        yeni_urun_id=int(input("Ürünün id\'sini giriniz:"))
        yeni_urun_basligi=input("Yeni Ürünün Başlığını giriniz:\n")
        yeni_urun_fiyati=float(input("Yeni Ürün Fiyatı"))
        yeni_urun_stok_sayisi=int(input("Yeni Ürün Stock Sayısını Giriniz:"))
        yeniUrunEkle(yeni_urun_id,yeni_urun_basligi,yeni_urun_fiyati,yeni_urun_stok_sayisi)
    elif islem==5:
        gunc_urun_id=int(input("Güncellenecek ürün ID\'sini yazınız:"))
        gunc_urun_title=input("Güncellenecek title\'ı yazınız:")
        gunc_urun_price=int(input("Güncellenecek ürün fiyatını giriniz:"))
        gunc_urun_stock=int(input("Güncellenecek stok sayısını giriniz:"))
        urunGuncelle(gunc_urun_id,gunc_urun_title,gunc_urun_price,gunc_urun_stock)
    elif islem==6:
        sil_urun_id=int(input("Silinecek ürünün id\'sini  giriniz:"))
        urunSilme(sil_urun_id)
    elif islem==7:
        gunc_stok_id=int(input("Stoğu güncellencek ürünün id\'sini giriniz:"))
        gunc_stok=int(input("Yeni stok sayısını giriniz:"))
        stokGuncelle(gunc_stok_id,gunc_stok)
    elif islem==8:
        title=input("Filtrelemek istediğiniz title girin:")
        title_filtreleme(title)
    elif islem==9:
        min_fiyat=int(input("Filtrelemek istediğiniz minimum fiyatı girin:"))
        max_fiyat=int(input("Filtrelemek istediğiniz maksimum fiyatı girin:"))
        filtreli_urunler = fiyat_araligina_gore_filtreleme(min_fiyat, max_fiyat)
        for urun in filtreli_urunler:
            print("Ürün Başlığı: {} Ürün Fiyatı: {} \n".format(urun["title"],urun["price"]))
  
    
    
urunIslemleri()

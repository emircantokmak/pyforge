kargo_Durumu= []

while True:
    islem=int(input("Yapmak istediğiniz işlemi seçiniz. \n1-Kargo İşlem Ekle \n2-İşlem Sil \n3-Kargo Güncel Durum\n0-Çıkış"))
    if islem == 1:
        islem_Sirasi=int(input("İşlem Sırası Giriniz:"))
        yeni_islem=input("İşlem Nedir:")
        islem_Bilgisi=input("İşlem Bilgisi Ekle:")
        islem_Durumu=input("İşlem Durumu Ekle")
        islem_Sehiri=input("İşlemin Yapıldığı Şehir Ekle:")
        teslim_Durumu=input("Teslim Durumunu Giriniz:")
        
        yeni_Durum={
            "islem_No":islem_Sirasi,
            "islem_Bilgi":islem_Bilgisi,
            "islem_Durum":islem_Durumu,
            "islem_Sehir":islem_Sehiri,
            "teslim":teslim_Durumu
        }
        kargo_Durumu.append(yeni_Durum)
        
    elif islem == 2:
        for sira, adim in enumerate(kargo_Durumu, start=1):
            print(f"[{sira}] {adim['islem_No']} | {adim['islem_Bilgi']}")
            print(f"    Detay: {adim['islem_Durum']}")
            print(f"    Konum: {adim['islem_Sehir']}")
            print(f"Teslim Durumu {adim["teslim"]}")
            
        print("Güncel Kargo Listesi\n")
        print("-" * 40) 
        silinecek_sira = int(input("Silenecek İslem Numarasını Giriniz:"))
        hedef_indeks = silinecek_sira - 1
        if hedef_indeks < len(kargo_Durumu):
            silinen = kargo_Durumu.pop(hedef_indeks)
            print(f"{silinecek_sira}. sıradaki işlem silindi.")
        else:
            print("Geçersiz bir sıra numarası girdiniz.")
        for sira, adim in enumerate(kargo_Durumu, start=1):
            print(f"[{sira}] {adim['islem_No']} | {adim['islem_Bilgi']}")
            print(f"    Detay: {adim['islem_Durum']}")
            print(f"    Konum: {adim['islem_Sehir']}")
            print(f"Teslim Durumu {adim["teslim"]}")
            print("-" * 40) 
    elif islem == 3:
        if len(kargo_Durumu) > 0:
    # -1 indeksi ile en son eklenen sözlüğü (elemanı) alıyoruz
            son_islem = kargo_Durumu[-1]
    
            print("--- KARGONUZUN SON DURUMU ---")
            print(f"Aşama  : {son_islem['islem_No']}")
            print(f"Durum  : {son_islem['islem_Bilgi']}")
            print(f"Detay  : {son_islem['islem_Durum']}")
            print(f"Konum  : {son_islem['islem_Sehir']}")
            print(f"Teslim Durumu : {son_islem['teslim']}")
            print("-----------------------------")    
    elif islem == 0:
        break
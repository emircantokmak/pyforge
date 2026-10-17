gorevler=[]

while True:
    islem = int(input("\nİşlem Yapmak İstediğiniz seçeneği seçiniz \n1-Yeni Görev Ekle \n2-Görev Sırasına Göre Görev Sil \n3-Görevleri Listele \n0-Çıkış"))
    if islem == 1: # Yeni Görev Ekle
        yeni_gorev=input("Yeni Görevi Yazınız:")
        gorevler.append(yeni_gorev.capitalize())
        
        print(f"Güncel Görevler Listesi\n")
        print(*gorevler, sep="\n")
    elif islem==2:
        k=0
        print(f"Mevcut Görev Listesi\n")
        for i in range(len(gorevler)):
            print(i+1,". Görev:",gorevler[k])
            k+=1
            i+=1

        sirali_gorevi_sil=int(input("Kaçıncı Görevi Silmek İstiyorsunuz."))
        gorevler.pop(sirali_gorevi_sil-1)
        print(f"Güncellenmiş Görev Listesi:\n")
        print(*gorevler,sep="\n")
                    
    elif islem == 3:
        for i in range(len(gorevler)):
            print(i+1,".Görev:",gorevler[i],"\n")
    
    elif islem == 0:
        break
"""
# OOP Haricinde Diğer Tüm Python Konularının Temel Örnekllerle Uygulamaları
#
#
###İçindekiler
# -1- Değişkenler ve Temel Veri Tipleri Dönüşümleri
# -2- Kullancıdan Veri Alma

"""
### - Değişkenler - ###

# - Değişken Tanımlama ve Temel Değişek İşlemleri

sayi1=5
sayi2=10
ad_Soyad="Emir Can Tokmak"
toplam=sayi1+sayi2
print("Toplam: ",toplam)
print("Ad Soyad: ",ad_Soyad)
dogru_Deger=True
yanlis_Deger=False
print("Doğru Değer: ",dogru_Deger)
print("Yanlış Değer: ",yanlis_Deger)
kelime="Merhaba Dünya"
print("Kelime: {0} - Kelime Uzunluğu: {1} ".format(kelime, len(kelime)))

# - Print ile Değişkenleri Ekrana Yazdırma

print("Sayın {0}\'ın ceketini alınız.".format(ad_Soyad))
ad="Cenk"
soyad="Çınar"
print(ad + " " + soyad)
print(ad,soyad,"Danışmaya Lütfen geliniz.")
yas=25
dogum_Yili=2026-yas
print("Yaş: {0} - Doğum Yılı: {1}".format(yas,dogum_Yili))
print("Hacker","Delete",sep="_")
print("Yıldızlı ","Pekiyi",sep="*",end="=>Perfect\n")
print("Yazı alta geçecek",end="\nSatır Başı\n")
print(*"Ayrık Yazı")

# - Kullanıcıdan Veri Alma ve Veri Tipi Dönüşümleri

vize_Notu=int(input("Vize Notunuzu Giriniz: "))
final_Notu=int(input("Final Notunuzu Giriniz: "))
gecerli_Notu=(vize_Notu*0.4)+(final_Notu*0.6)
if(gecerli_Notu>=50):
    print("Geçtiniz. Notunuz: ",gecerli_Notu)
else:
    print("Kaldınız. Notunuz: ",gecerli_Notu)
    







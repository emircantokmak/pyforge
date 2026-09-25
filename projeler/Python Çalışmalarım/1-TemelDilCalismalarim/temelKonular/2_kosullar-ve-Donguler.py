"""
#
#   Python Temel Konular
# - Kosullar ve Döngüler -
#
#

"""

# - Koşullar

vize=int(input("Vize Notunuzu Giriniz: "))
final=int(input("Final Notunuzu Giriniz: "))
büt=int(input("Bütünleme Notunuzu Giriniz: "))
gecer_notu=0.4*vize+0.6*final if final>=50 else 0.4*vize+0.6*büt

if gecer_notu>=50:
    print("Geçtiniz. Notunuz: ",gecer_notu)
else:
    print("Kaldınız. Notunuz: ",gecer_notu)
    
# - Döngüler
a=int(input("Bir sayı giriniz: "))
while True:
        print("*",end="\n")
        a=a-1
        if a==0:
            break
for i in range(1,5):
    print("*",end="\n")
    
meyveler=["Elma","Armut","Muz","Kivi"]
for meyve in meyveler:
    print(meyve,end="\n")

# - Hata Yakalama

try:
    bölünen = int(input("bölünecek sayı: "))
    bölen = int(input("bölen sayı: "))
except ValueError:
    print("Lütfen sadece sayı girin!")
else:
    try:
        print(bölünen/bölen)
    except ZeroDivisionError:
        print("Bir sayıyı 0'a bölemezsiniz!")

try:
    bölünen = int(input("bölünecek sayı: "))
    bölen = int(input("bölen sayı: "))
except ValueError:
        print("Lütfen sadece sayı girin!")
else:
    try:
        print(bölünen/bölen)
    except ZeroDivisionError:
        print("Bir sayıyı 0'a bölemezsiniz!")
        
try:
    dosya = open("dosyaadi.txt", "r")
except IOError:
    print("bir hata oluştu!")
finally:
    dosya.close()

bölünen1 = int(input("bölünecek sayı: "))
if bölünen1 == 23:
    raise Exception("Bu programda 23 sayısını görmek istemiyorum!")
bölen = int(input("bölen sayı: "))
print(bölünen1/bölen)

tr_karakter = "şçğüöıİ"
parola = input("Parolanız: ")
for i in parola:
    if i in tr_karakter:
        raise TypeError("Parolada Türkçe karakter kullanılamaz!")
    else:
        pass
print("Parola kabul edildi!")
    
"""    
#
# - Fonksiyonlar
#

"""

def kayit_olustur(isim, soyisim, issis, sehir):
    print("-"*30)
    print("isim : ", isim)
    print("soyisim : ", soyisim)
    print("işletim sistemi: ", issis)
    print("şehir : ", sehir)
    print("-"*30)
    
kayit_olustur("Fırat", "Özgül", "Ubuntu", "İstanbul")
kayit_olustur("Mehmet", "Öztaban", "Debian", "Ankara")

def kare_bul():
    sayi = 12
    cikti = "{} sayısının karesi {} sayısıdır"
    print(cikti.format(sayi, sayi**2))
kare_bul()

def ismin_ne():
    isim = input("ismin ne? ")
    return isim

x = 0
def fonk():
    x = 1
    return x
print('fonksiyon içindeki x: ', fonk())
print('fonksiyon dışındaki x: ', x)

global isim_degiskeni




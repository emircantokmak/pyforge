"""
#
# - OOP Konuları
#

"""

class HarfSayaci:
    def __init__(self):
        self.sesli_harfler = 'aeıioöuü'
        self.sayac = 0
    def kelime_sor(self):
        return input('Bir kelime girin: ')
    def seslidir(self, harf):
        return harf in self.sesli_harfler
    def artir(self):
        for harf in self.kelime:
            if self.seslidir(harf):
                self.sayac += 1
        return self.sayac
    def ekrana_bas(self):
        mesaj = "{} kelimesinde {} sesli harf var."
        sesli_harf_sayisi = self.artir()
        print(mesaj.format(self.kelime, sesli_harf_sayisi))
    def calistir(self):
        self.kelime = self.kelime_sor()
        self.ekrana_bas()

# - @classmethod Bezeyicisi ve cls

class Calisan():
    personel = []
    def __init__(self, isim):
        self.isim = isim
        self.kabiliyetleri = []
        self.personele_ekle()
    @classmethod
    def personel_sayisini_goruntule(cls):
        print(len(cls.personel))
    def personele_ekle(self):
        self.personel.append(self.isim)
        print('{} adlı kişi personele eklendi'.format(self.isim))
    @classmethod
    def personeli_goruntule(cls):
        print('Personel listesi:')
        for kisi in cls.personel:
            print(kisi)
    def kabiliyet_ekle(self, kabiliyet):
        self.kabiliyetleri.append(kabiliyet)
    def kabiliyetleri_goruntule(self):
        print('{} adlı kişinin kabiliyetleri:'.format(self.isim))
        for kabiliyet in self.kabiliyetleri:
            print(kabiliyet)

# - @staticmethod Bezeyicisi

@staticmethod
def statik_metot():
    print('merhaba statik metot!')
# - Gizli Üyeler 
__gizli = 'gizli'
s = sinif.Sinif()
s._Sinif__gizli
ahmet._CaliSan__personele_ekle()
_yarigizli = 'yarıgizli'
@property
def isim(self):
    return self._isim

# - Setter

@sayi.setter
def sayi(self, yeni_deger):
    if yeni_deger % 2 == 0:
        self._sayi = yeni_deger
    else:
        print('çift değil!')
    return self.sayi

# - Deleter

@sayi.deleter
def sayi(self):
    del self._sayi
    
# - Kalıtım

class Oyuncu():
    def __init__(self, isim, rutbe):
        self.isim = isim    
        self.rutbe = rütbe
        self.güc = 0
    def hareket_et(self):
        print('hareket ediliyor...')
    def puan_kazan(self):
        print('puan kazanıldı')
    def puan_kaybet(self):
        print('puan kaybedildi')
class Asker(Oyuncu):
    def __init__(self, isim, rutbe):
        self.güc = 100
        class Asker(Oyuncu):
            def __init__(self, isim, rutbe):
                super().__init__(isim, rutbe)
            self.guc = 100

if __name__ == '__main__':
    sayac = HarfSayaci()
    sayac.calistir()
    



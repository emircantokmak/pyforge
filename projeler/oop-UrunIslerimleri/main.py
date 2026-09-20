import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "products.json"

try:
    with open(DB_FILE, "r", encoding="utf-8") as dosya:
        urunler = json.load(dosya)
except FileNotFoundError:
    print("products.json dosyası bulunamadı.")
    urunler = []
except json.JSONDecodeError:
    print("products.json dosyasında hata var.")
    urunler = []
except Exception as e:
    print("Ürünler okunurken bir hata oluştu:", e)
    urunler = []


class Urun():

    def __init__(self, id=None, title=None, price=0.0, stock=0.0):
        self.id = id
        self.title = title
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.id} - {self.title} - {self.price} - {self.stock}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "stock": self.stock
        }

    def urunListele(self, limit):
        try:
            for urun in urunler[:limit]:
                print("Ürün id'si:", urun["id"])
                print("Ürün Başlığı:", urun["title"])
                print("Ürün Fiyatı:", urun["price"])
                print("Ürün Stok Sayısı:", urun["stock"])
                print("----------------------")
        except Exception as e:
            print("Ürünler listelenirken bir hata oluştu:", e)

    def idUrunAratma(self, aranan_id):
        try:
            urun_bulundu = False

            for urun in urunler:
                if urun.get("id") == aranan_id:
                    urun_bulundu = True
                    print("Ürün Bulundu.\n")
                    print("...ID'sine Göre Aranan Ürün Bilgileri...\n")
                    print("Ürün id'si:", urun["id"])
                    print("Ürün Başlığı:", urun["title"])
                    print("Ürün Fiyatı:", urun["price"])
                    print("Ürün Stok Sayısı:", urun["stock"])
                    break

            if not urun_bulundu:
                print("Ürün bulunamadı.")

        except Exception as e:
            print("Ürün aranırken bir hata oluştu:", e)

    def titleUrunAratma(self, aranan_title):
        try:
            urun_bulundu = False

            for urun in urunler:
                if urun.get("title", "").lower() == aranan_title.lower():
                    urun_bulundu = True
                    print("...Başlığına Göre Aranan Ürün Bilgileri...\n")
                    print("Ürün id'si:", urun["id"])
                    print("Ürün Başlığı:", urun["title"])
                    print("Ürün Fiyatı:", urun["price"])
                    print("Ürün Stok Sayısı:", urun["stock"])
                    print("----------------------")

            if not urun_bulundu:
                print("Bu başlıkta ürün bulunamadı.")

        except Exception as e:
            print("Ürün aranırken bir hata oluştu:", e)

    def urunEkle(self, urun_id, urun_title, urun_price, urun_stock):
        try:
            urunler.append({
                "id": urun_id,
                "title": urun_title,
                "price": urun_price,
                "stock": urun_stock
            })

            with open(DB_FILE, "w", encoding="utf-8") as dosya:
                json.dump(urunler, dosya, ensure_ascii=False, indent=4)

            print("Başarılı bir şekilde yeni ürün eklendi ve JSON dosyasına kaydedildi.")

        except Exception as e:
            print("Dosyaya kaydedilirken bir hata oluştu:", e)

    def urunGuncelle(self, urun_id, urun_title, urun_price, urun_stock):
        try:
            guncellendi_mi = False

            for urun in urunler:
                if urun["id"] == urun_id:
                    urun["title"] = urun_title
                    urun["price"] = urun_price
                    urun["stock"] = urun_stock
                    guncellendi_mi = True
                    break

            if guncellendi_mi:
                with open(DB_FILE, "w", encoding="utf-8") as dosya:
                    json.dump(urunler, dosya, ensure_ascii=False, indent=4)

                print("ID'si: {} olan ürün başarıyla güncellendi ve kaydedildi.".format(urun_id))
            else:
                print("Ürün bulunamadı.")

        except Exception as e:
            print("Ürün güncellenirken bir hata oluştu:", e)

    def urunSilme(self, urun_id):
        try:
            urun_bulundu = False

            for urun in urunler:
                if urun["id"] == urun_id:
                    urunler.remove(urun)
                    urun_bulundu = True
                    break

            if urun_bulundu:
                with open(DB_FILE, "w", encoding="utf-8") as dosya:
                    json.dump(urunler, dosya, ensure_ascii=False, indent=4)

                print("ID'si {} olan ürün silindi ve JSON dosyası güncellendi.".format(urun_id))
            else:
                print("Ürün bulunamadı.")

        except Exception as e:
            print("Ürün silinirken bir hata oluştu:", e)

    def stokGuncelle(self, urun_id, urun_yeni_stok):
        try:
            stok_guncellendi_mi = False

            for urun in urunler:
                if urun["id"] == urun_id:
                    urun["stock"] = urun_yeni_stok
                    stok_guncellendi_mi = True
                    break

            if stok_guncellendi_mi:
                with open(DB_FILE, "w", encoding="utf-8") as dosya:
                    json.dump(urunler, dosya, ensure_ascii=False, indent=4)

                print("ID'si {} olan ürün stok güncellendi ve JSON dosyası güncellendi.".format(urun_id))
            else:
                print("Ürün bulunamadı.")

        except Exception as e:
            print("Stok güncellenirken bir hata oluştu:", e)

    def title_filtreleme(self, title):
        try:
            filtrelenmis_sonuc = []

            for urun in urunler:
                if title.lower() in urun.get("title", "").lower():
                    filtrelenmis_sonuc.append(urun)

            if len(filtrelenmis_sonuc) > 0:
                print("\nTitle'a göre bulunan ürünler:\n")

                for urun in filtrelenmis_sonuc:
                    print("Ürün id'si:", urun["id"])
                    print("Ürün Başlığı:", urun["title"])
                    print("Ürün Fiyatı:", urun["price"])
                    print("Ürün Stok Sayısı:", urun["stock"])
                    print("----------------------")
            else:
                print("Aradığınız title ile eşleşen ürün bulunamadı.")

        except Exception as e:
            print("Title filtreleme sırasında bir hata oluştu:", e)

    def fiyat_araligina_gore_filtreleme(self, min_fiyat, max_fiyat):
        try:
            filtrelenmis_urunler = [
                urun for urun in urunler
                if min_fiyat <= urun["price"] <= max_fiyat
            ]

            return filtrelenmis_urunler

        except Exception as e:
            print("Fiyat filtreleme sırasında bir hata oluştu:", e)
            return []


if __name__ == "__main__":
    urun1 = Urun()

    while True:
        try:
            islem = int(input(
                "\nYapmak istediğiniz işlemi seçiniz:\n"
                "1-Ürün Listele\n"
                "2-id numarasına göre ürün listele\n"
                "3-title a göre ürün listele\n"
                "4-ürün oluştur\n"
                "5-ürün güncelle\n"
                "6-ürün sil\n"
                "7-stok güncelle\n"
                "8-Başlığa göre filtreleme\n"
                "9-Fiyat aralığına göre filtreleme\n"
                "10-Terminali temizle\n"
                "0-Çıkış\n"
            ))

        except ValueError:
            print("Lütfen menüden geçerli bir sayı giriniz.")
            continue
        except Exception as e:
            print("Bir hata oluştu:", e)
            continue

        try:
            if islem == 1:
                try:
                    limit = int(input("Sıralanacak ürün sayısını giriniz:"))
                    if limit < 0:
                        print("Ürün sayısı negatif olamaz.")
                        continue
                    urun1.urunListele(limit)
                except ValueError:
                    print("Lütfen ürün sayısını sayı olarak giriniz.")
                continue

            elif islem == 2:
                try:
                    aranan_urun_id = int(input("Lütfen aradığınız ürünün id'sini girin:"))
                    urun1.idUrunAratma(aranan_urun_id)
                except ValueError:
                    print("ID için sayı girmeniz gerekiyor.")
                continue

            elif islem == 3:
                aranan_urun_basligi = input("Aradığınız ürünün başlığını giriniz:")
                if aranan_urun_basligi.strip() == "":
                    print("Başlık boş bırakılamaz.")
                    continue
                urun1.titleUrunAratma(aranan_urun_basligi)
                continue

            elif islem == 4:
                try:
                    yeni_urun_id = int(input("Ürünün id'sini giriniz:"))
                    yeni_urun_basligi = input("Yeni Ürünün Başlığını giriniz:\n")

                    if yeni_urun_basligi.strip() == "":
                        print("Ürün başlığı boş bırakılamaz.")
                        continue

                    yeni_urun_fiyati = float(input("Yeni Ürün Fiyatı: "))
                    yeni_urun_stok_sayisi = int(input("Yeni Ürün Stock Sayısını Giriniz:"))

                    if yeni_urun_fiyati < 0 or yeni_urun_stok_sayisi < 0:
                        print("Fiyat ve stok negatif olamaz.")
                        continue

                    urun1.urunEkle(
                        yeni_urun_id,
                        yeni_urun_basligi,
                        yeni_urun_fiyati,
                        yeni_urun_stok_sayisi
                    )

                except ValueError:
                    print("ID, fiyat ve stok alanlarına geçerli sayılar giriniz.")
                continue

            elif islem == 5:
                try:
                    gunc_urun_id = int(input("Güncellenecek ürün ID'sini yazınız:"))
                    gunc_urun_title = input("Güncellenecek title'ı yazınız:")

                    if gunc_urun_title.strip() == "":
                        print("Ürün başlığı boş bırakılamaz.")
                        continue

                    gunc_urun_price = float(input("Güncellenecek ürün fiyatını giriniz:"))
                    gunc_urun_stock = int(input("Güncellenecek stok sayısını giriniz:"))

                    if gunc_urun_price < 0 or gunc_urun_stock < 0:
                        print("Fiyat ve stok negatif olamaz.")
                        continue

                    urun1.urunGuncelle(
                        gunc_urun_id,
                        gunc_urun_title,
                        gunc_urun_price,
                        gunc_urun_stock
                    )

                except ValueError:
                    print("ID, fiyat ve stok alanlarına geçerli sayılar giriniz.")
                continue

            elif islem == 6:
                try:
                    sil_urun_id = int(input("Silinecek ürünün id'sini giriniz:"))
                    urun1.urunSilme(sil_urun_id)
                except ValueError:
                    print("Silmek istediğiniz ürünün ID'sini sayı olarak giriniz.")
                continue

            elif islem == 7:
                try:
                    gunc_stok_id = int(input("Stoğu güncellenecek ürünün id'sini giriniz:"))
                    gunc_stok = int(input("Yeni stok sayısını giriniz:"))

                    if gunc_stok < 0:
                        print("Stok negatif olamaz.")
                        continue

                    urun1.stokGuncelle(gunc_stok_id, gunc_stok)

                except ValueError:
                    print("ID ve stok alanlarına geçerli bir sayı giriniz.")
                continue

            elif islem == 8:
                title = input("Filtrelemek istediğiniz title girin:")

                if title.strip() == "":
                    print("Filtreleme için bir title giriniz.")
                    continue

                urun1.title_filtreleme(title)
                continue

            elif islem == 9:
                try:
                    min_fiyat = float(input("Filtrelemek istediğiniz minimum fiyatı girin:"))
                    max_fiyat = float(input("Filtrelemek istediğiniz maksimum fiyatı girin:"))

                    if min_fiyat < 0 or max_fiyat < 0:
                        print("Fiyat negatif olamaz.")
                        continue

                    if min_fiyat > max_fiyat:
                        print("Minimum fiyat maksimum fiyattan büyük olamaz.")
                        continue

                    filtreli_urunler = urun1.fiyat_araligina_gore_filtreleme(
                        min_fiyat, max_fiyat
                    )

                    if len(filtreli_urunler) > 0:
                        for urun in filtreli_urunler:
                            print(
                                "Ürün Başlığı: {} Ürün Fiyatı: {}"
                                .format(urun["title"], urun["price"])
                            )
                    else:
                        print("Bu fiyat aralığında ürün bulunamadı.")

                except ValueError:
                    print("Fiyat alanlarına geçerli sayılar giriniz.")
                continue

            elif islem == 10:
                try:
                    import os

                    if os.name == "nt":
                        os.system("cls")
                    else:
                        os.system("clear")

                except Exception as e:
                    print("Terminal temizlenirken bir hata oluştu:", e)

                continue

            elif islem == 0:
                print("Programdan çıkış yapıldı.")
                break

            else:
                print("Menüde olmayan bir işlem seçtiniz.")

        except Exception as e:
            print("İşlem sırasında beklenmeyen bir hata oluştu:", e)

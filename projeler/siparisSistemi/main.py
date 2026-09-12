from pathlib import Path
import json
import random
from abc import ABC, abstractmethod

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "restaurant_menus.json"

if not DB_FILE.exists():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({"menuler": {}, "aktif_siparisler": []}, f, ensure_ascii=False, indent=4)


# --- 1. SOYUT TABAN SINIF (ABSTRACTION & ENCAPSULATION) ---
class Urun(ABC):
    def __init__(self, isim: str, fiyat: float, kategori: str, stok: int = 0):
        self.isim = isim
        self._fiyat = fiyat
        self.kategori = kategori
        self._stok = stok

    @property
    def fiyat(self):
        return self._fiyat

    @fiyat.setter
    def fiyat(self, yeni_fiyat):
        if yeni_fiyat < 0:
            raise ValueError("Fiyat negatif olamaz!")
        self._fiyat = yeni_fiyat

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, yeni_stok):
        if yeni_stok < 0:
            print(" Stok miktarı negatif olamaz!")
            return
        self._stok = yeni_stok

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class Icecek(Urun):
    def __init__(self, isim: str, fiyat: float, kategori: str, boyut: str, stok: int = 0):
        super().__init__(isim, fiyat, kategori, stok)
        self.boyut = boyut

    def __str__(self):
        return f"[İçecek] {self.isim} ({self.boyut}) - {self.fiyat} TL [Stok: {self.stok}]"

    def to_dict(self):
        return {
            "tip": "Icecek",
            "isim": self.isim,
            "fiyat": self.fiyat,
            "kategori": self.kategori,
            "boyut": self.boyut,
            "stok": self.stok
        }


class Yiyecek(Urun):
    def __init__(self, isim: str, fiyat: float, kategori: str, porsiyon: str, stok: int = 0):
        super().__init__(isim, fiyat, kategori, stok)
        self.porsiyon = porsiyon

    def __str__(self):
        return f"[Yiyecek] {self.isim} ({self.porsiyon}) - {self.fiyat} TL [Stok: {self.stok}]"

    def to_dict(self):
        return {
            "tip": "Yiyecek",
            "isim": self.isim,
            "fiyat": self.fiyat,
            "kategori": self.kategori,
            "porsiyon": self.porsiyon,
            "stok": self.stok
        }

class Menu:
    def __init__(self, menu_adi: str):
        self.menu_adi = menu_adi
        self.urunler = []

    def urun_ekle(self, urun: Urun):
        if any(u.isim.lower() == urun.isim.lower() for u in self.urunler):
            print(f" {urun.isim} bu menüde zaten var!")
            return False
        self.urunler.append(urun)
        return True

    def urun_bul(self, urun_ismi: str) -> Urun:
        for urun in self.urunler:
            if urun.isim.lower() == urun_ismi.lower():
                return urun
        return None

    def goster(self):
        print(f"\n---  {self.menu_adi.upper()} İÇERİĞİ ---")
        if not self.urunler:
            print("Bu menü henüz boş.")
            return
        for i, urun in enumerate(self.urunler, start=1):
            print(f"  {i}. {urun}")


# --- 4. SİPARİŞ / SEPET VE AKTİF SİPARİŞ YÖNETİMİ ---
class Siparis:
    def __init__(self, siparis_id: int = None, menu_adi: str = ""):
        self.siparis_id = siparis_id if siparis_id else random.randint(1000, 9999)
        self.menu_adi = menu_adi
        self.sepet = []

    def urun_ekle(self, urun: Urun, adet: int = 1):
        if adet <= 0:
            print(" Adet en az 1 olmalıdır.")
            return False
        if urun.stok < adet:
            print(f" Yetersiz stok! En fazla {urun.stok} adet ekleyebilirsiniz.")
            return False
        
        for item in self.sepet:
            if item["urun_ismi"].lower() == urun.isim.lower():
                if urun.stok < adet:
                    print(f" Stok aşılıyor! En fazla {urun.stok} adet daha alabilirsiniz.")
                    return False
                item["adet"] += adet
                urun.stok -= adet
                print(f" {urun.isim} adedi güncellendi ({item['adet']} adet).")
                return True
        
        self.sepet.append({"urun_ismi": urun.isim, "adet": adet, "fiyat": urun.fiyat})
        urun.stok -= adet
        print(f" {urun.isim} sepete/siparişe eklendi.")
        return True

    def urun_sil(self, urun: Urun, adet: int = 1):
        for item in self.sepet:
            if item["urun_ismi"].lower() == urun.isim.lower():
                if item["adet"] > adet:
                    item["adet"] -= adet
                    urun.stok += adet
                    print(f" {adet} adet {urun.isim} sepetten/siparişten düşüldü.")
                else:
                    urun.stok += item["adet"]
                    self.sepet.remove(item)
                    print(f" {urun.isim} tamamen silindi.")
                return True
        print(f" Siparişte '{urun.isim}' bulunamadı.")
        return False

    def toplam_tutar(self):
        return sum(item["fiyat"] * item["adet"] for item in self.sepet)

    def goster(self):
        if not self.sepet:
            print(f"\n Sipariş No #{self.siparis_id} içeriği boş.")
            return False
        print(f"\n --- SİPARİŞ NO: #{self.siparis_id} (Menü: {self.menu_adi}) ---")
        for item in self.sepet:
            print(f" {item['urun_ismi']} x {item['adet']} adet | Birim: {item['fiyat']} TL | Toplam: {item['fiyat'] * item['adet']} TL")
        print(f" Toplam Tutar: {self.toplam_tutar()} TL")
        return True

    def to_dict(self):
        return {
            "siparis_id": self.siparis_id,
            "menu_adi": self.menu_adi,
            "sepet": self.sepet
        }

    @staticmethod
    def from_dict(data):
        siparis = Siparis(data["siparis_id"], data["menu_adi"])
        siparis.sepet = data["sepet"]
        return siparis


# --- 5. ANA RESTORAN YÖNETİMİ ---
class Restaurant:
    def __init__(self, isim: str):
        self.isim = isim
        self.menuler = {}
        self.aktif_siparisler = []
        self.verileri_yukle()

    def yeni_menu_ekle(self, menu_adi: str):
        if menu_adi.lower() in [m.lower() for m in self.menuler]:
            print(f" '{menu_adi}' adında bir menü zaten mevcut.")
            return False
        self.menuler[menu_adi] = Menu(menu_adi)
        self.verileri_kaydet()
        print(f" '{menu_adi}' başarıyla oluşturuldu.")
        return True

    def menu_sil(self, menu_adi: str):
        hedef_key = next((k for k in self.menuler if k.lower() == menu_adi.lower()), None)
        if hedef_key:
            del self.menuler[hedef_key]
            self.verileri_kaydet()
            print(f" '{hedef_key}' ve tüm içeriği kalıcı olarak silindi.")
            return True
        print(f" '{menu_adi}' adında bir menü bulunamadı.")
        return False

    def hazır_sablon_yukle(self):
        self.yeni_menu_ekle("Standart Menü")
        sm = self.menuler["Standart Menü"]
        sm.urun_ekle(Yiyecek("Klasik Burger", 180.0, "Yiyecek", "Tek", 20))
        sm.urun_ekle(Yiyecek("Margarita Pizza", 220.0, "Yiyecek", "Orta", 15))
        sm.urun_ekle(Icecek("Kola", 40.0, "İçecek", "330ml", 50))
        sm.urun_ekle(Icecek("Ayran", 25.0, "İçecek", "250ml", 40))
        self.verileri_kaydet()
        print(" Hazır şablon 'Standart Menü' başarıyla sisteme kuruldu!")

    def menuleri_listele(self):
        if not self.menuler:
            print("Restoranda tanımlı menü bulunamadı.")
            return False
        print(f"\n --- {self.isim.upper()} MENÜ LİSTESİ ---")
        for i, m_adi in enumerate(self.menuler.keys(), start=1):
            print(f"{i}. {m_adi}")
        return True

    def aktif_siparisleri_listele(self):
        if not self.aktif_siparisler:
            print("\n Sistemde kayıtlı aktif bir sipariş bulunmuyor.")
            return False
        print("\n --- AKTİF SİPARİŞ LİSTESİ ---")
        print(f"{'Sipariş ID':<12} | {'Kullanılan Menü':<20} | {'Toplam Tutar':<12}")
        print("-" * 52)
        for s in self.aktif_siparisler:
            print(f"{s.siparis_id:<11} | {s.menu_adi:<20} | {s.toplam_tutar():<10} TL")
        print("-" * 52)
        return True

        def siparis_bul(self, siparis_id: int) -> Siparis:
        for s in self.aktif_siparisler:
            if s.siparis_id == siparis_id:
                return s
        return None

    def siparis_sil(self, siparis_id: int):
        siparis = self.siparis_bul(siparis_id)
        if not siparis:
            print(f"❌ #{siparis_id} numaralı sipariş bulunamadı.")
            return False
        
        menu = self.menuler.get(siparis.menu_adi)
        if menu:
            for item in siparis.sepet:
                urun = menu.urun_bul(item["urun_ismi"])
                if urun:
                    urun.stok += item["adet"]
        
        self.aktif_siparisler.remove(siparis)
        self.verileri_kaydet()
        print(f"🗑️ #{siparis_id} numaralı sipariş başarıyla iptal edildi.")
        return True

    def verileri_kaydet(self):
        data = {
            "menuler": {m_adi: [u.to_dict() for u in m_obj.urunler] for m_adi, m_obj in self.menuler.items()},
            "aktif_siparisler": [s.to_dict() for s in self.aktif_siparisler]
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def verileri_yukle(self):
        try:
            if DB_FILE.exists() and DB_FILE.stat().st_size > 0:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for m_adi, urun_listesi in data.get("menuler", {}).items():
                        yeni_menu = Menu(m_adi)
                        for item in urun_listesi:
                            if item["tip"] == "Icecek":
                                urun = Icecek(item["isim"], item["fiyat"], item["kategori"], item["boyut"], item.get("stok", 0))
                            else:
                                urun = Yiyecek(item["isim"], item["fiyat"], item["kategori"], item["porsiyon"], item.get("stok", 0))
                            yeni_menu.urunler.append(urun)
                        self.menuler[m_adi] = yeni_menu
                    self.aktif_siparisler = [Siparis.from_dict(s) for s in data.get("aktif_siparisler", [])]
        except Exception as e:
            print("⚠️ Veritabanı yüklenirken bir hata oluştu:", e)


# --- INTERAKTIF ANA EKRAN (MAIN) ---
def main():
    print("--- RESTORAN KURULUM SİSTEMİ ---")
    restoran_adi = input("Lütfen restoranınızın adını giriniz: ").strip()
    if not restoran_adi:
        restoran_adi = "Saray Lezzetleri"
    
    restoran = Restaurant(restoran_adi)
    
    if not restoran.menuler:
        hazir_onay = input("\nSistemde tanımlı menü bulunamadı. Hazır örnek 'Standart Menü' yüklensin mi? (E/H): ").strip().lower()
        if hazir_onay == 'e':
            restoran.hazır_sablon_yukle()

    while True:
        print(f"\n=== {restoran.isim.upper()} OTOMASYONU ===")
        print("1. Menü İşlemleri (Listele / Ekle / Sil / Güncelle)")
        print("2.  Yeni Sipariş Oluştur (Sepet)")
        print("3.  Siparişleri Listele (Özet & Detaylı Görünüm)")
        print("4.  Aktif Siparişi Güncelle (Ürün Ekle/Sil/Adet Değiştir)")
        print("5.  Aktif Siparişi Sil (İptal Et)")
        print("6. Çıkış")
        
        secim = input("İşlem Seçiniz (1-6): ").strip()

        if secim == "1":
            print("\n[ Menü Yönetim Paneli ]")
            print("1. Menüleri ve İçeriklerini Listele")
            print("2. Yeni Menü Başlığı Ekle")
            print("3. Komple Menü Sil")
            print("4. Menüye Ürün Ekle / Stok Güncelle")
            m_secim = input("Seçiminiz: ").strip()

            if m_secim == "1":
                if restoran.menuleri_listele():
                    m_adi = input("İçeriğini görmek istediğiniz menü adı: ").strip()
                    h_menu = next((restoran.menuler[k] for k in restoran.menuler if k.lower() == m_adi.lower()), None)
                    if h_menu: h_menu.goster()
                    else: print(" Geçersiz menü.")
            elif m_secim == "2":
                m_adi = input("Yeni oluşturulacak menünün adı ne olsun?: ").strip()
                if m_adi: restoran.yeni_menu_ekle(m_adi)
            elif m_secim == "3":
                if restoran.menuleri_listele():
                    m_adi = input("Silinecek menünün tam adını yazın: ").strip()
                    restoran.menu_sil(m_adi)
            elif m_secim == "4":
                if restoran.menuleri_listele():
                    m_adi = input("Güncellenecek menünün adını yazın: ").strip()
                    h_menu = next((restoran.menuler[k] for k in restoran.menuler if k.lower() == m_adi.lower()), None)
                    if h_menu:
                        print("1. Yiyecek Ekle | 2. İçecek Ekle | 3. Yiyecek Stok Güncelle | 4. İçecek Stok Güncelle")
                        g_secim = input("Seçim: ").strip()
                        if g_secim in ["1", "2"]:
                            isim = input("Ürün İsmi: ").strip()
                            try:
                                fiyat = float(input("Fiyat (TL): "))
                                kategori = input("Kategori Adı: ").strip()
                                stok = int(input("Başlangıç Stok Miktarı: "))
                                if g_secim == "1":
                                    h_menu.urun_ekle(Yiyecek(isim, fiyat, kategori, input("Porsiyon Tipi: "), stok))
                                else:
                                    h_menu.urun_ekle(Icecek(isim, fiyat, kategori, input("Boyut: "), stok))
                                restoran.verileri_kaydet()
                            except ValueError:
                                print(" Hatalı veri girişi!")
                        elif g_secim in ["3", "4"]:
                            u_adi = input("Stok miktarını değiştirmek istediğiniz ürünün adı: ").strip()
                            urun = h_menu.urun_bul(u_adi)
                            if urun:
                                try:
                                    urun.stok = int(input(f"Yeni Stok Değerini Girin (Mevcut: {urun.stok}): "))
                                    restoran.verileri_kaydet()
                                except ValueError:
                                    print(" Geçersiz sayı.")

        elif secim == "2":
            if restoran.menuleri_listele():
                m_secim = input("Hangi menüyü kullanarak sipariş oluşturmak istersiniz?: ").strip()
                h_menu = next((restoran.menuler[k] for k in restoran.menuler if k.lower() == m_secim.lower()), None)
                if h_menu:
                    gecici_siparis = Siparis(menu_adi=h_menu.menu_adi)
                    while True:
                        h_menu.goster()
                        print("\n[ Alışveriş Sepeti ] 1. Ürün Ekle | 2. Ürün Çıkar | 3. Siparişi Tamamla | 4. İptal")
                        s_secim = input("Seçim: ").strip()
                        if s_secim == "1":
                            u_adi = input("Sepete eklenecek ürünün adı: ").strip()
                            urun = h_menu.urun_bul(u_adi)
                            if urun:
                                try:
                                    adet = int(input(f"Kaç adet '{urun.isim}' eklemek istiyorsunuz?: "))
                                    gecici_siparis.urun_ekle(urun, adet)
                                except ValueError:
                                    print(" Geçersiz adet.")
                        elif s_secim == "2":
                            u_adi = input("Sepetten çıkarılacak ürünün adı: ").strip()
                            urun = h_menu.urun_bul(u_adi)
                            if urun:
                                try:
                                    adet = int(input("Kaç adet çıkarılsın?: "))
                                    gecici_siparis.urun_sil(urun, adet)
                                except ValueError:
                                    print(" Geçersiz adet.")
                        elif s_secim == "3":
                            if gecici_siparis.goster():
                                if input("Siparişi onaylayıp mutfağa göndermek istiyor musunuz? (E/H): ").strip().lower() == 'e':
                                    restoran.aktif_siparisler.append(gecici_siparis)
                                    restoran.verileri_kaydet()
                                    print(f" Sipariş onaylandı! Sipariş Numarası: #{gecici_siparis.siparis_id}")
                                    break
                        elif s_secim == "4":
                            for item in gecici_siparis.sepet:
                                urun = h_menu.urun_bul(item["urun_ismi"])
                                if urun: urun.stok += item["adet"]
                            print("Sipariş iptal edildi, sepet boşaltıldı.")
                            break

        elif secim == "3":
            if restoran.aktif_siparisleri_listele():
                detay_istek = input("Detaylarını görmek istediğiniz Sipariş Numarasını yazın (Geri dönmek için Enter): ").strip()
                if detay_istek:
                    try:
                        s_id = int(detay_istek)
                        bulunan_siparis = restoran.siparis_bul(s_id)
                        if bulunan_siparis: bulunan_siparis.goster()
                        else: print(" Aradığınız ID ile eşleşen bir sipariş bulunamadı.")
                    except ValueError:
                        print(" Lütfen geçerli sayısal bir ID girin.")

        elif secim == "4":
            if restoran.aktif_siparisleri_listele():
                try:
                    s_id = int(input("Güncelleme yapmak istediğiniz Sipariş Numarasını (ID) yazın: "))
                    siparis = restoran.siparis_bul(s_id)
                    if not siparis:
                        print("❌ Sipariş bulunamadı.")
                        continue
                    

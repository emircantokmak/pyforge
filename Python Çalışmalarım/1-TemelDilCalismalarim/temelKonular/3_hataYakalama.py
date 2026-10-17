"""
----------------------------------------------------------
#
# - Python Çalışmala Notlarım -
# - Konu - : Hata Yakalama
#
---------------------------------------------------
"""

sayi1=input("1. sayıyı giriniz:")
sayi2=input("2. sayıyı giriniz")

try:
    sayi1=float(sayi1)
    sayi2=float(sayi2)
    print("Sonuç:",sayi1/sayi2)
except ValueError:
    print("Sadece rakam girmelisiniz.")
    quit()
except ZeroDivisionError:
    print("Tanımsız")
finally:
    print("Program sonlandı.")

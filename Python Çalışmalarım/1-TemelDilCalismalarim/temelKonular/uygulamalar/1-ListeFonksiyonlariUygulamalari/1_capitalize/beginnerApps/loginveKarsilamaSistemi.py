kayitli_Kullanici="Ahmet"
girilen_Kullanici=input("İsminizi giriniz:")

if girilen_Kullanici.capitalize() == kayitli_Kullanici:
    print("Giriş Başarılı.Hoşgeldiniz {}.".format(girilen_Kullanici.capitalize()))
else:
    print(f"Giriş başarısız.Tekrar deneyiniz.")
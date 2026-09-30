"""
----------------------------------------------------------
#
# - Python Çalışmala Notlarım -
# - Konu - : Kontrollü İfadeler ve Döngüler
#
---------------------------------------------------
"""

# - if-elif-else Kontrolleri - 

vize=int(input("Vize notunu giriniz:"))
final=int(input("Final notunu giriniz:"))
if vize*0.4+final*0.6 >= 60:
    print("Geçtiniz")
else:
    print("Kaldınız")

meyveler= ["elma","armut","çilek"]
meyve=input("bir meyve ismi giriniz:")
if meyve in meyveler:
    print("Aradığınız {0} meyvesi sepette var.".format(meyve))
else:
    print("aradığınız meyve sepette yok")
    
# - for Döngüsü - 
for i in range(1,10):
    print("{0}. Üye Giriş Yaptı.\n".format(i))
for meyve in meyveler:
    print(meyve,"\n")
    
# - while Döngüsü -
i=1
while i <= 10:
    print("{0} \n".format(i)) 
    i+=1

    
            
    
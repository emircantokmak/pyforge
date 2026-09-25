"""

#
# - Python Veri Patternleri
# - 1- Lists
# - 2- Tuple
# - 3- Set
# - 4- Dictionary
#
    
"""

# - Lists

liste = ["öğe1", "öğe2", "öğe3"]
type(liste)

kardiz = "İstanbul Büyükşehir Belediyesi"
kardiz.split()
kardiz[0]

sayilar = [[0, 10], [6, 60], [12, 54], [67, 99]]
for i in sayilar:
    print(*range(*i))

for k in sayilar:
    print(k)

meyveler = ["elma", "armut", "çilek", "kiraz"]
for meyve in meyveler:
    print(meyve)
    print(meyveler[-1])

# - Tuple

demet = ("ahmet", "mehmet", 23, 45)
type(demet)

# - Dictionary

çeviri_tablosu = {"Ö": "O",
    "ç": "c",
    "Ü": "U",
    "Ç": "C",
    "İ": "I",
    "ı": "i",
    "Ğ": "G",
    "ö": "o",
    "ş": "s",
    "ü": "u",
    "Ş": "S",
    "ğ": "g"}

sozluk = {"kitap" : "book",
    "bilgisayar" : "computer",
    "programlama": "programming",
    "dil" : "language",
    "defter" : "notebook"}

print(sozluk["kitap"])

print(çeviri_tablosu["Ş"])

for i in çeviri_tablosu:
    print(çeviri_tablosu[i])
    

# - Sets ve Frozenset

kume = {'Python', 'C++', 'Ruby', 'PHP'}
type(kume)

liste3 = ["elma", "armut", "elma", "kiraz","çilek", "kiraz", "elma", "kebap"]
for i in set(liste3):
    print("{} listede {} kez geçiyor!".format(i, liste3.count(i)))
    

    
    



    





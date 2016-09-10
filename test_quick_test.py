import csv

lang_639_1 = []
lang_639_2_T = []
lang_639_2_B = []
lang_639_3 = []
lang_639_6 = []

with open('/Users/max/projects/LightMagic/test_languages.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar=',')
    for row in spamreader:
        item = str(row[0]).split(',')
        lang_639_1.append(item[0])
        lang_639_2_T.append(item[1])
        lang_639_2_B.append(item[2])
        lang_639_3.append(item[3])
        if len(item) > 4:
            lang_639_6.append(item[4])


print(lang_639_1)
print(lang_639_2_T)
print(lang_639_2_B)
print(lang_639_3)

lang_639_6 = [x for x in lang_639_6 if len(x) > 0]
print(lang_639_6)

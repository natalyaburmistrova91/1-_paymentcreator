def dict_to_cort_legioner(dict, started_number):
    list_cort = []
    list_key = dict.keys()
    for el1 in list_key:
        a = [dict.get(el1), el1]
        list_cort.append(a)
    list_legioner_sorted = sorted(list_cort, reverse=True)
    list_legioner_final = []
    for el2 in list_legioner_sorted:
        started_number += 1
        el2 = [started_number, el2[0], el2[1]]
        list_legioner_final.append(el2)
    return list_legioner_final


f_1 = open("Список_из_чата.txt", 'r', encoding="utf-8")
f_2 = open("Список_финальный.txt", 'a', encoding="utf-8")
f_3 = open("Рейтинг_легионеров.txt", 'r', encoding="utf-8-sig")

legioner_dict = {}

for line in f_3:
    c = line.split()
    legioner_dict[' '.join(c[:2])] = float(c[2])
f_3.close()


legioner_dict_current = {}
main_list_current = []
reserve_list_current = []

i = 0
k = 0

for line in f_1:
    c = line.split()
    c = c[2:]
    c[2] = (' '.join([c[0], c[1]])).strip(':')
    c = c[2:]
    if c[0] in legioner_dict:
        legioner_dict_current[c[0]] = legioner_dict.get(c[0])
    else:
        if len(c) == 2:
            k += 1
            main_list_current.append([k, c[0]])
        else:
            i += 1
            reserve_list_current.append([i, c[0]])

cort_legioner = dict_to_cort_legioner(legioner_dict_current, i)
#print(main_list_current, reserve_list_current, cort_legioner)

f_2.write('В основу: \n')
for m in main_list_current:
    m[0] = str(m[0])
    m = ". ".join(m)
    m = " ".join([m, '\n'])
    f_2.write(m)
f_2.write('В резерв: \n')
for r in reserve_list_current:
    r[0] = str(r[0])
    r = ". ".join(r)
    r = " ".join([r, '\n'])
    f_2.write(r)
for l in cort_legioner:
    l[0] = str(l[0])
    l[1] = str(l[1])
    l = ". ".join(l)
    l = " ".join([l, '\n'])
    f_2.write(l)

f_1.close()
f_2.close()

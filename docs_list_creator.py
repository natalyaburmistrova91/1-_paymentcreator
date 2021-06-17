import os

list_of_docs_durty = os.listdir(path=".")
list_of_docs_pure = []

for i in list_of_docs_durty:
    word = i.split('.')[0]
    if word[-5:] == '4sign':
        word = word[:-5]
    if word[:8] != 'перечень' and word != 'docs_list_creator':
        list_of_docs_pure.append(word)
f_1 = open(f'list_of_docs.txt', 'w', encoding="utf-8")
for i in list_of_docs_pure:
    f_1.write(f'{i}\n')
f_1.close()

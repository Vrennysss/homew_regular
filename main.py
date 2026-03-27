import re
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
file_list = []
headers = contacts_list[0]
file_list.append(headers)

for contact in contacts_list[1:]:
    norm_name = ' '.join(contact[:3]).split()

    if len(norm_name) >= 3:
        lastname = norm_name[0]
        firstname = norm_name[1]
        surname = norm_name[2]
    elif len(norm_name) == 2:
        lastname = norm_name[0]
        firstname = norm_name[1]
        surname = ''
    else:
        lastname = norm_name[0]
        firstname = ''
        surname = ''

    new_contact_list = [lastname,firstname,surname,contact[3],contact[4],contact[5],contact[6]]

    phone = new_contact_list[5]
    if phone:
        pattern = r'(\+7|8)?\s*?\(?(\d{3})\)?\s*?[-]?(\d{3})\s*?[-]?(\d{2})\s*[-]?(\d{2})\s*\(?(доб.)?\s*(\d{4})?\)?'
        match = re.search(pattern, phone)
        if match:
            true_number = f'+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}'
            if match.group(7):
                new_contact_list[5] = f'{true_number} доб.{match.group(7)}'
            else:
                new_contact_list[5] = true_number

    file_list.append(new_contact_list)

contacts_dict = {}
for contact in file_list[1:]:
    if contact[1] and contact[2]:
        key = f'{contact[0]}_{contact[1]}_{contact[2]}'
    elif contact[1]:
        key = f'{contact[0]}_{contact[1]}'
    else:
        key = f'{contact[0]}'
    if key not in contacts_dict:
        contacts_dict[key] = contact
    else:
        take_str = contacts_dict[key]
        for i in range(len(take_str)):
            if not take_str[i] and contact[i]:
                take_str[i] = contact[i]

final = [headers]
for j in contacts_dict.values():
    final.append(j)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(final)
from pprint import pprint
import re
import csv


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def separation(separate_list):
    print(range(len(separate_list)))
    for a in range(len(separate_list)):
        if a == 0 or a == 4:
            continue
        elif a in [1, 2, 5, 6, 7]:
            mod = separate_list[a][0].split(' ')
            for cl in separate_list:
                if cl == separate_list[a]:
                    cl[0] = mod[0]
                    cl[1] = mod[1]
                    cl[2] = mod[2]
        elif a == 3:
            mod = separate_list[a][1].split(' ')
            for cl in separate_list:
                if cl == separate_list[a]:
                    cl[1] = mod[0]
                    cl[2] = mod[1]
        elif a == 8:
            mod = separate_list[a][0].split(' ')
            for cl in separate_list:
                if cl == separate_list[a]:
                    cl[0] = mod[0]
                    cl[1] = mod[1]
    return separate_list


def create_list_num(mod_separate_list):
    num_list = []
    for cl in mod_separate_list:
        for i in cl:
            result = re.search(r'(\+7|8)\s*\(*(\d+)\)*[\s-]*(\d+)[\s-]*(\d+)[\s-]*(\d+)', i)
            result_ext = re.search(r'\s*\(?доб\.?\s*(\d+)\)?', i)
            if result is not None and result_ext is not None:
                appended = f'{result.group()}{result_ext.group()}'
                num_list.append(appended)
            elif result is not None:
                num_list.append(result.group())
    return num_list


def num_processing(num_list, mod_separated_list):
    for id_1, cl in enumerate(mod_separated_list):
        for id_2, i in enumerate(cl):
            if i in num_list:
                result2 = re.sub(r'(\+7|8)\s*\(*(\d+)\)*[\s-]*(\d+)[\s-]*(\d+)[\s-]*(\d+)', r'+7(\2)\3-\4-\5', i)
                result2_ext = re.sub(
                    r'(\+7|8)\s*\(*(\d+)\)*[\s-]*(\d+)[\s-]*(\d+)[\s-]*(\d+)\s*\(?доб\.?\s*(\d+)\)?',
                    r'+7(\2)\3-\4-\5 доб.\6',
                    i)
                if 'доб' in i:
                    mod_separated_list[id_1][id_2] = result2_ext
                else:
                    mod_separated_list[id_1][id_2] = result2
    return mod_separated_list


def merge(mod_separated_list):
    lastname = {}
    count = 0
    for id_1, cl in enumerate(mod_separated_list):
        for id_2, i in enumerate(cl):
            if id_2 == 0:
                if i in lastname.keys():
                    if len(cl) >= len(lastname[i]):
                        for id_j, j in enumerate(mod_separated_list[id_1]):
                            if j == '':
                                index = id_j
                                if id_j <= len(lastname[i])-1:
                                    mod_separated_list[id_1][index] = lastname[i][index]
                                count = 0
                    else:
                        for id_k, k in enumerate(lastname[i]):
                            if k == '':
                                index = id_k
                                if id_k <= len(cl) - 1:
                                    lastname[i][index] = mod_separated_list[id_1][index]
                                count = 1
                if count == 0:
                    lastname[i] = cl
    return lastname


def create_result_list(lastname_dict):
    result_list = list()
    for key in lastname_dict:
        result_list.extend([lastname_dict[key]])
    pprint(result_list)
    return result_list


if __name__ == '__main__':
    s = separation(contacts_list)
    c = create_list_num(s)
    n = num_processing(c, s)
    m = merge(n)
    final_result = create_result_list(m)

    with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_result)

import csv

def get_remain_name_list():
    remain_name_list = []
    with open('remain_authors.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            for name in row:
                if name != '':
                    remain_name_list.append(name)

    return remain_name_list
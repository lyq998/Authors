import pickle
from read_remain_authors import get_remain_name_list
import copy
import csv


def takeSecond(elem):
    return elem[1]


def takeFirst(elem):
    return elem[0]


with open('author_list.pkl', 'rb') as file:
    authors = pickle.load(file)

author_list = []
for author_line in authors:
    for author in author_line:
        author_list.append(author)
remain_name_list = get_remain_name_list()
all_authors = author_list + remain_name_list
all_authors_set_list = list(set(all_authors))
for i in range(len(all_authors_set_list)):
    author_name = all_authors_set_list[i]
    all_authors_set_list[i] = [author_name, all_authors.count(author_name)]

for i in range(len(all_authors_set_list)):
    name = all_authors_set_list[i][0]
    name_split = name.split(' ')
    if len(name_split) == 2:
        for j in range(i, len(all_authors_set_list)):
            search_name = all_authors_set_list[j][0]
            search_name_split = search_name.split(' ')
            if len(search_name_split) == 2:
                if name_split[0] == search_name_split[1] and name_split[1] == search_name_split[0]:
                    all_authors_set_list[i][1] += all_authors_set_list[j][1]
                    all_authors_set_list[j] = ['', 0]
                    break

all_authors_set_list_name = copy.deepcopy(all_authors_set_list)
all_authors_set_list.sort(key=takeSecond, reverse=True)
all_authors_set_list_name.sort(key=takeFirst)

with open('author_statistics.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['name', 'paper_num'])
    for row in all_authors_set_list_name:
        csv_writer.writerow(row)

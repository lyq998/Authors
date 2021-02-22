import re
import numpy as np
from arxiv import arxiv_authors
from ieee import ieee_authors
from springer import springer_authors
from sciencedirect import sciencedirect_authors
from acm import acm_authors
import time
import pickle
import logging
import sys

with open('authors_li.txt', 'r', encoding='utf-8') as file:
    content_list = file.readlines()
    content_acc = [x.strip() for x in content_list if x.find('accepted') != -1]

https_list = [re.sub(r'^.*a href="', "", x) for x in content_acc]
https_list = [re.sub(r'".*', "", x) for x in https_list]
domain_name_list = [re.sub("^.*//", "", x) for x in https_list]
domain_name_list = [re.sub("/.*$", "", x) for x in domain_name_list]
set_domain_list = list(set(domain_name_list))
print('domain set:' + str(set_domain_list))
set_list_count = [domain_name_list.count(set_domain_list[i]) for i in range(len(set_domain_list))]
set_list_count_arg = np.array(set_list_count).argsort()
# reverse
set_list_count_arg = set_list_count_arg[::-1]

# print top 10 domains, and we can get request from 'arxiv.org', 'ieeexplore.ieee.org', 'link.springer.com',
# 'www.sciencedirect.com', 'dl.acm.org'
for i in range(10):
    print('top {} is {}, count number is {}.'.format(i, set_domain_list[set_list_count_arg[i]],
                                                     set_list_count[set_list_count_arg[i]]))

# start to get requests
assert len(domain_name_list) == len(https_list)
remain_url_list = []
author_list = []
log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format, datefmt="%m/%d %H:%M:%S")
for i in range(len(https_list)):
    url = https_list[i]
    logging.info('temp url is: {}'.format(url))
    domain_name = domain_name_list[i]
    if domain_name == 'arxiv.org':
        logging.info('Get request from arxiv.')
        authors = arxiv_authors(url)
    elif domain_name == 'ieeexplore.ieee.org':
        # please change the ieeexplore.ieee.org/stamp to ieeexplore.ieee.org/abstract first
        logging.info('Get request from ieee.')
        authors = ieee_authors(url)
    elif domain_name == 'link.springer.com':
        logging.info('Get request from springer.')
        authors = springer_authors(url)
    elif domain_name == 'www.sciencedirect.com':
        logging.info('Get request from sciencedirect.')
        authors = sciencedirect_authors(url)
    elif domain_name == 'dl.acm.org':
        logging.info('Get request from acm.')
        authors = acm_authors(url)
    else:
        # save the url and check the authors manually
        remain_url_list.append(url)
        authors = None

    if authors is not None:
        author_list.append(authors)
    time.sleep(5)

with open('author_list.pkl', 'wb') as file:
    pickle.dump(author_list, file)

with open('remain_url.txt', 'w') as file:
    for url in remain_url_list:
        file.write(str(url) + '\n')

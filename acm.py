import requests
import re

my_headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def acm_authors(url):
    try:
        response = requests.get(url, headers=my_headers, timeout=4)
        if response.status_code != 200:
            author_names = None
        else:
            response.encoding = 'utf-8'
            html_text = response.text
            text_list = html_text.split('\n')
            author_lines = [text_line for text_line in text_list if text_line.find('rlist--inline loa truncate-list') != -1]
            author_line = author_lines[0]
            author_line = re.sub('^.*</b></li>', '', author_line).strip()
            author_list = author_line.split('<li class="loa__item">')
            # start from 1, because 0 is ""
            author_names = [re.sub('^.*"author-name" title="', '', author_x) for author_x in author_list[1:]]
            author_names = [re.sub('"><span class="loa__author-info".*$', '', author_x) for author_x in author_names]
        return author_names
    except:
        acm_authors(url)
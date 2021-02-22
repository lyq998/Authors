import requests
import re

my_headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def arxiv_authors(url):
    try:
        response = requests.get(url, headers=my_headers, timeout=4)
        if response.status_code != 200:
            author_names = None
        else:
            response.encoding = 'utf-8'
            html_text = response.text
            text_list = html_text.split('\n')
            author_lines = [text_line for text_line in text_list if text_line.find('citation_author') != -1]
            author_names = [re.sub('^.*content="', "", author_line) for author_line in author_lines]
            author_names = [re.sub('"/.*', "", author_line) for author_line in author_names]
            author_names = [author_name.replace(',', '') for author_name in author_names]
        return author_names
    except:
        arxiv_authors(url)
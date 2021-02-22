import requests
import re
import json

my_headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def ieee_authors(url):
    try:
        response = requests.get(url, headers=my_headers, timeout=4)
        if response.status_code != 200:
            author_names = None
        else:
            response.encoding = 'utf-8'
            html_text = response.text
            text_list = html_text.split('\n')
            author_lines = [text_line for text_line in text_list if text_line.find('"authors"') != -1]
            # assert len(author_lines) == 1
            author_line = author_lines[0]

            # The below is not suitable for IEEE Access
            # author_line = re.sub(',"isbn".*$', '', author_line)
            # author_line = re.sub('^.*"authors":', '', author_line)

            author_line = re.sub('^.*document.metadata=', '', author_line)
            # delete the ;
            author_line = author_line[:-1]
            metadata = json.loads(author_line)
            author_list = metadata['authors']
            author_names = []
            for author in author_list:
                author_names.append(author['name'])
        return author_names
    except:
        ieee_authors(url)

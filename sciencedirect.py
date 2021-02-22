import requests
import re
import json

my_headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def sciencedirect_authors(url):
    try:
        response = requests.get(url, headers=my_headers, timeout=4)
        if response.status_code != 200:
            author_names = None
        else:
            response.encoding = 'utf-8'
            html_text = response.text
            text_list = html_text.split('\n')
            author_lines = [text_line for text_line in text_list if text_line.find('application/json') != -1]
            # assert len(author_lines) == 1
            author_line = author_lines[0]
            author_line = re.sub('^<script type="application/json".*">', '', author_line)
            author_line = re.sub('</script>$', '', author_line)
            json_dic = json.loads(author_line)
            author_infos = json_dic['authors']['content'][0]['$$']

            author_names = []
            for author_info in author_infos:
                if author_info['#name'] == 'author':
                    author_name_infos = author_info['$$']
                    for author_name_info in author_name_infos:
                        if author_name_info['#name'] == 'given-name':
                            first_name = author_name_info['_']
                        elif author_name_info['#name'] == 'surname':
                            last_name = author_name_info['_']

                    author_name = first_name + ' ' + last_name
                    author_names.append(author_name)
        return author_names
    except:
        sciencedirect_authors(url)

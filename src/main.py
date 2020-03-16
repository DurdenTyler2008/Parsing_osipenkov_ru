'''
задача - написать скрипт, собирающий новые
кейсы  и блог с сайта https://osipenkov.ru
'''
import json
import requests
# from lxml import etree
from lxml.html import fromstring
from urllib.parse import urljoin

base_url = 'https://osipenkov.ru'
rubrics = ('blog', 'projects')


def crawl_projects():
    url = urljoin(base_url, 'projects')

    osipenkov_ru_data = {}
    source_code = requests.get(url).text  # получил текст
    page = fromstring(source_code)  # текст пересторил в дерево

    items = page.cssselect('.tt-post-3 > .tt-post-3-info')

    for item in items:  # проверка, существует ли item (принадлежит ли урл проектам и блогу)

        title = item.cssselect('h2 a')[0]
        headline = title.text

        print(f'crawling {headline[:30]}')  # распечатываю 30 букв headline для проверки работы в терминале

        url = title.attrib['href']
        pubdate = item.cssselect('.tt-post-3-label span')[0].text
        body = item.cssselect('.simple-text p')[0].text

        osipenkov_ru_data[url] = {'headline': headline, 'pubdate': pubdate, 'body': body}

        source_code = requests.get(url).text  # получил текст из title.attrib['href'],я внутри статьи
        article_page = fromstring(source_code)  # текст из title.attrib['href'] пересторил в дерево

        headline = article_page.cssselect('.tt-blog-title')
        pubdate = article_page.cssselect('.tt-blog-label span')
        body = article_page.cssselect('.simple-text')

        # Проверка, если есть запись в файле - перезаписываю, если нет - записываю:
        # если len(fake_page) равен 0,возврaщается пустой список, если нет - пасс
        if headline:
            osipenkov_ru_data[url]['headline'] = headline[0].text

        if pubdate:
            osipenkov_ru_data[url]['pubdate'] = pubdate[0].text

        if body:
            osipenkov_ru_data[url]['body'] = body[0].text_content()

        # osipenkov_ru_data[url]={'headline': headline, 'pubdate': pubdate, 'body': body }

    with open('osipenkov_ru_data.json', 'w') as file:
        json.dump(osipenkov_ru_data, file, indent=3, ensure_ascii=False)


def main():
    crawl_projects()


if __name__ == '__main__':
    main()
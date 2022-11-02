import bs4
import requests
import time
from constrains import URL, KEYWORDS

if __name__ == '__main__':
    page_number = 1
    data = []
    while True:
        sub_url = URL + f'/ru/all/page{page_number}/'
        response = requests.get(sub_url)
        time.sleep(0.1)
        if response.status_code != 200:
            break
        text = response.text
        soup = bs4.BeautifulSoup(text, features='html.parser')
        articles = soup.find_all(class_="tm-article-snippet__title-link")
        for article in articles:
            article_url = article.attrs['href']
            article_response = requests.get(URL + article_url)
            time.sleep(0.1)
            if article_response.status_code != 200:
                print('Произошла ошибка')
                break
            article_text = article_response.text
            article_soup = bs4.BeautifulSoup(article_text, features='html.parser')
            for word in KEYWORDS:
                if word in article_text:
                    article_time = article_soup.find('time')
                    print(f"<{article_soup.find('time').attrs['title']}> - <{article.text}> - <{article_response.url}>")

        page_number += 40
    print('finished!')
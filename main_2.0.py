import bs4
import requests
import grequests
from constrains import URL, KEYWORDS

def define_last_page(URL):
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    pages = soup.find(class_='tm-pagination__pages').find_all('a')
    return pages[-1].text.strip()
    
def get_pages_responses(head_url, last_page_number):
    result = []
    for i in range(1, last_page_number):
        URL = head_url + f'/ru/all/page{i}/'
        result.append(URL)
    responses = (grequests.get(url) for url in result)
    return grequests.map(responses)

def get_soup_articles_list(page_responses_list):
    result = []
    for response in page_responses_list:
        soup = bs4.BeautifulSoup(response.text, features='html.parser')
        result.append(soup.find_all(class_="tm-article-snippet__title-link"))
    return result

def get_articles_href_list(soup_articles_list):
    result = []
    for article in soup_articles_list:
        result.append(article.attrs['href'])
    return result

def get_articles_responses(href_list):
    responses = (grequests.get(href) for href in href_list)
    return grequests.map(responses)
        
def get_articles_with_keywords(articles_response_list, keywords):
    for response in articles_response_list:
        soup = bs4.BeautifulSoup(response.text, features='html.parser')
        for word in keywords:
            if word in soup:
                print(f"<{soup.find('time').attrs['title']}> - <{soup.find('h1').find('span').text}> - <{response.url}>")
                break

def get_articles_from_habr():
    pages_responses = get_pages_responses(URL, define_last_page(URL + '/ru/all/'))
    soup_articles_list = get_soup_articles_list(pages_responses)
    articles_href_list = get_articles_href_list(soup_articles_list)
    articles_responses = get_articles_responses(articles_href_list)
    get_articles_with_keywords(articles_responses)
    
if __name__ == '__main__':
    get_articles_from_habr()
    
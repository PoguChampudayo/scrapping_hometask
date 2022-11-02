import bs4
import grequests
import requests
import time
from constrains import URL, KEYWORDS

def define_last_page(URL):
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    pages = soup.find(class_='tm-pagination__pages').find_all('a')
    return pages[-1].text.strip()
    
def get_pages_responses(head_url, last_page_number):
    result = []
    for i in range(1, int(last_page_number) + 1):
        URL = head_url + f'/ru/all/page{i}/'
        result.append(URL)
    responses = (grequests.get(url) for url in result)
    return grequests.map(responses, size=15)

def get_soup_articles_list(page_responses_list):
    result = []
    for response in page_responses_list:
        soup = bs4.BeautifulSoup(response.text, features='html.parser')
        result.append(soup.find_all(class_="tm-article-snippet__title-link"))
    return result

def get_articles_href_list(soup_articles_list):
    result = []
    for page in soup_articles_list:
        for article in page:
            result.append(article.attrs['href'])
    return result

def get_articles_responses(href_list):
    responses = (grequests.get(URL + href) for href in href_list)
    return grequests.map(responses, size=15)
        
def get_articles_with_keywords(articles_response_list, keywords):
    for response in articles_response_list:
        soup = bs4.BeautifulSoup(response.text, features='html.parser')
        for word in keywords:
            if word in response.text:
                print(f"<{soup.find('time').attrs['title']}> - <{soup.find('h1').find('span').text}> - <{response.url}>")
                break

def get_articles_from_habr():
    pages_responses = get_pages_responses(URL, define_last_page(URL + '/ru/all/'))
    soup_articles_list = get_soup_articles_list(pages_responses)
    articles_href_list = get_articles_href_list(soup_articles_list)
    articles_responses = get_articles_responses(articles_href_list)
    get_articles_with_keywords(articles_responses, KEYWORDS)
    
if __name__ == '__main__':

    start_time = time.time()
    get_articles_from_habr()
    print("--- %s seconds ---" % (time.time() - start_time))


    
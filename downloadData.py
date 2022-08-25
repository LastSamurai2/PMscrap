import requests
from bs4 import BeautifulSoup

class Connection:

    def parse_html(self,url):
        r = requests.get(url)
        html_to_parse = r.text
        soup = BeautifulSoup(html_to_parse, 'html.parser')
        return soup

    def get_pagination(self,soup):
        search_result = soup.find(class_='ooa-1oll9pn e19uumca7')
        paging = search_result.find("div", {"class": "ooa-0"}).find("ul", {"class": "pagination-list ooa-1vdlgt7"}).find_all("a")
        paging2 = paging
        start_page = paging[1].text
        last_page = paging[len(paging) - 1].text
        print(last_page)
        return start_page, last_page


    def get_all_car(self,last_page):
        pages = list(range(1,int(last_page)))
        for page in pages:
            url="https: // www.otomoto.pl / osobowe?page = "+str(page)
            soup = self.parse_html(url)
            
    # if r.status_code == 200:
    #     html_to_parse = r.text
    #     soup = BeautifulSoup(html_to_parse, 'html.parser')
    #     search_result = soup.find(class_='ooa-p2z5vl e19uumca5')
    #     all_articles = search_result.find(class_='ooa-1bv2sx9 e1b25f6f17')
    #     h2_article = all_articles.find("h2")
    #     for a in h2_article.find_all('a', href=True):
    #         print("Found the URL:", a['href'])
    #
    # else:
    #     print("error")
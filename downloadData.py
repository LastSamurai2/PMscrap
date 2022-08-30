import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures



class Connection:
    MAX_THREADS = 30

    def parse_html(self,url):
        r = requests.get(url)
        html_to_parse = r.text
        soup = BeautifulSoup(html_to_parse, 'html.parser')
        return soup

    def get_pagination(self,soup):
        search_result = soup.find(class_='ooa-1oll9pn e19uumca7')
        paging = search_result.find("div", {"class": "ooa-0"}).find("ul", {"class": "pagination-list ooa-1vdlgt7"}).find_all("a")
        start_page = paging[1].text
        last_page = int(paging[len(paging) - 1].text)

        return start_page, last_page


    def get_all_car(self,last_page):
        start = time.time()
        car_link_table = []
        pages = list(range(1,33))
        for page in pages:
            url="https://www.otomoto.pl/osobowe?page="+str(page)
            print(url)
            soup = self.parse_html(url)
            search_result = soup.find(class_='ooa-p2z5vl e19uumca5')
            if search_result is None:
                continue
            else:
                all_articles = search_result.findAll('article')
                #all_articles = search_result.findAll(class_='ooa-1bv2sx9 e1b25f6f17')
                #print(len(all_articles))
                for aa in all_articles:
                    result = aa.find("h2").find_all('a', href=True)
                    car_link = result[0]['href']
                    car_link_table.append(car_link)
        print(car_link_table)
        end = time.time()
        print("Czas popbrania wszystkich aut: ",end - start)
        return car_link_table

    def get_car_info(self, car_link):
        info_dict = {}
        # for url in car_link_table:
        # for url in range(len(car_link_table)):
        # for url in range(1):#to do
        # car_link = car_link_table[url]
        soup = self.parse_html(car_link)
        title = soup.find("title").text
        price_tag = soup.find("div", {"class": "offer-header__row"}).find("div", {"class": "offer-price"})
        price = price_tag["data-price"]
        if soup.find("div", {"class": "photo-item"}).find("img") is None:
            photo="brak"
        else:
            photo_tag = soup.find("div", {"class": "photo-item"}).find("img")
            photo = photo_tag["data-lazy"]
        info_dict = {"title": title, "price": price, "photo": photo}
        all_details = soup.find("div", {"class": "parametersArea"}).find("div", {"class": "offer-params"})
        params_label = all_details.findAll("span", {"class": "offer-params__label"})
        params_value = all_details.findAll("div", {"class": "offer-params__value"})
        for x in range(len(params_label)):
            label = params_label[x].text.strip()
            value = params_value[x].text.strip()
            label = label.replace(" ", "_")
            value = value.replace(" ", "_")
            info_dict[label] = value
        return info_dict

    def test(self,car_link_table):
        list_of_car = []
        for car in car_link_table:
            print(car)
            car_data = self.get_car_info(car)
            list_of_car.append(car_data)

    def prepare_data(self,car_link_table):
        start = time.time()
        list_of_car = []
        threads = min(self.MAX_THREADS, len(car_link_table))

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for feature in executor.map(self.get_car_info, car_link_table):
                list_of_car.append(feature)

        # for car in car_link_table:
        #     print(car)
        #     car_data = self.get_car_info(car)
        #     list_of_car.append(car_data)
        end = time.time()
        print("Czas popbrania informacji dla " + str(len(car_link_table)) + " aut: ", end - start)
        final_df = pd.DataFrame(list_of_car)
        final_df.to_csv("filename2.csv")


            # print("Found the URL:", result[0]['href'])
        # h2_article = all_articles.find("h2")
        # for a in h2_article.find_all('a', href=True):
        #     print("Found the URL:", a['href'])

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

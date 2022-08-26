from downloadData import Connection




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    con = Connection()
    soup = con.parse_html("https://www.otomoto.pl/osobowe")
    lastpage = con.get_pagination(soup)
    car_list_table = con.get_all_car(lastpage)
    con.get_car_info(car_list_table)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

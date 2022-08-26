from downloadData import Connection




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    con = Connection()
    soup = con.parse_html("https://www.otomoto.pl/osobowe")
    lastpage = con.get_pagination(soup)
    con.get_all_car(lastpage)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

from downloadData import Connection




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    con = Connection()
    soup = con.parse_html("https://www.otomoto.pl/osobowe")
    con.get_pagination(soup)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

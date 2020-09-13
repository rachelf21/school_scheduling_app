from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
from selenium import webdriver


class Scraper:
    browser = webdriver.Edge()
    session = ''
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
    LANGUAGE = "en-US,en;q=0.5"

    def get_soup(self, url):
        """Constructs and returns a soup using the HTML content of `url` passed"""
        # initialize a session
        self.session = requests.Session()
        # set the User-Agent as a regular browser
        self.session.headers['User-Agent'] = self.USER_AGENT
        # request for english content (optional)
        self.session.headers['Accept-Language'] = self.LANGUAGE
        self.session.headers['Content-Language'] = self.LANGUAGE
        # make the request
        html = self.session.get(url)
        # return the soup
        return bs(html.content, "html.parser")
    
    def get_all_tables(self, soup):
        """Extracts and returns all tables in a soup object"""
        return soup.find_all("table")
    
    def get_table_headers(self, table):
        """Given a table soup, returns all the headers"""
        headers = []
        for th in table.find("thead").find_all("th"):
            headers.append(th.text.strip())
        return headers
    
    def get_table_rows(self, table):
        """Given a table, returns all its rows"""
        rows = []
        for tr in table.find_all("tr")[1:]:
            cells = []
            # grab all td tags in this table row
            tds = tr.find_all("td")
            if len(tds) == 0:
                # if no td tags, search for th tags
                # can be found especially in wikipedia tables below the table
                ths = tr.find_all("th")
                for th in ths:
                    cells.append(th.text.strip())
            else:
                # use regular td tags
                for td in tds:
                    cells.append(td.text.strip())
            rows.append(cells)
        return rows
    
    def save_as_csv(self, table_name, headers, rows):
        data = pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv", index=False)  
        #print("DATA:\n", data)
        
    def main(self, url):
        # get the soup
        soup = self.get_soup(url)
        # extract all the tables from the web page
        tables = self.get_all_tables(soup)
        print(f"[+] Found a total of {len(tables)} tables.")
        # iterate over all tables
        for i, table in enumerate(tables, start=1):
            # get the table headers
            headers = self.get_table_headers(table)
            # get all the rows of the table
            rows = self.get_table_rows(table)
            # save table as csv file
            table_name = f"table-{i}"
            print(f"[+] Saving {table_name}")
            #print("ROWS:\n", rows)
            print("HEADERS:\n", headers)      
            self.save_as_csv(table_name, headers, rows)    

url = 'https://mdy-attendance.herokuapp.com/today/8-103/A_M/1'
s = Scraper()
s.main(url)
            
    # if __name__ == "__main__":
    #     import sys
    #     try:
    #         url = sys.argv[1]
    #         #url = 'https://mdy-attendance.herokuapp.com/today/8-103/A_M/1'
    #     except IndexError:
    #         print("Please specify a URL.\nUsage: python html_table_extractor.py [URL]")
    #         sys.exit(1)
    #     main(url)
        

#https://www.thepythoncode.com/article/convert-html-tables-into-csv-files-in-python
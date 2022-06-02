from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time, csv, os, sys, re, io, random
import pandas as pd
import utils
        
# '2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019',
yearList = ['2020']

class Financial_House:

    def __init__(self):
        driver = webdriver.Firefox()
        driver.get('http://clerk.house.gov/public_disc/financial-search.aspx')
        self.search_records(driver)

    def search_records(self, driver):
        year_records = []
        for year in yearList:
            time.sleep(5)
            self.set_search_criteria(driver, year)
            time.sleep(5)
            year_records.append(self.paginate(driver))

            print(year_records)
        
        utils.file_download(year_records)
        utils.new_file_explorer()

        driver.quit
        sys.exit()

    def set_search_criteria(self, driver, year=''):
        if year:
            time.sleep(2)
            year_select = Select(driver.find_element_by_id('FilingYear'))
            year_select.select_by_visible_text(year)

        search_button_id = driver.find_element_by_css_selector('button.btn.btn-library.col-xs-12.col-sm-3[type="submit"]')

        try:
            time.sleep(2)
            search_button_id.click()
        except:
            print('Element not found')

        return


    def parse_links(self, driver):
        ptr_links = []
        search_table = driver.find_elements_by_xpath('//tr[@role="row"]/td/a')
        
        for row in search_table:
            ptr_link = row.get_attribute('href')
            time.sleep(1)
            name = row.text
            time.sleep(1)
            ptr_links.append([ptr_link, name])

        return ptr_links

        
    def paginate(self, driver):
        ptr_links = []

        if len(driver.find_elements_by_xpath('//span[@class="ellipsis"]')) == 1:
            elements = len(driver.find_elements_by_xpath('//div[@class="dataTables_paginate paging_simple_numbers"]/span/a'))
            for i in range(0, elements-1):
                elements = driver.find_elements_by_xpath('//div[@class="dataTables_paginate paging_simple_numbers"]/span/a')
                elements[i].click()
                time.sleep(2)
                ptr_links.append([self.parse_links(driver)])
                #parse_links

        if len(driver.find_elements_by_xpath('//span[@class="ellipsis"]')) == 2:
            while True:
                element = driver.find_element_by_xpath('//div[@class="dataTables_paginate paging_simple_numbers"]/span/a[4]')
                element.click()
                time.sleep(2)
                ptr_links.append([self.parse_links(driver)])
                if len(driver.find_elements_by_xpath('//span[@class="ellipsis"]')) == 1:
                    break

        elements = len(driver.find_elements_by_xpath('//div[@class="dataTables_paginate paging_simple_numbers"]/span/a'))
        for i in range(2, elements):
            elements = driver.find_elements_by_xpath('//div[@class="dataTables_paginate paging_simple_numbers"]/span/a')
            elements[i].click()
            time.sleep(2)
            ptr_links.append([self.parse_links(driver)])
            #parse_links

        return ptr_links

        
if __name__ == "__main__":
    house = Financial_House()
    
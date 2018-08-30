# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv


class MacauParkingStatistics:

    def __init__(self):
        self.browser = webdriver.Firefox(executable_path="/Users/liupeng/Documents/PythonProjects/geckodriver")

    def __del__(self):
        self.browser.close()

    def get_page(self, url):
        self.browser.get(url)
        page_source = self.browser.page_source

        return page_source

    def parse_page(self, page_source):

        html = BeautifulSoup(page_source, "html5lib")

        trs = html.find_all("tr")

        parks_item = []

        for tr in trs:
            tds = tr.find_all("td")

            park_name = ""
            timestemp = ""
            car_num = ""
            motor_num = ""

            single_park = []

            # td 0 : parking name and timestemp
            # parking name and timestamp
            span = tds[0].find("span")
            if span:
                park_name = span.text.replace("\n\t", "").replace("\n", "").strip()
            div = tds[0].find("div")
            if div:
                timestemp = div.text
                timestemp = timestemp.replace(park_name, "").replace("\n              ", "") \
                    .replace("\n            ", "").strip()

            # td 1: car num
            car_num = tds[1].text.strip()

            # td 2: motor num
            motor_num = tds[2].text.strip()

            # td 3: alink

            single_park.append(park_name)
            single_park.append(car_num)
            single_park.append(motor_num)

            parks_item.append(single_park)

        return parks_item


if __name__ == '__main__':

    macauparking = MacauParkingStatistics()
    url = "http://m.dsat.gov.mo/carpark.aspx?data=dsat"

    parks_names = ["塔石廣場地下上落客區(重型客車)","栢港","交通事務局大樓","永寧街","下環街市","氹仔中央公園",
                   "氹仔客運碼頭停車場","日昇樓","何賢公園","宋玉生廣場","居雅大廈","快富樓","亞馬喇前地","快達樓",
                   "和諧廣場停車場","河邊新街","馬六甲街","青翠樓","南灣(栢湖)","青葱大廈","青泉樓","青怡大廈","松樹尾",
                   "科學館","栢佳","栢寧","栢景","栢樂","栢蕙","栢濤","栢麗","栢威",
                   "祐漢公園","望善樓","黑橋街","望賢樓","湖畔大廈","華士古達嘉馬花園","業興大廈","蓮花路","藝園","樂群樓","麗都"]

    with open("macauparkingstatistics.csv", "a", newline="", encoding='utf-8-sig') as f:
        writer = csv.writer(f)

        # write header of excel
        parks_names.append("Time")
        writer.writerow(parks_names)

        while True:

            current_time = time.strftime("%Y/%M/%D %H:%M:%S")
            print(current_time)

            # load new page
            page_source = macauparking.get_page(url)
            parks_item = macauparking.parse_page(page_source)

            # save data
            data = []
            for item in parks_item:
                data.append(item[1])

            # add timestemp
            data.append(current_time)

            writer.writerow(data)
            f.flush()
            time.sleep(60)


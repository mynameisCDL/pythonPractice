# 导包
import sys
import datetime
import time
import re
from colorama import Fore
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# element = driver.find_element(By.CSS_SELECTOR, '#kw')   # #kw id选择器
# element = driver.find_element(By.CSS_SELECTOR, '.s_ipt')   # .s_ipt class选择器
# element = driver.find_element(By.CSS_SELECTOR, 'form #kw')   # 后代元素选择器
# 截图预览
# browser.get_screenshot_as_file('截图.png')
class OpenBrowser(object):
    def __init__(self):
        self.options_ = Options()
        self.options_.headless = True
        self.chrome_obj = Chrome(options=self.options_)
        # self.chrome_obj = Chrome()

    def save_TXT(self, TXT, path):
        f = open(path, 'w', encoding="utf-8", errors="ignore")
        for i in TXT:
            f.write(i.text + '\n')
        f.close()

    def red_HUANENG_Browser(self, previous_date):
        """
按输入的时间，爬取华能网站资讯信息
        :param previous_date: 起始时间
        """
        index_url='http://www.huaneng.net/info/'
        self.chrome_obj.get(index_url)
        # 先获取列表中总数
        pageCount = self.chrome_obj.find_element(By.CSS_SELECTOR, 'ul.pagination li:nth-last-child(1) a')
        page_url = pageCount.get_attribute('href')
        print(page_url)
        newsList = self.chrome_obj.find_elements(By.CSS_SELECTOR, '.bigNews-body ul li')

        for i in newsList:
            year = i.find_element(By.CLASS_NAME, 'year').text
            month = i.find_element(By.CLASS_NAME, 'month').text
            creatDate = str(year) + '-' + str(month)
            datetime.datetime.strptime(creatDate, "%Y-%m-%d").date()
            if creatDate > previous_date:
                title = i.find_element(By.CLASS_NAME, 'title').text
                news_url = i.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                #news_url = str(re.findall(r"'([^']*)'", news_url)[0])
                print('时间：'+str(creatDate)+',标题：'+str(title)+',url：'+news_url)
                i.find_element(By.CSS_SELECTOR, 'a').click()
                time.sleep(2)





if __name__ == '__main__':
    print('日期格式必须为 xxxx-xx-xx , 注意数字的位数是 4位-2位-2位！！！')
    previous_date = input("请输入起始日期（格式为：年-月-日）：")
    try:
        datetime.datetime.strptime(previous_date, "%Y-%m-%d").date()
        if previous_date > datetime.date.today().strftime("%Y-%m-%d"):
            sys.exit(1)
    except:
        print("请输入正确的日期！" + datetime.date.today().strftime("%Y-%m-%d"))
        sys.exit(1)
        print(Fore.BLUE + '[{}] [FLAG] 程序开始执行，访问海口华能发展有限公司首页'.format(
            time.strftime("%H:%M:%S", time.localtime())))

    openBrowser = OpenBrowser()
    openBrowser.red_HUANENG_Browser(previous_date)

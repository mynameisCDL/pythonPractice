import sys
import datetime
import os
import time
import xlrd
import xlwt
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 创建读取Excel对象
class redExcel(object):
    # 使用xlrd方式打开xls
    def __init__(self):
        print('准备打开表格')
    
    def test_execute2(self, path):
        tables = []
        book = xlrd.open_workbook(path)
        sh = book.sheet_by_index(0)
        for rx in range(sh.nrows):
            array = {'Ip': ''}
            array['Ip'] = sh.cell_value(rx, 0)
            # print(sh.row(rx))
        tables.append(array)
        
        return tables
    
    def save_Excel(self, save_path, Excels):
        """
        讲数据存储到excel
        :param save_path: 保存的文件路径
        :param Excels: 保存的数据
        """
        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet('企事业单位', cell_overwrite_ok=True)
        col = ('序号', '域名', '单位', '域名归属', 'IPv4地址', 'IPv6地址', '资产内容（网站、服务器、台式机等）', '备注')
        for i in range(0, col.__len__()):
            sheet.write(0, i, col[i])
        
        for i in range(0, Excels.__len__()):
            data = Excels[i]
            sheet.write(i + 1, 0, i + 1)
            sheet.write(i + 1, 1, data['Host'])
            sheet.write(i + 1, 2, data['title'])
            sheet.write(i + 1, 3, '')
            sheet.write(i + 1, 4, data['Ipv4'])
            sheet.write(i + 1, 5, data['Ipv6'])
            sheet.write(i + 1, 6, '网站')
        book.save(save_path)


class OpenBrowser(object):
    def __init__(self, host):
        self.options_ = Options()
        self.options_.headless = True
        self.chrome_obj = Chrome(options=self.options_)
        # self.chrome_obj = Chrome()
        self.chrome_obj.get(host)
        print('开始爬取数据')
    
    def getHostInfo(self, hostlist):
        tables = []
        # 开始爬取数据
        
        for rx in hostlist:
            hostInput = WebDriverWait(self.chrome_obj, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.theme-default-content .form-input')))
            sentBtn = WebDriverWait(self.chrome_obj, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.theme-default-content .button')))
            hostInput.clear()
            hostInput.send_keys(rx['Ip'])
            sentBtn.click()
            time.sleep(3)
            # 获取页面上的数据，如果获取不到那就抛出异常，并睡眠3秒重新获取
            ipv4Stact = WebDriverWait(self.chrome_obj, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tfhover"]/tbody/tr[2]/td[2]/span'))).text
            ipv6Stact = WebDriverWait(self.chrome_obj, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tfhover"]/tbody/tr[2]/td[3]/span'))).text
            HttpsIpv4State = WebDriverWait(self.chrome_obj, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tfhover"]/tbody/tr[3]/td[2]/span'))).text
            HttpsIpv6State = WebDriverWait(self.chrome_obj, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tfhover"]/tbody/tr[3]/td[3]/span'))).text
            
            if ipv4Stact == '400' or ipv6Stact == '400' or ipv4Stact == '200 请求成功' or ipv6Stact == '200 请求成功':
                array = {'Host': '', 'Ipv4': '', 'Ipv6': '', 'title': ''}
                array['Host'] = rx['Ip']
                try:
                    array['Ipv4'] = WebDriverWait(self.chrome_obj, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                                                            '//*[@id="tfhover"]/tbody/tr[1]/td[2]/span/a'))).text
                    array['Ipv6'] = WebDriverWait(self.chrome_obj, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                                                            '//*[@id="tfhover"]/tbody/tr[1]/td[3]/span/a'))).text
                except:
                    print(rx[
                              'Ip'] + ':其中有一个地址没有获取到,' + 'ipv4访问返回码:' + ipv4Stact + ',ipv6访问返回码:' + ipv6Stact)
                array['title'] = self.getHostTitle(rx['Ip'])
                # array['title'] = self.getHostTitle('海南大学')
                self.chrome_obj.back()
                tables.append(array)
                time.sleep(1.5)
            else:
                print('host:' + rx['Ip'] + ',ipv4访问返回码:' + ipv4Stact + ',ipv6访问返回码:' + ipv6Stact)
        self.chrome_obj.quit()
        return tables
    
    
    def getHostTitle(self, host):
        """
        根据传入的host字符串获取网站的标题
        :param host:url或者IP地址
        :return:返回网站标题
        """
        try:
            self.chrome_obj.get('http://' + host)
        except:
            print(host + ':异常')
        js = 'return document.title'
        time.sleep(1.5)
        title = self.chrome_obj.execute_script(js)
        time.sleep(1.5)
        # title=host
        print(title)
        return title


if __name__ == '__main__':
    case = redExcel()
    # 输入文件路径，文件最好放在根目录下
    print('请输入文件路径，文件最好放在根目录下，这样好识别')
    previous_fileName = input("请输入根目录下的文件：")
    # previous_fileName = '12.xls'
    # 读取所有Host
    hostlist = case.test_execute2(previous_fileName)
    # 设置host地址，打开浏览器爬取该host的数据
    host = 'https://ipw.cn/ipv6webcheck/'
    openBrowser = OpenBrowser(host)
    # 爬取
    hostData = openBrowser.getHostInfo(hostlist)
    
    save_path = "hostData.xls"
    case.save_Excel(save_path, hostData)

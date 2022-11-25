# coding: utf-8
# version: 1.0
# date: 2022-06-06
# last_update: 2022-07-31

import datetime
import random
import sys
from colorama import init, Fore
import time
from Basic_Web_Request import html_request, ioc_request
from message_parser import get_article_number, title_time_judgment, basic_info_get
from file_write import file_creat, basic_info_write, ioc_info_write
from ioc_process import ioc_get
from file_save import pdf_file_save


init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复

cookie = "Hm_lvt_5ceaa896b2dc6006d57f45a9d179ae6f=1663227157,1665191189,1665542742,1665550592; fsHash=B852556C3BF999AA6F568ABF11E37288; fsHashUid=2b45b866-3d12-43b7-ac9c-314c7c1930f4; JSESSIONID=33F49B68808A8720019AABCE09E6C5F7; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie1xuICAgIFwic3lzdGVtSWRcIjogMixcbiAgICBcImlkXCI6IDI2OTIsXG4gICAgXCJrZXlcIjogXCJ4TUVWRTlkRGtCOTB2SUw4NTZ0M0ZmZCtheXlqNitJUVlmdC9SU3d5RkVteE1COXlLSzc3S3pjPVwiXG59IiwiaWF0IjoxNjY1NTU0ODM4fQ.HZLmD4bMoI-gyC6SfDxGiPb9PxkoBlFrqT70tnlQ8X0; Hm_lpvt_5ceaa896b2dc6006d57f45a9d179ae6f=1665555494"


if __name__ == '__main__':
    # 日期没有做严格的校验，所以输入的时候要仔细一点
    print('日期格式必须为 xxxx-xx-xx , 注意数字的位数是 4位-2位-2位！！！')
    previous_date = input("请输入起始日期（格式为：年-月-日）：")
    try:
        datetime.datetime.strptime(previous_date, "%Y-%m-%d").date()
        if previous_date > datetime.date.today().strftime("%Y-%m-%d"):
            sys.exit(1)
    except:
        print("请输入正确的日期！")
        sys.exit(1)
    print(Fore.BLUE + '[{}] [FLAG] 程序开始执行，访问安恒威胁情报中心首页'.format(time.strftime("%H:%M:%S", time.localtime())))
    index_url = "https://ti.dbappsecurity.com.cn/info"
    index_html = html_request(index_url, cookie)
    # 获取最近一篇文章的链接编号
    article_number = get_article_number(index_html)
    # 如果有文章检索出错了，可以手动更改起始文章编号，绕过已经正常跑完结果的编号
    # article_number = '3695'

    while True:
        # 进入循环，开始获取文章信息，退出循环条件为日期
        url = "https://ti.dbappsecurity.com.cn/info/" + article_number
        article_html = html_request(url, cookie)

        if title_time_judgment(article_html, previous_date) is True:
            # 获取基本信息
            basic_info = basic_info_get(article_html, url)
            # 提取标题，创建结果文件
            title = basic_info['title']
            res_file = file_creat(title)
            # 基本信息写入结果文件
            basic_info_write(basic_info, res_file)
            # 根据标志位判断有无ioc信息，来决定是否提取并写入文件
            if basic_info['ioc'] == 1:
                # 包含IOC信息,提取，写入文件
                iocs = ioc_get(url, cookie)
                ioc_info_write(iocs, res_file)
            else:
                # 不包含ioc信息
                print(Fore.GREEN + '[{}] [INFO] 不包含IOC信息！'.format(time.strftime("%H:%M:%S", time.localtime())))

            pdf_file_save(url)

        article_number = str(int(article_number) - 1)
        time.sleep(random.randint(1, 3))

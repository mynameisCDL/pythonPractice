from bs4 import BeautifulSoup
from colorama import Fore
import time
import datetime
import sys


def basic_info_get(html, page_url):
    # 用于解析基本信息
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    data['url'] = page_url
    data['title'] = soup.title.string.rsplit('-', 1)[0].strip()
    create_time = soup.find(class_="user-text create-time").stripped_strings
    data['create_time'] = list(create_time)[0].split(" ")[0]
    data['text'] = soup.find("div", class_="info-content").find("p").string
    # 判断该文章有无ioc信息，加一个标志位
    div = soup.find("div", class_="ioc-content")
    if div is not None:
        data['ioc'] = 1
    else:
        data['ioc'] = 0

    print(Fore.GREEN + '[{}] [INFO] 基础信息 查询完成！'.format(time.strftime("%H:%M:%S", time.localtime())))

    return data


def get_article_number(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 查询出最近一篇文章的链接编号
    number = soup.find("div", class_="info-item").find("a", class_="info-title").get("href").split('/')[-1]
    print(Fore.GREEN + '[{}] [INFO] 最新的文章编号为 {}'.format(time.strftime("%H:%M:%S", time.localtime()), number))

    return number


def title_time_judgment(html, previous_date):
    article_creat_time = ""

    if html is not None:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.head.title.string.rsplit('-', 1)[0].strip()
        time_text = soup.find("span", class_="user-text create-time").strings
        for i in time_text:
            article_creat_time = i.split(' ')[0]
            break
        datetime.datetime.strptime(article_creat_time, "%Y-%m-%d").date()

        if article_creat_time < previous_date:
            print(Fore.GREEN + "[{}] [INFO] 该文章发布于截止日期之前，检索结束！程序退出！".format(time.strftime("%H:%M:%S", time.localtime())))
            print(
                Fore.BLUE + "[{}] [INFO] 请检查pdf_file文件夹下pdf文件是否全部下载完成。如有遗漏，请手动下载！".format(time.strftime("%H:%M:%S", time.localtime())))
            print(
                Fore.BLUE + "[{}] [INFO] 请手动下载所有文章的HTML格式文件，到pdf_file文件夹下！".format(time.strftime("%H:%M:%S", time.localtime())))
            print(
                Fore.BLUE + "[{}] [INFO] 执行 python pdf_move.py ,用途是将pdf_file下的附件全部移动到对应文章的文件夹！".format(time.strftime("%H:%M:%S", time.localtime())))
            sys.exit(0)

        if "周报" in title:
            print(Fore.GREEN + "[{}] [INFO] 该文章内容为统计周报，跳过录入！".format(time.strftime("%H:%M:%S", time.localtime())))
            return False
        else:
            return True

from colorama import Fore
import requests
import re
import json
import time


def html_request(url, cookie):
    # 基础的网页请求，用于网站首页访问和文章基本内容访问
    # 返回html内容
    # 自定义请求头
    headers = {
        "Referer": "https://ti.dbappsecurity.com.cn/info",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.93 Safari/537.36",
        "Cookie": cookie,
        "Host": "ti.dbappsecurity.com.cn",
    }

    r = requests.get(url, headers=headers, allow_redirects=False)
    # 根据响应码判断访问情况，成功响应则返回页面内容，传递给下一步做解析
    if r.status_code == 200:
        print(Fore.BLUE + '[{}] [FLAG] 页面 {} 访问成功！'.format(time.strftime("%H:%M:%S", time.localtime()), url))
        r.encoding = 'utf-8'
        return r.content
    else:
        print(Fore.RED + '[{}] [ERROR] 页面 {} 访问失败！无此页面！！'.format(time.strftime("%H:%M:%S", time.localtime()), url))
        # sys.exit(1)
        return None


def ioc_request(url, cookie, i, page):
    # 访问ioc信息，post方式，请求头必须包含个人认证信息
    # authorization字段的值从cookie中提取
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "Cookie": cookie,
        "Host": "ti.dbappsecurity.com.cn",
        "Origin": "https://ti.dbappsecurity.com.cn",
        "Referer": url,
        "Authorization": get_authorization_from_cookie2(cookie),
        "Accept": "application/json",
        "Accept - Encoding": "gzip, deflate, br",
        "Accept - Language": "zh - CN, zh;q = 0.9",
        "Content - Type": "application/json",
        "sec - ch - ua": "\"Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
        "sec - ch - ua - mobile": "?0",
        "sec - ch - ua - platform": "Windows",
        "Sec - Fetch - Dest": "empty",
        "Sec - Fetch - Mode": "cors",
        "Sec - Fetch - Site": "same - origin"
    }
    ioc_url = "https://ti.dbappsecurity.com.cn/web/info/ioc/infoIocs"
    # 准备post数据内容
    infoid = url.rsplit("/", 1)
    data = {"infoId": infoid[1], "iocType": i, "page": page, "size": 10}
    # 发送查询请求
    r = requests.post(ioc_url, headers=headers, json=data)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        return json.loads(r.text)


def get_authorization_from_cookie(cookie):
    authorization = ""
    # 在请求ioc页面时，请求头有一个特殊参数authorization，它的值是cookie中的token部分，此函数作用是从cookie中提取出authorization值
    # 此处对于authorization的分解有问题，要考虑token位于最后，没有 ；号的情况
    pattern = re.compile(r'token=.*;')
    try:
        m = pattern.search(cookie)
        authorization = m.group().split("=")[1].split(";")[0]
    except:
        print(Fore.RED + '[{}] [ERROR] 从cookie中提取authorization值出错，请检查cookie！'.format(
            time.strftime("%H:%M:%S", time.localtime())))
    # print(authorization)
    return authorization


def get_authorization_from_cookie2(cookie):
    authorization = ""
    # 另一种提取authorization的方法，按照 ； 把cookie分割，之后取出包含token的部分。此种方法比较臃肿，但是解决了上一种方法的弊端
    try:
        cookie_list = cookie.split(';')
        for cookie_value in cookie_list:
            if 'token' in cookie_value:
                authorization = cookie_value.split('=')[1]
    except:
        print(Fore.RED + '[{}] [ERROR] 从cookie中提取authorization值出错，请检查cookie！'.format(
            time.strftime("%H:%M:%S", time.localtime())))
    # print(authorization)
    return authorization

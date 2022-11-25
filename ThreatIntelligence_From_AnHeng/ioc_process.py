from Basic_Web_Request import ioc_request
import time
from colorama import Fore


def ioc_get(url, cookie):
    # 如果包含IOC内容，总共需要请求三个类型的数据，以第一类为例，判断第一页是否为空，不为空则表示有这类型数据，此时判断页数，然后逐页请求数据，要注意标签内容可能为空。
    # 最外层循环表示逐类请求domain,ip,hash信息
    ioc_list = []

    for type_num in range(1, 4):
        type_dic = {"1": "domain", "2": "ip", "3": "hash"}
        keyword = type_dic.get(str(type_num))
        # 请求此类型下第一页数据，如果包含内容，则计算页数，逐页请求此类型信息，将此类型下每页ioc信息存放到ioc_list中
        # 请求此IOC类型第一页数据
        page_one = ioc_request(url, cookie, type_num, 1)
        if have_ioc_type(page_one) is True:
            # 计算页数
            total = page_one.get("data").get("total")
            if total % 10 != 0:
                end_page = int(total) // 10 + 1
            else:
                end_page = int(total) // 10

            if end_page > 50:
                end_page = 50
                print(Fore.GREEN + '[{}] [INFO] IOC-{} 信息过多，仅读取500条！'.format(time.strftime("%H:%M:%S", time.localtime()),keyword))
            # 循环获取所有IOC信息
            for page in range(1, int(end_page) + 1):
                ioc_content = ioc_request(url, cookie, type_num, page)
                ioc_parser(ioc_content, keyword, ioc_list)
        else:
            # print("IOC中不包含{}信息！".format(keyword))
            pass

    print(Fore.GREEN + '[{}] [INFO] IOC信息 查询完成！'.format(time.strftime("%H:%M:%S", time.localtime())))

    return ioc_list


def have_ioc_type(dic_data):
    # 此函数作用是判断是否有某一类型的IOC
    if dic_data.get("data").get("title") is not None:
        return True
    else:
        return False


def ioc_parser(ioc_content, keyword, ioc_list):
    # IOC请求结果中的冗余数据较多，此函数提取用途是提取我们需要的数据
    ioc_data = ioc_content.get("data").get("data")
    for mes in ioc_data:
        info = mes.get(keyword)
        try:
            tag_name = mes.get("tags")[0].get("name")
        except:
            tag_name = ""

        ioc_list.append({"keyword": keyword, "info": info, "tag": tag_name})

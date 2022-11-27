# 导包
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':

    # 1.创建对象. 大写的C
    chrome_obj = Chrome()  # 运行会自动打开谷歌浏览器,上面会有提示,Chrome正受到自动化测试工具的控制
    # 手动指定浏览器驱动
    # chrome_obj = Chrome(executable_path='驱动文件的绝对路径/chromedriver.exe')  # 运行会自动打开谷歌浏览器,上面会有提示,Chrome正受到自动化测试工具的控制

    # 进行请求的发送,向网页地址栏填入url参数
    chrome_obj.get('https://www.baidu.com')  # 往浏览器的网页地址栏填入url参数
    

    # 重要:获取当前页面的数据  >>> 是网页源代码 elements      使用selenium做的（json html）
    # data_ = chrome_obj.page_source
    #
    # print(data_)
    # with open('baidu01.html','w',encoding='utf-8') as f:
    #     f.write(data_)
    # 1 浏览器最大化
    chrome_obj.maximize_window()

    # 2.网页的截图  使用selenium建议图片保存格式.png
    chrome_obj.save_screenshot('baidu02.png')  # 图片的名称

    time.sleep(1.5)
    # 3打开一下新的页面:在原来的窗口重新输入一个url
    chrome_obj.get('https://www.bilibili.com/')
    #
    time.sleep(1.5)
    # 4 回退操作
    chrome_obj.back()
    #
    time.sleep(1.5)
    # 5 前进操作
    chrome_obj.forward()

    # 6 打开一个新的窗口: selenium执行js代码
    time.sleep(1.5)
    chrome_obj.execute_script('window.open("https://www.baidu.com")')

    # 7 切换窗口
    # 1.获取窗口: 获取到一个列表,当前浏览器对象打开了几个窗口,, 列表里面就有多少个元素
    res_ = chrome_obj.window_handles
    # print(res_)
    # 进行窗口的切换
    time.sleep(1.5)
    chrome_obj.switch_to_window(res_[0])  # 切换到第一个窗口
    time.sleep(1.5)
    chrome_obj.switch_to_window(res_[1])  # 切换到第二个窗口

    # 3.selenium关闭浏览器
    # (1)关闭当前的页面窗口
    time.sleep(1.5)
    chrome_obj.close()
    #
    # # (2)关闭整个浏览器对象
    time.sleep(1.5)
    chrome_obj.quit()


# 导包

from selenium.webdriver import Chrome

from selenium.webdriver import ChromeOptions

if __name__ == '__main__':
    # 不打开浏览器模式
    """ options_ = Options()
     options_.headless = True
     chrome_obj = Chrome(options=options_) """
    # 实现规避检测
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_obj = Chrome(options=option)

    # 打开浏览器模式
# chrome_obj = Chrome()
chrome_obj.get('https://ti.dbappsecurity.com.cn/info')
# 返回
chrome_obj.back()
# 前进
chrome_obj.forward()
# 关闭浏览器
chrome_obj.quit()

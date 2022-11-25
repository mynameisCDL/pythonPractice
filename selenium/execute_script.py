from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


class casetest(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://wwww.baidu.com')

    def test_execute1(self):
        self.driver.execute_script("alert('test')")  # 同步执行
        sleep(2)
        self.driver.switch_to.alert.accept()

    def test_execute2(self):
        js = 'return document.title'
        title = self.driver.execute_script(js)  # 取到百度的title
        print(title)

    def test_execute3(self):
        js = 'var q=document.getElementById("kw");q.style.border="2px solid red"'
        self.driver.execute_script(js)  # 把百度搜索边框变为红色
        sleep(2)

    def test_execute4(self):
        # 滚动条滚动
        self.driver.find_element(By.ID, 'kw').send_keys('留白')
        self.driver.find_element(By.ID, 'su').click()
        sleep(2)
        # 滚动到底部
        js = 'window.scrollTo(0,document.body.scrollHeight)'
        self.driver.execute_script(js)
        sleep(2)


if __name__ == '__main__':
    case = casetest()
    # case.test_execute1()
    # case.test_execute2()
    case.test_execute3()
    # case.test_execute4()

# case.driver.quit()

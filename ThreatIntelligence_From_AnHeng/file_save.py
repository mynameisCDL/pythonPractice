import time
from colorama import Fore
from selenium import webdriver
import json


def pdf_file_save(url):
    chrome_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False,

        # "customMargins": {},
        # "marginsType": 2,
        # "scaling": 100,
        # "scalingType": 3,
        # "scalingTypePdf": 3,
        "isLandscapeEnabled": True,  # landscape横向，portrait 纵向，若不设置该参数，默认纵向
        "isCssBackgroundEnabled": True,
        "mediaSize": {
            "height_microns": 297000,
            "name": "ISO_A4",
            "width_microns": 210000,
            "custom_display_name": "A4 210 x 297 mm"
        },
    }

    chrome_options.add_argument('--enable-print-browser')
    # headless模式下，浏览器窗口不可见，可提高效率。有bug，该模式下文件下载不下来
    # chrome_options.add_argument('--headless')


    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': 'C:\ThreatIntelligence_From_AnHeng\pdf_file'  # 此处填写你希望文件保存的路径
    }
    chrome_options.add_argument('--kiosk-printing')  # 静默打印，无需用户点击打印页面的确定按钮
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    # 利用js修改网页的title，该title最终就是PDF文件名，利用js的window.print可以快速调出浏览器打印窗口，避免使用热键ctrl+P
    driver.execute_script('document.title=document.title; window.print();')
    print(Fore.GREEN + "[{}] [INFO] PDF文件保存完成！".format(time.strftime("%H:%M:%S", time.localtime())))

    driver.close()

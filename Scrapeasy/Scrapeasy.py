from scrapeasy import Website, Page


class creatScraeasy(object):
    def __init__(self):
        self.web = Website("https://www.w3school.com.cn/tiy/t.asp?f=eg_html_video")

    def getLinks(self):
        """
获取所有子站点的链接
        :return:返回所有链接
        """
        links = self.web.getSubpagesLinks()
        for i in links:
            print("http://www."+i)
        return links

    def getImages(self):
        """
获取所有站点的图片链接
        :return: 返回所有可用图像的链接
        """
        images = self.web.getImages()
        for i in images:
            print("http://www."+i)
        return images

    def getLinks(self):
        """
获取站点的链接域
        :return: 返回链接域地址
        """
        links= self.web.getLinks(intern=True, extern=True, domain=False)
        for i in links:
            print("http://www."+i)
        return links

    def getVideo(self):
        """
获取网站上的带有video标签的视频地址
        :return:
        """
        links = self.web.getVideo(reinit=True)
        for i in links:
            print("http://www." + i)
        return links



if __name__ == '__main__':
    new_scraeasy = creatScraeasy()
    new_scraeasy.getVideo()

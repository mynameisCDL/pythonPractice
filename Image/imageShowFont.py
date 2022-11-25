
import os
from PIL import Image
import pytesseract

# pyinstaller -F -w imageShowFont.py 打包python程序

def image_to_words(image_path):
    """
对路径的图片进行字体扫描，输出字体
    :param image_path: 图片的路径
    :return:返回识别的数据
    """
    image = Image.open(image_path)
    words = pytesseract.image_to_string(image, 'chi_sim')
    # print(words)
    return words


def save_words(save_path, words):
    """
将数据保存到word中
    :param save_path: 保存的文件路径
    :param words: 保存的数据
    """
    f = open(save_path, 'a+', encoding="utf-8", errors="ignore")
    # f.write(str(words).encode('utf-8', 'ignore'))
    f.write(words)
    f.close()

def save_txt(save_path, words):
    """
将数据存储到txt中
    :param save_path: 保存的文件路径
    :param words: 保存的数据
    """
    with open(save_path, 'a+', encoding="utf-8", errors="ignore") as f:
        f.write(words)

def save_Excel(save_path, Excels):
    """
讲数据存储到excel
    :param save_path: 保存的文件路径
    :param Excels: 保存的数据
    """
    with open(save_path, 'a+', encoding="utf-8", errors="ignore") as f:
        f.write(Excels)

def getPhoto():
    """
读取目录下所有图片
    :return:返回所有目录下的文件名
    """
    photo_Path = "E:\开发项目\python\Image\images"
    file_list = os.listdir(photo_Path)
    return file_list

# 程序入口
if __name__ == '__main__':
    path_images = getPhoto()
    save_path = r"1.txt"
    for i in path_images:
        words = image_to_words("images/"+i)
        save_txt(save_path, words)


    # save_path = r"1.txt"
    # image_path = r"images/m2.png"
    # words = image_to_words(image_path)
    # save_txt(save_path, words)


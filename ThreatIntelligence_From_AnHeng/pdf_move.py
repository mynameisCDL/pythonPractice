import shutil
import os


def get_articlename():
    article_list = []
    files = os.listdir()
    for file in files:
        if 'result' in file:
            article_list = os.listdir(file)

    return article_list


def get_resultfilename():
    files = os.listdir()
    for file in files:
        if 'result' in file:
            return file


if __name__ == "__main__":
    src_path = 'pdf_file/'
    dst_path = get_resultfilename()
    files = os.listdir('pdf_file')
    for articlename in get_articlename():
        for file in files:
            if articlename in file:
                shutil.move(src_path + file, dst_path + '/' + articlename + '/附件')
                print(f'{file}移动完成')

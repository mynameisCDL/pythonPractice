# coding: utf-8
import os

file_path = ["D:\\bjcert\\APT情报报送\\北京分中心-20220708", "D:\\bjcert\\APT情报报送\\北京分中心-20220714", "D:\\bjcert\\APT情报报送\\北京分中心-20220721", "D:\\bjcert\\APT情报报送\\北京分中心-20220728", "D:\\bjcert\\APT情报报送\\北京分中心-20220731"]

wfile = open("aptevent_name.txt", "w")
num = 1
for path in file_path:
    file_list = os.listdir(path)
    for file in file_list:
        info = str(num) + '、' + file +'\n'
        wfile.write(info)
        num = num + 1

wfile.close()
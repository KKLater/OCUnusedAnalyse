#!/usr/bin/python
# -*- coding: utf-8 -*-

import oc_analyse
import image_analyse

import sys
import file
import time

reload(sys)

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


def get_un_use_files(a_project_path):
    un_use_files = []

    print("开始查找未使用代码资源：")
    un_use_code_files = oc_analyse.get_un_use_code_files(a_project_path, _zh_uncheck_enable)
    print("查找未使用代码资源结束！")
    if len(un_use_code_files) > 0:
        print("未使用代码资源：")
    for c_file in un_use_code_files:
        print(c_file.name)
        un_use_files.append(c_file)

    if _image_unuse_search:
        print("开始查找未使用图片资源：")
        un_use_image_files = image_analyse.get_un_use_images(a_project_path, _zh_uncheck_enable)
        print("查找未使用图片资源结束！")
        if len(un_use_image_files) > 0:
            print("未使用图片资源：")
        for c_file in un_use_image_files:
            print(c_file.name)

        un_use_files.extend(un_use_image_files)

    if len(un_use_files) > 0:
        file.files_save(un_use_files, project_path, "UnUseFiles")



_zh_uncheck_enable = True
_image_unuse_search = True
_check_as_line = False

project_path = raw_input("Project Path:").strip()
image_unuse_search = raw_input("Image Search Enable?(Y/N)").strip()
zh_uncheck_enable = raw_input("ZH Check Enable?(Y/N)").strip()
check_as_line = raw_input("Check as Line?(Y/N)").strip()

_zh_uncheck_enable = zh_uncheck_enable == 'Y' or zh_uncheck_enable == 'y'
_image_unuse_search = image_unuse_search == 'Y' or image_unuse_search == 'y'
_check_as_line = check_as_line == 'Y' or check_as_line == 'y'

time_start = time.time()
get_un_use_files(project_path)
time_end = time.time()
print('Totally cost:%f' % (time_end - time_start))

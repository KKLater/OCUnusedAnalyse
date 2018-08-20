#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import progress

from file import File
from dir import Dir

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')


# =======================
# 获取没有使用到的图片文件
# =======================
def get_un_use_images(a_project_path, a_zh_un_check_enable, image_analyse_check_as_line=False):
    c__dir = Dir(a_project_path)
    c_files = c__dir.files()
    img_files = []
    check_files = []
    for c_file in c_files:
        match = False
        if a_zh_un_check_enable:
            match = zhPattern.search(unicode(c_file.name))
        not_system_file = ('xcodeproj' not in c_file.name) and ('xcworkspace' not in c_file.name)
        not_node_module = 'node_modules' not in c_file.path
        if 'Pod' not in c_file.path and (not match) and not_system_file and not_node_module:
            is_png = 'png' == c_file.get_extension()
            is_jpg = 'jpg' == c_file.get_extension()
            if is_png or is_jpg:
                is_app_icon = 'AppIcon' in c_file.path
                is_launch = 'LaunchImage' in c_file.path
                if not (is_app_icon or is_launch):
                    img_files.append(c_file)
            else:
                check_files.append(c_file)

    i = 0
    progress_index = 0
    count = len(img_files)
    print("Total Image Files Count: %d" % len(check_files))
    while i < len(img_files):
        progress_index += 1
        progress.show_progress(progress_index, count)

        # 逐文件排查
        img_file = img_files[i]
        contain = False
        if not isinstance(img_file, File):
            contain = True
        else:
            image_name = img_file.name.partition('.')[0]
            if "@2x" in image_name or "@3x" in image_name:
                image_name = image_name.partition('@')[0]

            for check_file in check_files:
                if 'js' == check_file.get_extension():
                    simple_contain_str = img_file.name
                    if "@2x" in simple_contain_str:
                        simple_contain_str = simple_contain_str.replace("@2x", "")
                    if "@3x" in simple_contain_str:
                        simple_contain_str = simple_contain_str.replace("@3x", "")
                    contain = check_file.has_contain(simple_contain_str, image_analyse_check_as_line)
                    if contain:
                        break

                # Json 内部查找，并且过滤到 .xcassets 内的 Content.json 的配置文件
                if 'json' in check_file.name and 'Content' not in check_file.name:
                    # 查找 json 串 "image_name"
                    simple_contain_str = "\"" + image_name + "\""
                    contain = check_file.has_contain(simple_contain_str, image_analyse_check_as_line)
                    if contain:
                        break

                    # 查找json 串：\"image_name\"
                    simple_contain_str = "\\\"" + image_name + "\\\""
                    contain = check_file.has_contain(simple_contain_str, image_analyse_check_as_line)
                    if contain:
                        break
                else:
                    # 查找 @"image_name"
                    contain_str = "@\"" + image_name + "\""
                    contain = check_file.has_contain(contain_str, image_analyse_check_as_line)
                    if contain:
                        break
        if contain:
            img_files.remove(img_file)
        else:
            i += 1

    return img_files
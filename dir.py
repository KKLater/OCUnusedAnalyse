#!/usr/bin/python
# coding=utf-8

import os
import file

from file import File


class Dir(object):

    def __init__(self, name):
        self.name = name

    def description(self):
        print "Name: %s" % self.name

    # ====================
    # 获取根目录下的所有文件
    # ====================
    def files(self):
        paths_list = []
        for main_dir, subdir, file_name_list in os.walk(self.name):
            for filename in file_name_list:
                a_path = os.path.join(main_dir, filename)
                a_file = File(a_path, filename)
                paths_list.append(a_file)
        return paths_list

    # ====================
    # 获取根目录下的所有文件路径
    # ====================
    def paths(self):
        paths_list = []
        all_files = self.files()
        for c_file in all_files:
            if isinstance(c_file, File):
                paths_list.append(c_file.path)

    # ====================
    # 计算总大小
    # ====================
    def total_size(self):
        size = file.files_total_size(self.files())
        return size


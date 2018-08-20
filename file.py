#!/usr/bin.python
# coding=utf-8

import os
import xlwt


class File(object):

    def __init__(self, path, name):
        if os.path.isfile(path):
            self.path = path
            self.name = name

    # ====================
    # 计算文件大小
    # ====================
    def get_size(self):
        return os.path.getsize(self.path)

    # ====================
    # 获取文件后缀
    # ====================
    def get_extension(self):
        name = self.name
        if '.' in name:
            strings = name.partition('.')
            return strings[len(strings) - 1]

    # ====================
    # 判定文件是否包含字段
    # ====================
    def has_contain(self, contain_str, as_line=False):
        if as_line and self.get_size() > 5 * 1024 * 1024:
            as_line = False
        if as_line:
            with open(self.path) as f:
                line = f.readline()
                while line:
                    if contain_str in line:
                        f.close()
                        return True
                        break
                    line = f.readline()
            f.close()
            return False
        else:
            contain = False
            with open(self.path) as f:
                texts = f.read()
                if contain_str in texts:
                    contain = True
            f.close()
            return contain

    def description(self):
        print "File:%s, Size:%f" % (self.path, self.get_size())


# ====================
# 通过paths，获取生成 File List 列表
# ====================
def files_for_paths(paths):
    file_paths = [File]
    for path in paths:
        file_path = File(path)
        file_paths.append(file_path)

    return file_paths


# ====================
# 计算 File 列表所有 File 文件的大小之和
# ====================
def files_total_size(file_list):
    total_size = 0
    for a_file in file_list:  # type: File
        if isinstance(a_file, File):
            total_size += a_file.get_size()

    return total_size


# ====================
# 保存 File 到本地 exml
# ====================
def files_save(_save_files, save_path, save_name, extensions=[]):
    sheet_names = []
    if len(extensions) <= 0:
        for c_file in _save_files:
            if can_read_info(c_file) == 1 and isinstance(c_file, File) and not ('/.' in c_file.path):
                extension_name = '%s' % c_file.get_extension()
                sheet_name = extension_name
                if sheet_name not in sheet_names:
                    sheet_names.append(sheet_name)
    else:
        sheet_names = extensions

    wb = xlwt.Workbook()
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 22
    style = xlwt.XFStyle()
    style.pattern = pattern
    for sheet_name in sheet_names:
        ws = wb.add_sheet(sheet_name)
        ws.write(0, 0, unicode('文件名'))
        ws.write(0, 1, unicode('地址'))
        ws.write(0, 2, unicode('类型'))
        ws.write(0, 3, unicode('大小'))
        i = 1
        for c_file in _save_files:
            if can_read_info(c_file) == 1 and isinstance(c_file, File) and not ('/.' in c_file.path):
                name = c_file.name
                path = c_file.path
                type_name = c_file.get_type()
                size = c_file.get_size()

                extension_name = '%s' % c_file.get_extension()
                if sheet_name == extension_name:
                    ws.write(i, 0, unicode("%s" % name))
                    ws.write(i, 1, unicode("%s" % path))
                    ws.write(i, 2, unicode("%s" % type_name))
                    ws.write(i, 3, size * 1.0)
                    i += 1
    wb.save(save_path + '/' + save_name + '.xls')


def can_read_info(c_file):
    if isinstance(c_file, File):
        if '/.' in c_file.path:
            return 0
    return 1

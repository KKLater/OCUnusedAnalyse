#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import progress

from dir import Dir

zhPattern = re.compile(u'[\u4e00-\u9fa5]+')


# =======================
# 获取没有使用到的代码文件
# =======================
def get_un_use_code_files(a_project_path, a_zh_un_check_enable):
    c__dir = Dir(a_project_path)
    c_files = c__dir.files()
    h_files = []
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
            if not (is_jpg or is_png):
                check_files.append(c_file)
                # 过滤pod
                if 'h' == c_file.get_extension():
                    h_files.append(c_file)

    i = 0
    progress_index = 0
    total = len(h_files)
    print("Total \'.h\' Files Count:%d" % total)
    while i < len(h_files):
        progress_index += 1
        progress.show_progress(progress_index, total)

        h_file = h_files[i]
        contain = has_code_file_contain(h_file, check_files)
        if contain:
            i -= 1
            h_files.remove(h_file)

        i += 1
    return h_files


def has_code_file_contain(h_file, files, oc_analyse_check_as_line=False):
    contain = False
    for c_file in files:
        if '+' in h_file.name:
            contain = True
            break
        else:
            not_same_file = c_file.name != h_file.name
            not_hm_file = c_file.name.partition('.')[0] != h_file.name.partition('.')[0]
            if not_same_file and not_hm_file:
                contain_str = h_file.name.partition('.')[0]
                contain = has_contain_code(c_file, contain_str, oc_analyse_check_as_line)
                if contain:
                    break
    return contain


def has_contain_code(c_file, contain_str, as_line=False):
    if as_line and c_file.get_size() > 5 * 1024 * 1024:
        as_line = False
    if as_line:
        with open(c_file.path) as f:
            line = f.readline()
            while line:
                if 'json' == c_file.get_extension():
                    if contain_str in line:
                        f.close()
                        return True
                        break
                else:
                    import_contain_str = "import \"" + contain_str + ".h\""
                    if import_contain_str in line:
                        f.close()
                        return True
                        break
                    else:
                        use_contain_str = contain_str + " "
                        if use_contain_str in line:
                            f.close()
                            return True
                            break

                line = f.readline()
        f.close()
        return False
    else:
        contain = False
        with open(c_file.path) as f:
            texts = f.read()
            if 'json' == c_file.get_extension():
                if contain_str in texts:
                    contain = True
            else:
                import_contain_str = "import \"" + contain_str + ".h\""
                if import_contain_str in texts:
                    contain = True
                else:
                    use_contain_str = contain_str + " "
                    if use_contain_str in texts:
                        contain = True
        f.close()
        return contain

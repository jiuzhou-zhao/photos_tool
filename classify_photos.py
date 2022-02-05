# -*- coding: utf-8 -*-
import shutil
import os
import exifread
import time
import sys
import getopt


def get_original_date(filename):
    try:
        fd = open(filename, 'rb')
    except:
        raise RuntimeError("unopen file[%s]" % filename)

    data = exifread.process_file(fd)
    if data:
        try:
            t = data['EXIF DateTimeOriginal']
            return str(t).replace(":", ".")[:7]
        except:
            pass

    state = os.stat(filename)
    return time.strftime("%Y.%m", time.localtime(state.st_mtime))


def classify_photo(src_root, src_file, dst_root, rename_dst_file, cp_flag):
    photo_src = os.path.join(src_root, src_file)
    f, e = os.path.splitext(photo_src)
    if e.lower() not in ('.jpg', '.jpeg', '.png', '.mp4', '.mov', '.3gp'):
        return

    info = "文件名: " + photo_src + " "
    t = ""
    try:
        t = get_original_date(photo_src)
    except Exception as e:
        print(info, e)
        return

    dst_root = os.path.join(dst_root, t)
    if not os.path.exists(dst_root):
        os.makedirs(dst_root)

    dst_file = os.path.join(dst_root, src_file)
    if os.path.exists(dst_file) and rename_dst_file:
        dst_file = os.path.join(dst_root, "1_"+src_file)
    if not os.path.exists(dst_file):
        if cp_flag:
            shutil.copy2(photo_src, dst_file)
        else:
            shutil.move(photo_src, dst_file)
    else:
        print("%s exists" % dst_file)


def classify_photos(src_root, dst_root, rename_dst_file, cp_flag):
    for root, dirs, files in os.walk(src_root, True):
        for filename in files:
            classify_photo(root, filename, dst_root, rename_dst_file, cp_flag)
        for d in dirs:
            classify_photos(os.path.join(src_root, d), dst_root, rename_dst_file, cp_flag)


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "-s:-d:-r-c-v", ["src", "dst", 'rename_dst_file', 'copy', 'version'])

    src = None
    dst = None
    rename_dst_file_var = False
    cp_flag_var = False
    for opt_name, opt_value in opts:
        if opt_name in ("-s", "--src"):
            src = opt_value
        if opt_name in ("-d", "--dst"):
            dst = opt_value
        if opt_name in ("-r", "--rename_dst_file"):
            rename_dst_file_var = True
        if opt_name in ("-c", "--copy"):
            cp_flag_var = True
        if opt_name in ("-v", "--version"):
            print("The version is v1.0")
            exit()
    if src is None or dst is None:
        print("no src or dst dir")
        exit(1)

    print(src + " => " + dst)
    classify_photos(src, dst, rename_dst_file_var, cp_flag_var)

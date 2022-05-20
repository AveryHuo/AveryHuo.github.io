from audioop import reverse
import os
import sys
import time
import re

from regex import B

repo_path = ""
git_repo = None
is_local = True

def timestamp2time(timestamp):
    time_struct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)

def get_file_modify_time(file_path):
    if is_local:
        t = os.path.getmtime(file_path)
        return timestamp2time(t)
    else:
        rel_path = file_path.replace(repo_path+"/", "")
        mod_time_str = git_repo.log(rel_path, format="%ad", date="format:%Y-%m-%d %H:%M:%S", max_count=1)
        return mod_time_str

def get_file_create_time(file_path):
    rel_path = file_path.replace(repo_path+"/", "")
    mod_time_str = git_repo.log(rel_path, diff_filter="A", format="%ad", date="format:%Y-%m-%d %H:%M:%S", reverse=True)
    return mod_time_str

def handle_file(file_path):
    modify_time = get_file_modify_time(file_path)
    create_time = get_file_create_time(file_path)
    file_data = ""
    source_date_txt = ""
    source_update_txt = ""
    source_title_txt = ""
    source_top_img_txt = ""
    first_img_line = ""
    with open(file_path, "r", encoding='utf-8') as f:
        for line in f:
            if "date:" in line:
                source_date_txt = line
            if "updated:" in line:
                source_update_txt = line
            if "title:" in line:
                source_title_txt = line
                print("处理中:%s"%source_title_txt)
            if "top_img" in line:
                source_top_img_txt = line
            if "/img/" in line and first_img_line == "":
                first_img_line = line
                print("找到图片：%s"%source_top_img_txt)
            file_data += line
    
    new_title_txt = source_title_txt

    if source_date_txt != "":
        file_data = file_data.replace(source_date_txt, "date: "+ create_time+"\n")
    else:
        new_title_txt = "{0}date: {1}\n".format(source_title_txt, create_time)
    print("创建时间：%s"%create_time)

    if source_update_txt != "":
        file_data = file_data.replace(source_update_txt, "updated: "+modify_time+"\n")
    else:
        new_title_txt = "{0}updated: {1}\n".format(new_title_txt, modify_time)
    print("更新时间：%s"%modify_time)
    
    if source_top_img_txt == "":
        new_title_txt = "{0}top_img: false\n".format(new_title_txt)
    
    if first_img_line != "":
        p = re.compile(r'[(](.*?)[)]', re.S)
        imgs = re.findall(p, first_img_line)
        if imgs != None and len(imgs) > 0:
            new_title_txt = "{0}cover: {1}\n".format(new_title_txt, imgs[0])

    file_data = file_data.replace(source_title_txt, new_title_txt)
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_data)
   

def standard_path(path_str):
    return path_str.replace("\\", "/")

def check_is_md_file(file_path):
    return file_path.endswith(".md")

if __name__ == "__main__":
    repo_in_str = input("target repository:")
    if repo_in_str == "":
        repo_path = sys.argv[1]
    else:
        repo_path = repo_in_str

    file_path_in_str = input("target file or folder(Empty -> <preset>): ")    
    if file_path_in_str == "":
        file_path = sys.argv[2]
    else:
        file_path = file_path_in_str
    
    is_local_in_str = input("is local(Y/N): ")
    if is_local_in_str == "Y" or is_local_in_str == "y":
        is_local = True
    else:
        is_local = False

    repo_path = standard_path(repo_path)
    file_path = standard_path(file_path)
    print("repo_path:{0}, fileorfolder_path:{1}, is_local:{2}".format(repo_path, file_path,is_local))
    from git import Repo
    repo = Repo(repo_path)
    git_repo = repo.git
    if os.path.isdir(file_path):
        for i,j,k in os.walk(file_path):
            for file_name in k:
                full_path = os.path.join(i, file_name)
                if check_is_md_file(full_path):
                    handle_file(full_path)
    else:
        if check_is_md_file(file_path):
            handle_file(file_path)
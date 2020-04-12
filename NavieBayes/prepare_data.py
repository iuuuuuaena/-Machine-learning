# coding:utf-8
# @Project Name deep_learn_test2
# @Name prepare_data
# @Author by jxd
# @Email waniiu@126.com
# @Time 2020/4/12 4:37 下午
# @Method for

import os
import random
import shutil


def get_email_path(path):
    '''
    邮件路径获取！
    :param path:
    :return:  返回邮件目录列表
    '''
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            # 相对路径
            eachpath = str(root+'/'+fn)
            fileArray.append(eachpath)
    return fileArray



if __name__ == '__main__':
    title_file_path = r"email"
    test_file_path = r"test"
    files = get_email_path(title_file_path)
    random.shuffle(files)
    # print(files)
    top10 = files[:10]
    print(top10)
    for file in top10:
        # 把前十个里面的每一个文件的目录用空格分离，获取最后一个文件名，拼接成test里面测试的文件名
        test_file_name = title_file_path+"/"+("/".join(file.split("/")[-2:]))
        # print(test_file_name)
        shutil.move(test_file_name, test_file_path)
        print(test_file_path + '/' + file.split('/')[-1])
        print(test_file_path+'/'+file.split('/')[-2]+"_"+file.split('/')[-1])
        os.rename(test_file_path+'/' + file.split('/')[-1],test_file_path+'/'+file.split('/')[-2]+"_"+file.split('/')[-1])
        # print("move {} successful".format(file.split("/")[-2:]))


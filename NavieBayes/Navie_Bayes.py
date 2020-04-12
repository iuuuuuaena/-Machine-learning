# coding:utf-8
# @Project Name deep_learning_test
# @Name beiyesi
# @Author by jxd
# @Email waniiu@126.com
# @Time 2020/4/11 8:10 下午
# @Method for  Navie_Bayes

import os
import matplotlib.pyplot as plt

def read_file(file_path,encoding):
    '''
    读邮件读取所有信息
    :param file_path:
    :param encoding:
    :return:  返回邮件内容
    '''
    with open(file_path, 'r', encoding = encoding) as f:
        lines = f.readlines()
    return lines


def clean_useless_symbol(email_path):
    '''
    预处理，处理各种符号和长度小于2的无用单词
    :param email_path:
    :return:  返回清理后的单词列表
    '''
    # 采用的方式：使用这些字符分开所有的内容
    punctuations = """,.<>()*&^%$#@!'";~`[]{}|、\\/~+_-=?"""
    content_list = read_file(email_path, 'utf8')
    # 使用空格分开所有的字符，把多行都归并为一行，单词全部使用空格隔开
    content = (' '.join(content_list)).replace('\r\n', ' ').replace('\t', ' ')
    # print(content)
    # 清理后的单词列表
    clean_word = []
    # 使用所有符号隔开邮件，并存放入clean_word中
    for punctuation in punctuations:
        # 单词之间用 隔开，使用  替代 。
        content = (' '.join(content.split(punctuation))).replace('  ', ' ')
        # 过滤掉所有长度小于等于2的单词
        clean_word = [word.lower()
                      for word in content.split(' ') if len(word) > 2]
    return clean_word


def get_emails_path(path):
    '''
    邮件路径获取！
    :param path:
    :return:  返回邮件目录列表
    '''
    fileArray = []
    for root, dirs, files in os.walk(path):
        # print(root)
        # print("----")
        # print(dirs)
        # print("----")
        # print(files)
        for fn in files:
            eachpath = str(root+'/'+fn) # 相对路径
            fileArray.append(eachpath)
    print("dasdsdsa")
    print(fileArray)
    return fileArray

def remote_repeated_word(root_emails_path):
    '''
    预处理，去掉邮件中重复的单词
    :param root_emails_path: 邮件种类目录，包括spam和ham
    :return:  返回正常邮件单词列表和无重复的列表
    '''
    word_list = []
    word_set = []
    emails_path_list = get_emails_path(root_emails_path) # 获取邮件路径列表
    print("-----------")
    print(emails_path_list)
    # print("-----------")
    # 循环遍历列表，获取每一个邮件的路径
    for each_email_path in emails_path_list:
        # print(each_email_path)
        email_word = clean_useless_symbol(each_email_path)  # 清除无用的符号
        word_list.append(email_word)
        word_set.extend(email_word)
    # 返回时，去重
    return word_list,set(word_set)

# def prepare_data(root_emails_path):
#     '''
#     数据预处理的总函数
#     :param root_emails_path:
#     :return: word_list, word_set
#     '''
#     word_list,word_set = remote_repeated_word(root_emails_path)
#     return word_list, word_set

def get_words_count_prob(email_list,union_set):
    '''
    获得单词出现的概率
    :param email_path_list:
    :param union_set:
    :return:  返回单词概率字典
    '''
    # 定义单词概率字典
    word_prob = {}
    # 遍历set列表
    for word in union_set:
        counter = 0  # 定义计数器，
        for email_word_list in email_list:
            if word in email_word_list: # 如果出现，计数器加一
                counter += 1
            else:
                continue
        prob = 0.0
        if counter != 0:
            # 最后获得每一个单词出现的次数占总单词数量的概率
            prob = counter / len(email_list)
        else:
            # 这里是为了防止出现极端情况，所以就算文章里没有这个单词，
            # 我们也把他的概率设置为0.01
            prob = 0.01
        # 把单词和概率对应起来
        word_prob[word] = prob
    return word_prob

def filter(ham_word_pro, spam_word_pro, test_files):
    '''
    过滤器，把训练集的正常邮件的单词概率和垃圾邮件的单词概率带入，求得测试邮件的垃圾概率
    :param ham_word_pro:
    :param spam_word_pro:
    :param test_file:
    :return:
    '''
    # 读取测试的十个文件的路径
    test_files_path =get_emails_path(test_files)
    for test_file_path in test_files_path:
        # 定义初始概率
        email_spam_prob = 0.0  # 垃圾邮件概率初始概率为0
        spam_prob = 0.5    # 垃圾邮件概率先验概率为50%
        ham_prob = 0.5     # 正常邮件概率先验概率为50%
        # 获测试文件名
        file_name = test_file_path.split('/')[-1]
        prob_dict = {}
        # 去掉重复的单词和无用的符号
        test_words_list = set(clean_useless_symbol(test_file_path))
        for word in test_words_list:
            Psw = 0.0
            # 条件概率
            # print(spam_word_pro)
            if word not in spam_word_pro:
                # 如果这个垃圾词汇不是垃圾邮件里的
                Psw = 0.4
            else:
                # 如果是垃圾邮件里的
                Pws = spam_word_pro[word]
                Pwh = ham_word_pro[word]
                # 条件概率公式
                Psw = spam_prob * (Pws / (Pwh * ham_prob + Pws * spam_prob))
            # 把获得的概率存入字典
            prob_dict[word] = Psw
        numerator = 1
        denominator_h = 1
        # 求所有单词的联合概率
        for k, v in prob_dict.items():
            numerator *= v
            denominator_h *= (1 - v)
        # print(prob_dict)
        # 带入联合概率计算公式
        email_spam_prob = round(numerator / (numerator + denominator_h), 4)
        if email_spam_prob > 0.5:
            print(file_name, 'spam', email_spam_prob)
        else:
            print(file_name, 'ham', email_spam_prob)

def draw(spam_word_pro):
    '''
    绘制柱状图
    :param spam_word_pro:
    :return:
    '''
    key = [k for k,v in list(spam_word_pro.items())[:5] ]
    value =  [v for k,v in list(spam_word_pro.items())[:5] ]
    print("k:")
    print(key)
    # 创建一个规格为 1 x 1 的子图
    plt.subplot(1, 1, 1)
    plt.xticks(range(5),key)
    plt.yticks(value)
    # 柱子的宽度
    width = 0.55
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色
    plt.bar(key, value, width, label="word_prot", color="#87CEFA")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 设置横轴标签
    plt.xlabel('word')
    # 设置纵轴标签
    plt.ylabel('prot')
    # 添加标题
    plt.title('spam_prot')
    # 添加纵横轴的刻度
    # 添加图例
    plt.legend(loc="upper right")
    plt.savefig("image.png")
    plt.show()


def main():
    ham_file = r"email/ham"
    spam_file = r"email/spam"
    test_file = r"test"
    # 数据预处理
    ham_list, ham_set = remote_repeated_word(ham_file)
    spam_list, spam_set = remote_repeated_word(spam_file)
    # 求两个set的并集
    union_set = ham_set | spam_set
    # print(union_set)
    # 获得单词垃圾概率
    ham_word_pro = get_words_count_prob(ham_list, union_set)
    spam_word_pro = get_words_count_prob(spam_list, union_set)
    draw(spam_word_pro)
    # print(spam_word_pro)
    # 进行预测
    filter(ham_word_pro, spam_word_pro, test_file)

if __name__ == '__main__':
    main()
# coding=<encoding UTF-8>

import re
import pymssql
import requests
from bs4 import BeautifulSoup


def remove_special_characters(strings, char1, char2):
    new_string = re.sub(char1, "", strings)
    new_string1 = re.sub(char2, "", new_string)
    return new_string1


list_title = []
list_time = []

a = 0
b = 0

connect = pymssql.connect(host='localhost', server='LAPTOP-D1L9BQA5', port='1433', user='spider_pycharm',
                          password='123456',
                          database='spider',
                          charset='UTF-8')
cursor = connect.cursor()

# 创建一个存储过程
cursor.execute("""
IF OBJECT_ID('persons', 'U') IS NOT NULL
    DROP TABLE persons
CREATE TABLE persons (
    id INT NOT NULL,
    Title NVARCHAR(4000),
    Time VARCHAR(4000),
    PRIMARY KEY(id)
)
""")

headers: dict[str, str] = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0'
}

i = 0
for i in range(0, 13, 1):
    if i == 0:
        arm = requests.get('https://kjt.nx.gov.cn/zwgk/fdgk/zcjd/', headers=headers).text  # GET方式，获取网页数据
    if i != 0:
        arm = requests.get(f'https://kjt.nx.gov.cn/zwgk/fdgk/zcjd/index_{i}.html', headers=headers).text

    soup = BeautifulSoup(arm, 'html.parser')
    All_titles = soup.find_all("a", attrs={"class": "c1"}, )
    All_time = soup.find_all("b")

    for title in All_titles:
        title11 = title.string
        uni = title11.split()
        list_title.insert(a, uni)
        # print(title.string)
        a = a + 1
    for time in All_time:
        list_time.insert(b, time.string)
        # print(time.string)
        b = b + 1

k = 0
for k in range(0, 26, 1):
    if k == 0:
        arm = requests.get('https://kjt.nx.gov.cn/kjdt/tzgg/', headers=headers).text  # GET方式，获取网页数据
    if k != 0:
        arm = requests.get(f'https://kjt.nx.gov.cn/kjdt/tzgg/index_{k}.html', headers=headers).text

    soup = BeautifulSoup(arm, 'html.parser')
    All_titles = soup.find_all("div", attrs={"class": "info_list"})
    All_time = soup.find_all("span", attrs={"class": "times03"})

    for title in All_titles:
        unis = title.find("a", attrs={"target": "_blank"})
        for uni in unis:
            if uni.string == "》":
                pass
            else:
                list_title.insert(a, uni.string)
                a = a + 1
    for time in All_time:
        list_time.insert(b, time.string)
        # print(time.string)
        b = b + 1

print(a)
print(b)
print(list_title)
print(list_time)

# 将数据导入数据库
m = 0
for m in range(0, a - 1, 1):
    cursor.executemany(
        "INSERT INTO persons VALUES (%d, %s, %s)",
        [(m, str(list_title[m]), list_time[m])])

# 如果连接时没有设置autocommit为True的话，必须主动调用commit() 来保存更改。
connect.commit()
# 查询记录
cursor.execute('SELECT * FROM persons WHERE Time=%s', 'John Doe')
# 获取一条记录
row = cursor.fetchone()
# 循环打印记录(这里只有一条，所以只打印出一条)
while row:
    print("ID=%d, Name=%s" % (row[0], row[1]))
    row = cursor.fetchone()
# 连接用完后记得关闭以释放资源
connect.close()

# '''
# total1 = requests.get('https://kjt.nx.gov.cn/zwgk/fdgk/zcjd/index_1.html', headers=headers).text  # GET方式，获取网页数据
# soup1 = BeautifulSoup(total1, 'html.parser')
# All_titles = soup1.find_all("a", attrs={"class": "c1"})
# for title1 in All_titles:
#     print(title1.string)
# '''
#
# '''
# # 打印爬取状态
# if requests.Response.ok:
#     print(total)  # 打印网站状态码
#     print(total)  # 爬取网站数据
#     print("访问成功")
# else:
#     print("访问失败")
# '''
#
# '''
# # 创建文件储存爬取数据
# path = 'C:\桌面'
# os.mkdir(path)
# os.chdir(path)
# fp = open('标题.txt', 'a+')
# fp.write(total)
# fp.close()
# '''
#
# '''
# # 创建爬取数据的方法
# def get_html(url):
#     headers: dict[str, str] = {
#         "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0'
#     }
#     total = requests.get('https://kjt.nx.gov.cn/zwgk/fdgk/zcjd/', headers=headers).text  # GET方式，获取网页数据
#     soup = BeautifulSoup(total, 'html.parser')
#     All_titles = soup.find_all("a", attrs={"class": "c1"})
#     for title in All_titles:
#         print(title.string)
# '''
#
# '''
# 爬取的网站
# https://kjt.nx.gov.cn/zwgk/fdgk/zcjd/
# https://kjt.nx.gov.cn/zwgk/fdgk/zcjd/index_1.html
# https://kjt.nx.gov.cn/zwgk/fdgk/zcjd/index_2.html
# 至
# https://kjt.nx.gov.cn/zwgk/fdgk/zcjd/index_12.html
#
#
#
# https://kjt.nx.gov.cn/kjdt/tzgg/
# '''

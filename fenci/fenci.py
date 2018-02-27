#!/usr/bin/env python
# coding = utf8
from collections import Counter
import jieba.analyse
import time
import pandas as pd
import xlwt

bill_path = r'../weibo/weibo1.txt'
bill_result_path = r'../weibo/words.txt'
# bill_result_path = r'result.txt'
with open(bill_path, 'r') as fr:
    data = jieba.cut(fr.read())
# 带次数
# data = dict(Counter(data))
# with open(bill_result_path,'w') as fw:
#     for k,v in data.items():
#         fw.write("%s,%d\n" % (k,v))

filter = ["全文", "via", "网页", "链接", "gt", "VOL"]


# 判断是否非汉字，数字和英文字符
def is_other(uchar):
    return not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar))


# 判断一个unicode是否是汉字
def is_chinese(uchar):
    return uchar >= u'\u4e00' and uchar <= u'\u9fa5'


# 判断一个unicode是否是英文字母
def is_alphabet(uchar):
    return (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a')


# 判断一个unicode是否是数字
def is_number(uchar):
    return uchar >= u'\u0030' and uchar <= u'\u0039'


# 分词并写入
# with open(bill_result_path, 'w') as fw:
#     for k in data:
#         if not (is_other(k) or k in filter):
#             fw.write("%s\n" % k)
# 从文件读取
with open(bill_result_path) as f:
    words = f.readlines()
word_list = list(map(lambda x: x.strip(), words))

# 使用pandas统计并降序排列
df = pd.DataFrame(word_list, columns=['word'])
result = df.groupby(['word']).size()
result = result.sort_values(ascending=False)

# 生成Excel
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
sheet.write(0, 0, "序号")
sheet.write(0, 1, "词语")
sheet.write(0, 2, "词频")
column = 1
for k, v in result.items():
    sheet.write(column, 0, column)
    sheet.write(column, 1, k)
    sheet.write(column, 2, str(v))
    column += 1
wbk.save('fenci_result.xls')

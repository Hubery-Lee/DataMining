from os import path
import os
import json
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud



# 将所有文件夹名转换为 str 类型
folder_name = " ".join(os.listdir(r"F:\mzitu"))

# jieba 分词
jieba.load_userdict(r".\data\jieba.txt")
seg_list = jieba.lcut(folder_name, cut_all=False)

# 利用字典统计词频
counter = dict()
for seg in seg_list:
    counter[seg] = counter.get(seg, 1) + 1
print(counter)
# 根据词频排序字典
counter_sort = sorted(
    counter.items(), key=lambda value: value[1], reverse=True
)
# print(counter_sort)

# 解析成 json 类型并写入文件
words = json.dumps(counter_sort, ensure_ascii=False)
with open(r".\data\words.json", "w+", encoding="utf-8") as f:
    f.write(words)

# 生成词云
font = r'C:\Windows\Fonts\simfang.ttf' # 设置字体路径
wordcloud = WordCloud(
    background_color = 'black',     # 背景颜色
    #mask = cloud_mask,             # 背景图片
    max_words = 100,                # 设置最大显示的词云数
    font_path = font,               # 设置字体形式（在本机系统中）
    height = 300,                   # 图片高度
    width = 600,                    # 图片宽度
    max_font_size = 100,            # 字体最大值
    random_state = 100,             # 配色方案的种类
).generate_from_frequencies(
    counter,max_font_size = 100
)
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
wordcloud.to_file("worldcloud.jpg")

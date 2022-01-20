import jieba
import jieba.posseg as posseg
import re
import os


def articleNLP(article):  # 传入参数为字符串类型
    jieba.enable_paddle()
    punctuation = '！（）——“：’；、。，？》《{}【】“”'
    not_location_words = "'小区''风景区''开发区''度假区''风景名胜区''园区'"
    not_ethnicity_words = "'中华民族''民族'"
    article = article.strip()
    article = article.replace("\n", "")
    article = re.sub(r"[%s]+" % punctuation, "", article)
    article = article.split("生效裁判审判人员")[0]

    person_concerned = set()  # 当事人
    court = set()  # 案件经手法院
    location = set()  # 地方
    ethnicity = set()   # 民族
    words = posseg.lcut(article, use_paddle=True)
    for word, flag in words:
        # print(word, flag)
        if flag == 'PER' and not re.search(r"\s|''", word):
            person_concerned.add(re.sub(r"\s|''", "", word))
        if flag == 'ORG':
            if re.search(r"法院", word):
                court.add(re.sub(r"\s", "", word))
        if flag == 'LOC':  # 尚未细分
            if re.search(r"省", word):
                location.add(re.sub(r"\s", "", word))
            if re.search(r"市", word):
                location.add(re.sub(r"\s", "", word))
            if re.search(r"区", word) and not re.search(r"[%s]+" % not_location_words, word):
                location.add(re.sub(r"\s", "", word))
        if re.search(r"族", word) and not re.search(r"[%s]+" % not_ethnicity_words, word):
            ethnicity.add(re.sub(r"\s", "", word))
    info_list = [person_concerned, court, location, ethnicity]
    print(info_list)
    return info_list


if __name__ == '__main__':

    txt_files = []
    for txt_file in os.listdir('./GuidingCase/'):  # 含有文件夹路径，测试需修改
        if txt_file.endswith(".txt"):
            txt_files.append(os.path.join('./GuidingCase/', txt_file))  # 含有文件夹路径，测试需修改
    for file in txt_files:
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()
            articleNLP(data)

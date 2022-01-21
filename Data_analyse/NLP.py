# -*- coding = utf-8 -*-
# @Time : 2022/1/13 15:35
# @Author : Sky
# @File : NLP.py
# @Software : PyCharm
import json
import os
import jieba
import jieba.posseg as pseg
from pyhanlp import HanLP
from NLP_get_time import getTime
import cn2an
import Duration


jieba.load_userdict("./NLP_Dictionary/jiebaDict.txt")
jieba.load_userdict("./NLP_Dictionary/CourtDict.txt")
jieba.load_userdict("./NLP_Dictionary/criminal_crime.txt")
jieba.load_userdict("./NLP_Dictionary/civil_crime.txt")
province = {'北京市', '天津市', '上海市', '重庆市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省',
            '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '台湾省', '内蒙古自治区', '广西壮族自治区',
            '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区', '澳门特别行政区'}


def CovertJavaListToPlist(java_list):
    python_list = []
    if java_list is None:
        return python_list
    for element in range(java_list.size()):
        python_list.append(str(java_list.get(element)))
    return python_list


def textNLP(data):
    infinite = True
    category = {}
    result = {}
    # jieba
    words = pseg.cut(data)
    for w in words:
        if category.get(w.flag) is None:
            category[w.flag] = {w.word, }
        else:
            category[w.flag].add(w.word)

    # HanLP
    segment = HanLP.newSegment().enableNameRecognize(True)
    java_list = segment.seg(data)
    python_list = CovertJavaListToPlist(java_list)
    for i in python_list:
        if i.endswith("/nr") and len(i.rstrip("/nr")) < 4:
            if category.get("name") is None:
                category["name"] = {i.rstrip("/nr"), }
            else:
                category["name"].add(i.rstrip("/nr"))

    # 得到时间
    result["time"] = getTime(data)
    if result.get("time"):
        for i in range(0, len(result['time'])):
            if not result['time'][i].startswith('19') and not result['time'][i].startswith('20'):
                result['time'][i] = '20' + cn2an.transform(result['time'][i], 'cn2an')

    if data.decode(encoding="UTF-8").find("判处有期徒刑") != -1:
        penalty_list = []
        begin_index = data.decode(encoding="UTF-8").find("判处有期徒刑") + 6
        end_index = begin_index
        while data.decode(encoding="UTF-8")[end_index] != '，' and data.decode(encoding="UTF-8")[end_index] != "(" \
                and data.decode(encoding="UTF-8")[end_index] != ',' and data.decode(encoding="UTF-8")[end_index] != '。'\
                and data.decode(encoding="UTF-8")[end_index] != '；':
            end_index = end_index + 1
        penalty = data.decode(encoding="UTF-8")[begin_index:end_index]
        penalty_list.append(penalty)
        if data.decode(encoding="UTF-8").find("执行有期徒刑", end_index) != -1:
            begin_index = data.decode(encoding="UTF-8").find("执行有期徒刑", end_index) + 6
            end_index = begin_index
            while data.decode(encoding="UTF-8")[end_index] != '，' and data.decode(encoding="UTF-8")[end_index] != "(" \
                    and data.decode(encoding="UTF-8")[end_index] != ',' and data.decode(encoding="UTF-8")[
                end_index] != '。' \
                    and data.decode(encoding="UTF-8")[end_index] != '；':
                end_index = end_index + 1
            penalty = data.decode(encoding="UTF-8")[begin_index:end_index]
            penalty_list.clear()
            penalty_list.append(penalty)
        else:
            if data.decode(encoding="UTF-8").find("判处有期徒刑", end_index) != -1:
                begin_index = data.decode(encoding="UTF-8").find("判处有期徒刑", end_index) + 6
                end_index = begin_index
                while data.decode(encoding="UTF-8")[end_index] != '，' and data.decode(encoding="UTF-8")[
                    end_index] != "(" \
                        and data.decode(encoding="UTF-8")[end_index] != ',' and data.decode(encoding="UTF-8")[
                    end_index] != '。' \
                        and data.decode(encoding="UTF-8")[end_index] != '；':
                    end_index = end_index + 1
                penalty = data.decode(encoding="UTF-8")[begin_index:end_index]
                penalty_list.clear()
                penalty_list.append(penalty)
        result["time"].append(penalty_list)
        infinite = False

    # 得到法院
    if category.get("nt"):
        nt = category.get("nt").copy()
        for element in nt:
            if not element.endswith("法院") or element == "人民法院" or element == "最高人民法院":
                category.get("nt").remove(element)
        result["court"] = category.get("nt")
    else:
        result["court"] = {}
    # 将jieba和hanlp的人名结果合并，取交集
    if category.get("name") and category.get("nr"):
        result["name"] = category["name"].intersection(category["nr"])
    elif category.get("name"):
        result["name"] = category["name"]
    elif category.get("nr"):
        result["name"] = category["nr"]
    else:
        result["name"] = []
    # 得到案发地点
    location = {"中华人民共和国", }
    result["location"] = {"国家": {"中华人民共和国", }, "省/直辖市/自治区/特别行政区": set(), "城市": set(), "县/区": set(),
                          "乡/镇": set()}
    if category.get("ns"):
        ns = category.get("ns").copy()
        for element in ns:
            if element.endswith("省") or element.endswith("市") or element.endswith("县") or element.endswith(
                    "区") or \
                    element.endswith("乡") or element.endswith("镇"):
                location.add(element)
    if "城市" in location:
        location.remove("城市")
    if "上市" in location:
        location.remove("上市")
    if "故省" in location:
        location.remove("故省")
    if "大省" in location:
        location.remove("大省")
    if "上海市" not in location and "上海" in category["ns"]:
        location.add("上海市")
    if "上海市浦东新区" in location:
        location.remove("上海市浦东新区")
        location.add("浦东新区")
    # 将location中的键值对加入result，并且划分行政级别
    for element in location:
        if element.endswith("国"):
            result["location"]["国家"].add(element)
        if element in province:
            result["location"]["省/直辖市/自治区/特别行政区"].add(element)
        else:
            if element.endswith("市"):
                result["location"]["城市"].add(element)
            if element.endswith("县") or element.endswith("区"):
                result["location"]["县/区"].add(element)
            if element.endswith("乡") or element.endswith("镇"):
                result["location"]["乡/镇"].add(element)
    # 删除没有元素的键值对并将其list
    result["location"]["国家"] = list(result["location"]["国家"])
    if not result["location"].get("省/直辖市/自治区/特别行政区"):
        del result["location"]["省/直辖市/自治区/特别行政区"]
    else:
        result["location"]["省/直辖市/自治区/特别行政区"] = list(result["location"]["省/直辖市/自治区/特别行政区"])
    if not result["location"].get("城市"):
        del result["location"]["城市"]
    else:
        result["location"]["城市"] = list(result["location"]["城市"])
    if not result["location"].get("县/区"):
        del result["location"]["县/区"]
    else:
        result["location"]["县/区"] = list(result["location"]["县/区"])
    if not result["location"].get("乡/镇"):
        del result["location"]["乡/镇"]
    else:
        result["location"]["乡/镇"] = list(result["location"]["乡/镇"])

    # 将set转为list

    result["court"] = list(result["court"])
    result["name"] = list(result["name"])

    return result, infinite

def singleNLP(file):
    with open(file, "r", encoding="utf-8") as f:
        data = f.read().encode("utf-8")
        return textNLP(data)


def multiNLP(file_path='./DataCase/'):
    txt_num = 0
    final_result = {}
    # 文件列表
    txt_files = []
    txt_path = './DataCase/'
    for txt_file in os.listdir(file_path):
        if txt_file.endswith(".txt"):
            txt_files.append(os.path.join(txt_path, txt_file))
    duration_list = []
    # 针对每个文件进行nlp，产出json文件，每个txt返回一个字典
    for txt_file in txt_files:
        sing_result = singleNLP(txt_file)
        result_file_path = "./CaseNote/" + txt_file[11:-4] + ".json"
        with open(result_file_path, "w+", encoding="UTF-8") as js:
            json.dump(sing_result, js, ensure_ascii=False)

        if txt_file.endswith("刑罚与执行变更审查刑事裁定书.txt") or txt_file.endswith("刑罚与执行变更刑事裁定书.txt") or txt_file.endswith("减刑假释刑事裁定书.txt"):
            sing_result = singleNLP(txt_file)
            final_result[os.path.splitext(os.path.basename(txt_file))[0]] = sing_result
            if not sing_result[1]:
                print(txt_file)
                txt_num += 1
                init = Duration.penalty_to_duration(sing_result[0]["time"][-1])
                actual_penalty_poss1 = Duration.calculate_duration(sing_result[0]["time"][0], sing_result[0]["time"][-3])
                # 最后一项是有立文书的时间
                actual_penalty_poss2 = Duration.calculate_duration(sing_result[0]["time"][1], sing_result[0]["time"][-3])
                # 第一项是有执行刑期的时间
                actual_penalty_poss3 = Duration.calculate_duration(sing_result[0]["time"][0], sing_result[0]["time"][-2])
                # 无最后一项立文书时
                try:
                    actual_penalty_poss4 = Duration.calculate_duration(sing_result[0]["time"][-4], sing_result[0]["time"][-3])
                    actual_penalty = max(actual_penalty_poss1, actual_penalty_poss2, actual_penalty_poss3,
                                         actual_penalty_poss4)
                except IndexError:
                    actual_penalty = max(actual_penalty_poss1, actual_penalty_poss2, actual_penalty_poss3)
                except ValueError:
                    actual_penalty = max(actual_penalty_poss1, actual_penalty_poss2, actual_penalty_poss3)
                if init > actual_penalty > 0.5 * init:
                    if init <= 60:
                        feature = 0
                    if 60 < init <= 120:
                        feature = 1
                    if init > 120:
                        feature = 2
                    duration_list.append([actual_penalty, init, float(format(actual_penalty/init, '.2f')), feature])
    print(duration_list)
    return duration_list


if __name__ == "__main__":
    # txt_path是txt的路径，可以是相对路径也可以是绝对路径
    txt_path = './DataCase/'
    multiNLP(txt_path)

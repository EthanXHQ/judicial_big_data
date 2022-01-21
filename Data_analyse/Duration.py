import NLP


def calculate_duration(begin_data, end_data):
    begin = [int(begin_data.split("年")[0]), int(begin_data.split("年")[1].split("月")[0]),
             int(begin_data.split("年")[1].split("月")[1].split("日")[0])]  # 将日期进行切割，分别得到年月日
    end = [int(end_data.split("年")[0]), int(end_data.split("年")[1].split("月")[0]),
           int(end_data.split("年")[1].split("月")[1].split("日")[0])]
    duration = (365 * (end[0] - begin[0]) + 30 * (end[1] - begin[1]) + 1 * (end[2] - begin[2])) // 30
    return duration


def penalty_to_duration(penalty_list):
    sum = 0
    for penalty in penalty_list:
        if len(penalty.split("年")) == 1:
            year = 0
        else:
            year = penalty.split("年")[0]
        if len(penalty.split("年")) == 1:
            month = penalty.split("年")[0].split("个月")[0]
        else:
            if len(penalty.split("年")[1]) == 0:
                month = 0
            else:
                month = penalty.split("年")[1].split("个月")[0]
        num_list_ten = ["零", '', "二", "三", "四", "五", "六", "七", "八", "九"]
        num_list_single = ["", '一', "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
        try:
            year = int(year)
        except ValueError:
            if year.find("十") != -1:
                year = num_list_ten.index(year.split("十")[0]) * 10 + num_list_single.index(year.split("十")[1])
            else:
                year = num_list_single.index(year)
        try:
            month = int(month)
        except ValueError:
            if month.find("零") != -1:
                month = month.split("零")[1]
            if month.find("又") != -1:
                month = month.split("又")[1]
            month = num_list_single.index(month)
        total = year * 12 + month
        sum += total
    return sum


if __name__ == '__main__':
    pass
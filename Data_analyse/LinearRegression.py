import matplotlib.pyplot as plt
import numpy
import math


def liner_regression_process(x_list, y_list):
    x_average = calculate_average(x_list)
    y_average = calculate_average(y_list)
    b = calculate_l_xy(x_list, y_list) / calculate_l_xx(x_list)
    a = y_average - b * x_average
    return a, b


def index_regression_process(x_list, y_list):
    y_index_list = []
    for i in y_list:
        y_index_list.append(numpy.log(i) / numpy.log(e))
    ln_a, b = liner_regression_process(x_list, y_index_list)
    return numpy.exp(ln_a), b


def log_regression_process(x_list, y_list):
    x_log_list = []
    for i in x_list:
        x_log_list.append(numpy.log(i) / numpy.log(e))
    a, b = liner_regression_process(x_log_list, y_list)
    return a, b


def calculate_average(num_list):
    average = 0
    for i in range(0, len(num_list)):
        average += num_list[i] / len(num_list)
    return average


def calculate_l_xx(x_list):
    x_average = calculate_average(x_list)
    l_xx = 0
    for i in range(0, len(x_list)):
        l_xx += (x_list[i] - x_average) * (x_list[i] - x_average)
    return l_xx


def calculate_l_xy(x_list, y_list):
    x_average = calculate_average(x_list)
    y_average = calculate_average(y_list)
    l_xy = 0
    for i in range(0, len(x_list)):
        l_xy += (x_list[i] - x_average) * (y_list[i] - y_average)
    return l_xy


def show_liner_regression_line(point_list):
    x_list = getX_list(point_list)
    y_list = getY_list(point_list)
    a, b = liner_regression_process(x_list, y_list)
    x = numpy.linspace(min(x_list),  max(x_list), 50)
    y = a + b * x
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(12, 6), dpi=100)
    plt.scatter(x_list, y_list)
    plt.plot(x, y)
    plt.title("线性回归模型拟合")
    plt.xlabel("初始判定刑期")
    plt.ylabel("实际刑期")
    plt.show()


def show_index_regression_line(point_list):
    x_list = getX_list(point_list)
    y_list = getY_list(point_list)
    a, b = index_regression_process(x_list, y_list)
    x = numpy.linspace(min(x_list),  max(x_list), 50)
    y = a * numpy.exp(b * x)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(12, 6), dpi=100)
    plt.scatter(x_list, y_list)
    plt.plot(x, y)
    plt.title("指数回归模型拟合")
    plt.xlabel("初始判定刑期")
    plt.ylabel("实际刑期")
    plt.show()


def show_log_regression_line(point_list):
    x_list = getX_list(point_list)
    y_list = getY_list(point_list)
    a, b = log_regression_process(x_list, y_list)
    x = numpy.linspace(min(x_list),  max(x_list), 1000)
    y = a + b * numpy.log(x) / numpy.log(e)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(12, 6), dpi=100)
    plt.scatter(x_list, y_list)
    plt.plot(x, y)
    plt.title("对数回归模型拟合")
    plt.xlabel("初始判定刑期")
    plt.ylabel("实际刑期")
    plt.show()


def calculate_pearson(x_list, y_list):
    molecular = calculate_Cov(x_list, y_list)  # 分子
    denominator = math.sqrt(calculate_Var(x_list)) * math.sqrt(calculate_Var(y_list))  # 分母
    return molecular / denominator


def calculate_Cov(x_list, y_list):
    # 协方差计算
    ex = calculate_average(x_list)
    ey = calculate_average(y_list)
    xy_list = []
    for i in range(0, len(x_list)):
        xy_list.append(x_list[i] * y_list[i])
    exy = calculate_average(xy_list)
    return exy - ex * ey


def calculate_Var(num_list):
    # 方差计算
    num_average = calculate_average(num_list)
    summary = 0
    for i in range(0, len(num_list)):
        summary += (num_list[i] - num_average) * (num_list[i] - num_average)
    return summary / len(num_list)


def getX_list(data):
    x_list = []
    for i in data:
        x_list.append(i[0])
    return x_list


def getY_list(data):
    y_list = []
    for i in data:
        y_list.append(i[1])
    return y_list


def calculate_deciding_coefficient_liner(point_list):
    x_list = getX_list(point_list)
    y_list = getY_list(point_list)
    a, b = liner_regression_process(x_list, y_list)
    y_regression_list = []
    for i in range(0, len(x_list)):
        y_regression_list.append(a + b * x_list[i])
    y_average = calculate_average(y_list)
    SR = 0
    ST = 0
    Sy = 0
    for i in range(0, len(x_list)):
        SR += math.pow(y_regression_list[i] - y_average, 2)
        ST += math.pow(y_list[i] - y_average, 2)
        Sy += math.pow(y_regression_list[i] - y_list[i], 2)
    return SR / ST, math.sqrt(Sy / (len(x_list) - 2))


def calculate_deciding_coefficient_index(point_list):
    x_list = getX_list(point_list)
    y_list = getY_list(point_list)
    a, b = index_regression_process(x_list, y_list)
    y_regression_list = []
    for i in range(0, len(x_list)):
        y_regression_list.append(a * numpy.exp(b * x_list[i]))
    y_average = calculate_average(y_list)
    SR = 0
    ST = 0
    Se = 0
    for i in range(0, len(x_list)):
        SR += math.pow(y_regression_list[i] - y_average, 2)
        ST += math.pow(y_list[i] - y_average, 2)
        Se += math.pow(y_regression_list[i] - y_list[i], 2)
    return 1 - Se / ST, math.sqrt(Se / (len(x_list) - 2))


def calculate_deciding_coefficient_log(point_list):
    x_list = getX_list(point_list)
    y_list = getY_list(point_list)
    a, b = log_regression_process(x_list, y_list)
    y_regression_list = []
    for i in range(0, len(x_list)):
        y_regression_list.append(a + b * numpy.log(x_list[i]) / numpy.log(e))
    y_average = calculate_average(y_list)
    SR = 0
    ST = 0
    Se = 0
    for i in range(0, len(x_list)):
        SR += math.pow(y_regression_list[i] - y_average, 2)
        ST += math.pow(y_list[i] - y_average, 2)
        Se += math.pow(y_regression_list[i] - y_list[i], 2)
    return 1 - Se / ST, math.sqrt(Se / (len(x_list) - 2))


if __name__ == '__main__':
    data = [[136, 180, 0.76, 2], [151, 180, 0.84, 2], [54, 56, 0.96, 0], [154, 180, 0.86, 2], [168, 180, 0.93, 2],
            [144, 168, 0.86, 2], [121, 126, 0.96, 2], [154, 180, 0.86, 2], [156, 162, 0.96, 2], [171, 180, 0.95, 2],
            [161, 180, 0.89, 2], [177, 183, 0.97, 2], [176, 180, 0.98, 2], [175, 180, 0.97, 2], [175, 180, 0.97, 2],
            [167, 180, 0.93, 2], [175, 180, 0.97, 2], [115, 122, 0.94, 2], [143, 180, 0.79, 2], [174, 180, 0.97, 2],
            [127, 132, 0.96, 2], [166, 180, 0.92, 2], [168, 174, 0.97, 2], [166, 180, 0.92, 2], [85, 90, 0.94, 1],
            [168, 180, 0.93, 2], [44, 48, 0.92, 0], [159, 168, 0.95, 2], [168, 180, 0.93, 2], [172, 180, 0.96, 2],
            [163, 180, 0.91, 2], [174, 180, 0.97, 2], [97, 102, 0.95, 1], [149, 156, 0.96, 2], [65, 66, 0.98, 1],
            [141, 180, 0.78, 2], [177, 180, 0.98, 2], [177, 180, 0.98, 2], [93, 108, 0.86, 1], [147, 180, 0.82, 2],
            [172, 180, 0.96, 2], [75, 90, 0.83, 1], [171, 180, 0.95, 2], [171, 180, 0.95, 2], [75, 84, 0.89, 1],
            [167, 180, 0.93, 2], [163, 168, 0.97, 2], [163, 180, 0.91, 2], [99, 102, 0.97, 1], [167, 180, 0.93, 2],
            [83, 90, 0.92, 1], [166, 180, 0.92, 2], [142, 180, 0.79, 2], [165, 180, 0.92, 2], [64, 72, 0.89, 1],
            [76, 84, 0.9, 1], [144, 181, 0.8, 2], [139, 156, 0.89, 2], [146, 162, 0.9, 2], [155, 180, 0.86, 2],
            [123, 126, 0.98, 2], [163, 180, 0.91, 2], [35, 36, 0.97, 0], [30, 36, 0.83, 0], [159, 180, 0.88, 2],
            [175, 180, 0.97, 2], [166, 180, 0.92, 2], [165, 180, 0.92, 2], [122, 150, 0.81, 2], [155, 180, 0.86, 2],
            [144, 162, 0.89, 2], [148, 180, 0.82, 2], [83, 90, 0.92, 1], [155, 180, 0.86, 2], [155, 180, 0.86, 2],
            [137, 144, 0.95, 2], [148, 180, 0.82, 2], [175, 180, 0.97, 2], [153, 180, 0.85, 2], [40, 48, 0.83, 0],
            [152, 192, 0.79, 2], [135, 180, 0.75, 2], [167, 180, 0.93, 2], [148, 180, 0.82, 2], [43, 48, 0.9, 0],
            [114, 120, 0.95, 1], [174, 180, 0.97, 2], [115, 126, 0.91, 2], [133, 150, 0.89, 2], [107, 129, 0.83, 2],
            [153, 180, 0.85, 2], [171, 180, 0.95, 2], [129, 132, 0.98, 2], [169, 180, 0.94, 2], [168, 180, 0.93, 2],
            [132, 180, 0.73, 2], [39, 42, 0.93, 0], [104, 108, 0.96, 1], [127, 132, 0.96, 2], [89, 96, 0.93, 1],
            [44, 49, 0.9, 0], [103, 108, 0.95, 1], [32, 36, 0.89, 0], [177, 180, 0.98, 2], [140, 180, 0.78, 2],
            [58, 63, 0.92, 1], [75, 96, 0.78, 1], [40, 45, 0.89, 0], [80, 84, 0.95, 1], [159, 180, 0.88, 2],
            [87, 96, 0.91, 1], [97, 116, 0.84, 1], [123, 132, 0.93, 2], [164, 180, 0.91, 2], [32, 34, 0.94, 0],
            [176, 180, 0.98, 2], [28, 36, 0.78, 0], [174, 180, 0.97, 2], [66, 84, 0.79, 1], [125, 132, 0.95, 2],
            [84, 90, 0.93, 1], [175, 180, 0.97, 2], [113, 120, 0.94, 1], [147, 150, 0.98, 2], [112, 120, 0.93, 1],
            [175, 180, 0.97, 2], [152, 157, 0.97, 2], [95, 102, 0.93, 1], [84, 102, 0.82, 1], [113, 120, 0.94, 1],
            [77, 84, 0.92, 1], [150, 168, 0.89, 2], [111, 114, 0.97, 1], [104, 118, 0.88, 1], [167, 180, 0.93, 2],
            [90, 96, 0.94, 1], [137, 144, 0.95, 2], [163, 180, 0.91, 2], [53, 84, 0.63, 1], [96, 132, 0.73, 2],
            [141, 148, 0.95, 2], [57, 84, 0.68, 1], [62, 90, 0.69, 1], [167, 180, 0.93, 2], [110, 126, 0.87, 2],
            [141, 168, 0.84, 2], [92, 108, 0.85, 1], [108, 132, 0.82, 2], [150, 156, 0.96, 2], [145, 168, 0.86, 2],
            [160, 180, 0.89, 2], [84, 101, 0.83, 1], [75, 84, 0.89, 1], [80, 88, 0.91, 1], [168, 180, 0.93, 2],
            [94, 120, 0.78, 1], [167, 180, 0.93, 2], [170, 180, 0.94, 2], [150, 156, 0.96, 2], [115, 120, 0.96, 1],
            [150, 162, 0.93, 2], [173, 180, 0.96, 2], [35, 42, 0.83, 0], [154, 180, 0.86, 2], [137, 180, 0.76, 2],
            [138, 180, 0.77, 2], [148, 155, 0.95, 2], [82, 90, 0.91, 1], [78, 96, 0.81, 1], [133, 180, 0.74, 2],
            [167, 180, 0.93, 2], [121, 144, 0.84, 2], [159, 180, 0.88, 2], [86, 102, 0.84, 1], [137, 180, 0.76, 2],
            [140, 180, 0.78, 2], [95, 102, 0.93, 1], [125, 132, 0.95, 2], [174, 180, 0.97, 2], [31, 36, 0.86, 0],
            [175, 180, 0.97, 2], [82, 90, 0.91, 1], [78, 96, 0.81, 1], [133, 180, 0.74, 2], [167, 180, 0.93, 2],
            [121, 144, 0.84, 2], [159, 180, 0.88, 2], [86, 102, 0.84, 1], [137, 180, 0.76, 2], [140, 180, 0.78, 2],
            [95, 102, 0.93, 1], [125, 132, 0.95, 2], [174, 180, 0.97, 2], [176, 180, 0.98, 2], [175, 180, 0.97, 2],
            [78, 101, 0.77, 1], [167, 204, 0.82, 2], [93, 98, 0.95, 1], [174, 180, 0.97, 2], [125, 137, 0.91, 2],
            [127, 143, 0.89, 2], [155, 180, 0.86, 2], [174, 180, 0.97, 2], [144, 168, 0.86, 2], [175, 180, 0.97, 2],
            [47, 48, 0.98, 0], [114, 137, 0.83, 2], [165, 180, 0.92, 2], [167, 180, 0.93, 2], [66, 84, 0.79, 1],
            [139, 180, 0.77, 2], [118, 132, 0.89, 2], [136, 180, 0.76, 2], [129, 144, 0.9, 2], [135, 180, 0.75, 2],
            [90, 102, 0.88, 1], [124, 180, 0.69, 2], [165, 180, 0.92, 2], [84, 108, 0.78, 1], [35, 36, 0.97, 0],
            [69, 84, 0.82, 1], [156, 161, 0.97, 2], [97, 132, 0.73, 2], [166, 180, 0.92, 2], [142, 180, 0.79, 2],
            [174, 180, 0.97, 2], [174, 180, 0.97, 2], [33, 39, 0.85, 0], [70, 92, 0.76, 1],
            [112, 126, 0.89, 2], [165, 180, 0.92, 2], [134, 168, 0.8, 2], [175, 180, 0.97, 2], [60, 66, 0.91, 1],
            [35, 40, 0.88, 0], [81, 88, 0.92, 1], [64, 72, 0.89, 1], [64, 72, 0.89, 1], [129, 156, 0.83, 2],
            [153, 180, 0.85, 2], [126, 162, 0.78, 2], [36, 48, 0.75, 0], [112, 120, 0.93, 1], [144, 180, 0.8, 2],
            [144, 180, 0.8, 2], [24, 37, 0.65, 0], [71, 108, 0.66, 1], [27, 41, 0.66, 0], [80, 93, 0.86, 1],
            [122, 144, 0.85, 2], [165, 180, 0.92, 2], [119, 144, 0.83, 2], [163, 180, 0.91, 2], [85, 120, 0.71, 1],
            [33, 48, 0.69, 0], [43, 48, 0.9, 0], [170, 180, 0.94, 2], [80, 93, 0.86, 1], [52, 60, 0.87, 0],
            [40, 50, 0.8, 0], [106, 144, 0.74, 2], [127, 180, 0.71, 2], [111, 132, 0.84, 2], [142, 156, 0.91, 2],
            [116, 156, 0.74, 2], [100, 144, 0.69, 2], [26, 44, 0.59, 0], [112, 156, 0.72, 2], [27, 36, 0.75, 0],
            [73, 108, 0.68, 1], [85, 96, 0.89, 1], [142, 180, 0.79, 2], [25, 42, 0.6, 0], [122, 138, 0.88, 2],
            [170, 180, 0.94, 2], [92, 120, 0.77, 1], [162, 180, 0.9, 2], [92, 108, 0.85, 1], [144, 168, 0.86, 2],
            [137, 180, 0.76, 2], [164, 180, 0.91, 2], [115, 144, 0.8, 2], [161, 180, 0.89, 2], [148, 180, 0.82, 2],
            [107, 144, 0.74, 2], [162, 180, 0.9, 2], [144, 180, 0.8, 2], [138, 156, 0.88, 2], [162, 180, 0.9, 2],
            [82, 96, 0.85, 1], [85, 96, 0.89, 1], [161, 180, 0.89, 2], [151, 161, 0.94, 2], [102, 120, 0.85, 1],
            [74, 96, 0.77, 1], [153, 180, 0.85, 2], [41, 48, 0.85, 0], [65, 84, 0.77, 1], [149, 180, 0.83, 2],
            [158, 180, 0.88, 2], [58, 72, 0.81, 1], [164, 180, 0.91, 2], [72, 84, 0.86, 1], [75, 97, 0.77, 1],
            [92, 108, 0.85, 1], [159, 180, 0.88, 2], [49, 66, 0.74, 1], [32, 42, 0.76, 0], [102, 108, 0.94, 1],
            [123, 156, 0.79, 2], [30, 36, 0.83, 0], [70, 87, 0.8, 1], [147, 180, 0.82, 2], [83, 108, 0.77, 1],
            [144, 156, 0.92, 2], [96, 102, 0.94, 1], [39, 48, 0.81, 0], [101, 108, 0.94, 1], [39, 44, 0.89, 0],
            [115, 132, 0.87, 2], [25, 37, 0.68, 0], [43, 48, 0.9, 0], [42, 45, 0.93, 0], [84, 102, 0.82, 1],
            [83, 96, 0.86, 1], [92, 108, 0.85, 1], [92, 108, 0.85, 1], [97, 117, 0.83, 1], [171, 180, 0.95, 2],
            [101, 120, 0.84, 1], [135, 180, 0.75, 2], [151, 180, 0.84, 2], [138, 156, 0.88, 2], [171, 180, 0.95, 2],
            [101, 120, 0.84, 1], [146, 180, 0.81, 2], [135, 180, 0.75, 2], [151, 180, 0.84, 2], [89, 99, 0.9, 1],
            [138, 156, 0.88, 2], [112, 132, 0.85, 2], [99, 120, 0.82, 1], [130, 138, 0.94, 2], [158, 180, 0.88, 2],
            [147, 180, 0.82, 2], [175, 180, 0.97, 2], [161, 180, 0.89, 2], [105, 120, 0.88, 1], [164, 180, 0.91, 2],
            [74, 84, 0.88, 1], [150, 156, 0.96, 2], [168, 180, 0.93, 2], [168, 180, 0.93, 2], [116, 126, 0.92, 2],
            [52, 60, 0.87, 0], [114, 144, 0.79, 2], [30, 36, 0.83, 0], [156, 180, 0.87, 2], [141, 180, 0.78, 2],
            [164, 180, 0.91, 2], [103, 120, 0.86, 1], [114, 120, 0.95, 1], [148, 180, 0.82, 2], [176, 180, 0.98, 2],
            [129, 168, 0.77, 2], [36, 48, 0.75, 0], [167, 180, 0.93, 2], [160, 180, 0.89, 2], [134, 156, 0.86, 2],
            [75, 84, 0.89, 1], [132, 144, 0.92, 2], [175, 180, 0.97, 2], [92, 168, 0.55, 2], [64, 90, 0.71, 1],
            [165, 180, 0.92, 2], [101, 132, 0.77, 2], [159, 180, 0.88, 2], [212, 216, 0.98, 2], [174, 180, 0.97, 2],
            [168, 180, 0.93, 2], [170, 180, 0.94, 2], [89, 108, 0.82, 1], [176, 180, 0.98, 2], [163, 168, 0.97, 2],
            [89, 96, 0.93, 1], [127, 144, 0.88, 2], [127, 156, 0.81, 2], [67, 96, 0.7, 1], [22, 28, 0.79, 0],
            [75, 84, 0.89, 1], [186, 192, 0.97, 2], [65, 90, 0.72, 1], [71, 84, 0.85, 1], [167, 180, 0.93, 2],
            [77, 90, 0.86, 1], [149, 180, 0.83, 2], [156, 183, 0.85, 2], [53, 57, 0.93, 0], [94, 110, 0.85, 1],
            [85, 96, 0.89, 1], [49, 54, 0.91, 0], [142, 180, 0.79, 2], [33, 39, 0.85, 0], [108, 126, 0.86, 2],
            [170, 180, 0.94, 2], [92, 108, 0.85, 1], [162, 180, 0.9, 2], [138, 180, 0.77, 2], [151, 156, 0.97, 2],
            [166, 180, 0.92, 2], [96, 102, 0.94, 1], [160, 180, 0.89, 2], [45, 51, 0.88, 0], [134, 156, 0.86, 2],
            [85, 102, 0.83, 1], [155, 180, 0.86, 2], [157, 162, 0.97, 2], [133, 161, 0.83, 2], [156, 168, 0.93, 2],
            [75, 94, 0.8, 1], [82, 96, 0.85, 1], [164, 180, 0.91, 2], [73, 84, 0.87, 1], [145, 168, 0.86, 2],
            [176, 180, 0.98, 2], [114, 120, 0.95, 1], [183, 186, 0.98, 2], [146, 180, 0.81, 2], [70, 84, 0.83, 1],
            [149, 162, 0.92, 2], [96, 108, 0.89, 1], [161, 180, 0.89, 2], [143, 156, 0.92, 2], [83, 90, 0.92, 1],
            [150, 156, 0.96, 2], [167, 180, 0.93, 2], [166, 180, 0.92, 2], [156, 180, 0.87, 2], [141, 180, 0.78, 2],
            [73, 90, 0.81, 1], [169, 180, 0.94, 2], [157, 180, 0.87, 2], [72, 84, 0.86, 1], [162, 180, 0.9, 2],
            [124, 132, 0.94, 2], [157, 180, 0.87, 2], [141, 168, 0.84, 2]]
    e = numpy.exp(1)
    # 建立初始数据集，x为初始判定量，y为实际执行量
    data_list = []
    index_list = []
    log_list = []
    for item in data:
        data_list.append([item[1], item[0]])
        index_list.append([item[1], numpy.log(item[0]) / numpy.log(e)])
        log_list.append([numpy.log(item[1]) / numpy.log(e), item[0]])
    print(calculate_pearson(getX_list(data_list), getY_list(data_list)))
    print(calculate_deciding_coefficient_liner(data_list))
    print(calculate_deciding_coefficient_index(data_list))
    print(calculate_deciding_coefficient_log(data_list))
    show_liner_regression_line(data_list)
    show_index_regression_line(data_list)
    show_log_regression_line(data_list)

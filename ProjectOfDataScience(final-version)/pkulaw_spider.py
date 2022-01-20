import time
import requests
from bs4 import BeautifulSoup
import os
# 本地Chrome浏览器设置方法
from selenium import webdriver  # 从selenium库中调用webdriver模块
from selenium.webdriver.chrome.options import Options  # 从options模块中调用Options类


def makeDirectory(dir_name):
    # 指导性案例——GuidingCase
    # 公报案例——PublicCase
    # 典型案例——TypicalCase
    # 参阅案例——ReferentialCase
    # 经典案例——ClassicCase
    # 评析案例——AnalyticalCase
    # 刑事案件——CriminalCase
    # 民事案件——CivilCase
    # 知识产权案件——IntellectualPropertyRightCase
    # 行政案件——AdministrativeCase
    # 国家赔偿案件——StateCompensationCase
    # 贩毒案——DrugCase
    if not (os.path.exists(dir_name)):
        cd = os.getcwd()
        os.mkdir(cd + '\\' + dir_name)


def spiderThroughHrefList(href_list, dir_name):
    headers = {
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/45.0.2454.101 Safari/537.36",
        "Host": "www.pkulaw.cn",
        "Cookie": "Hm_lvt_58c470ff9657d300e66c7f33590e53a8=1641902191,1641949988; "
                  "Hm_lpvt_58c470ff9657d300e66c7f33590e53a8=1641968302; Encoding=true; "
                  "ASP.NET_SessionId=wtl1pclj2v2v1nmablf1khej; CookieId=wtl1pclj2v2v1nmablf1khej; CheckIPAuto=0",
        # Cookie是写死的
        "Upgrade-Insecure-Requests": "1",
        "Proxy-Connection": "keep-alive"
    }

    case_num = 0  # 将MTitle为空的article命名为：'检例第caseNum号'
    for item in href_list:
        href = item['href']
        article_res = requests.get('https://www.pkulaw.cn' + href, headers=headers)
        article_bs = BeautifulSoup(article_res.text, 'html.parser')

        m_title = article_bs.find('font', class_='MTitle')

        # 处理MTitle格式
        if m_title:
            m_title_str = m_title.text
            m_title_str = m_title_str.replace("/", "")
            m_title_str = m_title_str.split('——')[0]
            m_title_str = m_title_str.split('\n')[0]
            m_title_str = m_title_str.strip()
            m_title_str = m_title_str.replace("/", "")
        else:
            m_title_str = '检例第' + str(case_num + 100 + 1) + '号'

        case_num = case_num + 1
        # 保存到本地 GuidingCase文件夹中
        article_text = article_bs.find('div', class_='articleText')
        file = open(dir_name + '/No.' + str(case_num) + '_' + m_title_str + '.txt', 'w',
                    encoding='utf-8')  # MTitleStr为文件名
        file.write(article_text.text)
        file.close()


# 指导性案例——GuidingCase
def guidingCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@more_code="01" and @href="javascript:void(0);"]')  # 第一次点击[更多] 需修改
    button_more.click()
    time.sleep(2)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'GuidingCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 公报案例——PublicCase
def publicCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@more_code="02" and @href="javascript:void(0);"]')  # 第一次点击[更多] 需修改
    button_more.click()
    time.sleep(2)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'PublicCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 典型案例——TypicalCase
def typicalCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@more_code="03" and @href="javascript:void(0);"]')  # 第一次点击[更多] 需修改
    button_more.click()
    time.sleep(2)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'TypicalCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 参阅案例——ReferentialCase
def referentialCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@more_code="04" and @href="javascript:void(0);"]')  # 第一次点击[更多] 需修改
    button_more.click()
    time.sleep(2)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'ReferentialCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 经典案例——ClassicCase
def classicCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@more_code="05" and @href="javascript:void(0);"]')  # 第一次点击[更多] 需修改
    button_more.click()
    time.sleep(2)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'ClassicCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 评析案例——AnalyticalCase
def analyticalCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@more_code="09" and @href="javascript:void(0);"]')  # 第一次点击[更多] 需修改
    button_more.click()
    time.sleep(2)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'AnalyticalCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 刑事案件——CriminalCase
def criminalCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@href="javascript:void(0);" and @cluster_code="001"]')  # 第一次点击[刑事]
    button_more.click()
    time.sleep(3)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'CriminalCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 民事案件——CivilCase
def civilCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@href="javascript:void(0);" and @cluster_code="002"]')  # 第一次点击[民事]
    button_more.click()
    time.sleep(3)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'CivilCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 知识产权案件——IntellectualPropertyRightCase
def intellectualPropertyRightCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@href="javascript:void(0);" and @cluster_code="003"]')  # 首次点击[知识产权]
    button_more.click()
    time.sleep(3)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'IntellectualPropertyRightCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 行政案件——AdministrativeCase
def administrativeCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@href="javascript:void(0);" and @cluster_code="005"]')  # 第一次点击[行政]
    button_more.click()
    time.sleep(3)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'AdministrativeCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 国家赔偿案件——StateCompensationCase
def stateCompensationCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome(options=chrome_options)  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    button_more = driver.find_element_by_xpath('//a[@href="javascript:void(0);" and @cluster_code="007"]')  # 首次点击[国家赔偿]
    button_more.click()
    time.sleep(3)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 4:  # 目前写死为100份，可以修改为用户输入
        button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
        # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
        button_page_next.click()
        time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'StateCompensationCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


# 贩毒案——DrugCase
def drugCaseSpider():
    chrome_options = Options()  # 实例化Option对象
    chrome_options.add_argument('--headless')  # 把Chrome浏览器设置为静默模式
    driver = webdriver.Chrome()  # 设置引擎为Chrome，在后台默默运行 options=chrome_options

    driver.get('https://www.pkulaw.cn/case/')
    time.sleep(3)
    # 点击[刑事]
    button_more = driver.find_element_by_xpath('//a[@href="javascript:void(0);" and @cluster_code="001"]')
    button_more.click()
    time.sleep(3)
    # 点击[妨害社会管理秩序罪]
    button_blemish = driver.find_element_by_xpath('//a[@href="javascript:void(0);" and @cluster_code="00106"]')
    button_blemish.click()
    time.sleep(3)
    # 点击[走私、贩卖、运输、制造毒品罪]
    button_drug_sell = driver.find_element_by_xpath('//a[@href="javascript:void(0);" and @cluster_code="0010607"]')
    button_drug_sell.click()
    time.sleep(3)
    # 点击[走私、贩卖、运输、制造毒品罪]
    button_drug_sell_sub = driver.find_element_by_xpath(
        '//a[@href="javascript:void(0);" and @cluster_code="001060701"]')
    button_drug_sell_sub.click()
    time.sleep(3)
    page_source = driver.page_source

    home_page_bs = BeautifulSoup(page_source, 'html.parser')
    href_list = home_page_bs.find_all(class_='title')  # 单个页面的所有href

    i = 0
    while i < 49:  # 一千份案例
        try:
            button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
            # button_page_next = driver.find_element_by_id('btnPageNext') 同样可行
            button_page_next.click()
            time.sleep(3)
        except Exception:
            time.sleep(9)  # 需在9秒内准确完成"拖动滑块解锁"
            button_page_next = driver.find_element_by_xpath('//input[@id="btnPageNext"]')  # 第二次点击[下一页]
            button_page_next.click()
            time.sleep(3)
        page_source = driver.page_source
        case_page_bs = BeautifulSoup(page_source, 'html.parser')
        case_page_href_list = case_page_bs.find_all(class_='title')  # 单个页面的所有href
        href_list += case_page_href_list
        i += 1

    dir_name = 'DrugCase'  # 需修改

    makeDirectory(dir_name)
    spiderThroughHrefList(href_list, dir_name)

    driver.close()


def spider(case_choice):  # 传入案件类型
    if case_choice == 'guidingCase':
        guidingCaseSpider()
    elif case_choice == 'typicalCase':
        typicalCaseSpider()
    elif case_choice == 'publicCase':
        publicCaseSpider()
    elif case_choice == 'referentialCase':
        referentialCaseSpider()
    elif case_choice == 'classicCase':
        classicCaseSpider()
    elif case_choice == 'analyticalCase':
        analyticalCaseSpider()
    elif case_choice == 'criminalCase':
        criminalCaseSpider()
    elif case_choice == 'civilCase':
        civilCaseSpider()
    elif case_choice == 'intellectualPropertyRightCase':
        intellectualPropertyRightCaseSpider()
    elif case_choice == 'administrativeCase':
        administrativeCaseSpider()
    elif case_choice == 'stateCompensationCase':
        stateCompensationCaseSpider()
    elif case_choice == 'drugCase':  # 对[走私、贩卖、运输、制造毒品罪]的一千份案例爬取
        drugCaseSpider()


if __name__ == '__main__':
    case = input("请输入案件类型：")
    spider(case)  # 传入案件类型

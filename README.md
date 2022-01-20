## README

This is the final version of our projrct of Fundamental of Data Science.

------

### 项目开始

#### 解决的问题：

构建自动化裁判文书爬取与标注分析应用。其主要功能模块包括：

1. **爬虫模块：**

   利用自动化爬虫工具从文书网获取指定案件类型的大量裁判文书，作为数据源。

2. **自动化标注模块：**

   对传入的裁判文书，通过自然语言处理，提取涉案人员、案件相关法院、地区、民族等案件文本信息。

3. **可视化分析模块：**

   提供用户界面，用户可自主选择案件类型，自动爬取案例；手动标注，并查看和筛选自动标注信息，并自动保存标注。

#### 解决思路：

1. **爬虫模块：**

   1. 使用selenium自动化浏览案件目录，获取100份案件的超链接目标的URL。
   2. 使用requests模拟浏览器请求头，请求每一份案件的URL，获取100份案件的超文本标记语言。
   3. 使用BeautifulSoup处理requests取得的超文本标记语言，提取案件文本。
   4. 将案件文本以.txt格式保存到本地。

2. **自动化标注模块：**

   1. 使用jieba分词，处理文本，除去噪声，返回过滤后的文本。
   2. 使用jieba.posseg处理文本，获得词频、词性。
   3. 根据词频、词性，并利用裁判文书的文书特性通过正则表达式提取文本要素（涉案人员、案件相关法院、地区、民族）。
   4. 将文本要素返回用户界面。

3. **可视化分析模块：**
1. 使用PyQt5进行用户界面的构建

------

### 项目构建

#### 爬虫模块：**`pkulaw_spider.py`**

运行后会在相同目录下生成新的文件夹，保存对应100份案件于该文件夹中。

**函数说明：**

1. 使用selenium自动化浏览案件目录，存入参数href_list。

   ```python
   def guidingCaseSpider():	# 以指导性案例为例，其他类型案件的爬取函数同理
   ```

2. 在相同目录下新建文件夹，存放某一类型案件。

   ```python
   def makeDirectory(dir_name):
   ```

3. 使用requests和BeautifulSoup获取案件并保存到本地。

   ```python
   def spiderThroughHrefList(href_list, dir_name):
   ```

4. 爬虫调用接口，传入参数为想爬取的案件类型。

   ```python
   def spider(case_choice):
   ```

5. **特殊说明：**

   函数drugCaseSpider为爬取1000份涉毒案件，供数据分析使用。

   ```python
   def drugCaseSpider():
   ```

#### 自动化标注模块：**`light_nlp.py`**

**函数说明：**

1. 通过jieba分词，对传入文本处理，返回涉案人员、案件相关法院、地区、民族。

   ```python
   def articleNLP(article):  # 传入参数为字符串类型
   ```

#### 可视化分析模块：**`MyQtGUI.py`** **`QNote.py`** **`QUtills.py`**

**类说明：**

`MyQtGUI`类、`QNote`类、`QUtills`类，分别包含在`MyQtGUI.py`文件、`QNote.py`文件、`QUtills.py`文件下。

使用PyQt5进行用户界面的构建，运行后会在相同目录下生成新的文件夹file_save以保存txt文本文件和json注释文件。

1、MyQtGUI

~~~python
class MainMenu(QLabel):		# 项目主体菜单页面，继承自QLabel类
	class ManualMenu(QFrame):	# 子控件手动标注页面，继承自QFrame类
    
    class AutoMenu(QFrame):		# 子控件自动标注页面，继承自QFrame类
    
    class CrawlerMenu(QFrame):		# 子控件爬取案例页面，继承自QFrame类
~~~

2、QNote

~~~~python
class QNoteArea(QFrame):  # 标注区域，涉及到标注的增删改查，由该类完成
    class QNote(QFrame):	# 手动输入标注类，标签和内容均由用户输入
    
    class QCheckNote(QFrame):	# 自动生成标注类，通过NLP对文本进行处理，得出可供用户选择的内容
~~~~

3、QUtills

~~~~python
class MenuButton(QFrame):	# 主菜单按钮类，包括按钮实体与图像
   
class CrawlerDialog(QDialog):	# 爬虫案例类型选择窗口

class CrawlerThread(QThread):	# 爬虫子线程类，由于爬虫时间较长且受网速等多因素影响，由子线程完成
~~~~

------

### 项目测试：

1. **爬虫模块：**

   写有供手工测试用的main函数。

   测试方法：

   1. 可在控制台手动输入案件类型，运行即可开始自动爬虫。

2. **自动化标注模块：**

   写有供手工测试用的main函数。

   测试方法：

   1. 在文件相同目录下添加带有文书的文件夹。
   2. 手工修改main函数中文件夹路径。
   3. 运行即可打印测试结果。

3. **可视化分析模块：**

   写有main函数。

   测试方法：

   1. 执行main函数会实例化一个MainMenu。
   2. 在MainMenu可以测试所有的控件操作。

------

### 环境配置：

1. **爬虫模块：**

   1. requests库，安装方法：在Windows系统cmd中 `pip install requests`
   2. BeautifulSoup库，安装方法：在Windows系统cmd中 `pip install BeautifulSoup4`
   3. selenium库，安装方法：在Windows系统cmd中 `pip install selenium`
   4. Chrome浏览器，推荐安装**版本 97.0.4692.71**（目前最新版本）
   5. ChromeDriver驱动器，下载链接：http://npm.taobao.org/mirrors/chromedriver/，请务必安装所使用的Chrome浏览器**对应版本**的ChromeDriver驱动器。驱动器下载后得到.exe文件，请将文件放入python的安装根目录所在的目录。
   6. 需要登录南京大学IP，以获得文书网的使用权。

2. **自动化标注模块：**

   1. jieba库，安装方法：在Windows系统cmd中 `pip install jieba`
   2. 需要使用jieba分词paddle模式下的分词和词性标注功能，下载方法：在Windows系统cmd中 `pip install paddlepaddle-tiny==1.6.1`

3. **可视化分析模块：**

   1. PyQt5库，安装方法：在Windows系统cmd中 `pip install PyQt5`，

      如安装过慢可通过镜像网站，在Windows系统cmd中 `pip install PyQt5 -i https://pypi.tuna.tsinghua.edu.cn/simple`


------

### 相关功能思考：

1. **爬虫模块：**
   - 在爬取的案例数量达到400份后，文书网会弹出“拖动滑块来解锁”，反爬虫。目前的解决方法是，在遇到“拖动滑块来解锁”的情况时，web工具会将控制权交换用户，用户解锁后，web工具自动收回控制权。可通过图像识别方法，进行缺口识别，升级为自动拖动滑块，增强爬虫的自动化能力。
   - 通过与法学专业的同学交流，了解到通过关键词搜索的用户对文书精准度的要求远大于对文书数量的要求，因此删减了通过关键词搜索爬取的功能。
2. **自动化标注模块：**
   - 裁判文书属于特殊类型的文本，会出现较多未登录词，可根据法律文书特殊性，加入基于法学词成词能力的马尔科夫模型。
   - 可加入法律词汇词典实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图 (DAG)
3. **可视化分析模块：**
   - 可添加登录界面，为用户设立账户，记住使用习惯等用户信息。
   - 面对大量信息，通过开辟云储存空间为用户保存数据。

------

### 项目引用：

1. **爬虫模块：**

   爬虫的调用接口，传入参数为想爬取的案件类型。

   ```python
   def spider(case_choice):
   ```

   爬取的各类型案例与对应传入参数（均为字符串类型）：

   ```python
   # 指导性案例——guidingCase
   # 公报案例——publicCase
   # 典型案例——typicalCase
   # 参阅案例——referentialCase
   # 经典案例——classicCase
   # 评析案例——analyticalCase
   # 刑事案件——criminalCase
   # 民事案件——civilCase
   # 知识产权案件——intellectualPropertyRightCase
   # 行政案件——administrativeCase
   # 国家赔偿案件——stateCompensationCase
   ```

2. **自动化标注模块：**

   NLP的调用接口：

   **传入参数：**需要分析的案件文本（字符串类型）。

   ```python
   def articleNLP(article):  # 传入参数为字符串类型
   ```

   **传出参数：**各个要素均为集合，所有集合合为一个列表，从左至右的顺序如下。

   ```python
   [{'涉案人员'}{'案件相关法院'}{'地区'}{'民族'}]
   ```

3. **可视化分析模块：**

   是应用的**入口**，执行main函数会实例化一个MainMenu，生成用户界面，在界面中可进行控件操作。

   

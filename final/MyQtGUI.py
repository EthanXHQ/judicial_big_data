import os.path
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
import QUtils
import QNote
import json
import light_nlp


class MainMenu(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setGeometry(100, 200, 800, 538)
        self.backgroundImage = QtGui.QPixmap("./img/bg_img.jpg")  # MainMenu的背景图片设置
        self.backgroundLabel = QLabel(parent=self)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setPixmap(self.backgroundImage)
        self.manualFrame = QUtils.MenuButton(parent=self, image="./img/manual.png", text="手动标注",  # 手动标注页面切换按钮的设置
                                             func=self.show_manual_menu)
        self.manualFrame.setGeometry(550, 170, 150, 50)
        self.manualFrame.set_image(50, 50)
        self.automaticFrame = QUtils.MenuButton(parent=self, image="./img/auto.png", text="自动标注",  # 自动标注页面切换按钮的设置
                                                func=self.show_automatic_menu)
        self.automaticFrame.setGeometry(550, 230, 150, 50)
        self.automaticFrame.set_image(43, 43)
        self.crawlerFrame = QUtils.MenuButton(parent=self, image="./img/crawler.png", text="爬取案例",
                                              func=self.show_crawler_menu)  # 爬虫页面切换按钮的设置，这边爬虫image的大小是不同于前面的
        self.crawlerFrame.setGeometry(540, 280, 170, 58)
        self.crawlerFrame.set_image(58, 58)
        self.crawlerFrame.set_button(60, 15)
        self.manualMenu = ManualMenu(parent=self)  # 先设置背景图片置于底层，否则会将所有的Menu遮挡
        self.automaticMenu = AutomaticMenu(parent=self)
        self.crawlerMenu = CrawlerMenu(parent=self)
        self.return_main_menu()
        """
        # 不同于tkinter，PyQt5的控件自动显示，控件位置要用move移动，默认是在(0, 0)
        # self.height() self.width()
        # setVisible来处理各个页面之间的交互  # PyQt5关联Button函数用connect"""

    def show_main_menu(self):
        self.manualFrame.setVisible(True)
        self.automaticFrame.setVisible(True)
        self.crawlerFrame.setVisible(True)

    def show_manual_menu(self):
        self.clear_main_menu()
        self.manualMenu.setVisible(True)

    def show_automatic_menu(self):
        self.clear_main_menu()
        self.automaticMenu.setVisible(True)

    def show_crawler_menu(self):
        self.clear_main_menu()
        self.crawlerMenu.setVisible(True)

    """
    关于由主菜单页面跳转至三个分支页面时，主页面需要清除的控件
    1.三个按钮的button
    2.三个按钮的icon
    """
    def clear_main_menu(self):
        self.manualMenu.setVisible(False)
        self.automaticMenu.setVisible(False)
        self.crawlerMenu.setVisible(False)
        self.manualFrame.setVisible(False)
        self.automaticFrame.setVisible(False)
        self.crawlerFrame.setVisible(False)

    def return_main_menu(self):
        self.clear_main_menu()
        self.show_main_menu()

    def get_manual_menu(self):
        return self.manualMenu


class ManualMenu(QFrame):
    # ManualMenu控件的初始化
    # 框架中ManualMenu是位于MainMenu之上的，而非跟MainMenu同级的，Auto与Crawler同
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setGeometry(0, 0, self.parent.width(), self.parent.height())
        self.title = QLabel(parent=self, text="手动标注", font=QUtils.TitleFont)
        self.text = QPlainTextEdit(parent=self)
        self.noteArea = QNote.QNoteArea(parent=self)
        # 五个按钮，包括返回，文件浏览，清空文本域，
        self.exitButton = QPushButton(parent=self, text="返回初始页面")
        self.fileBrowser = QPushButton(parent=self, text="导入本地文件")
        self.textClearButton = QPushButton(parent=self, text="清除文本内容")
        self.addNoteButton = QPushButton(parent=self, text="添加案例标注")
        self.saveFileButton = QPushButton(parent=self, text="保存案例与标注")
        # 五个按钮函数的连接
        self.exitButton.clicked.connect(self.return_main_menu)
        self.fileBrowser.clicked.connect(self.file_read)
        self.textClearButton.clicked.connect(self.text_clear)
        self.addNoteButton.clicked.connect(self.add_note)
        self.saveFileButton.clicked.connect(self.save_file)

        self.show_menu()

    # ManualMenu的布局
    def show_menu(self):
        self.title.move((self.parent.width()-self.title.width()-50)//2, 10)
        self.text.setGeometry(50, 50, self.parent.width() - 100, self.height() - 300)
        gap = (self.text.width() - 4 * self.exitButton.width() - self.saveFileButton.width() - 10)//4
        self.exitButton.move(50, 300)
        self.fileBrowser.move(self.exitButton.x() + self.exitButton.width() + gap, 300)
        self.textClearButton.move(self.fileBrowser.x() + self.fileBrowser.width() + gap, 300)
        self.addNoteButton.move(self.textClearButton.x() + self.textClearButton.width() + gap, 300)
        self.saveFileButton.move(self.addNoteButton.x() + self.addNoteButton.width() + gap, 300)

    # 返回按钮的函数执行
    @staticmethod
    def return_main_menu():
        mainMenu.return_main_menu()  # 调用的父菜单的的方法

    # 导入本地文件按钮的函数执行
    def file_read(self):
        path, file_mode = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files(*)")  # 第二个参数是文件选择对话框的Title，
        print(path)
        print(file_mode)
        if path != "":
            with open(path, "r", encoding="UTF-8") as f:  # file_read读取文件内容为中文时需修改encoding格式为UTF-8
                file_content = f.read()
                self.text.setPlainText(file_content)

    # 清空文本区域按钮的函数执行
    def text_clear(self):
        self.text.setPlainText("")

    # 添加标注按钮的函数执行
    def add_note(self):
        text, pressed = QInputDialog.getText(self, "司法大数据", "请输入标注的实体(最长为4个字)")
        if text != "" and pressed:
            self.noteArea.add_input_note(text=text[0:4])

    # 保存文件按钮的函数执行
    def save_file(self):
        if not os.path.exists("./file_save"):
            os.makedirs("./file_save")
        file_path = "./file_save/" + "file_content.txt"
        with open(file_path, 'w+', encoding="UTF-8") as f:
            f.write(self.text.toPlainText())
        dictionary = self.noteArea.notes_to_dict()
        json_file_path = "./file_save/" + "file_note.json"
        with open(json_file_path, "w+", encoding="UTF-8") as js_file:
            print(dictionary)
            json.dump(dictionary, js_file, ensure_ascii=False)
        QMessageBox.information(self, "Title", "成功保存至" + os.path.abspath("./MyQtGUI.py")[0:-10] + "file_save",
                                QMessageBox.Yes)


class AutomaticMenu(QFrame):
    # AutoMenu控件的初始化
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setGeometry(0, 0, self.parent.width(), self.parent.height())
        self.title = QLabel(parent=self, text="自动标注", font=QUtils.TitleFont)
        self.text = QPlainTextEdit(parent=self)
        self.noteArea = QNote.QNoteArea(parent=self)
        # 六个按钮，包括返回，文件浏览，清空文本域，自动进行分词
        self.exitButton = QPushButton(parent=self, text="返回初始页面")
        self.fileBrowser = QPushButton(parent=self, text="导入本地文件")
        self.textClearButton = QPushButton(parent=self, text="清除文本内容")
        self.addNoteButton = QPushButton(parent=self, text="添加案例标注")
        self.autoLanguageProcess = QPushButton(parent=self, text="智能标注分析")
        self.saveFileButton = QPushButton(parent=self, text="保存案例与标注")

        # 六个按钮函数的连接
        self.exitButton.clicked.connect(self.return_main_menu)
        self.fileBrowser.clicked.connect(self.file_read)
        self.textClearButton.clicked.connect(self.text_clear)
        self.addNoteButton.clicked.connect(self.add_note)
        self.autoLanguageProcess.clicked.connect(self.auto_text_process)
        self.saveFileButton.clicked.connect(self.save_file)

        self.show_menu()

    # AutoMenu的布局
    def show_menu(self):
        self.title.move((self.parent.width() - self.title.width() - 50) // 2, 10)
        self.text.setGeometry(50, 50, self.parent.width() - 100, self.height() - 300)
        gap = (self.text.width() - 5 * self.exitButton.width() - self.saveFileButton.width() - 10) // 5
        self.exitButton.move(50, 300)
        self.fileBrowser.move(self.exitButton.x() + self.exitButton.width() + gap, 300)
        self.textClearButton.move(self.fileBrowser.x() + self.fileBrowser.width() + gap, 300)
        self.addNoteButton.move(self.textClearButton.x() + self.textClearButton.width() + gap, 300)
        self.autoLanguageProcess.move(self.addNoteButton.x() + self.addNoteButton.width() + gap, 300)
        self.saveFileButton.move(self.autoLanguageProcess.x() + self.autoLanguageProcess.width() + gap, 300)

    # 返回按钮的函数执行
    @staticmethod
    def return_main_menu():
        mainMenu.return_main_menu()  # 调用的父菜单的的方法

    # 导入本地文件按钮的函数执行
    def file_read(self):
        path, file_mode = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files(*)")  # 第二个参数是文件选择对话框的Title，
        if path != "":
            with open(path, "r", encoding="UTF-8") as f:  # file_read读取文件内容为中文时需修改encoding格式为UTF-8
                file_content = f.read()
                self.text.setPlainText(file_content)

    # 清空文本区域按钮的函数执行
    def text_clear(self):
        self.text.setPlainText("")

    # 添加标注按钮的函数执行
    def add_note(self):
        text, pressed = QInputDialog.getText(self, "司法大数据", "请输入标注的实体(最长为4个字)")
        if text != "" and pressed:
            self.noteArea.add_input_note(text=text[0:4])

    # 智能标注分析按钮的函数执行
    def auto_text_process(self):
        self.noteArea.add_check_note(value_list=light_nlp.articleNLP(self.text.toPlainText()))

    # 保存文件按钮的函数执行
    def save_file(self):
        if not os.path.exists("./file_save"):
            os.makedirs("./file_save")
        file_path = "./file_save/" + "file_content.txt"
        with open(file_path, 'w+', encoding="UTF-8") as f:
            f.write(self.text.toPlainText())
        dictionary = self.noteArea.notes_to_dict()
        json_file_path = "./file_save/" + "file_note.json"
        with open(json_file_path, "w+", encoding="UTF-8") as js_file:
            json.dump(dictionary, js_file)
        QMessageBox.information(self, "Title", "成功保存至" + os.path.abspath("./MyQtGUI.py")[0:-10] + "file_save",
                                QMessageBox.Yes)


class CrawlerMenu(QFrame):
    # CrawlerMenu控件的初始化
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setGeometry(0, 0, self.parent.width(), self.parent.height())
        self.title = QLabel(parent=self, text="爬取案例", font=QUtils.TitleFont)
        self.text = QPlainTextEdit(parent=self)
        self.noteArea = QNote.QNoteArea(parent=self)

        # 六个按钮，包括返回，文件浏览，清空文本域，自动进行分词(相比AutoMenu去除了手动添加note，同时添加了爬虫按钮)
        self.exitButton = QPushButton(parent=self, text="返回初始页面")
        self.fileBrowser = QPushButton(parent=self, text="导入本地文件")
        self.textClearButton = QPushButton(parent=self, text="清除文本内容")
        self.autoLanguageProcess = QPushButton(parent=self, text="智能标注分析")
        self.crawlerButton = QPushButton(parent=self, text="爬取相关数据")
        self.saveFileButton = QPushButton(parent=self, text="保存案例与标注")

        # 六个按钮函数的连接
        self.exitButton.clicked.connect(self.return_main_menu)
        self.fileBrowser.clicked.connect(self.file_read)
        self.textClearButton.clicked.connect(self.text_clear)
        self.autoLanguageProcess.clicked.connect(self.auto_text_process)
        self.saveFileButton.clicked.connect(self.save_file)
        self.crawlerButton.clicked.connect(self.crawl_web)

        self.show_menu()

    # CrawlerMenu的布局
    def show_menu(self):
        self.title.move((self.parent.width() - self.title.width() - 50) // 2, 10)
        self.text.setGeometry(50, 50, self.parent.width() - 100, self.height() - 300)
        gap = (self.text.width() - 5 * self.exitButton.width() - self.saveFileButton.width() - 10) // 5
        self.exitButton.move(50, 300)
        self.fileBrowser.move(self.exitButton.x() + self.exitButton.width() + gap, 300)
        self.textClearButton.move(self.fileBrowser.x() + self.fileBrowser.width() + gap, 300)
        self.autoLanguageProcess.move(self.textClearButton.x() + self.textClearButton.width() + gap, 300)
        self.crawlerButton.move(self.autoLanguageProcess.x() + self.autoLanguageProcess.width() + gap, 300)
        self.saveFileButton.move(self.crawlerButton.x() + self.crawlerButton.width() + gap, 300)

    # 返回按钮的函数执行
    @staticmethod
    def return_main_menu():
        mainMenu.return_main_menu()  # 调用的父菜单的的方法

    # 导入本地文件按钮的函数执行
    def file_read(self):
        path, file_mode = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files(*)")  # 第二个参数是文件选择对话框的Title，
        if path != "":
            with open(path, "r", encoding="UTF-8") as f:  # file_read读取文件内容为中文时需修改encoding格式为UTF-8
                file_content = f.read()
                self.text.setPlainText(file_content)

    # 清空文本区域按钮的函数执行
    def text_clear(self):
        self.text.setPlainText("")

    # 智能标注分析按钮的函数执行
    def auto_text_process(self):
        self.noteArea.add_check_note(value_list=light_nlp.articleNLP(self.text.toPlainText()))

    # 爬虫功能的函数执行
    def crawl_web(self):
        dialog = QUtils.CrawlerDialog(parent=self)
        dialog.exec()
        print(dialog.get_cause_choice())

    # 保存文件按钮的函数执行
    def save_file(self):
        if not os.path.exists("./file_save"):
            os.makedirs("./file_save")
        file_path = "./file_save/" + "file_content.txt"
        with open(file_path, 'w+', encoding="UTF-8") as f:
            f.write(self.text.toPlainText())
        dictionary = self.noteArea.notes_to_dict()
        json_file_path = "./file_save/" + "file_note.json"
        with open(json_file_path, "w+", encoding="UTF-8") as js_file:
            json.dump(dictionary, js_file)
        QMessageBox.information(self, "Title", "成功保存至" + os.path.abspath("./MyQtGUI.py")[0:-10] + "file_save",
                                QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = MainMenu()
    mainMenu.setWindowIcon(QIcon('icon.ico'))
    mainMenu.setWindowTitle("司法大数据")
    mainMenu.setFixedSize(800, 538)
    mainMenu.show()  # 无父控件需要自己手动show()才会显示
    sys.exit(app.exec())

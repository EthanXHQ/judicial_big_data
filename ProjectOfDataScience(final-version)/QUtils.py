from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import Qt
import pkulaw_spider


class MenuButton(QFrame):

    # 初始化，应该含有MenuButton应有的组件，包括image和Button
    def __init__(self, parent=None, image=None, text=None, func=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.label = QLabel(parent=self)
        self.image = QtGui.QPixmap(image)
        self.button = QPushButton(parent=self, text=text)
        self.button.clicked.connect(func)
        self.label.setPixmap(self.image)
        self.button.move(50, 5)
        self.label.setGeometry(0, 0, 50, 50)

    def set_image(self, x, y):
        self.label.setGeometry(0, 0, x, y)
        self.label.setScaledContents(True)

    def set_button(self, x, y):
        self.button.move(x, y)


class CrawlerDialog(QDialog):
    # 爬取数据类型选择窗口类
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.cause = ["指导性案例", "公报案例", "典型案例", "参阅案例", "经典案例",
                      "评析案例", "刑事案件", "民事案件", "知识产权案件",
                      "行政案件", "国家赔偿案件"]
        self.crawl_parameter = ["guidingCase", "publicCase", "typicalCase", "referentialCase", "classicCase",
                                "analyticalCase", "criminalCase", "civilCase", "intellectualPropertyRightCase",
                                "administrativeCase", "stateCompensationCase"]
        # self.reference_level = ["指导性案例", "公报案例", "典型案例", "参阅案例", "评析案例", "经典案例", "更多"]
        # 原计划为修改提供三个不同的label
        #  self.trial_court = ["最高人民法院", "北京市"]
        self.cause_combo_box = QComboBox(parent=self)
        self.cause_combo_box.addItems(self.cause)
        self.setWindowTitle("爬虫类型选择")
        self.setWindowModality(Qt.Qt.ApplicationModal)
        self.titleLabel = QLabel(parent=self, font=TitleFont)
        self.titleLabel.setText("案例类型")
        self.loading = QLabel(parent=self)
        self.loading_gif = Qt.QMovie('./img./loading.gif')
        self.loading.setMovie(self.loading_gif)
        self.loading_gif.start()
        self.crawl_begin = QPushButton(parent=self, text="开始爬取100份文书")
        self.crawl_begin.clicked.connect(self.show_loading)
        self.loading.setVisible(False)
        self.crawl_is_running = True
        self.self_layout()

    def get_cause_choice(self):
        return self.crawl_parameter[self.cause_combo_box.currentIndex()]

    def self_layout(self):
        self.setGeometry(800, 500, 400, 180)
        self.cause_combo_box.move(60, 70)
        self.crawl_begin.move(210, 68)
        self.titleLabel.move(135, 20)
        self.loading.move(130, 50)

    def show_loading(self):
        self.hide_all_widgets_except_crawl()
        self.titleLabel.setText("Loading")
        self.crawl_is_running = True
        self.loading.setVisible(True)
        self.thread = CrawlerThread(cause=self.get_cause_choice())
        self.thread.finishSignal.connect(self.stop)
        self.thread.start()
        # self.close()

    def hide_all_widgets_except_crawl(self):
        self.crawl_begin.setVisible(False)
        self.cause_combo_box.setVisible(False)
        self.crawl_begin.setVisible(False)

    def stop(self, spider_is_finished=False):
        if spider_is_finished:
            QMessageBox.information(self, "Title", "已成功爬取100份文书", QMessageBox.Yes)
            self.close()


class CrawlerThread(Qt.QThread):
    finishSignal = Qt.pyqtSignal(bool)

    def __init__(self, parent=None, cause=None):
        super().__init__(parent=parent)
        self.cause = cause

    def run(self):
        pkulaw_spider.spider(self.cause)
        self.finishSignal.emit(True)


TitleFont = QtGui.QFont("楷体", 20)

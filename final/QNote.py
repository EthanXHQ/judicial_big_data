from PyQt5.QtWidgets import *
from PyQt5 import Qt


class QNoteArea(QFrame):
    """
    将整个的Note区域合并为一个大类，然后所有的相关的操作全部由该类来实现，减少与整体Menu的相互
    """
    # Note类，用于手动标注，与自动标注的生成
    # 母组件的text域width为700，组件长为800
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setGeometry(50, 350, parent.width() + 7, 250)  # 整体的的NoteArea域需要进行修改，大小应该为Menu页面left的部分
        self.noteArea = QScrollArea(parent=self)
        self.w = QWidget()
        self.w.setMinimumSize(700, 150)
        self.lay = QVBoxLayout(self.w)
        self.noteArea.setWidget(self.w)
        self.noteArea.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAsNeeded)
        self.noteArea.setLayout(QVBoxLayout())
        self.noteArea.resize(700 + 23, 152)  # 实测scrollBar的width为23
        # self.noteArea.setStyleSheet("QScrollArea {background-color:transparent;}")
        self.viewport = self.noteArea.viewport()
        self.height = 0
        self.index = 0  # index代表现有note，也代表下一个即将产生的note的下标
        self.noteList = []
        self.isDeleted = []

    def add_input_note(self, text=None):
        if self.height + 50 > self.w.height():
            self.w.resize(self.w.width(), self.w.height() + 50)  # 如果新的注释要添加进来，然后w空间不够需要进行扩展空间
        note = self.QNote(parent=self.w, text=text, y=self.height, index=self.index, note_area=self)
        self.height += 50
        self.index += 1
        self.noteList.append(note)
        self.isDeleted.append(0)

    def add_check_note(self, value_list=[set(), set(), set(), set()]):
        laebl_List = ["涉案人员", '相关法院', '地区', "民族"]
        for i in range(0, len(value_list)):
            if value_list[i] != set():
                if self.height + 50 > self.w.height():
                    self.w.resize(self.w.width(), self.w.height() + 50)  # 如果新的注释要添加进来，然后w空间不够需要进行扩展空间
                note = self.QCheckNote(parent=self.w, label_text=laebl_List[i], check_list=value_list[i], y=self.height,
                                       index=self.index, note_area=self)
                self.height += 50
                self.index += 1
                self.noteList.append(note)
                self.isDeleted.append(0)

    def delete_note(self, index):
        self.isDeleted[index] = 1
        self.height = self.height - 50
        for i in range(index, len(self.noteList)):
            if self.isDeleted[i] == 0:
                QNoteArea.QNote.move_up(self.noteList[i])

    def area_resize_after_delete(self):
        if self.w.height() > self.height:
            self.w.resize(self.w.width(), self.w.height() - 50)

    def notes_to_dict(self):
        dictionary = {}
        for i in range(0, len(self.noteList)):
            if self.isDeleted[i] == 0:
                if isinstance(self.noteList[i], QNoteArea.QNote):
                    dictionary[self.noteList[i].get_label_str()] = self.noteList[i].get_text_str()
                else:
                    dictionary[self.noteList[i].get_label_str()] = self.noteList[i].get_check_result()
        return dictionary

    """
    QNoteArea的子类
    """
    class QNote(QFrame):
        def __init__(self, parent=None, text=None, y=None, index=None, note_area=None):
            super().__init__(parent=parent)
            self.height = y
            self.setGeometry(0, y, 700, 50)
            self.noteArea = note_area
            self.label = QLabel(parent=self, text=text)
            self.label.setAlignment(Qt.Qt.AlignCenter)
            self.textInput = QLineEdit(parent=self)
            self.deleteButton = QPushButton(parent=self, text="删除")
            self.deleteButton.clicked.connect(self.delete)
            self.index = index
            self.show_note()

        def show_note(self):
            self.label.setGeometry(5, 8, 60, 30)
            self.textInput.setGeometry(80, 8, 520, 30)
            self.deleteButton.setGeometry(620, self.label.y(), 60, 30)
            self.setVisible(True)

        def delete(self):
            self.resize(0, 0)
            self.noteArea.delete_note(self.index)
            self.noteArea.area_resize_after_delete()

        def move_up(self):
            self.move(0, self.height - 50)
            self.height = self.height - 50

        def get_label_str(self):
            return self.label.text()

        def get_text_str(self):
            return self.textInput.text()

    class QCheckNote(QFrame):
        def __init__(self, parent=None, label_text=None, check_list=[], y=None, index=None, note_area=None):
            super().__init__(parent=parent)
            self.height = y
            self.setGeometry(0, y, 700, 50)
            self.noteArea = note_area
            self.label = QLabel(parent=self, text=label_text)
            self.label.setAlignment(Qt.Qt.AlignCenter)
            # self.textInput = QLineEdit(parent=self)
            self.deleteButton = QPushButton(parent=self, text="删除")
            self.deleteButton.clicked.connect(self.delete)
            self.index = index
            self.checkBoxList = []
            self.checkBoxAreaX = 80
            self.show_note()
            self.add_check_note(check_list)

        def add_check_note(self, check_list=()):
            for i in check_list:
                check_box = QCheckBox(parent=self, text=i)
                self.checkBoxList.append(check_box)
                check_box.move(self.checkBoxAreaX, self.label.y() + 7)
                if self.checkBoxAreaX + check_box.width() < 600:
                    check_box.setVisible(True)
                self.checkBoxAreaX += check_box.width()

        def show_note(self):
            self.label.setGeometry(5, 8, 60, 30)
            # self.textInput.setGeometry(80, 0, 520, 30)
            self.deleteButton.setGeometry(620, self.label.y(), 60, 30)
            self.setVisible(True)

        def delete(self):
            self.resize(0, 0)
            self.noteArea.delete_note(self.index)
            self.noteArea.area_resize_after_delete()

        def move_up(self):
            self.move(0, self.height - 50)
            self.height = self.height - 50

        def get_label_str(self):
            return self.label.text()

        def get_check_result(self):
            result = []
            for i in self.checkBoxList:
                if i.isChecked():
                    result.append(i.text())
                else:
                    continue
            return result

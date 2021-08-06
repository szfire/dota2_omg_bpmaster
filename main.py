import sys
from PyQt5 import QtWidgets, QtCore
from bpmaster_ui import *
from get_rank import *


class Buttons(object):

    def __init__(self):
        pass


def turn_red(str1):
    return '<span style=\" color: #ff502f;\">%s</span>' % str1


def turn_blue(str1):
    return '<span style=\" color: #ffb549;\">%s</span>' % str1


def turn_white(str1):
    return '<span style=\" color: #ffffff;\">%s</span>' % str1


def click_get_rank():
    rank_table = GetRank().get_rank_table()  # 获取技能排名表
    # rank_table:[name_cn, rank, location[num], num, ability_id, rank_current]
    for item in rank_table:
        name_cn = item[0]
        rank = item[1]
        num = item[3]
        ability_id = item[4]
        img_path = "./ability_pic/{}.jpg".format(ability_id)
        rank_current = item[5]
        if rank_current <= 5:  # 更改输出颜色
            func = turn_red
        elif rank_current <= 12:
            func = turn_blue
        else:
            func = turn_white
        name_cn = func(str(name_cn))
        rank = func('排名:' + str(rank))
        rank_current = func(str(rank_current))

        exec("ui.ability_{}.setText(name_cn)".format(num+1))
        exec("ui.rank_{}.setText(rank)".format(num+1))
        exec("ui.rank_current_{}.setText(rank_current)".format(num+1))
        exec("ui.pic_{}.setIcon(QtGui.QIcon(img_path))".format(num+1))
        exec("ui.pic_{}.setIconSize(QtCore.QSize(41, 41))".format(num + 1))
    ui.textBrowser.setText('成功！  感谢为少技术支持！')


def click_reset():
    ui.textBrowser.setText('reset没用是暂时的  喝冻是神是永恒的')


def click_check():
    ui.textBrowser.setText('为少是不可缺少的  check是可以替代的')


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()  # Ui_MainWindow是类名
    ui.setupUi(MainWindow)

    MainWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # 设置窗口置顶
    # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
    MainWindow.setWindowOpacity(0.8)  # 窗口透明度
    MainWindow.setStyleSheet("#MainWindow{background:#000000}")  # 设置背景颜色
    # MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 背景透明(黑)
    MainWindow.setWindowTitle("dota2 omg bp master beta1.2 打工人szz叹气")

    MainWindow.show()

    # 关联动作与函数
    ui.resetButton.clicked.connect(click_reset)
    ui.get_rank_button.clicked.connect(click_get_rank)
    ui.checkButton.clicked.connect(click_check)

    sys.exit(app.exec_())

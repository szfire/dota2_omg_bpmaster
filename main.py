import sys
from PyQt5 import QtWidgets, QtCore
from bpmaster_ui import *
from get_rank import *
from functools import partial


def turn_red(str1):
    return '<span style=\" color: #ff0000;\">%s</span>' % str1


def click_get_rank():
    rank_table = GetRank().get_rank_table()
    # rank_table:[name_cn, rank, location[num], num, ability_id, rank_current]
    for item in rank_table:
        name_cn = item[0]
        rank = item[1]
        rank_current = item[5]
        num = item[3]
        if rank_current <= 10:
            name_cn = turn_red(str(name_cn))
            rank = turn_red('排名:' + str(rank))
            rank_current = turn_red(str(rank_current))
        else:
            name_cn = str(name_cn)
            rank = '排名:' + str(rank)
            rank_current = str(rank_current)
        exec("ui.ability_{}.append(name_cn)".format(num+1))
        exec("ui.ability_{}.append(rank)".format(num+1))
        exec("ui.ability_{}.append(rank_current)".format(num+1))
    ui.textBrowser.setText('成功！  感谢为少技术支持！')


def click_clear():
    for i in range(48):
        exec("ui.ability_{}.clear()".format(i+1))
    ui.textBrowser.setText('清空成功！  感谢为少技术支持！')


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()  # Ui_MainWindow是类名
    ui.setupUi(MainWindow)

    MainWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # 设置窗口置顶
    MainWindow.setWindowOpacity(0.8)  # 窗口透明度
    MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 背景透明
    MainWindow.setWindowTitle("dota2 omg bp master beta1.1 致谢喝冻")

    MainWindow.show()

    ui.clearButton.clicked.connect(click_clear)
    ui.get_rank_button.clicked.connect(click_get_rank)

    sys.exit(app.exec_())

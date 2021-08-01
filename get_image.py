import win32con
import win32gui
import win32ui
import win32print
import numpy as np
import cv2


class GetImg(object):

    def __init__(self):
        self.win_title = 'Dota 2'  # 窗口标题
        self.win_class = 'SDL_app'  # 窗口类
        self.dpi = 1  # 初始化缩放大小参数
        self.refresh_dpi()  # 获得当前系统缩放比例
        self.screen = None
        self.rst1 = None
        self.rst2 = None

    def get_rst1(self):
        """获取小技能图区"""
        if self.rst1 is None:
            print("请先运行get_screen()和get_ability_area1()")
        return self.rst1

    def get_rst2(self):
        """获取大招图区"""
        if self.rst2 is None:
            print("请先运行get_screen()和get_ability_area2()")
        return self.rst2

    def refresh_dpi(self):
        """获得当前系统缩放比例"""
        hdc = win32gui.GetDC(0)
        dpi1 = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES) / win32print.GetDeviceCaps(hdc, win32con.HORZRES)
        dpi2 = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 0.96 / 100
        if dpi1 == 1:
            self.dpi = dpi2
        elif dpi2 == 1:
            self.dpi = dpi1
        elif dpi1 == dpi2:
            self.dpi = dpi1
        else:
            self.dpi = -1
            print("请调整系统缩放比例！")
            exit(1)

    def get_dpi(self):
        return self.dpi

    def get_screen(self):
        hwnd = win32gui.FindWindow(self.win_class, self.win_title)  # 获取窗口句柄
        left, top, right, bot = win32gui.GetWindowRect(hwnd)  # 获取句柄窗口的大小信息

        # right = int(right * self.dpi)
        # bot = int(bot * self.dpi)
        width = right - left
        height = bot - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)  # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)  # 创建设备描述表
        save_dc = mfc_dc.CreateCompatibleDC()  # 创建内存设备描述表
        bit_map = win32ui.CreateBitmap()  # 创建位图对象准备保存图片
        bit_map.CreateCompatibleBitmap(mfc_dc, width, height)  # 为bitmap开辟存储空间
        save_dc.SelectObject(bit_map)  # 将截图保存到bit_map中
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)  # 保存bit_map到内存设备描述表

        signed_ints_array = bit_map.GetBitmapBits(True)
        img = np.fromstring(signed_ints_array, dtype='uint8')
        img.shape = (height, width, 4)
        cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        img = img[:, :, :-1]
        img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LINEAR)  # 原图归一化
        self.screen = img
        cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

        win32gui.DeleteObject(bit_map.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        return 0

    def save_img(self, path="./cache/screen.jpg", img=None):
        if img is None:
            img = self.screen
        cv2.imwrite(path, img)  # 保存
        return 0

    def show_img(self, img=None):
        if img is None:
            img = self.screen
        cv2.namedWindow('img', cv2.WINDOW_NORMAL)  # 命名窗口
        cv2.imshow("img", img)  # 显示
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_ability_area1(self):
        img = self.screen
        pa = np.array([[722, 341], [1197, 341], [669, 835], [1250, 835]], dtype="float32")  # 小技能框
        pb = np.array([[0, 0], [500, 0], [0, 500], [500, 500]], dtype="float32")  # 参考矩形
        mat = cv2.getPerspectiveTransform(pa, pb)  # 小技能区域变换矩阵
        self.rst1 = cv2.warpPerspective(img, mat, (500, 500))  # 校正后小技能框

    def get_ability_area2(self):
        img = self.screen
        pa = np.array([[672, 142], [1247, 142], [686, 339], [1233, 339]], dtype="float32")  # 大招框
        pb = np.array([[0, 0], [575, 0], [0, 200], [575, 200]], dtype="float32")  # 参考矩形
        mat = cv2.getPerspectiveTransform(pa, pb)  # 大招区域变换矩阵
        self.rst2 = cv2.warpPerspective(img, mat, (575, 200))  # 校正后大招框

        # pa = np.array([[675, 377], [1244, 377], [613, 930], [1305, 930]], dtype="float32")  # 小技能框
        # pa = np.array([[618, 156], [1302, 156], [634, 377], [1286, 377]], dtype="float32")  # 大招框
        # img = cv2.resize(img, (1920, 1200), interpolation=cv2.INTER_LINEAR)  # 原图归一化

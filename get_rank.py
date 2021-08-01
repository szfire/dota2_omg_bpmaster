from get_image import *
import os
import json
import pandas as pd


class GetRank(object):

    def __init__(self):
        x = 80
        self.img_shape = (x, x)

    def get_rank_table(self, save_img=False, save_sta=False):
        """rank_table : [name_cn, rank, location[num], num, ability_id]"""
        gi = GetImg()  # 初始化截图工具
        gi.get_screen()  # 截图全屏
        gi.get_ability_area1()  # 截图小技能区域
        gi.get_ability_area2()  # 截图大招区域
        rst1 = gi.get_rst1()  # 获取小技能区域
        rst2 = gi.get_rst2()  # 获取大招区域

        if save_img:  # 保存截图到缓存文件夹
            print(gi.get_dpi())
            print(gi.screen.shape)
            gi.save_img()
            gi.save_img("./cache/ability_area1.jpg", rst1)
            gi.save_img("./cache/ability_area2.jpg", rst2)

        # 每个技能的坐标 先小技能后大招 注释为其行列
        a1 = rst1[5:56, 10:63]  # 11
        a2 = rst1[5:56, 91:143]  # 12
        a3 = rst1[5:56, 171:223]  # 13
        a4 = rst1[5:56, 278:330]  # 14
        a5 = rst1[5:56, 358:410]  # 15
        a6 = rst1[5:56, 440:492]  # 16

        a7 = rst1[82:134, 10:63]  # 21
        a8 = rst1[82:134, 91:143]  # 22
        a9 = rst1[82:134, 171:223]  # 23
        a10 = rst1[82:134, 278:330]  # 24
        a11 = rst1[82:134, 358:410]  # 25
        a12 = rst1[82:134, 440:492]  # 26

        a13 = rst1[161:211, 10:63]  # 31
        a14 = rst1[161:211, 91:143]  # 32
        a15 = rst1[161:211, 171:223]  # 33
        a16 = rst1[161:211, 278:330]  # 34
        a17 = rst1[161:211, 358:410]  # 35
        a18 = rst1[161:211, 440:492]  # 36

        a19 = rst1[281:331, 12:64]  # 41
        a20 = rst1[281:331, 92:144]  # 42
        a21 = rst1[281:331, 172:224]  # 43
        a22 = rst1[281:331, 279:330]  # 44
        a23 = rst1[281:331, 358:410]  # 45
        a24 = rst1[281:331, 438:490]  # 46

        a25 = rst1[357:408, 12:64]  # 51
        a26 = rst1[357:408, 92:144]  # 52
        a27 = rst1[357:408, 172:224]  # 53
        a28 = rst1[357:408, 279:330]  # 54
        a29 = rst1[357:408, 358:410]  # 55
        a30 = rst1[357:408, 438:490]  # 56

        a31 = rst1[434:484, 13:65]  # 61
        a32 = rst1[434:484, 92:144]  # 62
        a33 = rst1[434:484, 172:224]  # 63
        a34 = rst1[434:484, 279:330]  # 64
        a35 = rst1[434:484, 358:410]  # 65
        a36 = rst1[434:484, 438:490]  # 66

        a37 = rst2[22:80, 16:73]  # D11
        a38 = rst2[22:80, 113:170]  # D12
        a39 = rst2[22:80, 211:269]  # D13
        a40 = rst2[22:80, 309:366]  # D14
        a41 = rst2[22:80, 407:464]  # D15
        a42 = rst2[22:80, 505:561]  # D16

        a43 = rst2[122:181, 16:73]  # D21
        a44 = rst2[122:181, 113:170]  # D22
        a45 = rst2[122:181, 211:269]  # D23
        a46 = rst2[122:181, 309:366]  # D24
        a47 = rst2[122:181, 407:464]  # D25
        a48 = rst2[122:181, 505:561]  # D26

        # 坐标存放矩阵
        location = ['A 1,1', 'A 1,2', 'A 1,3', 'A 1,4', 'A 1,5', 'A 1,6',
                    'A 2,1', 'A 2,2', 'A 2,3', 'A 2,4', 'A 2,5', 'A 2,6',
                    'A 3,1', 'A 3,2', 'A 3,3', 'A 3,4', 'A 3,5', 'A 3,6',
                    'A 4,1', 'A 4,2', 'A 4,3', 'A 4,4', 'A 4,5', 'A 4,6',
                    'A 5,1', 'A 5,2', 'A 5,3', 'A 5,4', 'A 5,5', 'A 5,6',
                    'A 6,1', 'A 6,2', 'A 6,3', 'A 6,4', 'A 6,5', 'A 6,6',
                    'U 1,1', 'U 1,2', 'U 1,3', 'U 1,4', 'U 1,5', 'U 1,6',
                    'U 2,1', 'U 2,2', 'U 2,3', 'U 2,4', 'U 2,5', 'U 2,6']

        all_name = os.listdir("./ability_pic")  # 全技能文件名列表
        file = open('./winrate/abilitieswinrate.json', encoding='utf-8')
        load_dict = file.read()
        new_dict = json.loads(load_dict)  # 读取json
        ability_dict = new_dict['rows']  # 得到技能的字典列表
        sta_table = []  # 存放最终结果

        for num in range(48):
            i2 = num + 1
            temp1 = eval('a{}'.format(i2))  # 获得上面的例如 a1 变量
            a = cv2.resize(temp1, self.img_shape, interpolation=cv2.INTER_LINEAR)  # 归一化

            ls = []  # 存放与所有技能的匹配结果
            for filename in all_name:  # 遍历技能
                b1 = cv2.imread(r'./ability_pic/' + filename)
                b2 = cv2.resize(b1, self.img_shape, interpolation=cv2.INTER_LINEAR)
                res = cv2.matchTemplate(a, b2, cv2.TM_CCORR_NORMED)  # 模板匹配
                ls.append([filename, res[0]])  #

            ls.sort(key=lambda x: x[1])  # 按相似度排序

            the_id = ls[-1][0][:4]  # 获取最佳匹配结果的id
            if the_id[-1] == '.':  # 三位数情况
                the_id = the_id[:3]

            for j in ability_dict:
                if j['abilityId'] == int(the_id):
                    rank = ability_dict.index(j) + 1  # 排名
                    ability_id = j['abilityId']  # id
                    name_cn = j['nameCn']  # 技能名
                    sta_table.append([name_cn, rank, location[num], num, ability_id])
                    continue

        sta_table.sort(key=lambda x: x[1])
        index = 1
        for item in sta_table:  # 获取当局中排名
            item.append(index)
            index = index + 1
        # print(sta_table[0])
        # print(sta_table[1])

        if save_sta:
            final_table = [tmp[:3] for tmp in sta_table]
            csv_name = ['名称', '排名', '位置']
            my_csv = pd.DataFrame(columns=csv_name, data=final_table)
            my_csv.to_csv('./cache/result.csv', encoding='utf_8_sig')

        file.close()

        return sta_table

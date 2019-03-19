"""
# Copyright (c) 2019 Ji Lei
# Updated on 2019-3-19
# Author:Ji Lei
# Version 1.4
# Title: Enigma(增加了反射器）
"""

import numpy as np
import pickle


class EnigmaRotor:
    # 转子定义初始化
    gear1 = np.zeros(shape=(2, 26))
    gear2 = np.zeros(shape=(2, 26))
    gear3 = np.zeros(shape=(2, 26))
    reflector = np.zeros(shape=(2, 13))

    # 三个转子的起始位置
    gear1_num = []
    gear2_num = []
    gear3_num = []

    # 加密次数计数器
    counter1 = 0
    counter2 = 0
    counter3 = 0

    # 字母表
    letter = np.array(
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
         'W', 'X', 'Y', 'Z'])

    # 密文，明文声明
    ciphertext = ""
    plaintext = ""
    # 密文/明文长度，因为一样长啊(￣▽￣)~*
    length = 0

    def __init__(self):
        self.plaintext = input("input you plaintext:")
        self.length = len(self.plaintext)
        self.ciphertext = list(self.ciphertext)  # 初始化密文
        self.plaintext = list(self.plaintext)  # 初始化明文
        self.read_info()
        self.transcoding()

    def read_info(self):
        # 读取转子初始数据
        self.gear1 = np.load('data\\gear\\' + 'gear1.npy')
        self.gear2 = np.load('data\\gear\\' + 'gear2.npy')
        self.gear3 = np.load('data\\gear\\' + 'gear3.npy')
        self.reflector = np.load('data\\' + 'reflector.npy')

        # 转子初始设定gear_num
        self.gear1_num = [self.gear1[0, 0], self.gear1[1, 0]]
        self.gear2_num = [self.gear2[0, 0], self.gear2[1, 0]]
        self.gear3_num = [self.gear3[0, 0], self.gear3[1, 0]]
        print('转子初始设定')
        print('self.gear3_num=', self.gear3_num)
        print('self.gear2_num=', self.gear2_num)
        print('self.gear1_num=', self.gear1_num)

        # 读取计数器counter初始数据
        countername1 = 'counter1.data'
        countername2 = 'counter2.data'
        countername3 = 'counter3.data'
        f1 = open('data\\counter\\' + countername1, 'rb')
        f2 = open('data\\counter\\' + countername2, 'rb')
        f3 = open('data\\counter\\' + countername3, 'rb')
        self.counter1 = pickle.load(f1)
        self.counter2 = pickle.load(f2)
        self.counter3 = pickle.load(f3)
        f1.close()
        f2.close()
        f3.close()

    def transcoding(self):
        plainfile = open('data\\text\\' + 'plaintext.data', 'wb')
        pickle.dump(self.plaintext, plainfile)
        plainfile.close()
        print("要加密的明文")
        print(self.plaintext)
        for i in range(self.length):
            self.plaintext[i] = ord(self.plaintext[i])  # 将密文转换成数字
            if 97 <= self.plaintext[i] <= 122:
                self.plaintext[i] = self.plaintext[i] - 97
            elif 65 <= self.plaintext[i] <= 90:
                self.plaintext[i] = self.plaintext[i] - 65
        print(self.plaintext)

    def rotate(self):  # 加密一次转一次
        # 1.每次加密快转子必然转一次
        # 2.快转子转一圈，中转子转一次
        # 3.中转子转一圈，慢转子转一次
        # 4.转完了之后，要把转子数据和counter再一块写入文件
        """
        注释里都是错的emmmmmm
        if self.counter < 26:  # 快转子将要起舞
            if self.counter == 25:  # 已经加密了26次，快转子要归零了，快转子和中转子都旋转1/26圈
                # 设置第三方变量，存储到头的gear3[0,25]和gear3[1,25]，以及中转子的gear2[0,25]和gear2[1,25]
                third_30 = self.gear3[0, 25]
                third_31 = self.gear3[1, 25]
                third_20 = self.gear2[0, 25]
                third_21 = self.gear2[1, 25]
                for i in range(25, 0, -1):
                    self.gear3[0, i] = self.gear3[0, i - 1]
                    self.gear3[0, i] = self.gear3[0, i - 1]
                    # 以下是满一圈的额外部分
                    self.gear2[0, i] = self.gear2[0, i - 1]
                    self.gear2[0, i] = self.gear2[0, i - 1]
                self.gear3[0, 0] = third_30
                self.gear3[1, 0] = third_31
                self.gear2[0, 0] = third_20
                self.gear2[1, 0] = third_21
            else:  # 不满26次，就只有快转子转1/26圈
                # 设置第三方变量，存储到头的gear3[0,25]和gear3[1,25]，以及中转子的gear2[0,25]和gear2[1,25]
                third_30 = self.gear3[0, 25]
                third_31 = self.gear3[1, 25]
                for i in range(25, 0, -1):
                    self.gear3[0, i] = self.gear3[0, i - 1]
                    self.gear3[0, i] = self.gear3[0, i - 1]
                self.gear3[0, 0] = third_30
                self.gear3[1, 0] = third_31
        if 26 <= self.counter < 676:  # 中转子将要起舞
            if self.counter == 675:  # 已经加密了675次，快转子和中转子都要归零了，快转子、中转子和慢转子都旋转1/26圈
                # 设置第三方变量
                third_30 = self.gear3[0, 25]
                third_31 = self.gear3[1, 25]
                third_20 = self.gear2[0, 25]
                third_21 = self.gear2[1, 25]
                third_10 = self.gear1[0, 25]
                third_11 = self.gear1[1, 25]
                for i in range(25, 0, -1):
                    # 快转子
                    self.gear3[0, i] = self.gear3[0, i - 1]
                    self.gear3[0, i] = self.gear3[0, i - 1]
                    # 中转子
                    self.gear2[0, i] = self.gear2[0, i - 1]
                    self.gear2[0, i] = self.gear2[0, i - 1]
                    # 慢转子
                    self.gear1[0, i] = self.gear1[0, i - 1]
                    self.gear1[0, i] = self.gear1[0, i - 1]
                self.gear3[0, 0] = third_30
                self.gear3[1, 0] = third_31
                self.gear2[0, 0] = third_20
                self.gear2[1, 0] = third_21
                self.gear1[0, 0] = third_10
                self.gear1[1, 0] = third_11
            else:  # 不满576次，就只有中转子转1/26圈
                # 设置第三方变量，存储到头的gear3[0,25]和gear3[1,25]，以及中转子的gear2[0,25]和gear2[1,25]
                third_20 = self.gear2[0, 25]
                third_21 = self.gear2[1, 25]
                for i in range(25, 0, -1):
                    self.gear2[0, i] = self.gear2[0, i - 1]
                    self.gear2[0, i] = self.gear2[0, i - 1]
                self.gear2[0, 0] = third_20
                self.gear2[1, 0] = third_21
        """
        counter1_old = self.counter1
        counter2_old = self.counter2
        if self.counter3 == 26:  # ，快转子要转一圈了，中转子要转了
            if self.counter2 == 25:  # 判断一下中转子是不是该转满一圈了
                self.counter1 = self.counter1 + 1  # 慢转子转1/26
                self.counter2 = self.counter2 + 1 - 26
                self.counter3 = self.counter3 - 26  # 快转子转1/26
            else:
                self.counter2 = self.counter2 + 1  # 中转子转1/26
                self.counter3 = self.counter3 - 26  # 快转子转1/26

        # 快转子先转一次
        third_30 = self.gear3[0, 25]
        third_31 = self.gear3[1, 25]
        for i in range(25, 0, -1):
            self.gear3[0, i] = self.gear3[0, i - 1]
            self.gear3[1, i] = self.gear3[1, i - 1]
        self.gear3[0, 0] = third_30
        self.gear3[1, 0] = third_31
        # 判断中转子需不需要转
        if self.counter2 != counter2_old:
            # 中转子转一次
            third_20 = self.gear2[0, 25]
            third_21 = self.gear2[1, 25]
            for i in range(25, 0, -1):
                self.gear2[0, i] = self.gear2[0, i - 1]
                self.gear2[1, i] = self.gear2[1, i - 1]
            self.gear2[0, 0] = third_20
            self.gear2[1, 0] = third_21
        # 判断慢转子需不需要转
        if self.counter1 != counter1_old:
            # 中转子转一次ear1[0, 25]
            third_10 = self.gear1[0, 25]
            third_11 = self.gear1[1, 25]
            for i in range(25, 0, -1):
                self.gear1[0, i] = self.gear1[0, i - 1]
                self.gear1[1, i] = self.gear1[1, i - 1]
            self.gear1[0, 0] = third_10
            self.gear1[1, 0] = third_11
        self.write_info()

    def write_info(self):
        # 将三个转子的初始数据保存，读取，用以进行转子旋转的初始化
        # 已初始化完成
        np.save('data\\gear\\' + 'gear1.npy', self.gear1)
        np.save('data\\gear\\' + 'gear2.npy', self.gear2)
        np.save('data\\gear\\' + 'gear3.npy', self.gear3)
        # reflector已初始化完毕
        # np.save('data\\' + 'reflector.npy', self.reflector)
        # counter是计数器
        countername1 = 'counter1.data'
        countername2 = 'counter2.data'
        countername3 = 'counter3.data'
        f1 = open('data\\counter\\' + countername1, 'wb')
        f2 = open('data\\counter\\' + countername2, 'wb')
        f3 = open('data\\counter\\' + countername3, 'wb')
        pickle.dump(self.counter1, f1)
        pickle.dump(self.counter2, f2)
        pickle.dump(self.counter3, f3)
        f1.close()
        f2.close()
        f3.close()
        # gear_num是转子初始状态，用于解密用
        num1file = 'gear1_num.data'
        num2file = 'gear2_num.data'
        num3file = 'gear3_num.data'
        f1 = open('data\\init_num\\' + num1file, 'wb')
        f2 = open('data\\init_num\\' + num2file, 'wb')
        f3 = open('data\\init_num\\' + num3file, 'wb')
        pickle.dump(self.gear1_num, f1)
        pickle.dump(self.gear2_num, f2)
        pickle.dump(self.gear3_num, f3)
        f1.close()
        f2.close()
        f3.close()

    def search_num(self, gear, n):  # 这个函数用于在三个转子中寻找连线对应的数字的在数组中的位置,n为gear[0,n],返回gear[1,?]
        for i in range(25):
            if gear[1, i] == gear[0, n]:
                break
            else:
                continue
        return i

    def anti_search(self, gear, n):
        for i in range(25):
            if gear[0, i] == gear[1, n]:
                break
            else:
                continue
        return i

    def reflect(self, gear3_end):
        # 对当前字母进行反射
        anti_gear3_fir = 0
        for m in range(1):
            for n in range(12):
                if gear3_end == self.reflector[m, n]:
                    if m == 0:
                        anti_gear3_fir = self.reflector[1, n]
                        break
                    else:
                        anti_gear3_fir = self.reflector[0, n]
                        break
                else:
                    continue
        # 向前反射
        # anti_gear3_fir = gear3_end
        anti_gear3_end = self.anti_search(self.gear3, anti_gear3_fir)
        anti_gear2_fir = anti_gear3_end
        anti_gear2_end = self.anti_search(self.gear2, anti_gear2_fir)
        anti_gear1_fir = anti_gear2_end
        anti_gear1_end = self.anti_search(self.gear1, anti_gear1_fir)  # 最后返回了一个位置
        # 将当前字符追加入ciphertext中
        self.ciphertext.append(self.letter[anti_gear1_end])

    def encode(self):
        for i in range(self.length):
            # num = self.search_num(self.gear3, self.search_num(self.gear2, self.search_num(self.gear1,i)))
            # self.ciphertext.append(self.gear3[1, num])
            gear1_fir = self.plaintext[i]  # 这是输入数据,[18, 13, 20, 6, 23, 2, 19]，原来是i，已更改
            gear1_end = self.search_num(self.gear1, gear1_fir)  # 末尾返回位置数据
            gear2_fir = gear1_end  # 继承上一个转子的位置
            gear2_end = self.search_num(self.gear2, gear2_fir)
            gear3_fir = gear2_end
            gear3_end = self.search_num(self.gear3, gear3_fir)
            # 通过反射器反射gear3_end
            self.reflect(gear3_end)
            # 完成了一次加密，快转子计数器加一，随后转子就要就要旋转
            self.counter3 = self.counter3 + 1
            self.rotate()
        # 加密后的数组
        print('快转子', self.gear3)
        print('中转子', self.gear2)
        print('慢转子', self.gear1)
        print('反射器', self.reflector)
        print('快转子计数=', self.counter3)
        print('中转子计数=', self.counter2)
        print('慢转子计数=', self.counter1)
        print("得到的密文")
        print(self.ciphertext)
        cipherfile = open('data\\text\\' + 'ciphertext.data', 'wb')
        pickle.dump(self.ciphertext, cipherfile)
        cipherfile.close()

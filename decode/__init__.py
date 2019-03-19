"""
# Copyright (c) 2019 Ji Lei
# Updated on 2019-3-19
# Author:Ji Lei
# Version 1.4
# Title: Enigma(增加了反射器）
"""

import numpy as np
import pickle


class EnigmaDecode:
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
        self.length = len(self.plaintext)
        self.ciphertext = list(self.ciphertext)  # 初始化密文
        self.plaintext = list(self.plaintext)  # 初始化明文

    def read_info(self):
        # 读取转子
        self.gear1 = np.load('data\\gear\\' + 'gear1.npy')
        self.gear2 = np.load('data\\gear\\' + 'gear2.npy')
        self.gear3 = np.load('data\\gear\\' + 'gear3.npy')
        self.reflector = np.load('data\\' + 'reflector.npy')
        # 读取转子初始值
        n1 = open('data\\init_num\\' + 'gear1_num.data', 'rb')
        n2 = open('data\\init_num\\' + 'gear2_num.data', 'rb')
        n3 = open('data\\init_num\\' + 'gear3_num.data', 'rb')
        self.gear1_num = pickle.load(n1)
        self.gear2_num = pickle.load(n2)
        self.gear3_num = pickle.load(n3)
        n1.close()
        n2.close()
        n3.close()
        # 读取counter，虽然只是解密的时候计数用
        f1 = open('data\\counter\\' + 'counter1.data', 'rb')
        f2 = open('data\\counter\\' + 'counter2.data', 'rb')
        f3 = open('data\\counter\\' + 'counter3.data', 'rb')
        self.counter1 = pickle.load(f1)
        self.counter2 = pickle.load(f2)
        self.counter3 = pickle.load(f3)
        f1.close()
        f2.close()
        f3.close()
        # 读取密文
        cipherfile = open('data\\text\\ciphertext.data', 'rb')
        self.ciphertext = pickle.load(cipherfile)
        cipherfile.close()
        print(self.ciphertext)

    def init_rotate(self):
        # 先转gear3
        for i in range(26):
            if self.gear3[0, 0] == self.gear3_num[0]:
                break
            else:
                third_30 = self.gear3[0, 25]
                third_31 = self.gear3[1, 25]
                for j in range(25, 0, -1):
                    self.gear3[0, i] = self.gear3[0, i - 1]
                    self.gear3[1, i] = self.gear3[1, i - 1]
                self.gear3[0, 0] = third_30
                self.gear3[1, 0] = third_31
        # 再转gear2
        for i in range(26):
            if self.gear2[0, 0] == self.gear2_num[0]:
                break
            else:
                third_20 = self.gear2[0, 25]
                third_21 = self.gear2[1, 25]
                for j in range(25, 0, -1):
                    self.gear2[0, i] = self.gear2[0, i - 1]
                    self.gear2[1, i] = self.gear2[1, i - 1]
                self.gear2[0, 0] = third_20
                self.gear2[1, 0] = third_21
        # 最后转gear1
        for i in range(26):
            if self.gear1[0, 0] == self.gear1_num[0]:
                break
            else:
                third_10 = self.gear1[0, 25]
                third_11 = self.gear1[1, 25]
                for j in range(25, 0, -1):
                    self.gear1[0, i] = self.gear1[0, i - 1]
                    self.gear1[1, i] = self.gear1[1, i - 1]
                self.gear1[0, 0] = third_10
                self.gear1[1, 0] = third_11

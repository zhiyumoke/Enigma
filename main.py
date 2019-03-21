"""
# Copyright (c) 2019 Ji Lei
# Updated on 2019-3-19
# Author:Ji Lei
# Version 1.4
# Title: Enigma(增加了反射器）
"""

import encode

if __name__ == '__main__':
    # 加密
    my_enigma = encode.EnigmaRotor()
    encode.EnigmaRotor.encode(my_enigma)
    # encode.EnigmaRotor.text(my_enigma)
    '''
    my_enigma = decode.EnigmaDecode
    decode.EnigmaDecode.read_info(my_enigma)
'''

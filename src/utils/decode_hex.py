import base64

from Crypto.Cipher import AES


class Decode_hex:
    @staticmethod
    def to_int(code:str, move_prefix=True):
        if move_prefix:
            return int(code[2:], 16)
        else:
            return int(code, 16)

    @staticmethod
    def zfill(msg, pre_fix ='0x', len = 64):
        if msg.startswith('0x'):
            msg = msg[2:].zfill(64)
        else:
            msg = msg.zfill(64)
        return msg


    @staticmethod
    def encode_aes(key:str, data:str, base64_flag = True):
        # 待加密文本
        # 初始化加密器
        aes = AES.new(Decode_hex.add_to_16(key), AES.MODE_ECB)
        # 先进行aes加密
        encrypt_data = aes.encrypt(Decode_hex.add_to_16(data))
        if base64_flag:
            # 用base64转成字符串形式
            encrypt_data = str(base64.encodebytes(encrypt_data), encoding='utf-8')  # 执行加密并转码返回bytes

        return encrypt_data

    @staticmethod
    def decode_aes(key:str, encode_data:str, base64_flag = True):
        # 初始化加密器
        aes = AES.new(Decode_hex.add_to_16(key), AES.MODE_ECB)

        if base64_flag:
            # 优先逆向解密base64成bytes
            encode_data = base64.decodebytes(encode_data.encode(encoding='utf-8'))

        # 执行解密密并转码返回str
        decrypted_text = str(aes.decrypt(encode_data), encoding='utf-8').replace('\0', '')
        return decrypted_text
    @staticmethod
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    @staticmethod
    # str不是32的倍数那就补足为16的倍数
    def add_to_32(value):
        while len(value) % 32 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes


if __name__ == '__main__':
    d = Decode_hex()

    encode_data = d.encode_aes(key = 'test001',data='0x4e51b96b771dc26482293ed5961570570efb31210312')
    print('data:',encode_data)

    print(d.decode_aes(key = 'test001',encode_data= encode_data))
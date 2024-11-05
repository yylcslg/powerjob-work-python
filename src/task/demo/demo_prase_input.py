from src.task_core.web3_wrap import Web3Wrap
from src.utils.block_chain import Block_chain


def process():
    w = Web3Wrap(block_chain=Block_chain.BSC_TEST, gas_flag=False)
    data_parse(w)

#
#
# from :0xF2788598c1521602e5d4245B7A72bBC7DD5755f6
# nft contract: 0x655FEbFEF98fF56A6a64A673e7601b8Cda322c11
# to: 0xA0924Cc8792836F48D94759c76D32986BC74B54c
def data_parse(w:Web3Wrap):
    print('----------------------data_parse_3--------------------------')

    data_1 = '0xb341ee9f0000000000000000000000000000000000000000000000000000079308cd6c6e00000000000000000000000000000000000000000000000000038f504e109fdb00000000000000000000000000000000000000000000000000000068dcee6c6c'

    w.parse_input(data_1)




if __name__ == '__main__':
    process()
    print('finish.....')
    pass
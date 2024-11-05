from enum import Enum


class Block_chain(Enum):
    ETH = ('https://mainnet.infura.io/v3/a4c5b4ef4d704823980c3349f3b99d18',1, 'pos')
    LINEA = ('https://linea.blockpi.network/v1/rpc/public', 59144, 'pos')
    ZKS_ERA = ('https://mainnet.era.zksync.io', 324, 'pos')
    BSC = ('https://bsc-dataseed.binance.org/', 56, 'pos', 'BKB2APPEW672F9AFU3B41D6UW3VE3W722G')
    BSC_ANKR = ('https://rpc.ankr.com/bsc/', 56, 'pos', 'pos')
    OPBNB = ('https://opbnb-mainnet.nodereal.io/v1/64a9df0874fb4a93b9d0a3849de012d3', 204, 'pos', 'pos')
    POLYGON = ('https://polygon-mainnet.infura.io/v3/a4c5b4ef4d704823980c3349f3b99d18', 137, 'pos', 'pos')
    OPTIMISM = ('https://opt-mainnet.g.alchemy.com/v2/ortzM6D1U0ATdXD0WkjCLmXkNs5vdaSD', 10, 'pos')

    ZETA = ('https://zetachain-evm.blockpi.network/v1/rpc/public', 7000, 'pos')

    #####test
    #'https://goerli.infura.io/v3/5d843434cf044d7a92cc987b26819d3c'
    GOERLI_TEST = ('https://rpc.ankr.com/eth_goerli', 5, 'poa')
    #Sepolia = ('https://rpc.sepolia.org/', 11155111, 'pos')
    Sepolia = ('https://eth-sepolia.g.alchemy.com/v2/EyV7ENP2A1ThkoaSun3d7tooPkFll2JK', 1513, 'pos')
    Story = ('https://testnet.storyrpc.io', 11155111, 'pos')
    Plume = ('https://testnet-rpc.plumenetwork.xyz/http', 161221135, 'pos')
    BSC_TEST = ('https://endpoints.omniatech.io/v1/bsc/testnet/public/', 97, 'pos')

    LINEA_TEST = ('https://rpc.goerli.linea.build/', 59140, 'poa')
    ZKS_ERA_TEST = ('https://testnet.era.zksync.dev', 280, 'poa')
    SCROLL_TEST = ('https://scroll-alphanet.public.blastapi.io', 534353, 'pos')
    SCROLL_SEP_TEST = ('https://sepolia-rpc.scroll.io/', 534351, 'pos')
    SCROLL_SEP_ALPHA_TEST = ('https://alpha-rpc.scroll.io/l2', 534353, 'pos')
    OKB_X1 = ('https://testrpc.x1.tech', 195, 'pos')

    TAIKO_TEST = ('https://rpc.katla.taiko.xyz', 167008, 'pos')



    def __init__(self, url, chain_id, middleware, apiKey=''):
        self.url = url
        self.chain_id = chain_id
        self.middleware = middleware
        self.apiKey = apiKey
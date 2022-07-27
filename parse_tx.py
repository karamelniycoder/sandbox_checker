import json
from web3 import Web3
from multiprocessing.dummy import Pool


def take(check_addr):
    if addrlist.count(check_addr) == 1: wonlist.append(check_addr)


web3 = Web3(Web3.HTTPProvider("https://matic-mainnet.chainstacklabs.com"))
if web3.isConnected() != True:
    print('error, web3 is not connected')
    exit(':(')

dannie = input('peretashi file s addresami suda: ')

addrlist = []
wonlist = []
tx = json.loads(web3.toJSON(web3.eth.getTransactionReceipt(0xdbfda24b0e61e392c1fab76a75904e3faeff91b3cab88026a1024838f3892bf5)))
for logs in tx['logs']:
    addr = '0x' + (logs['topics'][-1])[-40:].lower()
    addrlist.append(addr)


with open(dannie, 'r') as file:
    wantaddr = [row.strip() for row in file]
if len(wantaddr) > 1000:
    threads = 1000
else:
    threads = len(wantaddr)


with Pool(threads) as p:
    p.map(take, wantaddr)
if len(wonlist) > 0:
    for addr in wonlist:
        with open('won_addr.txt', 'a') as file:
            file.write(f'{addr}\n')
        print(addr)
    print('tak zhe sozdal dlya tebya file s viygrishnimy adresami (won_addr.txt)')
else: print('no won addresses :C ebash dalshe drug')

input('\npress Enter to exit...')

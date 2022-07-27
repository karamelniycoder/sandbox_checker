import json
import requests
from web3 import Web3
from multiprocessing.dummy import Pool


def take(check_addr):
    if addrlist.count(check_addr) > 0: wonlist.append(check_addr)


def wait_for_tx():
    url = f'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x3845badade8e6dff049820680d1f14bd3903a5d0&address=0x047545a7e69bfb4676eb65da917e2d5435dc1ee1&page=1&offset=100&startblock=15218464&endblock=27025780&sort=asc&apikey=RCRIT5J2IGMHVXK5KI4RB32TK97G2DY7DR'
    tx_hash = ''
    print('waiting for transaction...')
    while not len(tx_hash) > 0:
        r = requests.get(url)
        if str(r.json()['status']) == '1':
            for res in r.json()['result']:
                if res['from'] == '0x047545a7e69bfb4676eb65da917e2d5435dc1ee1':
                    tx_hash = res['hash']
                    if str(res["value"]).startswith("5"):
                        print('tranza poimana za hvost!!')
                    else:
                        print(f'transa est", no ona somnitelnaya, {tx_hash}')
                    return (tx_hash)



eth = 'https://mainnet.infura.io/v3/bf3238e1cc0e4a40bfa83e6bd63679e9'
web3 = Web3(Web3.HTTPProvider(eth))
if web3.isConnected() != True:
    exit('web3 is not connected')

addrlist = []
wonlist = []

dannie = input('peretashi file s addresami suda: ')

with open(dannie, 'r') as file:
    wantaddr = [row.strip() for row in file]
if len(wantaddr) > 1000:
    threads = 1000
else:
    threads = len(wantaddr)

tx_hash = wait_for_tx()

tx = json.loads(web3.toJSON(web3.eth.getTransactionReceipt(tx_hash)))
for logs in tx['logs']:
    addr = '0x' + (logs['topics'][-1])[-40:].lower()
    addrlist.append(addr)


with Pool(threads) as p:
    p.map(take, wantaddr)
if len(wonlist) > 0:
    for addr in wonlist:
        with open('won_addr.txt', 'a') as file:
            file.write(f'{addr}\n')
        print(addr)
    print('tak zhe sozdal dlya tebya file s won adresami (won_addr.txt)')
else: print('no won addresses :C ebash dalshe drug')

input('\npress Enter to exit...')

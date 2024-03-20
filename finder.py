from colorama import Fore, Style
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional
import json
import multiprocessing
from multiprocessing import Pool
import threading

koinhacker = '''

██╗░░██╗░█████╗░██╗███╗░░██╗██╗░░██╗░█████╗░░█████╗░██╗░░██╗███████╗██████╗░
██║░██╔╝██╔══██╗██║████╗░██║██║░░██║██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗
█████═╝░██║░░██║██║██╔██╗██║███████║███████║██║░░╚═╝█████═╝░█████╗░░██████╔╝
██╔═██╗░██║░░██║██║██║╚████║██╔══██║██╔══██║██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██║░╚██╗╚█████╔╝██║██║░╚███║██║░░██║██║░░██║╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░╚═╝░╚════╝░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
--------------------------------------------------------
[x] Software: ETHxMNEMONIC
[x] Author: KoinHacker
[x] Github: koinhacker
[x] Version: 1.0
--------------------------------------------------------
Donate me BTC: bc1qhzems2lsstx795ae8er698zp0vvcvg3p39e3yr
========================================================

▀▀█▀▀ ░█▀▀█ ▀█▀ ─█▀▀█ ░█─── 　 ░█──░█ ░█▀▀▀ ░█▀▀█ ░█▀▀▀█ ▀█▀ ░█▀▀▀█ ░█▄─░█ 
─░█── ░█▄▄▀ ░█─ ░█▄▄█ ░█─── 　 ─░█░█─ ░█▀▀▀ ░█▄▄▀ ─▀▀▀▄▄ ░█─ ░█──░█ ░█░█░█ 
─░█── ░█─░█ ▄█▄ ░█─░█ ░█▄▄█ 　 ──▀▄▀─ ░█▄▄▄ ░█─░█ ░█▄▄▄█ ▄█▄ ░█▄▄▄█ ░█──▀█
'''

PRINT = Fore.GREEN + koinhacker + Fore.RESET
print('\n\n', Fore.RED, str(PRINT), Style.RESET_ALL, '\n')

r = 1
cores = 8

def finder(r): 
    filename = "eth500.txt"
    with open (filename) as f: 
        add = f.read().split()
    add = set(add)
    
    z = 1
    w = 0
    while True:
        PASSPHRASE: Optional[str] = None
        MNEMONIC: str = generate_mnemonic(language="english", strength=128)

        bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)

        bip44_hdwallet.from_mnemonic(
            mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
        )
        
        bip44_hdwallet.clean_derivation()        
        
        for address_index in range(10):
            bip44_derivation: BIP44Derivation = BIP44Derivation(
                cryptocurrency=EthereumMainnet, account=0, change=False, address=address_index
            )
            bip44_hdwallet.from_path(path=bip44_derivation)
            addr = bip44_hdwallet.address()
            private_key = bip44_hdwallet.private_key()
            mnemonic = MNEMONIC
            bip44_hdwallet.clean_derivation()


        print('Winner Wallet:',Fore.GREEN, str(w), Fore.YELLOW,'Total Scan:',Fore.WHITE, str(z), Fore.YELLOW, Fore.YELLOW, 'Addr:', Fore.WHITE, str(addr), Fore.YELLOW, 'Private:', Fore.WHITE, str(private_key), end='\r', flush=True)
        z += 1
        
        if addr in add:
            print('Winning', Fore.GREEN, str(w), Fore.WHITE, str(z), Fore.YELLOW, 'Total Scan Checking ----- BTC Address =', Fore.GREEN, str(addr), end='\r')
            w += 1
            z += 1
            f = open("winner.txt", "a")
            f.write('\nAddress = ' + str(addr))
            f.write('\nPrivate Key = ' + str(private_key))
            f.write('\nMnemonic Phrase = ' + str(mnemonic))
            f.write('\n=========================================================\n')
            f.close()
            print('Winner information Saved On text file = ADDRESS ', str(addr))
            continue

        
finder(r)

if __name__ == '__main__':
    jobs = []
    for r in range(cores):
        p = multiprocessing.Process(target=finder, args=(r,))
        jobs.append(p)
        p.start()
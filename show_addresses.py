from binascii import hexlify, unhexlify
from bitcoin import bip32, bip39, script
from bitcoin.networks import NETWORKS

def show_addresses():
    f = open('mnemonic.txt', 'r')
    mnemonic = f.read()
    f.close()

    #Mnemonic to seed [64 bytes]: PBKDF2 key derivation
    passwd = input("Introduce password for key derivation: ")

    seed = bip39.mnemonic_to_seed(mnemonic, password=passwd)

    net = input("Choose network [mainet->1] or [testnet->2]: ")

    while net != "1" and net != "2":
        net = input("Invalid input, [mainet->1] or [testnet->2]: ")

    if net == "1":
        net = "main"
        hardened_derivation = "m/84h/0h/0h"
    else:
        net = "test"
        hardened_derivation = "m/84h/1h/0h"

    root = bip32.HDKey.from_seed(seed, version=NETWORKS[net]['xprv'])
    account = root.derive(hardened_derivation)
    #MAINET - NATIVE SEGWIT
    account.version = NETWORKS[net]['zprv']

    xpub = account.to_public()

    n = int(input("Introduce a number of addresses: "))

    for i in range(n):
        derivation = "m/0/"+str(i)
        pubkey=xpub.derive(derivation).key
        sc = script.p2wpkh(pubkey)
        addr = sc.address(network = NETWORKS[net])
        print("Address nº%s :" % i, addr)








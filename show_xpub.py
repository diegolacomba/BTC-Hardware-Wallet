from bitcoin import bip32, bip39
from bitcoin.networks import NETWORKS
from ubinascii import hexlify

def show_xpub():
    f = open('mnemonic.txt', 'r')
    mnemonic = f.read()
    f.close()

    #Mnemonic to seed [64 bytes]: PBKDF2 key derivation
    passwd = input("Introduce password for key derivation: ")

    seed = bip39.mnemonic_to_seed(mnemonic, password=passwd)

    network = input("Choose network [mainet->1] or [testnet->2]: ")

    while network != "1" and network != "2":
        network = input("Invalid input, [mainet->1] or [testnet->2]: ")

    if network == "1":
        root = bip32.HDKey.from_seed(seed, version=NETWORKS['main']['xprv'])
        hardened_derivation = "m/84h/0h/0h"
        account = root.derive(hardened_derivation)
        #MAINET - NATIVE SEGWIT
        account.version = NETWORKS['main']['zprv']
    else:
        root = bip32.HDKey.from_seed(seed, version=NETWORKS['test']['xprv'])
        hardened_derivation = "m/84h/1h/0h"
        account = root.derive(hardened_derivation)
        #TESTNET - NATIVE SEGWIT
        account.version = NETWORKS['test']['zprv']

    # [fingerprint/derivation]xpub to import to Bitcoin Core with descriptors

    # root fingerprint from any child of the root key
    fingerprint = root.child(0).fingerprint
    xpub = account.to_public()
    print("XPUB:")
    print("[%s%s]%s" % (
                hexlify(fingerprint).decode('utf-8'),
                hardened_derivation[1:],
                xpub.to_base58())
        )

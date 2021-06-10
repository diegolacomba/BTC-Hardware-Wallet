from binascii import hexlify, unhexlify
from bitcoin import bip32, script
from bitcoin.networks import NETWORKS

seed = unhexlify("f48aa8573251a70991d95984287a0a18dbaaa7ffce64fa9681a26d9f256541e824a476e4ad38af5c3335b732f4f078437cdb8fbff99efb90a2bfaafa6b15ce91")
print("Seed:", seed)

#KEY DERIVATION
#BIP-32 root key - BIP-84 + TESTNET

root = bip32.HDKey.from_seed(seed, version=NETWORKS['test']['zprv'])
print("Root: ", root.to_base58())

#BIP-84 - Testnet
#Derivation path - Account Extended Private Key - m/<purpose>/<coin/network>/<account_number>

account = root.derive("m/84h/1h/0h")
#account.version = NETWORKS['test']['zprv']
print("Account: ", account.to_base58())

#Convert AEPK to Master Public Key
#Derivation path - Account Extended Public Key

xpub = account.to_public()
#xpub.version = NETWORKS['test']['zpub']
#print("xpub: ", xpub.to_base58(version=NETWORKS['test']['zpub']))
print("xpub: ", xpub.to_base58())

#Our pub key for the first receiving address
#pubkey = object( chain code + key )

pubkey = xpub.derive("m/0/0").key
print("First pubkey: ", pubkey)
#print(hexlify(pubkey.sec()))

#Our priv key for the first receiving address
#no corresponde
privkey = account.derive("m/0/0").key
print("First privkey: ", privkey)
#print(hexlify(pubkey.sec())


#GET SCRIPTS AND ADDRESSES

#P2PKH SCRIPT from pubkey - LEGACY ADDRESS
sc = script.p2pkh(pubkey)
#Structure of the script
print("P2PKH script: ", hexlify(sc.data))
# OP_DUP (76), OP_HASH160 (a9), HEX representation of 20 (14), 20 bytes, OP_EQV (88), OP_CHECKSIG (ac)

#By default MainNET, If you want to use it for the tesnet: NETWORKS['test']
address = sc.address(network = NETWORKS['test'])
#First segwit receiving address, Legacy p2pkh address
print("First address (p2pkh): ",address)


#P2WPKH SCRIPT from pubkey - NATIVE SEGWIT
sc2 = script.p2wpkh(pubkey)
print("P2WPKH script: ", hexlify(sc2.data))
#SEGWIT VERSION (00), HEX representation of 20 (14), 20 bytes

address2 = sc2.address(network = NETWORKS['test'])

print("First address (p2wpkh): ",address2)

#P2SH SCRIPT from pubkey - NESTED SEGWIT
sc3 = script.p2sh(sc2)
print("P2SH script: ", hexlify(sc3.data))
#OP_HASH160 (a9), HEX representation of 20 (14), 20 bytes <hash160(script.data)>, OP_EQV

address3 = sc3.address(network = NETWORKS['test'])

print("First address (p2wpkh): ",address3)


#MULTISIGNATURE SCRIPT

#3 pubkeys derived from master public key
pukeys = [xpub.derive("m/0/%d" % i).key fot i in range(3)]

#Lets generate 2 of 3 multisig address - THE ORDER MATTERS!
#MULTISIG SCRIPT from 3 pubkeys
msig = script.multisig(2, sorted(pubkeys))
print("MULTISIG script: ", hexlify(msig.data))
# OP_2 (we want 2 addresses to be correct) (52), length next field (21) = 33 bytes, <pubkey1>,
# (21) = 33, <pubkey2>, (21) = 33, <pubkey3>, OP_3 ( OP_2 - 2 of 3 multisig ) (53), OP_CHECKMULTISIG (ae)

'''
msig.address() will fail because this script type doesn't have an address representation
'''

sc4 = script.p2wsh(msig).address())
sc5 = script.p2sh(msig).address()) #Legacy multisig address







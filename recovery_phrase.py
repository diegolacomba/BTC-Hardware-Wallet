import machine, os, hashlib
from binascii import hexlify
from bitcoin import bip39, bip32, script
from bitcoin.networks import NETWORKS

#TRNG
trng_entropy = os.urandom(256)

#Entropy from ADC pins
adc1 = machine.ADC(machine.Pin(35))
adc2 = machine.ADC(machine.Pin(34))
adc3 = machine.ADC(machine.Pin(32))
adc4 = machine.ADC(machine.Pin(33))

#Entropy from ADC pin to bytes
adc_entropy = bytes([(adc1.read()+adc2.read()+adc3.read()+adc4.read())%256 for i in range(2048)])

#16 bytes from sha256( total entropy )
final_entropy = hashlib.sha256(trng_entropy+adc_entropy).digest()[:16]

#Mnemonic phrase: Convert entropy to binary, add checksum from sha256, split into parts of 11 bits, each part is one word
phrase = bip39.mnemonic_from_bytes(final_entropy)

#Mnemonic to seed: PBKDF2 key derivation
seed = bip39.mnemonic_to_seed(phrase, password="pedir por terminal")

print("Entropy:", hexlify(final_entropy))
print("Recovery phrase:", phrase)
print("Seed:", hexlify(seed))

#BIP-32 root key
root = bip32.HDKey.from_seed(seed)
print(root.to_base58())

#BIP-84 - Testnet
#Derivation path - Account Extended Private Key - m/<purpose>/<coin/network>/<account_number>
account = root.derive("m/84h/1h/0h")
print(account.to_base58(version=NETWORKS['test']['zprv']))

#Convert AEPK to Master Public Key
#Derivation path - Account Extended Public Key
xpub = account.to_public()
print(xpub.to_base58(version=NETWORKS['test']['zpub']))

#Our pub key for the first receiving address
#pubkey = object( chain code + key )
pubkey = xpub.derive("m/0/0")
print(pubkey.key)
print(hexlify(pubkey.sec()))

#Get address
#Build script from pubkey - pay 2 witness pub key hash
sc = script.p2wpkh(pubkey)
#By default MainNET, If you want to use it for the tesnet: NETWORKS['test']
address = sc.address(NETWORKS['test'])
#First segwit receiving address
print(addr)




























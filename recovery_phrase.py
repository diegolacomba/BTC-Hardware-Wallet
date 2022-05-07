import machine, os, hashlib
from binascii import hexlify
from bitcoin import bip39, bip32, script
from bitcoin.networks import NETWORKS
from time import sleep

#RECOVERY/MNEMONIC PHRASE
def new_phrase():
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

    #MNEMONIC PHRASE: Convert entropy to binary, add checksum from sha256, split into parts of 11 bits, each part is one word
    phrase = bip39.mnemonic_from_bytes(final_entropy)
    print(phrase)

    f = open('mnemonic.txt', 'w')
    f.write("")
    f.close()
    f = open('mnemonic.txt', 'w')
    f.write(phrase)
    f.close()

def recover():
    print("WARNING: Make sure the mnemonic is correct")
    mnemonic = input("Type the mnemonic: ")

    f = open('mnemonic.txt', 'w')
    f.write("")
    f.close()
    f = open('mnemonic.txt', 'w')
    f.write(mnemonic)
    f.close()

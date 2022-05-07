from bitcoin import script
from bitcoin import bip32
from bitcoin import bip39
from bitcoin.networks import NETWORKS
from bitcoin import psbt
from ubinascii import unhexlify, hexlify
from ubinascii import a2b_base64, b2a_base64

def sign_tx():
    f = open("mnemonic.txt", "r")
    mnemonic = f.read()
    f.close()

    passwd = input("Introduce password for key derivation: ")

    seed = bip39.mnemonic_to_seed(mnemonic, password=passwd)

    network = input("Choose network [mainet->1] or [testnet->2]: ")

    while network != "1" and network != "2":
        network = input("Invalid input, [mainet->1] or [testnet->2]: ")

    if network == "1":
        network = "main"
    else:
        network = "test"

    root = bip32.HDKey.from_seed(seed, version=NETWORKS[network]["xprv"])

    fingerprint = root.child(0).fingerprint

    # parse psbt transaction
    b64_psbt = input("Paste here psbt transaction from Bitcoin Core: ")
    # convert it to binary
    raw = a2b_base64(b64_psbt)
    # parse
    tx = psbt.PSBT.parse(raw)

    # print how much we are spending and where
    total_in = 0
    for inp in tx.inputs:
        total_in += inp.witness_utxo.value

    print("Inputs:", total_in, "satoshi")

    change_out = 0 # btc that goes back to us
    send_outputs = []

    for i, out in enumerate(tx.outputs):
        # check if it is a change or not:
        change = False

        # should be one or zero for single-key addresses
        for pub in out.bip32_derivations:
            # check if it is our key
            if out.bip32_derivations[pub].fingerprint == fingerprint:
                hdkey = root.derive(out.bip32_derivations[pub].derivation)
                mypub = hdkey.key.get_public_key()
                #or
                mypub = hdkey.to_public().key
                if mypub != pub:
                    raise ValueError("Derivation path doesn't look right")
                # now check if provided scriptpubkey matches
                sc = script.p2wpkh(mypub)
                if sc == tx.tx.vout[i].script_pubkey:
                    change = True
                    continue

        if change:
            change_out += tx.tx.vout[i].value
            print("Change output: ",tx.tx.vout[i].value,"to",tx.tx.vout[i].script_pubkey.address(NETWORKS["test"]))
        else:
            send_outputs.append(tx.tx.vout[i])

    fee = total_in-change_out

    for out in send_outputs:
        fee -= out.value
        print("Send output: ",out.value,"to",out.script_pubkey.address(NETWORKS["test"]))

    print("------------")
    print("Sending: ", total_in)
    print("Spending", total_in-change_out, "satoshi")
    print("Fee:",fee,"satoshi")
    print("Change:",change_out,"satoshi")

    # sign the transaction - include into the psbt the partial signatures
    tx.sign_with(root)
    raw = tx.serialize()

    # convert to base64
    b64_psbt = b2a_base64(raw)

    # b2a ends with \n
    if b64_psbt[-1:] == b"\n":
        b64_psbt = b64_psbt[:-1]

    print("\nSigned transaction:")
    print(b64_psbt.decode('utf-8'))
    # now transaction is ready to be finalized and broadcasted it can be done with Bitcoin Core bitcoin-cli [-testnet/-regtest/...] finalizepsbt [b64_psbt]

from machine import Pin, I2C
from time import sleep
import ssd1306, recovery_phrase, show_xpub, psbt, show_addresses

pinesI2C = I2C(1, scl=Pin(4), sda=Pin(5))   # SCL = GPIO4, SDA = GPIO5

oled = ssd1306.SSD1306_I2C(128, 64, pinesI2C)

botonUP = Pin(15, Pin.IN)
botonDOWN = Pin(0, Pin.IN)
botonOK = Pin(14, Pin.IN)

next = 1

shutdown = True

# M E N U

def menu(option1, option2, option3, prev_value, next_value, up_ok, down_ok):
    global next
    next = next_value

    mostrar_menu(option1, option2, option3)

    while next == next_value:
        sleep(0.1)
        if botonUP.value() == 0 and up_ok:
            sleep(0.35)
            next = next_value-1

        if botonDOWN.value() == 0 and down_ok:
            sleep(0.35)
            next = next_value+1

        if botonOK.value() == 0:
            if prev_value != 0:
                sleep(0.35)
                next = prev_value
            else:
                sleep(0.35)
                next = 0


def mostrar_menu(option1, option2, option3):
    oled.fill(0)
    oled.text(option1, 22, 0)
    oled.text('/', 42, 10)
    oled.text('\\', 47, 10)
    oled.text('|', 45, 13)
    oled.text('|', 45, 16)
    oled.text(option2, 22, 28)
    oled.text('|', 45, 39)
    oled.text('|', 45, 42)
    oled.text('\\', 42, 45)
    oled.text('/', 47, 45)
    oled.text(option3, 22, 55)
    oled.show()

def disconnect():
    global next
    next == 71
    oled.fill(0)
    oled.text('Press OK to', 0, 0)
    oled.text('DISCONNECT', 0, 10)
    oled.text('Press UP/DOWN to', 0, 30)
    oled.text('CANCEL', 0, 40)
    oled.show()

    while next == 71:
        sleep(0.1)

        if botonUP.value() == 0:
            sleep(0.35)
            next = 7

        if botonDOWN.value() == 0:
            sleep(0.35)
            next = 7

        if botonOK.value() == 0:
            sleep(0.35)
            next = 0

def main():
    print('empiezo')
    global shutdown
    global next
    oled.fill(0)
    oled.text('WELCOME', 28, 28)
    oled.show()
    sleep(3)

    while shutdown:
        while next == 1:
            menu('-------', 'New Recovery', 'Show xpub', 0, next, False, True)

            if next == 0:
                next = 11
                #Recovery menu
                while next > 1:
                    while next == 11:
                        menu('-------', 'Generate', '  Back', 0, next, False, True)

                        if next == 0:
                            next = 111

                            f = open("mnemonic.txt", "r")
                            mnemonic = f.read()
                            f.close()
                            if len(mnemonic) > 0:
                                print("WARNING: this will delete the previous mnemonic")
                                des = input("Are you sure do you want to continue? [y/n]")

                                while des != "y" and des != "n":
                                    network = input("Invalid input, [continue->\"y\"] or [cancel->\"n\"]: ")

                                if des == "y":
                                    recovery_phrase.new_phrase()
                                else:
                                    next = 1
                            else:
                                recovery_phrase.new_phrase()

                            while next == 111:
                                menu('-------', 'Succesfull', '-OK to exit-', 1, next, False, False)

                    while next == 12:
                        menu('Generate', '  Back', '-------', 1, next, True, False)

        while next == 2:
            menu('New Recovery', 'Show xpub', 'Sign transaction', 0, next, True, True)

            if next == 0:
                next = 21
                #Show xpub menu
                while next > 2:
                    while next == 21:
                        menu('-------', 'OK to show', '  Back', 0, next, False, True)

                        if next == 0:
                            next = 211

                            f = open("mnemonic.txt", "r")
                            mnemonic = f.read()
                            f.close()
                            if len(mnemonic) > 0:
                                show_xpub.show_xpub()
                            else:
                                print("There is not a mnemonic in the device")
                                next = 2

                            while next == 211:
                                menu('-------', 'Succesfull', '-OK to exit-', 2, next, False, False)

                    while next == 22:
                        menu('OK to show', '  Back', '-------', 2, next, True, False)

        while next == 3:
            menu('Show xpub', 'Sign transaction', 'Old recovery', 0, next, True, True)

            if next == 0:
                next = 31
                #Sign transaction menu
                while next > 3:
                    while next == 31:
                        menu('-------', 'OK to sign', '  Back', 0, next, False, True)

                        if next == 0:
                            next = 311

                            f = open("mnemonic.txt", "r")
                            mnemonic = f.read()
                            f.close()
                            if len(mnemonic) > 0:
                                psbt.sign_tx()
                            else:
                                print("There is not a mnemonic in the device")
                                next = 3

                            while next == 311:
                                menu('-------', 'Succesfull', '-OK to exit-', 3, next, False, False)

                    while next == 32:
                        menu('OK to sign', '  Back', '-------', 3, next, True, False)

        while next == 4:
            menu('Sign transaction', 'Old recovery', 'Show addresses', 0, next, True, True)

            if next == 0:
                next = 41
                #Old recovery menu
                while next > 4:
                    while next == 41:
                        menu('-------', 'Ok to restore', '  Back', 0, next, False, True)

                        if next == 0:
                            next = 411

                            f = open("mnemonic.txt", "r")
                            mnemonic = f.read()
                            f.close()
                            if len(mnemonic) > 0:
                                print("WARNING: this will delete the previous mnemonic")
                                des = input("Are you sure do you want to continue? [y/n]")

                                while des != "y" and des != "n":
                                    network = input("Invalid input, [continue->\"y\"] or [cancel->\"n\"]: ")

                                if des == "y":
                                    recovery_phrase.recover()
                                else:
                                    next = 4
                            else:
                                recovery_phrase.recover()

                            while next == 411:
                                menu('-------', 'Succesfull', '-OK to exit-', 4, next, False, False)

                    while next == 42:
                        menu('Ok to restore', '  Back', '-------', 4, next, True, False)

        while next == 5:
            menu('Old recovery', 'Show addresses', 'Show mnemonic', 0, next, True, True)

            if next == 0:
                next = 51
                #Show address menu
                while next > 5:
                    while next == 51:
                        menu('-------', 'OK to show', '  Back', 0, next, False, True)

                        if next == 0:
                            next = 511

                            f = open("mnemonic.txt", "r")
                            mnemonic = f.read()
                            f.close()
                            if len(mnemonic) > 0:
                                show_addresses.show_addresses()
                            else:
                                print("There is not a mnemonic in the device")
                                next = 5

                            while next == 511:
                                menu('-------', 'Succesfull', '-OK to exit-', 5, next, False, False)

                    while next == 52:
                        menu('OK to show', '  Back', '-------', 5, next, True, False)

        while next == 6:
            menu('Show addresses', 'Show mnemonic', 'Disconnect', 0, next, True, True)

            if next == 0:
                next = 61
                #Show mnemonic menu
                while next > 6:
                    while next == 61:
                        menu('-------', 'OK to show', '  Back', 0, next, False, True)

                        if next == 0:
                            next = 611

                            f = open("mnemonic.txt", "r")
                            mnemonic = f.read()
                            f.close()
                            if len(mnemonic) > 0:
                                print(mnemonic)
                            else:
                                print("There is not a mnemonic in the device")
                                next = 6

                            while next == 611:
                                menu('-------', 'Succesfull', '-OK to exit-', 6, next, False, False)

                    while next == 62:
                        menu('OK to show', '  Back', '-------', 6, next, True, False)


        while next == 7:
            menu('Show mnemonic', 'Disconnect', '-------', 0, next, True, False)

            if next == 0:
                next = 71
                disconnect()
                if next == 0:
                    oled.fill(0)
                    oled.text('Disconnecting...', 0, 28)
                    oled.show()
                    sleep(2)
                    oled.fill(0)
                    oled.text('BYE BYE', 20, 28)
                    oled.show()
                    sleep(1)
                    oled.fill(0)
                    oled.show()
                    shutdown = False

    print('Fin programa')

if __name__ == '__main__':
    main()











































































































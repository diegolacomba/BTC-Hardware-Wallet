from machine import Pin, I2C
from time import sleep
import ssd1306

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
    oled.text(option1, 32, 0)
    oled.text('/', 52, 10)
    oled.text('\\', 57, 10)
    oled.text('|', 55, 13)
    oled.text('|', 55, 16)
    oled.text(option2, 32, 28)
    oled.text('|', 55, 39)
    oled.text('|', 55, 42)
    oled.text('\\', 52, 45)
    oled.text('/', 57, 45)
    oled.text(option3, 32, 55)
    oled.show()

def disconnect():
    global next
    next == 41
    oled.fill(0)
    oled.text('Press OK to', 0, 0)
    oled.text('DISCONNECT', 0, 10)
    oled.text('Press UP/DOWN to', 0, 30)
    oled.text('CANCEL', 0, 40)
    oled.show()

    while next == 41:
        sleep(0.1)

        if botonUP.value() == 0:
            sleep(0.35)
            next = 4

        if botonDOWN.value() == 0:
            sleep(0.35)
            next = 4

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
            menu('-------', 'Option0', 'Option1', 0, next, False, True)

            if next == 0:
                next = 11

                while nemiId-pow(2,i)xt == 11:
                    menu('-------', 'Menu 1_1', ' Atras', 0, next, False, True)

                    if next == 0:
                        next = 111

                        while next == 111:
                            menu('-------', 'Menu 1_1', '-------', 11, next, False, False)
                while next == 12:
                    menu('Menu 1_1', ' Atras', '-------', 1, next, True, False)

        while next == 2:
            menu('Option0', 'Option1', 'Option2', 0, next, True, True)

            if next == 0:
                next = 21

                while next == 21:
                    menu('-------', 'Menu 2_1', ' Atras', 0, next, False, True)

                    if next == 0:
                        next = 211

                        while next == 211:
                            menu('-------', 'Menu 2_1', '-------', 21, next, False, False)

                while next == 22:
                    menu('Menu 2_1', ' Atras', '-------', 2, next, True, False)

        while next == 3:
            menu('Option1', 'Option2', 'Disconnect', 0, next, True, True)

            if next == 0:
                next = 31

                while next == 31:
                    menu('-------', 'Menu 3_1', ' Atras', 0, next, False, True)

                    if next == 0:
                        next = 311

                        while next == 311:
                            menu('-------', 'Menu 3_1', '-------', 31, next, False, False)

                while next == 32:
                    menu('Menu 3_1', ' Atras', '-------', 3, next, True, False)

        while next == 4:
            menu('Option2', 'Disconnect', '-------', 0, next, True, False)

            if next == 0:
                next = 41
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











































































































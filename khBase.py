from kahoot import client as account
from os import system

bots = []

def add_bots(pin, name, n):
    print(f"\n Sending {n} bots too {pin}...")
    n = int(n)
    index = 0
    while(index != n):
        bot = account()
        bot.join(pin, f"{name}{index + 1}")
        bots.append(bot)
        index += 1
    print("Bots Sent!")

def leave_room():
    print("\n Removing bots...")
    auth = True
    for bot in bots:
        try:
            bot.leave()
        except:
            print("ERROR: There are no bots in mentioned kahoot")
            auth = False
            break  
    bots.clear()
    if(auth == True):
        print("Bots removed!")

def main():
    system("cls")
    auth = False

    print("#=----------------------------=#\n       KahootBotter.live  V1\n          by DarthOCE\n ")
    pin = input(" Insert Kahoot Pin >")
    name = input("Enter the name of the bots >")

    while(auth == False):
        try:
            n = int(input("Enter the number of bots >"))
            auth = True
        except:
            print("ERROR: 'NUMBER OF BOTS' VALUE MUST BE AN INTEGER NUMBER.")
            auth = False

    add_bots(pin, name, n)
    input("(PRESS ENTER TO REMOVE BOTS FROM ROOM)")
    leave_room()
    input("(PRESS ENTER TO GO BACK TO TOP...)")
    main()

if(__name__ == "__main__"):
    main()

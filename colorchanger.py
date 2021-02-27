from socket import socket
import threading
import time
import random

# Settings
# These things are the only things you need to change!
premium = "true" # keep this set to "true" if you have Twitch Prime or Twitch Turbo. If you don't have either of them, set it to "false"
colorChangeMin = 3000 # minimum time between every color change (in milliseconds); don't set this too low!
colorChangeMax = 7500 # maximum time between every color change (in milliseconds)
twitchName = "beatz41" # your Twitch name
twitchOAuthToken = "oauth:***" # your OAuth token; don't remove the PASS at the beginning; get one from: https://twitchapps.com/tmi/
# End of settings; if you changed the settings above, you can now run this script by double-clicking the file OR by opening the console and running "py FILENAME"

print('Script is starting...')

sockt = socket()
regularColors = "Blue", "BlueViolet", "CadetBlue", "Chocolate", "Coral", "DodgerBlue", "Firebrick", "GoldenRod", "Green", "HotPink", "OrangeRed", "Red", "SeaGreen", "SpringGreen", "YellowGreen" # colors that are available for everyone, sorted alphabetically
    
def sendRequest(data):
    sockt.send(bytes(data + '\r\n', 'utf-8')) # sends a request to Twitch's irc server using the UTF-8 standard

def changeColor():
    if premium == "true":
        while True:
            delay = random.choice(range(colorChangeMin, colorChangeMax)) / 1000
            print("Changing color again in " + str(delay) + " seconds!")
            time.sleep(delay)
            randomNumber = random.randint(0, 16777215) # selects a random color; 16777215 stands for the amount of different colors that are available
            hexValue = str(hex(randomNumber))
            sendRequest('PRIVMSG #beatz41 :/color  #' + hexValue[2:])
            print("Changed color to " + hexValue[2:] + "!")
    else:
        while True:
            delay = random.choice(range(colorChangeMin, colorChangeMax)) / 1000
            print("Changing color again in " + str(delay) + " seconds!")
            time.sleep(delay)
            selectedColor = random.choice(regularColors);
            sendRequest('PRIVMSG #beatz41 :/color ' + selectedColor)
            print("Changed color to " + selectedColor + "!")

def keepRunning():
    while True:
        chat = sockt.recv(1024).decode('utf -8', errors='replace') # listens to messages from Twitch
        
        if "PING" in chat:
            sendRequest("PONG") # keeps the script running

def runScript():
    sockt.connect(('irc.chat.twitch.tv', 6667))  # connects to Twitch.tv
    sendRequest("PASS " + twitchOAuthToken) # your OAuth token
    sendRequest("NICK " + twitchName) # your Twitch name
    sendRequest('CAP REQ :twitch.tv/commands')
    sendRequest('CAP REQ :twitch.tv/tags')
    keepRunning()
    
timerr = threading.Thread(target=changeColor)
timerr.start()

runScript()

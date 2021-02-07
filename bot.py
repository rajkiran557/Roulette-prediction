import pyautogui, sys
import time
import json
from PIL import Image, ImageGrab

class Bot:
    def __init__(self, raw_data):
        """Each raw_data element contains 200 output colors. raw_data will be divided into training_data and test_data.
        I-th element of training_data contains 100 colors. The i-th element of test_data are the next 50."""
        self.raw_data = raw_data
        self.current_data = []

    def convertToColor(self, pixel):
        if pixel[0]>250:
            return "RED"
        elif pixel[1]>250:
            return "GREEN"
        elif pixel[0]>55 and pixel[0]<65:
            return "BLACK"
        else:
            return "Error. Couldn't detect any color."

    def saveData(self, pixel):
        if pixel[0]>250: 
            self.current_data.append(-1) # red
        elif pixel[1]>250:
            self.current_data.append(0) # green
        elif pixel[0]>55 and pixel[0]<65:
            self.current_data.append(1) # black
        else:
            print("Error. Couldn't detect any color.")

    def save(self, filename):
        self.raw_data.append(self.current_data)
        data = {"raw_data": self.raw_data}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()

def load(filename):
    """Loads the raw_data array"""
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    bot = Bot(data["raw_data"])
    return bot

if __name__ == '__main__': 
    #uncomment the first time you execute the program
    #raw_data = []
    #bot = Bot(raw_data)

    for i in range(0,16):
        start=time.time()
        bot = load("data.txt") # comment this the first time you execute
        first=1;
        print('Press Ctrl-C to quit.')
        try:
            for i in range(1,201): 
                if first:
                    first=0
                    pyautogui.click(795, 705) # punta 1 euro
                    pyautogui.click(870, 690) # rosso
                    time.sleep(1)
                pyautogui.click(900, 900) # gira
                time.sleep(2)
                pixels = ImageGrab.grab(bbox =(1268, 320, 1269, 321)).load()
                bot.saveData(pixels[0,0])
                #print(f"{i}: {bot.convertToColor(pixels[0,0])}")
            bot.save("data.txt")
            #print(f"Ci ho messo {time.time()-start} secondi.")
        except KeyboardInterrupt:
            print('Ending...')
    

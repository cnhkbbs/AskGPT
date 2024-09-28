import pyautogui
import pynput.mouse as Mouse
import pynput.keyboard as Keyboard
import clipboard
from chromectrl import ChromeCtrl


class Controller:
    # Mouse and Keyboard
    mouse = Mouse.Controller()
    keyboard = Keyboard.Controller()

    # Listener state
    server_state = False

    copy_text = ''
    is_pressed = False

    def __init__(self, message_queue, phone_borad):
        self.message_queue = message_queue
        self.phone_borad = phone_borad
        self.chrome = ChromeCtrl(message_queue)
        try:
            self.keyboard_listener = Keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.keyboard_listener.start()
        except Exception:
            print(Exception)

    def set_server_state(self, state):
        self.server_state = state

    def on_press(self, key):
        try:
            if key == Keyboard.Key.tab:
                self.change_state()
            if self.server_state:
                if not self.is_pressed:
                    if key.char == 'q' or key.char == 'w':
                        self.mouse.press(Mouse.Button.left)
                        self.is_pressed = True
                if key.char == 'e':
                    self.chrome.call_gpt()
                elif key.char == 'r':
                    self.chrome.get_element()
                elif key.char == 't' and self.phone_borad:
                    self.chrome.get_response_content()
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if self.is_pressed and self.server_state:
                if key.char == 'q' or key.char == 'w':
                    self.mouse.release(Mouse.Button.left)
                    self.is_pressed = False
                if key.char == 'q':
                    self.get_selected_text()
                    self.chrome.clear_textarea()
                    self.chrome.fill_textarea(self.copy_text)
                    self.chrome.call_gpt()
                elif key.char == 'w':
                    self.get_selected_text()
                    self.chrome.fill_textarea(self.copy_text)
        except AttributeError:
            pass

    def change_state(self):
        if self.server_state:
            for i in range(6):
                print("▄" * 100)
            self.server_state = False
        else:
            if self.chrome.get_element():
                for i in range(6):
                    print("." * 100)
                self.server_state = True
                if self.phone_borad:
                    self.chrome.minimize()
            else:
                self.server_state = False

    def get_selected_text(self):
        pyautogui.hotkey('ctrl', 'c')
        self.copy_text = clipboard.get_text()


def start_listen(message_queue, phone_borad):
    print("Starting keyboard listener...")
    control = Controller(message_queue, phone_borad)
    while True:
        try:
            if control.keyboard_listener is None or not control.keyboard_listener.is_alive():
                control.keyboard_listener = Keyboard.Listener(on_press=control.on_press, on_release=control.on_release)
                control.keyboard_listener.start()
            elif control.keyboard_listener.is_alive():
                control.keyboard_listener.join()
        except Exception as e:
            print(e)

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
from config import exception_info, runtime_info, chrome_config


class ChromeCtrl:
    # 浏览器驱动选项
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    service = ChromeService(executable_path=chrome_config.CHROME_DRIVER_PATH)

    def __init__(self, message_queue):
        print(runtime_info.starting_chrome)
        self.submit_element = None
        self.textarea = None
        self.message_queue = message_queue
        self.driver = Chrome(service=self.service, options=self.options)
        self.driver.execute_cdp_cmd(chrome_config.CHROME_CMD, chrome_config.CHROME_CMD_ARGS)
        self.driver.maximize_window()
        self.driver.get(chrome_config.GPT_URL)

    def get_element(self):
        try:
            self.textarea = self.driver.find_element(By.XPATH, chrome_config.TEXTAREA_XPATH)
            self.submit_element = self.driver.find_element(By.XPATH, chrome_config.SUBMIT_XPATH)
            print(runtime_info.get_element)
            return True
        except NotImplementedError:
            print(exception_info.NotImplementedError)
            return False
        except Exception:
            print(exception_info.get_element_exception)
            return False

    def call_gpt(self):
        try:
            if self.textarea is not None:
                textarea_content = self.get_textarea_content()
            else:
                return False
            if textarea_content is not None or textarea_content == '':
                print(f"ask: {textarea_content}")
                if self.submit_element is not None:
                    self.submit_element.click()
                    return True
        except NotImplementedError:
            print(exception_info.NotImplementedError)
        except Exception as e:
            print(exception_info.call_gpt_exception)
            return False

    def get_textarea_content(self):
        js_executor = self.driver.execute_script
        try:
            textarea_content = js_executor("return arguments[0].value;", self.textarea)
            return textarea_content
        except Exception as e:
            print(exception_info.get_textarea_exception)
            return None

    def fill_textarea(self, text):
        if self.textarea is None:
            return
        try:
            self.textarea.send_keys(text)
            print(runtime_info.fill_textarea)
        except Exception as e:
            print(exception_info.fill_textarea_exception)

    def clear_textarea(self):
        if self.textarea is None:
            return False
        self.textarea.clear()

    def get_response_content(self):
        try:
            response = self.driver.find_elements(By.CLASS_NAME, chrome_config.RESPONSE_ELEMENT_CLASS_NAME)
            if len(response) == 0:
                return None
            anser_element = response[-1]
            anser_content = anser_element.get_attribute('outerHTML')
            self.message_queue.put(anser_content)
            return anser_content
        except Exception as e:
            print(exception_info.get_response_content_exception)
            return None

    def maximize(self):
        self.driver.maximize_window()

    def minimize(self):
        self.driver.minimize_window()

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


bcolor = Bcolors()
instructions = [
    ("User guide", ""),
    ("Tab", "start the keyboard control"),
    ("Q", "Press down to select sentences, release to ask the Bot."),
    ("W", "Press down to select sentences,release to fill in the textarea."),
    ("E", "Ask the Bot."),
    ("R", "Retrieve the web page element"),
    ("T", "Synchronize response to other devices(Mobile Phone Whiteboard)")
]

max_key_width = max(len(key) for key, _ in instructions)

whote_board_instructions = bcolor.OKGREEN + ("Start the Mobile Phone Whiteboard? (Type 1 for 'yes' 2 for 'no' ) \n In "
                                             "this way you can view the response on your phone\n") + bcolor.ENDC


class ChromeConfig:
    CHROME_DRIVER_PATH = r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    CHROME_CMD = "Page.addScriptToEvaluateOnNewDocument"
    CHROME_CMD_ARGS = {"source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """}

    GPT_URL = "https://tongyi.aliyun.com/qianwen/"
    TEXTAREA_XPATH = '/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[1]/div/textarea'
    SUBMIT_XPATH = '/html/body/div[1]/div/div[3]/div/div[2]/div[1]/div[3]/div[4]/div[2]/span'
    RESPONSE_ELEMENT_CLASS_NAME = "tongyi-markdown"


class ExceptionInfo:
    NotImplementedError = bcolor.FAIL + "NotImplementedError" + bcolor.ENDC
    call_gpt_exception = bcolor.FAIL + "error at call_gpt()" + bcolor.ENDC
    get_element_exception = bcolor.FAIL + "error at get_element" + bcolor.ENDC
    get_textarea_exception = bcolor.FAIL + "error at get_textarea" + bcolor.ENDC
    fill_textarea_exception = bcolor.FAIL + "error at fill_textarea" + bcolor.ENDC
    get_response_content_exception = bcolor.FAIL + "error at get_response_content" + bcolor.ENDC
    invalid_input = bcolor.FAIL + "Invalid input" + bcolor.ENDC


class RuntimeInfo:
    get_element = "get_element success"
    fill_textarea = "fill_textarea success"
    starting_chrome = "starting chrome....."


server_port = 8848
open_port_command = 'netsh advfirewall firewall add rule name="Allow TCP Port ' + str(server_port) +'" protocol=TCP localport=' + str(server_port) +' dir=in action=allow'
close_port_command = 'netsh advfirewall firewall delete rule name="Allow TCP Port ' + str(server_port) +'"'

exception_info = ExceptionInfo()
runtime_info = RuntimeInfo()
chrome_config = ChromeConfig()

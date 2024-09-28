import ctypes
import config


async def open_tcp_port():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", 'cmd.exe', '/c ' + config.open_port_command, None, 0)


async def close_tcp_port():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", 'cmd.exe', '/c ' + config.close_port_command, None, 0)

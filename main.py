import multiprocessing
from multiprocessing import Process

import config
import controller
import server


def guide():
    for key, desc in config.instructions:
        print(f'{key:<{config.max_key_width}} {desc}')

    while True:
        try:
            command = input(config.whote_board_instructions)
            if command == '1':
                return True
            elif command == '2':
                return False
            else:
                print(config.exception_info.invalid_input)
                continue
        except ValueError:
            print(ValueError)
            continue


if __name__ == '__main__':
    phone_borad = guide()
    # Message queue for inter-process communication
    message_queue = multiprocessing.JoinableQueue()
    # WebBrowser and Keyboard control process
    control_process = Process(target=controller.start_listen, args=(message_queue, phone_borad))
    processes = [control_process]
    if phone_borad:
        server_process = Process(target=server.start_server, args=(message_queue,))
        processes.append(server_process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

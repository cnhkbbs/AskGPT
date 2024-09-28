import asyncio
import multiprocessing
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse

import config
import portctrl
from html import index as indexpage
import socket
import qrcode_terminal

app = FastAPI()

message_queue = None
connected_clients = []
message_queue_listening = False


@app.get("/", response_class=HTMLResponse)
async def index(background_tasks: BackgroundTasks):
    if not message_queue_listening:
        background_tasks.add_task(listen_for_messages)
    return HTMLResponse(content=indexpage, status_code=200)


# WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global connected_clients
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        if websocket in connected_clients:
            connected_clients.remove(websocket)


@app.on_event("startup")
async def app_startup():
    global message_queue
    await portctrl.open_tcp_port()


@app.on_event("shutdown")
async def app_shutdown():
    global message_queue
    await portctrl.close_tcp_port()
    message_queue.put("Application is shutting down...")


async def listen_for_messages():
    global connected_clients, message_queue, message_queue_listening
    print("listening multiprocess queue")
    message_queue_listening = True
    while True:
        try:
            try:
                content = message_queue.get_nowait()
            except multiprocessing.queues.Empty:
                content = None
                pass
            if content is not None:
                if content == "Application is shutting down...":
                    return
                for client in connected_clients[:]:
                    try:
                        await client.send_text(content)
                    except WebSocketDisconnect:
                        if client in connected_clients:
                            connected_clients.remove(client)
        except Exception as e:
            print(f"error at update_content: {str(e)}")
        await asyncio.sleep(1)


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def start_server(queue):
    global message_queue
    message_queue = queue
    print("starting server")
    host_ip = get_host_ip()
    qrcode_terminal.draw('http://' + host_ip + ':' + str(config.server_port))
    try:
        uvicorn.run(app, host=str(host_ip), port=config.server_port)
    except Exception as e:
        print(f"Error starting server: {str(e)}")

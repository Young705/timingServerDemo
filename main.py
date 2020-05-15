import asyncio
import websockets
import random,time,threading
websocket_users = set()

#定时单方向传送信息
async def only_ecv_user_msg(websocket):
        time.sleep(1)
        print('thread %s is running...' % threading.current_thread().name)
        response_text = str(random.randint(1,12))
        print("response_text:", response_text)
        await websocket.send("timing info->"+response_text)

#随时接受用户信息并返回记录
async def recv_user_msg(websocket):
        print('thread %s is running...' % threading.current_thread().name)
        recv_text = await websocket.recv()
        print("recv_text:", recv_text)
        response_text = f"Server return:{recv_text}"
        print("response_text:", response_text)
        await websocket.send(response_text)


async def run(websocket, path):
    while True:
        try:
            await only_ecv_user_msg(websocket)
            await recv_user_msg(websocket)
        except websockets.ConnectionClosed:
            print("ConnectionClosed...", path)
            print("websocket_users old:", websocket_users)
            websocket_users.remove(websocket)
            print("websocket_users new:", websocket_users)
            break
        except websockets.InvalidState:
            print("InvalidState...")
            break
        except Exception as e:
            print("Exception:", e)

if __name__ == '__main__':
    print("127.0.0.1:10011 websocket...")
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, "127.0.0.1", 10011))
    asyncio.get_event_loop().run_forever()






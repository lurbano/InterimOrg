import asyncio
from aiohttp import web, ClientSession
from datetime import datetime
import json
import os
#from getIP import getIP
from uAio import *

# database
from db.InterimDBs import studentDB
from db.InterimDBs import sessionDB
StuDB = studentDB()
SesDB = sessionDB()

dir_path = os.path.dirname(os.path.abspath(__file__))

async def handle(request):
    with open(dir_path+"/"+"index.html", "r") as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type='text/html')

async def handlePost(request):
    data = await request.json()
    rData = {}
    print(data)
    # print(data["action"], data["value"])

    if data['action'] == "getTime":
        now = datetime.now()
        print(now.ctime())
        rData['item'] = "time"
        rData['status'] = now.ctime() # a string representing the current time

    if data['action'] == 'showStudents':
        info = data['value']
        
        everything = { "students": StuDB.getStudents(), "sessions": SesDB.getAll()}
        
        rData['item'] = 'everything'
        rData['status'] = everything

    if data['action'] == 'getSessions':
        info = data['value']
        
        rData['item'] = 'sessions'
        rData['status'] = SesDB.getAll()

    if data['action'] == 'addSession':
        info = data['value']
        print("info:", info)

        SesDB.add_session(info['sessionName'], info['sessionFaculty'], info['sessionStudentLead'], info['sessionLocation'])
        
        rData['item'] = 'addSession'
        rData['status'] = 'Added Session'


    if data['action'] == 'updateStudentSession':
        info = data['value'].split("@")
        student = info[0]
        session = info[1]
        dayTime = info[2]

        
        rData['item'] = 'updateStudentSession'
        rData['status'] = StuDB.updateStudentSession(student, session, dayTime)

    response = json.dumps(rData)
    print("Response: ", response)
    return web.Response(text=response, content_type='text/html')

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_post("/", handlePost)

    # Serve static files from the "static" directory
    static_path = os.path.join(os.path.dirname(__file__), 'static')
    app.router.add_static('/static/', path=static_path, name='static')
    
    runner = web.AppRunner(app)
    await runner.setup()
    port = 17320

    host = getIP()
    site = web.TCPSite(runner, host, port)  # Bind to the local IP address
    await site.start()
    print(f"Server running at http://{host}:{port}/")

    # asyncio.create_task(print_hello())
    # asyncio.create_task(getLightLevel(dt=5))

    '''Testing post request'''
    # await postRequest("192.168.1.142:8000", action="Rhythmbox", value="play")
    # await postRequest("192.168.1.142:8000", action="Rhythmbox", value="play")

    await asyncio.Event().wait()  # Keep the event loop running

if __name__ == '__main__':
    asyncio.run(main())
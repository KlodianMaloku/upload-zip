import asyncio

import socketio

from shikimi.core.index import ask

sio = socketio.AsyncServer(async_mode='asgi',
                           cors_allowed_origins=[
                               'http://localhost:3000',
                               'https://techdebtgpt.ngrok.io',
                               'https://app.techdebtgpt.com'
                           ])


async def generate_large_text(input_text: str, sid: str):
    large_text = input_text * 100  # example
    for char in large_text:
        await sio.emit('large_text', char)
        await asyncio.sleep(0.01)


# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def disconnect(sid):
    print("disconnect ", sid)


@sio.event
async def text_message(sid, data):
    print("message ", data)
    parsed_message = data.split('@@@')
    await ask(parsed_message[1], parsed_message[0], answer_text_message, sid)


@sio.event
async def start_overview(sid, data):
    print("message ", data)
    parsed_message = data.split('@@@')
    await ask(parsed_message[1], parsed_message[0], overview_token, sid)


@sio.event
async def overview_token(sid, data):
    await sio.emit('overview_token', data, sid)


@sio.event
async def answer_text_message(sid, data):
    await sio.emit('answer_text_message', data, sid)


@sio.event
async def repo_scanning_started(sid, data):
    print("message ", data)
    await sio.emit('repo_scanning_started', 'Scanning the repo started.....')


@sio.event
async def repo_scanning_finished(sid, data):
    print("message ", data)
    await sio.emit('repo_scanning_finished', 'Scanning the repo finished. You can start asking the super intelligent'
                                             ' techdebt analyser. :) ')

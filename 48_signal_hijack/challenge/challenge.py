#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目48: 信号劫持
难度: 大师
漏洞点: 连 __builtins__ 名字都被封死，exec 命名空间里的钥匙只能靠 globals() 挖
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337
BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'popen', 'signal', 'eval', 'exec', 'compile', 'builtins', '__class__', '__base__', '__subclasses__', '__globals__', 'catch_', '_wrap_', 'sys', 'modules']

def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #48 ===\n")
        conn.sendall(b"Even the name of __builtins__ is burned. Dig with globals().\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return

        exec(data, {"__builtins__": __builtins__})
    except Exception as e:
        conn.sendall(("Error: " + repr(e)).encode() + b"\n")
    finally:
        conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(16)
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle, args=(conn,), daemon=True).start()


if __name__ == '__main__':
    main()

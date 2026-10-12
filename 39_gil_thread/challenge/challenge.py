#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目39: GIL 与线程逃逸
难度: 地狱
漏洞点: 单线程沙箱，但可用 threading 起子线程，在子线程中修改沙箱状态
        或利用 GIL 释放时机绕过检查
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
             'eval', 'exec', 'compile', 'open', 'read', 'FLAG', '__class__',
             '__base__', '__subclasses__', '__globals__', '__builtins__',
             '__init__', '__mro__', '__bases__', 'marshal', 'CodeType', 'opcode']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #39 ===\n")
        conn.sendall(b"Single-threaded. But threads can rewrite state.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        result = eval(data, {"__builtins__": __builtins__, "threading": threading})
        conn.sendall(str(result).encode() + b"\n")
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
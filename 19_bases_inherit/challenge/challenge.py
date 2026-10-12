#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目19: bases 继承逃逸
难度: 进阶
漏洞点: 过滤 __mro__ 与 __subclasses__，但 __bases__ 可逐层爬回 object
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['__mro__', '__subclasses__', 'import', 'os', 'system', 'environ', 'getenv', 'popen']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #19 ===\n")
        conn.sendall(b"__mro__ and __subclasses__ banned. __bases__ is your only ladder.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        result = eval(data, {"__builtins__": __builtins__})
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
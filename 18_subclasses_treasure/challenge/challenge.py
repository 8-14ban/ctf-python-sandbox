#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目18: subclasses 宝库
难度: 进阶
漏洞点: 禁 builtins，但 object.__subclasses__() 可枚举所有类，从其中偷 builtins/os
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['__builtins__', 'import', 'os', 'system', 'environ', 'getenv', 'popen', 'eval']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #18 ===\n")
        conn.sendall(b"builtins untouched, but scanning stops at words. subclasses() is a treasure vault.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        # 仅过滤字面量；builtins 仍完整，但关键词需拼接
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
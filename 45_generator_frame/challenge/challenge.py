#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目45: 生成器墓穴
难度: 大师
漏洞点: 空内置，唯一活物是一个挂起的生成器对象
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337
BLACKLIST = ['sys', '_getframe', 'catch_', '_wrap_', 'subclasses', 'environ', 'FLAG', 'gi_', '__globals__']

DORMANT = (i for i in range(3))

def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #45 ===\n")
        conn.sendall(b"One key: getattr. One corpse: a dormant generator.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return

        result = eval(data, {"__builtins__": {"getattr": getattr}, "gen": DORMANT})
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目23: getattr 链式
难度: 进阶
漏洞点: 过滤点号 . 与下划线魔法字面量，但 getattr 可以逐级动态拼属性
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['.', '__class__', '__base__', '__bases__', '__mro__', '__subclasses__',
             '__globals__', '__init__', 'import', 'os', 'system', 'environ']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #23 ===\n")
        conn.sendall(b"Dots and magic names banned. getattr() builds the whole road.\n")
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
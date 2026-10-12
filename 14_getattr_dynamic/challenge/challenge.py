#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目14: getattr 动态调用
难度: 入门
漏洞点: 关键属性名被黑名单过滤，但 getattr(obj, name) 可在运行时用拼接的字符串调用
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['__class__', '__bases__', '__subclasses__', '__globals__', '__mro__',
             '__init__', 'import', 'os', 'system', 'environ', 'getenv']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #14 ===\n")
        conn.sendall(b"Magic attribute names are banned in source.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        # getattr 内置可用，属性名可拼接绕过黑名单
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
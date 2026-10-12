#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目38: opcode 拼接
难度: 地狱
漏洞点: 过滤了所有关键词，但可用 opcode 级别的操作码拼接出可执行代码，
        通过 __code__ 替换或 ctypes 调用
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
        conn.sendall(b"=== Python Sandbox #38 ===\n")
        conn.sendall(b"Words banned. Opcodes don't have words.\n")
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目29: 内存底层的低语
难度: 困难
漏洞点: 字符串、字节码都被盯防，但 memoryview/buffer 直接读写底层内存，
        可绕过一切高层过滤
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
             '__import__', 'eval', 'exec', 'open', 'read', 'FLAG']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #29 ===\n")
        conn.sendall(b"Watches strings and bytecode. memoryview still sees the raw bytes.\n")
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
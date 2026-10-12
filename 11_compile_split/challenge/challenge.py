#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目11: compile 分片与转义
难度: 入门
漏洞点: 黑名单过滤字面量，但 Python 字符串支持 unicode/八进制转义，可重造字符
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['_', 'import', 'os', 'system', 'popen', 'environ', 'getenv', 'open', 'exec']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #11 ===\n")
        conn.sendall(b"Raw substrings banned. But escape sequences can rebuild them.\n")
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目25: 无内置之日
难度: 困难
漏洞点: __builtins__ 置空，但 object 的类树里有 warning.catch_warnings，
        其 __init__.__globals__['__builtins__'] 藏着完整内置
目标: 恢复内置函数，读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #25 ===\n")
        conn.sendall(b"No builtins. But they hide in a warning class's globals.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        ns = {"__builtins__": {}}
        result = eval(data, ns)
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
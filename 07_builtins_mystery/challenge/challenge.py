#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目07: __builtins__ 之谜
难度: 零基础
漏洞点: 把 __builtins__ 置为 None，但可从任意对象的内置函数恢复
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #7 ===\n")
        conn.sendall(b"__builtins__ is disabled. No builtins for you!\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        # 把 builtins 置为 None，但对象仍携带可恢复入口
        result = eval(data, {"__builtins__": None})
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
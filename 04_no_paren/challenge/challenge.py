#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目04: 括号禁区
难度: 零基础
漏洞点: 过滤 "("，但可用装饰器 @ 隐式调用函数
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #4 ===\n")
        conn.sendall(b"No parentheses ( allowed!\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        if "(" in data:
            conn.sendall(b"( not allowed!\n")
            return
        # 用 exec 执行，可借助装饰器 @ 隐式调用函数
        ns = {"__builtins__": __builtins__}
        exec(data, ns)
        conn.sendall(b"executed.\n")
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
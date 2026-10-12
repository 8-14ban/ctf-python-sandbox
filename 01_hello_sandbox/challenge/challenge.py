#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目01: 首沙箱 Hello 不执行
难度: 零基础
漏洞点: 过度信任 eval + 无任何过滤
目标: 逃逸读取环境变量 FLAG
"""
import socket
import sys
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def banner(sock):
    sock.sendall(b"=== Python Sandbox #1 ===\n")
    sock.sendall(b"Welcome! Enter your Python expression. We eval() it for you.\n")
    sock.sendall(b">>> ")


def handle(conn):
    try:
        banner(conn)
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        # 洞一：直接 eval 用户输入，无任何过滤，甚至可以 exec 语句
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
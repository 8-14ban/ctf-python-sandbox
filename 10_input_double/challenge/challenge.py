#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目10: 双重 eval（输入的二重身份）
难度: 入门
漏洞点: 先 eval 你的表达式，若结果是字符串又 eval 一次 —— 二次注入
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #10 ===\n")
        conn.sendall(b"We eval() twice: once on your code, again on its string result.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        ns = {"__builtins__": __builtins__}
        first = eval(data, ns)          # 第一次 eval
        if isinstance(first, str):
            conn.sendall(b"[second eval]\n")
            second = eval(first, ns)    # 第二次 eval —— 注入点
            conn.sendall(str(second).encode() + b"\n")
        else:
            conn.sendall(str(first).encode() + b"\n")
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
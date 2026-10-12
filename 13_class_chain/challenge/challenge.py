#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目13: class 链（第一课：从对象到 object）
难度: 入门
漏洞点: 过滤 __builtins__，但 () 对象的 __class__ 链可爬到 object 及所有子类
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #13 ===\n")
        conn.sendall(b"builtins off. But every object carries its class chain.\n")
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
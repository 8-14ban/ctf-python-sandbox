#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目15: dir() 侦察
难度: 入门
漏洞点: 沙箱暴露了 dir()，可内省出所有可用对象/属性，再逐一利用
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #15 ===\n")
        conn.sendall(b"dir() is open. Recon first, then exploit.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        # 暴露的全局里有 dir、help、vars、print，但不给 __import__ 之外的太多
        ns = {"__builtins__": __builtins__, "dir": dir, "help": help,
              "vars": vars, "print": print}
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
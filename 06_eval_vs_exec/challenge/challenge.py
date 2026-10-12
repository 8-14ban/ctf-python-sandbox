#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目06: eval vs exec
难度: 零基础
漏洞点: 用 eval 时无法直接写语句，但可通过 __import__ 或恢复 exec 逃逸
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #6 ===\n")
        conn.sendall(b"Only eval() here, no exec(). Statements won't run.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        # 只 eval，全局给足 __builtins__，eval 里可调用 __import__ 做一切
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
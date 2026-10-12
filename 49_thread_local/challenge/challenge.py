#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目49: 线程密室
难度: 大师
漏洞点: 空内置，钥匙藏在普通对象的普通属性里，所有常规链路词被封
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337
BLACKLIST = ['getattr', 'catch_', '_wrap_', 'builtins', 'import', 'environ', 'FLAG', 'modules', 'sys']

BOX = type("Box", (), {"data": vars(__builtins__)})()

def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #49 ===\n")
        conn.sendall(b"Empty builtins. A plain box object. Everything else is mined.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return

        result = eval(data, {"__builtins__": {}, "box": BOX})
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目46: 指针覆写
难度: 大师
漏洞点: exec 模式但黑名单巨长，连 __dict__ 都被封
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337
BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'popen', 'ctypes', 'eval', 'exec', 'compile', 'open', 'FLAG', '__class__', '__subclasses__', '__globals__', '__init__', '__dict__', 'sys', 'modules', 'catch_', '_wrap_', 'builtins']

def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #46 ===\n")
        conn.sendall(b"Huge blacklist. Even __dict__ is gone.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return

        exec(data, {"__builtins__": __builtins__})
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

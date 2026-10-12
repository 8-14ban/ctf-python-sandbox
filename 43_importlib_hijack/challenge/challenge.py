#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目43: 导入器劫持
难度: 大师
漏洞点: __import__ 被替换为白名单假货，真导入器埋在类树深处
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337
BLACKLIST = ['builtins', '_module', 'catch_', '_wrap_', 'sys', 'modules', 'environ', 'FLAG']

ALLOWED_MODULES = ('math', 'json')


def fake_import(name, *a, **k):
    if name in ALLOWED_MODULES:
        return __import__(name, *a, **k)
    raise ImportError("module locked: " + name)

def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #43 ===\n")
        conn.sendall(b"__import__ is ours now. Whitelist: math, json only.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return

        result = eval(data, {"__builtins__": {"__import__": fake_import, "getattr": getattr}})
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

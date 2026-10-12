#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目26: 字节码注入
难度: 困难
漏洞点: 字符串被逐字过滤，但可把代码编成字节码(code object)再加载执行
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'popen', 'open', 'read', 'FLAG',
             '__import__', 'eval', 'exec']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #26 ===\n")
        conn.sendall(b"Source is scanned hard. But bytecode has no words.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        # 保留 compile 与 types/marshal 相关可用路径，源码层扫描才叫挑战
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
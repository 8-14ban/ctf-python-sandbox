#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目32: 覆盖过滤函数
难度: 困难
漏洞点: 沙箱用 filter() 做黑名单，但 filter 本身可被替换/篡改，
        或利用其闭包/默认参数绕过
目标: 篡改过滤逻辑，读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #32 ===\n")
        conn.sendall(b"The filter() is the gate. But gates can be rewritten.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
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
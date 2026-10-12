#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目12: 编码混淆（base64）
难度: 入门
漏洞点: 黑名单过滤明文，但可用 base64 编码载荷再解码执行
目标: 逃逸读取环境变量 FLAG
"""
import base64
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['import', 'os', 'system', 'popen', 'environ', 'getenv', 'open', 'read', 'FLAG']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #12 ===\n")
        conn.sendall(b"Plaintext is scanned. Encoded payloads slip through.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        # 全局保留 base64 与 exec，方便"合法"编码执行
        result = eval(data, {"__builtins__": __builtins__, "b64": base64})
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
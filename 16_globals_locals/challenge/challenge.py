#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目16: globals/locals 侦察
难度: 入门
漏洞点: 沙箱在命名空间里藏了 os 模块对象 _os，黑名单只过滤源码；locals() 可翻出它
目标: 逃逸读取环境变量 FLAG
"""
import os
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'FLAG', 'popen']


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #16 ===\n")
        conn.sendall(b"A handle to 'os' is hidden among the local names. Recon it.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        # 刻意把 os 模块以隐藏名注入，并在局部藏一个字符串，供 locals() 掘出
        _honest_os_module = os
        result = eval(data, {"__builtins__": __builtins__, "_honest_os_module": _honest_os_module})
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
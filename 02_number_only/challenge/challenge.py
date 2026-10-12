#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目02: 数字陷阱
难度: 零基础
漏洞点: 只放行数字/符号/三个别名 B g c，所有字母必须用 chr() 逐个拼出
目标: 逃逸读取环境变量 FLAG
"""
import builtins
import re
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

# 仅放行数字、常用符号，以及 globals 提供的三个别名 B / g / c
ALLOWED = re.compile(r"^[Bgc0-9+\-*/.(),' \n=:\[\]]+$")


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #2 ===\n")
        conn.sendall(b"No letters allowed (except your tools: B, g, c).\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        if not ALLOWED.match(data):
            conn.sendall(b"Not allowed: contains forbidden characters\n")
            return
        # B = builtins 字典, g = getattr, c = chr
        # 其余一切字母都必须用 c(数字) 现场构造
        ns = {"B": vars(builtins), "g": getattr, "c": chr}
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
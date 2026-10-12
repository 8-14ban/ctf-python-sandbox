#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目08: 无声的沙箱（无回显）
难度: 零基础
漏洞点: 正常执行结果不回显，但异常会回显 traceback 局部信息
目标: 盲逃逸，通过异常侧信道读取 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #8 ===\n")
        conn.sendall(b"No output for you. Only silence...\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        # 正常结果不回显，只回一句执行成功
        ns = {"__builtins__": __builtins__}
        eval(data, ns)
        conn.sendall(b"ok\n")
    except Exception as e:
        # 异常会回显，可作盲侧信道
        conn.sendall(("ERR: " + str(e)).encode() + b"\n")
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
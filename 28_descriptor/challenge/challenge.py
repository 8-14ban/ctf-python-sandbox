#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目28: 描述符协议
难度: 困难
漏洞点: 沙箱重写 __getattribute__ 拦截属性访问，但描述符协议有优先级，
        可用 __class__ 或 __dict__ 绕过
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337


class Guard:
    def __getattribute__(self, name):
        if name.startswith('__'):
            raise AttributeError("magic blocked")
        return object.__getattribute__(self, name)


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #28 ===\n")
        conn.sendall(b"__getattribute__ guards magic names. Descriptors have priority.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        # 给一个 Guard 实例，其 __getattribute__ 拦截 __ 开头属性
        # 但 __class__ 是类型描述符，优先级高于实例 __getattribute__
        result = eval(data, {"__builtins__": __builtins__, "g": Guard()})
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
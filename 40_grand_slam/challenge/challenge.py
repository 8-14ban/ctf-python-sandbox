#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目40: 终极大满贯
难度: 地狱
漏洞点: 无内置、无globals、全过滤、纯字节码出网，
        需要组合所有技巧：对象图爬取+字节码构造+底层内存操作
目标: 逃逸读取环境变量 FLAG
"""
import ast
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
             'eval', 'exec', 'compile', 'open', 'read', 'write', 'FLAG',
             '__class__', '__base__', '__subclasses__', '__globals__',
             '__builtins__', '__init__', '__mro__', '__bases__', 'marshal',
             'CodeType', 'opcode', 'ctypes', 'memoryview', 'sys', 'threading']


def ast_check(code):
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                return False
            if isinstance(node, ast.Attribute) and node.attr.startswith('__'):
                return False
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('eval', 'exec', 'compile'):
                return False
    except:
        return False
    return True


def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #40 ===\n")
        conn.sendall(b"FINAL: no builtins, no globals, full filter, bytecode only.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        if not ast_check(data):
            conn.sendall(b"AST check failed\n")
            return
        # 空内置，但刻意留两把钥匙 getattr / globals —— AST 与黑名单围堵其一切用法
        ns = {"__builtins__": {"getattr": getattr, "globals": globals}}
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
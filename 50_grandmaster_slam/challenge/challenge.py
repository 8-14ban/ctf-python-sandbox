#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目50: 宗师大满贯
难度: 大师
漏洞点: AST 拦 dunder 属性与 getattr/globals 直呼，空内置仅一把 G，黑名单覆盖全部拼接词
目标: 逃逸读取环境变量 FLAG
"""
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses
import ast

HOST = '0.0.0.0'
PORT = 1337
BLACKLIST = ['environ', 'FLAG', 'import', 'os', 'sys', 'modules', 'catch_', '_wrap_close', 'builtins', '__subclasses__', '__globals__', 'getattr', 'globals', 'warnings', '_module']


def ast_check(code):
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                return False
            if isinstance(node, ast.Attribute) and node.attr.startswith('__'):
                return False
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('getattr', 'globals', 'eval', 'exec', 'compile'):
                return False
    except Exception:
        return False
    return True

def handle(conn):
    try:
        conn.sendall(b"=== Python Sandbox #50 ===\n")
        conn.sendall(b"GRANDMASTER: AST + empty builtins + one key G. Everything else burned.\n")
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

        result = eval(data, {"__builtins__": {}, "G": getattr})
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
题目33: 多层过滤叠加
难度: 地狱
漏洞点: AST检查+关键字黑名单+字符白名单三重过滤，但AST只查属性不查Name，
        __builtins__ 作为Name可访问
目标: 逃逸读取环境变量 FLAG
"""
import ast
import socket
import threading
import warnings  # 确保 catch_warnings 注册到 subclasses

HOST = '0.0.0.0'
PORT = 1337

BLACKLIST = ['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
             'eval', 'exec', 'compile', 'open', 'read', 'write', 'FLAG']
ALLOWED_CHARS = set(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789_+-*/.()\'", \n=:[]<>!&|^~')


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
        conn.sendall(b"=== Python Sandbox #33 ===\n")
        conn.sendall(b"Triple filter: AST + blacklist + charset.\n")
        conn.sendall(b">>> ")
        data = conn.recv(4096).decode('utf-8', 'ignore').strip()
        if not data:
            return
        for w in BLACKLIST:
            if w in data:
                conn.sendall(("blocked: " + w).encode() + b"\n")
                return
        if not all(c in ALLOWED_CHARS for c in data):
            conn.sendall(b"charset violation\n")
            return
        if not ast_check(data):
            conn.sendall(b"AST check failed\n")
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
#!/bin/bash
# 题目入口：保留 FLAG 环境变量（由平台以 docker run -e FLAG=xxx 动态注入），
# 直接启动沙箱服务。选手需在沙箱内逃逸读取 FLAG 环境变量。
exec python3 /app/challenge.py
FROM python:3.11-slim

WORKDIR /app

# 沙箱源码由每题的 challenge/challenge.py 提供
COPY challenge/challenge.py /app/challenge.py
COPY challenge/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 动态 FLAG 通过环境变量注入，启动脚本负责落盘到 /tmp/flag
# 平台/调度器以 docker run -e FLAG=xxx 启动

USER nobody
EXPOSE 1337

ENTRYPOINT ["/app/start.sh"]
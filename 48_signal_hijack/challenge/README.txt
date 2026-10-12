信号劫持
难度: 大师

exec 模式，连 __builtins__ 这个名字都被封死。钥匙就在 exec 命名空间的地基里，用 globals() 一锹挖出来。

目标: 逃逸沙箱，读取环境变量 FLAG。
连接: nc <host> 1337，把你的 payload 粘贴发送。

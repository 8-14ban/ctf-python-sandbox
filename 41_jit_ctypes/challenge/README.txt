JIT 疑云
难度: 大师

exec 模式沙箱，但所有危险关键字（import/os/environ/ctypes...）全部进入黑名单。执行结果无回显，异常消息是你唯一的眼睛。

目标: 逃逸沙箱，读取环境变量 FLAG。
连接: nc <host> 1337，把你的 payload 粘贴发送。

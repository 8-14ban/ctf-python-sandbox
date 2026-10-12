宗师大满贯
难度: 大师

终极合围：AST 拦双下划线属性、拦 getattr/globals 直呼；空内置只发一把 G；黑名单覆盖 import/os/sys/modules/catch_/_wrap_close/builtins/warnings/_module 等全部整词。最后的钥匙是 socket 埋下的类。

目标: 逃逸沙箱，读取环境变量 FLAG。
连接: nc <host> 1337，把你的 payload 粘贴发送。

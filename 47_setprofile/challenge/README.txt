性能剖析
难度: 大师

getattr 与 globals 两个名字本身进入黑名单，AST 再拦双下划线属性。命名空间里只剩 S 与 G 两个代号。

目标: 逃逸沙箱，读取环境变量 FLAG。
连接: nc <host> 1337，把你的 payload 粘贴发送。

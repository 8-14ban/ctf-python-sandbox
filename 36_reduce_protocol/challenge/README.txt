[Python Sandbox 36] reduce 协议
难度: ★★★★★ 地狱
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  eval/exec 双双落锁，pickle 的字样也被拉黑。可反序列化协议里有一个
  特殊钩子 __reduce__：对象重建的那一刻，它说出的可调用对象就会被
  毫不迟疑地调用。让协议替你按下扳机。
目标:
  构造 __reduce__ 载荷，读取环境变量 FLAG。

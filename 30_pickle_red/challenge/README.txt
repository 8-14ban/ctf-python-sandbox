[Python Sandbox 30] pickle 反序列化
难度: ★★★★ 困难
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  eval 和 exec 都被禁了，看似断了活路。可 pickle.loads() 会忠实地重建
  对象——而 __reduce__ 协议允许对象在重建时"亲口"说出一个可调用对象。
  让 pickle 替你按下执行键。
目标:
  构造 pickle 载荷，读取环境变量 FLAG。

[Python Sandbox 25] 无内置之日
难度: ★★★★ 困难
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  所有内置都被扒走，你手里只剩一个空 dict。可 Python 的每个角落都藏着
  builtins 的影子——警告模块里那个爱咳嗽的类，__init__.__globals__
  ['__builtins__'] 就是失散多年的全家桶。去把它接回来。
目标:
  从零恢复 builtins，读取环境变量 FLAG。

[Python Sandbox 20] init 的全局
难度: ★★★ 进阶
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  每个函数都揣着一个 __globals__，装着它所属模块的全部家当。一个类只要
  __init__ 过一次，它的 __init__.__globals__ 就是通向 os 的密道。
  找到那个在警告模块里咳嗽的类，掏它的口袋。
目标:
  借助 __init__.__globals__，读取环境变量 FLAG。

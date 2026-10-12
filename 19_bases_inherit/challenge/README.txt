[Python Sandbox 19] bases 继承
难度: ★★★ 进阶
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  __mro__ 和 __subclasses__ 都被下了禁令，只留下 __bases__。不要紧，
  继承树本来就是靠 bases 撑起来的。一个类一个类向上推，推到 object，
  整棵子树都在你脚下。
目标:
  借助 __bases__ 继承链，读取环境变量 FLAG。

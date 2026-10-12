[Python Sandbox 34] 栈帧窃听
难度: ★★★★★ 地狱
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  经典魔法属性、关键词、内置函数全部封禁。但 sys._getframe 还在——它
  能翻看调用栈上每一层的 f_globals 与 f_back。沙箱自己执行的函数帧里，
  满是你想要的私有家当。栈，本身就是一本户口册。
目标:
  借助 sys._getframe 读取栈帧，读取环境变量 FLAG。

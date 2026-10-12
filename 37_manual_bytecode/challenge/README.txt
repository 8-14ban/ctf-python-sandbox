[Python Sandbox 37] 手工字节码
难度: ★★★★★ 地狱
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  marshal 与 CodeType 都被点名，编译入口被焊死。可函数的 __code__
  本身是个可替换的零件——任何函数都是宿主，注入手工编写的 co_code，
  它就替你执行任何字节。
目标:
  手工构造 code object，读取环境变量 FLAG。

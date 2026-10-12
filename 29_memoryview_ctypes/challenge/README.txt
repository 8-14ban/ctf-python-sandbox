[Python Sandbox 29] 内存底层
难度: ★★★★ 困难
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  字符串、字节码全被盯防，过滤做得滴水不漏。可所有 Python 对象底层都
  是指针和字节。memoryview 能直接看进对象的内存，ctypes 能绕过
  C 层调用——高层过滤挡不住底层视角。
目标:
  借助 memoryview / ctypes 底层能力，读取环境变量 FLAG。

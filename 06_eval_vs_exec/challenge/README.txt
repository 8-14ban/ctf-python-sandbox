[Python Sandbox 06] eval vs exec
难度: ★ 零基础
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  沙箱只开了 eval 的门：表达式能算，语句却无处安放。可 eval 的返回值里，
  藏着整个 __builtins__。一个 __import__ 丢进去，exec 的权限照样被借
  了出来。eval 与 exec 的距离，只差一次调用。
目标:
  借助 eval，读取环境变量 FLAG。

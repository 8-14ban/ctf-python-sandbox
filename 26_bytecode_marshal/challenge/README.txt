[Python Sandbox 26] 字节码注入
难度: ★★★★ 困难
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  源码层被逐字扫描，每个关键词都无处遁形。可代码一旦编译成字节码，就
  不再是一行行文字，而是一串数字。code object 就是没有名字的代码——
  扫描器认不出字节码里的 intent。
目标:
  借助 code object / marshal 绕过扫描，读取环境变量 FLAG。

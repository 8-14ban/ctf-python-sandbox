[Python Sandbox 22] subprocess 变奏
难度: ★★★ 进阶
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  os.system 与 Popen 双双上了通缉令。可能执行命令的又何止这两个？
  subprocess 全家都住在类树里，叫不上名字也能按索引揪出来。executor
  不止一个，这条路不通，就换一条。
目标:
  找到另一个命令执行器，读取环境变量 FLAG。

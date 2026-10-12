[Python Sandbox 31] help 暗管
难度: ★★★★ 困难
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  os、system 都进了黑名单。可 help() 是个好心想帮忙的帮手——它内部调用
  pydoc，pydoc 又用 subprocess 启动分页器。一条命令从帮助系统的
  管道里悄悄溜出。
目标:
  借道 help/pydoc 的 subprocess，读取环境变量 FLAG。

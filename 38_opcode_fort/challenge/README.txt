[Python Sandbox 38] opcode 碉堡
难度: ★★★★★ 地狱
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  黑名单又长了一截：连 opcode、marshal、CodeType 都上了墙。可字节码
  从来不需要字母——一条条操作码只是整数。把整数缝进函数的代码体里，
  解释器会照单全收。
目标:
  手工拼接 opcode，读取环境变量 FLAG。

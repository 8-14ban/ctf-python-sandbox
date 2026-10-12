[Python Sandbox 33] 多层过滤叠加
难度: ★★★★★ 地狱
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  三重防线同时上膛：字符白名单收走你的字母弹药，黑名单把 import/os/eval
  全部点名，AST 检查再把 __ 开头的属性访问拦在半空。可任何一层过滤器
  都有注意力死角——AST 只盯 Attribute，Name 却从眼皮底下溜走。
目标:
  突破三重过滤，读取环境变量 FLAG。

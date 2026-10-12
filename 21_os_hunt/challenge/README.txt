[Python Sandbox 21] os 猎手
难度: ★★★ 进阶
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  你说"os"？这个词早就进了黑名单。可 os 是一个活生生的模块，总得有人
  把它 import 进来。在 subclasses 的深林里，有一个类的 __globals__ 就
  是 os 的老家。不念它的名字，顺着引用摸过去。
目标:
  在类树中猎取 os，读取环境变量 FLAG。

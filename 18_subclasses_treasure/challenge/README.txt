[Python Sandbox 18] subclasses 宝库
难度: ★★★ 进阶
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  object 之下有千千万万的子类，全都活在同一片内存里。().__class__.
  __base__.__subclasses__() 把整座宝库摆到你面前——总有一个类的
  __globals__ 里躺着 os 和 builtins。找对那一个，门就开了。
目标:
  遍历 subclasses 宝库，读取环境变量 FLAG。

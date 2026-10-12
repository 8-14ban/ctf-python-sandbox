[Python Sandbox 23] getattr 链
难度: ★★★ 进阶
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  点号 . 被没收，魔法名字也被拉黑。可 getattr(obj, name) 只需一个对象
  和一个字符串。把每个属性名拆成两段拼接，用 getattr 一节一节搭桥，
  点号没了，路还在。
目标:
  用纯 getattr 链，读取环境变量 FLAG。

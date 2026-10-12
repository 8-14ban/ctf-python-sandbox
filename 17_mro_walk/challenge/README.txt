[Python Sandbox 17] MRO 爬行
难度: ★★★ 进阶
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  __base__ 和 __bases__ 被贴了封条，可 __mro__ 还在。方法解析顺序是
  一条向上的天梯：().__class__.__mro__[1] 一路通向 object。封住一扇
  门，天梯还在。
目标:
  借助 MRO 爬到 object，读取环境变量 FLAG。

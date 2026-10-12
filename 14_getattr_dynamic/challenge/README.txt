[Python Sandbox 14] getattr 暗号
难度: ★★ 入门
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  __class__、__subclasses__、__globals__ 这些魔法属性名全被拉黑。可
  Python 从不把属性名写死在代码里——getattr(obj, name) 让名字变成
  运行时才能揭晓的变量。拆成两半的字符串，在 getattr 眼里完好如初。
目标:
  借助 getattr 动态拼装属性名，读取环境变量 FLAG。

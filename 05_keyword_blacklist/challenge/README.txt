[Python Sandbox 05] 关键字黑名单
难度: ★ 零基础
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  import、open、system、os 全部进了黑名单。沙箱以为把这些词抹掉就安全
  了。可它不懂，Python 的世界里一切皆对象，而对象的名字可以从字符串里
  现拼出来。chr() 一组合，getattr() 一动，黑名单形同虚设。
目标:
  绕过黑名单，读取环境变量 FLAG。

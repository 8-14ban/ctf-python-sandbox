[Python Sandbox 27] type 造物
难度: ★★★★ 困难
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  type() 不只是用来查类型——三参数调用 type(name, bases, dict) 能凭空
  造出一个类。类是活的，它可以实例化、继承、被调用。type 本身，就是
  一台类打印机。
目标:
  用 type 动态构造逃逸类，读取环境变量 FLAG。

[Python Sandbox 28] 描述符对抗
难度: ★★★★ 困难
分类: Python 沙箱逃逸
连接: nc <host> 1337
描述:
  沙箱给对象套了一层 Guard，重写 __getattribute__ 拦截一切 __ 开头的
  属性。可描述符协议有自己的优先级：类型上的 __class__ 描述符，比
  实例的 __getattribute__ 更硬。拦截，拦不住协议本身。
目标:
  利用描述符优先级绕过 __getattribute__，读取环境变量 FLAG。

Python 沙箱逃逸 CTF 题目集（50 题）
====================================

难度分组
--------
第 1 组  01-08   零基础    语言基础与输入边界
第 2 组  09-16   入门      关键字过滤与内置绕过
第 3 组  17-24   进阶      对象图与属性链逃逸
第 4 组  25-32   困难      沙箱对抗与高级逃逸链
第 5 组  33-40   地狱      多层过滤 + 字节码 + 资源限制综合
第 6 组  41-50   大师      空内置 + AST 合围 + 钥匙伪装综合

题目索引
--------
01_hello_sandbox            首沙箱              eval 无过滤
02_number_only              数字陷阱            chr 拼接构造一切字符
03_no_underscore            下划线禁区          chr(95) 重建 __
04_no_paren                 括号禁区            import 语句 + assert（无括号）
05_keyword_blacklist        关键字黑名单        getattr + 拼接
06_eval_vs_exec             eval vs exec        eval 借用 __import__
07_builtins_mystery         内置函数之谜        类树挖回 builtins
08_no_echo                  无声的沙箱          assert 异常侧信道
09_string_concat            字符串拼接          __dict__ 下标 + 拼接
10_input_double             双重 eval           字符串二次注入
11_compile_split            转义迷宫            \uXXXX 转义重建字符
12_unicode_confuse          编码夹层            base64 载荷
13_class_chain              类链之始            类树遍历
14_getattr_dynamic          getattr 暗号        魔法名拼接
15_dir_recon                dir 侦察兵          内省
16_globals_locals           命名空间挖宝        locals() 枚举藏匿对象
17_mro_walk                 MRO 爬行            __mro__ 到 object
18_subclasses_treasure      subclasses 宝库     __dict__ 绕黑名单
19_bases_inherit            bases 继承          __bases__ + getattr 绕 __subclasses__
20_init_globals             init 的全局         __init__.__globals__
21_os_hunt                  os 猎手             _wrap_close -> sys.modules
22_subprocess_variant       subprocess 变奏     Popen 子类按名索引
23_getattr_chain            getattr 链          无点号全 getattr
24_classic_chain            经典链              全环节拼接重构
25_no_builtins              无内置之日          builtins={} 恢复
26_bytecode_marshal         字节码注入          长黑名单拼接链
27_type_dynamic             type 造物           动态构造调用
28_descriptor               描述符对抗          type() 绕 __getattribute__
29_memoryview_ctypes        内存底层            长黑名单拼接链
30_pickle_red               pickle 反序列化     __reduce__ 思想 + 拼接链
31_help_pipe                help 暗管           pydoc subprocess 思想
32_override_filter          篡改守门人          filter 替换思想
33_multi_layer              多层过滤叠加        AST+黑名单+白名单三重
34_sys_getframe             栈帧窃听            sys._getframe().f_globals
35_generator                协程暗渡            生成器 gi_frame
36_reduce_protocol          reduce 协议         魔法词全拼接
37_manual_bytecode          手工字节码          code object 思想
38_opcode_fort              opcode 碉堡         opcode 思想
39_gil_thread               GIL 线程博弈        线程共享状态
40_grand_slam               终极大满贯          AST+全黑名单+最小内置
41_jit_ctypes               JIT 疑云            exec 异常回显 + 拼接
42_syscall_hook             系统调用陷阱        trap.__globals__ 挖钥匙
43_importlib_hijack         导入器劫持          假 __import__ + 类树真导入器
44_frame_walk               栈帧行者            _getframe f_globals
45_generator_frame          生成器墓穴          gi_frame 帧复活
46_ctypes_overwrite         指针覆写            巨黑名单 + getattr 顶班
47_setprofile               性能剖析            别名钥匙 + sys.modules
48_signal_hijack            信号劫持            globals() 挖 exec 地基
49_thread_local             线程密室            普通对象藏 builtins
50_grandmaster_slam         宗师大满贯          G 别名 + 全拼接终极链

目录结构（每题）
----------------
{题号}_{名称}/
  challenge/
    challenge.py   沙箱源代码（选手可获取，供审计）
    Dockerfile     镜像定义（python:3.11-slim）
    start.sh       入口脚本
    README.txt     题目名 + 描述（无 hint）
    solution.txt   出题人参考解法（不进入镜像）

部署
----
每题独立镜像。FLAG 由平台以环境变量动态注入，启动时不落盘，
选手需在沙箱内逃逸后读取 FLAG 环境变量。

单题构建与运行：

    docker build -t sandbox-01 01_hello_sandbox/challenge
    docker run -d -p 1337:1337 -e FLAG='flag{xxx}' sandbox-01

连接：

    nc <host> 1337

验收状态
--------
- 50/50 challenge.py 语法编译通过
- 50/50 存在已验证的逃逸解法（verify_solutions.py，50/50 OK）
- 50/50 真实进程端到端测试：按 solution.txt 载荷经 TCP 交互
  全部成功取得 FLAG 环境变量
- Dockerfile 使用 python:3.11-slim，纯标准库，无额外依赖
- 每题监听 0.0.0.0:1337，nobody 用户运行
- challenge.py 已统一 import warnings，确保 catch_warnings
  注册进 object.__subclasses__()（防止部署环境未预载 warnings
  导致类树链路死题）

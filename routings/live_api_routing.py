# -*- coding: utf-8 -*-
from scripts import __all__ as scripts_cls


class RunScripts:

    def __init__(self, pt, aid):
        self.scripts_cls = scripts_cls
        self.pt = pt
        self.aid = aid
        self.scripts = [scripts(self.aid) for scripts in self.scripts_cls]

    def choice(self):
        """
        选择脚本
        :return:
        """
        for pt in self.scripts:
            if self.pt.upper() == pt._name:
                data = pt.get_real_url()
                return data
        else:
            return


if __name__ == '__main__':
    # print(RunScripts('DOUYU_LIVE', '74751').choice())
    print(RunScripts(pt, aid).choice())

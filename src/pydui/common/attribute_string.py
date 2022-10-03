# -*- coding: utf-8 -*-
import shlex
from typing import Any


class PyDuiAttrStrParser:
    @staticmethod
    def is_attrstr(path: str) -> bool:
        if path.startswith("file='"):
            return True
        return False

    @staticmethod
    def parse(path: str) -> dict[str, Any]:
        args = list(shlex.shlex(path))
        result = dict[str, Any]()
        last_key = ""
        last_is_equal = False
        for v in args:
            if v == "=":
                last_is_equal = True
                continue
            if last_key != "":
                if v.startswith('"') and v.endswith('"'):
                    v = v[1:-1]
                elif v.startswith("'") and v.endswith("'"):
                    v = v[1:-1]
                result[last_key] = v if last_is_equal else True
                last_key = ""
                last_is_equal = False
            else:
                last_key = v
        return result

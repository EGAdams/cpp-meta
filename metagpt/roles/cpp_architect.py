#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : architect.py
"""

from metagpt.actions import WriteCppDesign, WriteCppPRD
from metagpt.roles import Role


class CppArchitect( Role ):
    """Architect: Listen to PRD, responsible for designing API, designing code files"""
    def __init__(self, name="Sujit", profile="Architect", goal="Design a concise, usable, complete C++ system",
                 constraints="Try to specify good open source tools as much as possible"):
        super().__init__(name, profile, goal, constraints)
        self._init_actions([ WriteCppDesign ])
        self._watch({ WriteCppPRD })

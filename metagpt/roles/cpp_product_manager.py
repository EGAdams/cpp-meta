#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : product_manager.py
"""
from metagpt.actions import BossRequirement, WriteCppPRD
from metagpt.roles import Role


class CppProductManager(Role):
    def __init__(self, name="Gizelle", profile="Product Manager", goal="Efficiently create a successful product",
                 constraints=""):
        super().__init__(name, profile, goal, constraints)
        self._init_actions([ WriteCppPRD ])
        self._watch([ BossRequirement ])

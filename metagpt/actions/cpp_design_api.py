#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 19:26
@Author  : alexanderwu
@File    : design_api.py

@TODO:Possibly adjust 8192 chars or 2048 tokens to 16384 chars or 4096 tokens
"""
import shutil
from pathlib import Path
from typing import List

from metagpt.actions import Action, ActionOutput
from metagpt.const import WORKSPACE_ROOT
from metagpt.logs import logger
from metagpt.utils.common import CodeParser
from metagpt.utils.mermaid import mermaid_to_file

PROMPT_TEMPLATE = """
# Context
{context}

## Format example
{format_example}
-----
Role: You are an architect; the goal is to design a state-of-the-art  system; make the best use of good open source tools.
Requirement: Fill in the following missing information based on the context, note that all sections are responded with code form separately.
Max Output: 8192 chars or 2048 tokens. Try to use them up.
Attention: Use '##' to split sections, not '#', and '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote.

## Implementation approach: Provide as Plain text. Analyze the difficult points of the requirements, select the appropriate open-source framework.

## Cpp library name: Provide as a Cpp string with cpp triple quote, concise and clear, characters should only use a combination of letters (both uppercase and lowercase) and underscores.

## File list: Provided as Python list[str], the list of ONLY REQUIRED files needed to write the program(LESS IS BETTER!). Only need relative paths. Comply with C++14-compliant standards.  ALWAYS include a main.cpp here.

## Data structures and interface definitions:Use mermaid classDiagram code syntax, including classes (INCLUDING constructors) and functions (with type annotations), CLEARLY MARK the RELATIONSHIPS between classes, and comply with C++14-compliant standards.  The data structures SHOULD BE VERY DETAILED and the API should be comprehensive with a complete design.

## Program call flow: Use sequenceDiagram code syntax, COMPLETE and VERY DETAILED, using CLASSES AND API DEFINED ABOVE accurately, covering the construction, destruction, and main operations of each object, SYNTAX MUST BE CORRECT.

## Anything UNCLEAR: Provide as Plain text. Make clear here.

"""
FORMAT_EXAMPLE = """
---
## Implementation approach
We will ...

## Cpp library name
```cpp
"SnakeGame"
```

## File list
```cpp
[
    "main.cpp",
]
```

## Data structures and interface definitions
```mermaid
classDiagram
    class Game{
        +int score
    }
    ...
    Game "1" -- "1" Food: has
```

## Program call flow
```mermaid
sequenceDiagram
    participant M as Main
    ...
    G->>M: end game
```

## Anything UNCLEAR
The requirement is clear to me.
---
"""
OUTPUT_MAPPING = {
    "Implementation approach": (str, ...),
    "Cpp library name": (str, ...),
    "File list": (List[str], ...),
    "Data structures and interface definitions": (str, ...),
    "Program call flow": (str, ...),
    "Anything UNCLEAR": (str, ...),
}


class WriteCppDesign( Action ):
    def __init__(self, name, context=None, llm=None):
        super().__init__(name, context, llm)
        self.desc = "Based on the PRD, think about the system design, and design the corresponding APIs, " \
                    "data structures, library tables, processes, and paths. Please provide your design, feedback " \
                    "clearly and in detail."

    def recreate_workspace(self, workspace: Path):
        try:
            shutil.rmtree(workspace)
        except FileNotFoundError:
            pass  # The folder doesn't exist, but we don't care
        workspace.mkdir(parents=True, exist_ok=True)

    def _save_prd(self, docs_path, resources_path, prd):
        prd_file = docs_path / 'prd.md'
        quadrant_chart = CodeParser.parse_code(block="Competitive Quadrant Chart", text=prd)
        mermaid_to_file(quadrant_chart, resources_path / 'competitive_analysis')
        logger.info(f"Saving PRD to {prd_file}")
        prd_file.write_text(prd)

    def _save_system_design(self, docs_path, resources_path, content):
        data_api_design = CodeParser.parse_code(block="Data structures and interface definitions", text=content)
        seq_flow = CodeParser.parse_code(block="Program call flow", text=content)
        mermaid_to_file(data_api_design, resources_path / 'data_api_design')
        mermaid_to_file(seq_flow, resources_path / 'seq_flow')
        system_design_file = docs_path / 'system_design.md'
        logger.info(f"Saving System Designs to {system_design_file}")
        system_design_file.write_text(content)

    def _save(self, context, system_design):
        if isinstance(system_design, ActionOutput):
            content = system_design.content
            ws_name = CodeParser.parse_str(block="Cpp library name", text=content)
        else:
            content = system_design
            ws_name = CodeParser.parse_str(block="Cpp library name", text=system_design)
        workspace = WORKSPACE_ROOT / ws_name
        self.recreate_workspace(workspace)
        docs_path = workspace / 'docs'
        resources_path = workspace / 'resources'
        docs_path.mkdir(parents=True, exist_ok=True)
        resources_path.mkdir(parents=True, exist_ok=True)
        self._save_prd(docs_path, resources_path, context[-1].content)
        self._save_system_design(docs_path, resources_path, content)

    async def run(self, context):
        prompt = PROMPT_TEMPLATE.format(context=context, format_example=FORMAT_EXAMPLE)
        # system_design = await self._aask(prompt)
        system_design = await self._aask_v1(prompt, "system_design", OUTPUT_MAPPING)
        self._save(context, system_design)
        return system_design

"""
Instruction set for the stack-based VM (Phase 2 skeleton)
"""
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional


class Opcode(IntEnum):
    # Sensors (inputs)
    SEE_FOOD = 0x01
    SEE_WALL = 0x02
    MY_ENERGY = 0x03

    # Logic (stack ops)
    PUSH = 0x10
    POP = 0x11
    ADD = 0x12
    SUB = 0x13
    CMP = 0x14  # compares top2, pushes -1/0/1
    JUMP = 0x15
    JUMP_IF = 0x16
    STORE = 0x17
    LOAD = 0x18

    # Actions (outputs)
    MOVE_FWD = 0x20
    MOVE_BACK = 0x21
    ROTATE = 0x22
    ATTACK = 0x23
    SPLIT = 0x24
    NOOP = 0xFF


@dataclass
class Instruction:
    op: Opcode
    arg: Optional[int] = None

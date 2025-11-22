"""
Genome encoding/decoding and simple seed genomes (Phase 2 skeleton)
"""
from typing import List
from .instructions import Instruction, Opcode


def seed_wanderer() -> List[Instruction]:
    """A minimal genome that just moves forward steadily."""
    return [
        Instruction(Opcode.MOVE_FWD),
        Instruction(Opcode.NOOP),
    ]


def seed_turner() -> List[Instruction]:
    """Genome that rotates a little and moves forward."""
    return [
        Instruction(Opcode.ROTATE, arg=10),
        Instruction(Opcode.MOVE_FWD),
    ]


def encode(program: List[Instruction]) -> List[int]:
    """Encode to a simple int list [op,arg,op,arg,...] for storage."""
    out: List[int] = []
    for ins in program:
        out.append(int(ins.op))
        out.append(int(ins.arg) if ins.arg is not None else -1)
    return out


def decode(data: List[int]) -> List[Instruction]:
    """Decode from int list produced by encode()."""
    program: List[Instruction] = []
    it = iter(data)
    for op_val in it:
        arg_val = next(it, -1)
        arg = None if arg_val == -1 else int(arg_val)
        program.append(Instruction(Opcode(op_val), arg))
    return program

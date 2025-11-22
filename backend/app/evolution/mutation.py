"""
Mutation operations for genomes (Phase 2 skeleton)
"""
import random
from typing import List
from ..core.vm.instructions import Instruction, Opcode


ALL_OPS = [
    Opcode.SEE_FOOD, Opcode.SEE_WALL, Opcode.MY_ENERGY,
    Opcode.PUSH, Opcode.POP, Opcode.ADD, Opcode.SUB, Opcode.CMP,
    Opcode.JUMP, Opcode.JUMP_IF, Opcode.STORE, Opcode.LOAD,
    Opcode.MOVE_FWD, Opcode.MOVE_BACK, Opcode.ROTATE, Opcode.ATTACK, Opcode.SPLIT,
    Opcode.NOOP,
]


def mutate(program: List[Instruction], rate: float = 0.01, max_len: int = 200) -> List[Instruction]:
    out = list(program)

    # Point mutation
    if out and random.random() < rate:
        idx = random.randrange(len(out))
        op = random.choice(ALL_OPS)
        arg = out[idx].arg
        # small chance to randomize arg
        if random.random() < 0.3:
            arg = random.randint(-180, 180)
        out[idx] = Instruction(op, arg)

    # Insertion
    if len(out) < max_len and random.random() < rate * 0.5:
        idx = random.randrange(len(out) + 1)
        out.insert(idx, Instruction(random.choice(ALL_OPS), random.choice([None, 0, 1, 10, -10, 45, -45])))

    # Deletion
    if len(out) > 2 and random.random() < rate * 0.5:
        idx = random.randrange(len(out))
        del out[idx]

    # Duplication
    if out and random.random() < rate * 0.3:
        a = random.randrange(len(out))
        b = random.randrange(a, len(out))
        frag = out[a:b]
        out.extend(frag)

    return out[:max_len]

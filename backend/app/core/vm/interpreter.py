"""
Stack-based VM interpreter (Phase 2 skeleton)
Currently supports a minimal subset to drive movement.
"""
from typing import List
from .instructions import Instruction, Opcode


class VMInterpreter:
    def __init__(self, max_gas: int = 50):
        self.max_gas = max_gas

    def execute(self, creature, program: List[Instruction]):
        stack: List[float] = []
        memory = creature.__dict__.setdefault("vm_memory", {})
        pc = 0
        gas = self.max_gas
        n = len(program)

        def pop_default(default=0.0):
            return stack.pop() if stack else default

        while gas > 0 and 0 <= pc < n:
            ins = program[pc]
            gas -= 1
            pc += 1

            op = ins.op
            arg = ins.arg

            # Sensors
            if op == Opcode.MY_ENERGY:
                stack.append(float(creature.energy))
                continue

            # Logic
            if op == Opcode.PUSH:
                stack.append(float(arg if arg is not None else 0))
                continue
            if op == Opcode.POP:
                pop_default()
                continue
            if op == Opcode.ADD:
                b = pop_default(); a = pop_default()
                stack.append(a + b)
                continue
            if op == Opcode.SUB:
                b = pop_default(); a = pop_default()
                stack.append(a - b)
                continue
            if op == Opcode.CMP:
                b = pop_default(); a = pop_default()
                stack.append(-1.0 if a < b else (1.0 if a > b else 0.0))
                continue
            if op == Opcode.STORE:
                v = pop_default()
                k = arg if arg is not None else 0
                memory[int(k)] = v
                continue
            if op == Opcode.LOAD:
                k = arg if arg is not None else 0
                stack.append(float(memory.get(int(k), 0.0)))
                continue
            if op == Opcode.JUMP:
                if arg is not None and 0 <= arg < n:
                    pc = arg
                continue
            if op == Opcode.JUMP_IF:
                cond = pop_default()
                if cond and arg is not None and 0 <= arg < n:
                    pc = arg
                continue

            # Actions (minimal behavior wiring)
            if op == Opcode.MOVE_FWD:
                creature._vm_move = max(creature.__dict__.get("_vm_move", 0.0), 1.0)
                continue
            if op == Opcode.MOVE_BACK:
                creature._vm_move = min(creature.__dict__.get("_vm_move", 0.0), -1.0)
                continue
            if op == Opcode.ROTATE:
                delta = (arg or 0) / 180.0 * 3.141592653589793
                creature._vm_rotate = creature.__dict__.get("_vm_rotate", 0.0) + delta
                continue
            if op == Opcode.SPLIT:
                creature._vm_split = True
                continue
            if op == Opcode.ATTACK or op == Opcode.NOOP:
                continue

        # Apply action intents to creature (simple mapping)
        if hasattr(creature, "_vm_rotate"):
            creature.angle += creature._vm_rotate
            creature.__dict__.pop("_vm_rotate", None)
        if hasattr(creature, "_vm_move"):
            # Map -1..1 to speed
            speed = 30.0 * float(creature._vm_move)
            from math import cos, sin
            creature.vx = cos(creature.angle) * speed
            creature.vy = sin(creature.angle) * speed
            creature.__dict__.pop("_vm_move", None)
        return gas

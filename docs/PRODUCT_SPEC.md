# VIVARIUM ZERO Product Specification (Sanitized)

Version: 1.0  
Status: Public (English Primary)  
Chinese Translation: docs/zh/PRODUCT_SPEC_ZH.md

## 1. Vision
VIVARIUM ZERO is a 24/7 artificial life simulation where organisms evolve executable logic (genetic programming) rather than only numeric parameters. A lightweight virtual machine executes genomes, enabling emergent adaptive strategies.

## 2. Core World & Rules
### 2.1 Energy Model
- Passive Gain: Small baseline energy per second allows stationary strategies.
- Food Particles: Randomly spawned high-energy nutrition.
- Predation: Attacking transfers a portion of target energy.
- Metabolic Costs: Passive decay plus complexity tax (longer code / more sensors).
- Death: Energy <= 0 converts organism into a food resource.

### 2.2 Space
- Bounded 2D arena ("dish") with wall rebounds.
- Tactical implications: Corners allow reduced exposure.

### 2.3 Combat
- Optional aggression; no forced hostility.
- Attack organ required for damage output.
- Damage = attacker power - defender armor (future balancing).

## 3. Evolution Engine
### 3.1 Genome & VM
Genome = ordered instruction tape interpreted by a stack-based VM.
Categories:
- Sensors: SEE_FOOD, SEE_WALL, MY_ENERGY (extensible).
- Logic: IF, JUMP, ADD, SUB, MEMORY_SET.
- Actions: MOVE_FWD, ROTATE, ATTACK, SPLIT.

### 3.2 Mutation Types
- Point change (opcode substitution)
- Insertion (new instruction)
- Deletion (remove segment)
- Duplication (copy block)
Safeguards: instruction budget ("gas") per tick prevents infinite loops.

## 4. Architecture Overview
- Backend: Python + FastAPI simulation loop and VM interpreter.
- Optimization: Later optional JIT/vectorization.
- Persistence: Periodic world snapshots (SQLite + JSON serialization) for rollback.
- Frontend: Web canvas (p5.js) for phenotype visualization.

## 5. Phased Roadmap
Phase 1 (Genesis): Minimal movement + feeding demo.  
Phase 2 (Explosion): Introduce VM logic + divergence of behaviors.  
Phase 3 (Time Control): Snapshot timeline and rollback UI.

## 6. Risk Mitigation
| Risk | Description | Countermeasure |
|------|-------------|---------------|
| Infinite loops | Unbounded logic stalls loop | Gas limit per organism |
| Population spike | Over-reproduction | Dynamic energy scarcity & caps |
| Evolution stagnation | Converges to trivial exploit | Periodic environmental perturbations |

## 7. Language Policy
Primary repository language: English.  
Secondary language: Chinese (stored under docs/zh/, clearly labeled).  
Internal/private drafts belong in `private/` (ignored by VCS).

## 8. Privacy & Sanitization
Removed personal identifiers (names, specific home lab details, management tooling). Hardware generalized as an edge server environment.

## 9. Extension Points
- Additional sensors (directional food density, proximity heatmap)
- Defensive traits (armor, camouflage)
- Social signaling instructions
- Multi-layer memory model

## 10. Non-Goals (Current)
- Real-time distributed clustering
- Photorealistic rendering
- Complex fluid simulation

## 11. License & Contribution
Open source under MIT. See CONTRIBUTING.md and CODE_OF_CONDUCT.md.

---
This document is the sanitized public product reference replacing the previous PRD.

# Contributing to VIVARIUM ZERO

感谢你对 VIVARIUM ZERO 的兴趣！本项目旨在探索基于“进化代码逻辑” (Genetic Programming) 的人工生命系统。我们欢迎改进性能、可视化、虚拟机解释器、进化策略与生态动力学相关的贡献。

---
## 快速开始
1. Fork 仓库并克隆到本地
2. 创建虚拟环境并安装依赖：
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```
3. 运行模拟：
```bash
./start.sh
```
4. 打开浏览器访问 `http://localhost:8000`

---
## 分支命名规范
- 功能: `feat/<模块>-<简述>` 例如: `feat/vm-jump-instruction`
- 修复: `fix/<模块>-<问题>` 例如: `fix/physics-overlap`
- 性能: `perf/<模块>-<点>` 例如: `perf/grid-hash`
- 重构: `refactor/<模块>`
- 文档: `docs/<范围>`

## Commit 信息规范 (遵循 Conventional Commits)
- `feat:` 新功能
- `fix:` Bug 修复
- `perf:` 性能优化
- `refactor:` 非功能性重构
- `docs:` 文档更新
- `test:` 测试相关
- `chore:` 构建/依赖/杂项
- `ci:` 持续集成配置

示例：
```
feat(vm): add stack frame depth limit
fix(world): prevent negative energy reproduction
perf(physics): reduce collision passes using broadphase grid
```

---
## 代码规范
### Python
- 遵循 PEP8
- 使用类型注解
- 复杂函数保持在 40 行以内，优先拆分
- 热路径可在后期用 Numba/Cython 优化（先保持清晰）

### JavaScript (前端)
- 使用 ES6+ (const/let, arrow functions)
- 模块命名使用 camelCase
- 可视化逻辑集中在 `visualizer.js`，不要混入控制逻辑

---
## 测试
- 在 `backend/tests/` 中添加或扩展测试
- 单元测试：实体、物理、突变、解释器
- 建议新增：VM 指令执行测试、突变概率与边界测试
```bash
cd backend
pytest -v
```

---
## 提交 Pull Request 流程
1. 保持分支更新：`git pull origin main --rebase`
2. 保证测试全部通过
3. 如涉及性能，附上基准数据 (tick/s, population, CPU%)
4. PR 描述包含：
   - 目的 / 背景
   - 关键改动点
   - 测试覆盖情况
   - 性能或行为变化
5. 标记需要讨论的 TODO（如：`# TODO: optimize sensor range cache`）

---
## 行为与演化模块建议贡献方向
- VM 指令扩展：引用记忆、随机数、邻居查询
- 生态事件：灾难、资源再分配、季节变化
- 多样性度量：Shannon Index、基因距离、谱系树
- 可视化：基因调用栈、热力图、进化轨迹
- 时间机器：增量快照、差异压缩

---
## 性能建议基准
目标在 Mac mini 上：
| 阶段 | Pop | FPS | CPU |
|------|-----|-----|-----|
| Phase 1 | 300 | 60 | <25% |
| Phase 2 | 500 | 60 | <40% |
| Phase 3 | 800 | 60 | <60% |

---
## 问题反馈
提交 Issue 时请包含：
- 重现步骤
- 期望 vs 实际行为
- 环境（OS / Python 版本 / 浏览器）
- 相关日志或截图

---
## 安全
若发现潜在安全问题（如 RCE、拒绝服务风险），请发送邮件至：
`security@placeholder.example` （未来启用）

---
## 许可证
本项目采用 MIT 许可证。贡献表示你同意将所提交代码以 MIT 方式开源。

感谢你推动人工生命模拟向前发展！🌱

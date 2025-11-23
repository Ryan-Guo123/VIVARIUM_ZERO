# AGENTS.md（中文说明）

本指南面向在 VIVARIUM ZERO 仓库上运行的 AI 编码代理。公共仓库主语言为英文；本文为中文辅助说明，英文原文位于仓库根目录 `AGENTS.md`。

## 项目概览
- 领域：人工生命模拟，使用栈式虚拟机执行“基因”指令。
- 后端：Python + FastAPI；可选 Docker，默认本地 venv。
- 前端：Vanilla JS + p5.js，WebSocket 实时可视化。
- CI：GitHub Actions 运行 pytest。
- 语言策略：英文为主，中文位于 `docs/zh/`。

## 目录结构（要点）
- `backend/app/` — FastAPI、核心引擎、VM、进化逻辑
- `frontend/` — 静态资源（index.html、js、css），由后端提供
- `scripts/` — `start.sh`、`stop.sh`
- `docs/` — 公共英文文档
- `docs/zh/` — 中文翻译文档
- `private/` — 私有草稿（已忽略，请勿提交）

## 启动与运行
推荐本地 venv；仅当需要时使用 Docker。
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./start.sh
# 访问 http://localhost:8000
```
可选 Docker：
```
# start.sh 可自动检测 Docker；如需手动：
# docker build -t vivarium_zero .
# docker run -p 8000:8000 vivarium_zero
```

## 测试
```
# 处于 venv 环境
pip install -r requirements-dev.txt  # 若无此文件可跳过
pytest -q
```
- CI 工作流：`.github/workflows/ci.yml`

## 代码风格与约定
- Python 遵循 PEP 8，命名清晰，避免一字母变量。
- 最小化改动范围，避免无关重构。
- 公共文档使用英文；中文翻译放在 `docs/zh/`，文件名加 `_ZH`。
- 谨慎引入依赖，优先标准库。

## 代理工作流
1. 阅读 `AGENTS.md`、`README.md` 与相关 `docs/`。
2. 使用待办工具制定计划，分步提交小范围补丁。
3. 使用 `apply_patch` 进行最小化变更。
4. 先运行与改动相关的测试，再运行更广的测试。
5. 若公共接口或行为变化，请更新文档。
6. 遵守隐私与语言策略（见下）。

## 隐私与语言策略
- 不在公共文件中出现个人标识（姓名、邮箱、家庭实验室细节等）。
- 英文为主；中文翻译置于 `docs/zh/` 并注明。
- 内部草稿放在 `private/`，已被 `.gitignore` 忽略。
- 若发现历史提交包含敏感信息，提出过滤重写方案。

## 性能提示
- 空间网格降低碰撞复杂度，应保持启用。
- VM 每 Tick 有 gas 限制，避免无限循环。
- 后续阶段在 Python 3.11 或容器内可考虑启用 Numba。

## 常用命令
```
./start.sh
./stop.sh
curl http://localhost:8000/api/health
pytest -q
```

## 提交与 PR
- 遵循 PR 模板，标题简洁。
- 提供动机、约束与测试。
- 不提交 `private/` 内容。

## 非目标
- 无必要不引入新语言/框架。
- 避免大规模无关重构。
- 禁止提交个人信息。

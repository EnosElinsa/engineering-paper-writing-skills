# Engineering Paper Writing Skills

[![Validate skills](https://github.com/EnosElinsa/engineering-paper-writing-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/EnosElinsa/engineering-paper-writing-skills/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/EnosElinsa/engineering-paper-writing-skills)](https://github.com/EnosElinsa/engineering-paper-writing-skills/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) | 简体中文

这是一组用于起草、修改和审查工程类研究论文的 agent skill，覆盖从引言到结论的各节以及审稿回复信。每个 skill 都带有一份章节契约（含硬性质量门）、一套经过测量的团队写作风格（house style），以及一个只依赖 Python 标准库的脚本，用来把草稿和这套风格对照。

这些 skill 采用开放的 [Agent Skills](https://agentskills.io) 格式，任何能读取 `SKILL.md` 的 agent 都能使用，包括 Claude Code、Codex、Cursor 和 Kiro。

## 快速开始

用 [`skills` CLI](https://github.com/vercel-labs/skills)（需要 Node.js 22.20 或更高版本）为当前用户安装全部 8 个 skill：

```bash
npx skills add EnosElinsa/engineering-paper-writing-skills -g --skill '*'
```

CLI 会询问要装到哪些 agent。它在 `~/.agents/skills/` 下只保留一份副本，再把各个 agent 的 skill 目录链接过去。如果想直接指定 agent、跳过提问：

```bash
npx skills add EnosElinsa/engineering-paper-writing-skills -g --skill '*' -a claude-code -a codex -a kiro-cli -y
```

安装后，按任务向 agent 提出请求即可，例如：

```text
用 write-introductions 修改 paper/main.tex 的引言，四篇参考论文在 refs/ 里。
根据 results/summary.md 起草实验节，并用风格指纹脚本检查。
用 latex-prose-audit 审查 paper/main.tex 的行文，按行给出问题。
```

## 包含的 skill

| Skill | 负责的内容 |
|---|---|
| [`write-introductions`](skills/write-introductions/SKILL.md) | 因果动机链、研究分类、从场景推出方法、引用的经济使用、有界的贡献 |
| [`write-related-work`](skills/write-related-work/SKILL.md) | 按机制组织文献、有证据支撑的研究边界、本文要补上的缺口 |
| [`write-system-models`](skills/write-system-models/SKILL.md) | 继承已有架构、运行流程、符号、时序、约束，以及问题建模的闭合 |
| [`write-methods`](skills/write-methods/SKILL.md) | 模型到算法的对应、新颖性边界、可执行的语义、部署方式和复杂度 |
| [`write-experiments`](skills/write-experiments/SKILL.md) | 评估契约、公平比较、从证据到结论的写法、统计、消融和鲁棒性 |
| [`write-abstracts-and-conclusions`](skills/write-abstracts-and-conclusions/SKILL.md) | 标题、带定量结果的摘要、关键词、贡献列表、路线图、结论和未来工作 |
| [`write-revision-responses`](skills/write-revision-responses/SKILL.md) | 审稿意见台账、回复信、逐字引用、多份文档的同步、合入合作者的修改 |
| [`latex-prose-audit`](skills/latex-prose-audit/SKILL.md) | 按行审查 LaTeX 行文：主语与施事、术语、冠词、符号、引用和来源一致性 |

只装一个 skill 时用 `--skill`，例如 `npx skills add EnosElinsa/engineering-paper-writing-skills -g --skill write-experiments`。每个 skill 目录都自成一体，任意挑选其中几个都能单独使用。

## 工作方式

- **章节契约**：每个章节 skill 先加载通用契约和硬性质量门，再按论文需要加载方法路线（进化算法、强化学习）和领域包（移动边缘计算），用不到的不加载。
- **团队写作风格**：一页的速查卡规定默认的作者语态、禁用结构、句长带宽、合并规则、连接词和结构，完整的 house style 文件保存背后的测量表。两者都来自团队已发表的四篇 IEEE Transactions 论文和对导师修改的测量。详见 [docs/house-style.md](docs/house-style.md)。
- **风格指纹脚本**：每个 skill 里的 `scripts/style_fingerprint.py` 可测量中文或英文的 `.tex`、`.md`、`.txt` 草稿，报告句子节奏、禁用结构、过度拆句、图表题、小节标题、路线图、声明的规模、术语表变体和缩写问题。它给出的旗标是需要回读的线索，不是结论。详见 [docs/style-fingerprint.md](docs/style-fingerprint.md)。
- **证据边界**：关于新颖性、因果、最优性、鲁棒性和性能的说法不能超出所给证据，工作用的台账不写进稿件。

仓库结构、共享文件的同步机制以及如何新增领域包，见 [docs/architecture.md](docs/architecture.md)。

## 环境要求

- 一个能加载 Agent Skills 的 agent。
- Node.js 22.20 或更高版本，用于 `skills` CLI。
- Python 3.10 或更高版本，用于随附的风格指纹脚本（只用标准库）。没有 Python 时 skill 仍可使用，agent 会跳过测量检查并说明这一点。

## 更新与卸载

```bash
npx skills check -g        # 列出有更新的已安装 skill
npx skills update -g       # 更新它们
npx skills remove -g write-experiments
```

Windows 上没有创建符号链接的权限时，在 `npx skills add` 后加 `--copy`，并在每次发布新版本后重新运行安装命令，而不是用 `update`。

## 文档

- [架构](docs/architecture.md)：分层、仓库结构、共享文件、领域包和质量门
- [写作风格](docs/house-style.md)：house style 规定了什么、怎样测得、怎样重新校准
- [风格指纹脚本](docs/style-fingerprint.md)：脚本的全部模式和选项
- [参与贡献](CONTRIBUTING.md)：开发环境、检查流程和约定
- [更新日志](CHANGELOG.md)

文档正文为英文。

## 引用

如果这些 skill 对你的论文写作有帮助，请按 [CITATION.cff](CITATION.cff) 引用本仓库。

## 许可

本仓库以 [MIT 许可](LICENSE) 发布。用于校准写作风格的参考论文不随仓库分发。

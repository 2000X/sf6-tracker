# SF6 大赛追踪

街霸6（Street Fighter 6）大型赛事追踪：CPT 2026 赛季的赛程、冠亚军结果、日本观赛时间，以及 Capcom Cup 13 已确认名额。每天早上由 Claude 自动检索并更新。

| 入口 | 地址 | 谁能看 |
|---|---|---|
| 公开网站 | https://2000x.github.io/sf6-tracker/ | 任何人，无需账号 |
| Claude 页面 | https://claude.ai/artifact/6KshnNYxxiUb2c2cew77vJ | 仅自己（可在分享菜单开放给有 Claude 账号的人） |

## 怎么运作

```
每天 08:50 (JST) 定时任务启动
  → 检索最新赛果、赛程、直播时间、CC13 名额
  → 写入 Claude 页面的数据库（events / meta/status）
  → 从数据库导出 data.json，推送到本仓库 main 分支
  → GitHub Pages 自动重新部署公开网站
```

两个页面显示的是同一份数据：Claude 页面实时读取它的数据库，公开网站读取仓库里的 `data.json`。

## 目录

| 路径 | 用途 |
|---|---|
| `index.html` | 公开网站页面（GitHub Pages 从仓库根目录发布） |
| `data.json` | 网站数据，每日任务只改这个文件 |
| `src/artifact.html` | Claude 页面的源码（读取页面数据库的版本） |
| `scripts/build_data.py` | 把从数据库导出的 JSON 文件合并成 `data.json` |
| `scripts/check_data.py` | 检查 `data.json` 字段是否齐全、格式是否正确 |
| `docs/data-schema.md` | 数据字段说明 |
| `docs/daily-task.md` | 每日定时任务的设置与完整指令 |
| `docs/project-log.md` | 项目由来、设计决策、已知待确认事项 |
| `CHANGELOG.md` | 版本变更记录 |

## 想修改时

直接在 Claude 对话里说想改什么即可（例如「加上 Red Bull Kumite」「换配色」「更新时间改到晚上」）。在新对话里改的话，附上本仓库地址或 Claude 页面链接。

- 改**内容/数据**：改数据库和 `data.json`，两边保持一致。
- 改**页面外观**：`index.html` 和 `src/artifact.html` 要同步修改（两者只差数据读取方式），改完重新发布 Claude 页面并推送本仓库。
- 改**每日任务**：更新定时任务的指令，同时更新 `docs/daily-task.md`。

## 本地预览

```bash
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
python3 scripts/check_data.py   # 检查数据
```

数据来源：Capcom Pro Tour 官网、Liquipedia、start.gg、evo.gg 及各赛事报道。

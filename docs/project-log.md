# 项目记录

## 由来（2026-09-28）

需求：追踪整理街霸6的大型赛事，并每日更新。整个项目在一次 Claude 对话里搭建完成，过程如下：

1. **调研赛季现状**：检索 CPT 2026 赛季的 Premier 赛事、EWC、Topanga、亚运会与 Capcom Cup 13 的赛程和结果。
2. **做成 Claude 页面**：页面数据放在页面自带的数据库里，这样每日更新只需改数据，不必重新发布页面。
3. **设置每日定时任务**：每天 08:50（日本时间）检索并更新，完成后推送通知。
4. **加入日本观赛时间**：用户在日本，所以每个未开赛项目都附上换算好的日本时间；官方未公布时按往年推算并标「预估」。
5. **公开分享**：Claude 页面只能分享给有 Claude 账号的人。为了让朋友不用账号也能看，改为同时发布到 GitHub Pages：安装 Claude GitHub App → 推送网站 → 打开 Pages → 每日任务同时推送 `data.json`。
6. **整理成项目**：补齐文档、数据检查脚本和版本记录。

## 设计决策

| 决策 | 原因 |
|---|---|
| 数据和页面分开（数据库 / `data.json`） | 每日只改数据，页面代码保持稳定，出错面小 |
| 公开网站用 GitHub Pages | 免费、无需账号即可访问、推送后自动部署 |
| 两个页面共用一套设计 | `index.html` 和 `src/artifact.html` 只差数据读取方式，改外观时两边同步 |
| 所有日期按日本时间 | 用户在日本；海外周日晚的决赛常落在日本周一凌晨，按日本时间才不会看错 |
| 预估时间明确标注 | 官方未公布时段时给出参考，但不当作准确信息 |
| 只收录大型赛事 | Premier、EVO 系列、EWC、邀请赛、总决赛等；线上周赛不收录，World Warrior 区域决赛合并为一条 |

## 截至 2026-09-28 的待确认事项

- **EVO 2026 亚军**：报道显示为 Shigematsu，尚未在官方来源逐字核实。
- **EVO 2026 的 Capcom Cup 13 名额顺延**：冠军 MenaRD 已凭 Blink Respawn 获得资格，名额顺延给谁尚未确认。
- **Tokido 的资格途径**：CEO 2026 前已获得资格，具体途径未核实。
- **EVO France 2026 观赛时间**：官方未公布 SF6 时段，目前按 2025 年（决赛为法国时间周日 18:00）推算为日本时间 10/12（一）01:00 左右。
- **World Warrior 区域决赛、Capcom Cup 13 每日开赛时刻**：待官方公布。

## 主要来源

- Capcom Pro Tour 官网：https://sf.esports.capcom.com/
- Liquipedia：https://liquipedia.net/fighters/Capcom_Pro_Tour/2026
- start.gg、evo.gg、EventHubs、Shacknews、esports.gg 的赛事页面与报道

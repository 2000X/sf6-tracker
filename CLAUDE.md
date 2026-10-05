# SF6 大赛追踪 · 维护补充规则

定时更新任务的完整指令见 `docs/daily-task.md`，字段说明见 `docs/data-schema.md`。下面是 2026-10-05 起新增、定时任务指令里可能还没写到的规则，更新数据时一并遵守：

## 系列赛 / 联赛（`series` + `stages`）

- 跨数周、分多个赛段的赛事要加 `series: true` 和 `stages`：目前是 `cpt-ww-finals-2026`（World Warrior 区域决赛）、`sfl-japan-2026`（SFL JAPAN 日本联赛）、`sfl-playoffs-2026`（SFL 各赛区季后赛）。单场或单个周末的大型赛事不要标。
- `stages` 每项 `{date, name, time?, tentative?}`：`date` 是日本时间 `YYYY-MM-DD`，`name` 如 `"Division F 第 3 节"`，`time` 是日本时间如 `"18:40"`，官方未确认的加 `tentative: true`。列出全部已公布赛段，已结束的保留。
- 页面把系列赛放在顶部「系列赛 · 联赛」选项卡和赛程表的单独分组里，按下一赛段排序；「大型赛事」选项卡只显示下一场非系列赛事。
- 赛段改期、新公布（季后赛、总决赛日期等）时同步改 `stages`；`watch` 只写最近一两个赛段和最值得看的一项（`key`）。

## SFL JAPAN（`sfl-japan-2026`）

- 每次更新都核对最近几节的结果和 Division S / F 积分排名，写进 `note`（各组领先队伍）。
- 季后赛日期（目前按赛事站整理的 2027-01-10/11，标为预估）和总决赛（2027-02-23 东京 Big Sight）有官方消息时更新。
- 来源优先 sf.esports.capcom.com/sfl/、esports-world.jp、sf6freak.com。

## EWC 2027（`meta/status.ewc`）

2026-10-05 新增。字段说明见 `docs/data-schema.md` 的 `meta/status.ewc` 一节。每次定时更新都要核对：

- **日程**：EWC 2027 整体日程和 SF6 项目日期（目前只公布了利雅得、CS2 7/20–8/1）。SF6 日期公布后：更新 `facts` 里「SF6 项目」卡片和 `schedule` 里「SF6 正赛」一项（`state` 改 `set`）；同时在 `events` 新建 `ewc-2027`（kind `major`，city `沙特 利雅得`，写 `watch`；利雅得 UTC+3，比日本慢 6 小时）。
- **名额规则**：CPT 2027 赛季规则、Road to EWC 2027 预选赛、LCQ 公布后，把 `ref` 换成 2027 的实际分配（`title` 改成「名额构成 · EWC 2027（共 N 人）」），填 `slotsTotal`，相应 `schedule` 项改 `set` 并写日期。
- **已获名额**：有选手拿到 EWC 2027 名额（Premier 冠亚军、预选赛、顺延、LCQ）就加进 `ewc.qualified`，`via` 写清途径，并在 `log` 记一条。
- 每次更新 `ewc.checked`。`ewc` 是 `meta/status` 的子字段，用 update 写整个 `ewc` 对象。
- 来源优先 esportsworldcup.com、sf.esports.capcom.com/cpt/rules/、liquipedia.net/fighters、eventhubs。

## 更新日志

`meta/status.log` 仍然最多 30 条，页面只显示最近 3 条，其余折叠。

## 页面文件

定时任务只改 `data.json`，不要改 `index.html` 和 `src/artifact.html`。

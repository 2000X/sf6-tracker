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

## 更新日志

`meta/status.log` 仍然最多 30 条，页面只显示最近 3 条，其余折叠。

## 页面文件

定时任务只改 `data.json`，不要改 `index.html` 和 `src/artifact.html`。

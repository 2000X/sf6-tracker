# 数据格式

同一份数据存在两个地方：

- **Claude 页面的数据库**：集合 `events`（每个赛事一个文档）和文档 `meta/status`。
- **`data.json`**（公开网站用）：

```json
{
 "status": { ...与 meta/status 相同... },
 "events": { "<doc_id>": { ...与 events/<doc_id> 相同... } }
}
```

两边必须完全一致。`scripts/build_data.py` 负责把数据库导出转换成 `data.json`。

## events/&lt;doc_id&gt;

`doc_id` 用小写英文加连字符，例如 `evo-france-2026`。

| 字段 | 类型 | 说明 |
|---|---|---|
| `name` | 字符串 | 赛事名（英文原名） |
| `kind` | 字符串 | `premier`（CPT Premier）/ `major` / `invitational` / `team` / `final` / `online` |
| `city` | 字符串 | 城市（中文） |
| `venue` | 字符串 | 场馆 |
| `start` / `end` | `YYYY-MM-DD` | 按日本时间的开始、结束日期 |
| `entrants` | 数字 | 参赛人数 |
| `prize` | 字符串 | 奖金 |
| `champion` / `championChar` | 字符串 | 冠军与角色，角色写成 `"(Blanka)"` |
| `runnerUp` / `runnerUpChar` | 字符串 | 亚军与角色 |
| `score` | 字符串 | 决赛比分，如 `"GF 3-1，重置 3-0"` |
| `note` | 字符串 | 一句中文要点 |
| `preview` | 字符串 | 未开赛时的一句看点 |
| `link` | 字符串 | 必须是 `https://` 链接 |
| `watch` | 数组 | 日本观赛时间，见下 |
| `stream` | 字符串 | 直播频道 |
| `watchNote` | 字符串 | 时差、来源、是否预估的说明 |

`watch` 每项：

| 字段 | 说明 |
|---|---|
| `when` | 日本时间，如 `"10/12（一）01:00 左右"`，星期用中文 |
| `what` | 这一时段看什么，如 `"SF6 Top 8 决赛"` |
| `tentative` | `true` 表示按往年推算、官方未公布（页面显示「预估」） |
| `key` | `true` 表示最值得看的一项，显示在「下一站」卡片 |

### 系列赛 / 联赛：`series` 与 `stages`

跨数周、分多个赛段的赛事（World Warrior 区域决赛、SFL JAPAN、SFL 各赛区季后赛）加 `series: true` 和 `stages`：

| 字段 | 说明 |
|---|---|
| `series` | `true`：放进顶部「系列赛 · 联赛」选项卡和赛程表的系列赛分组，按下一赛段排序，不占「大型赛事」选项卡 |
| `stages` | 数组 `{date, name, time?, tentative?}`；`date` 为日本时间 `YYYY-MM-DD`，`time` 如 `"18:40"`，`tentative: true` 显示「预估」 |

页面取第一个日期不早于今天的赛段作为「下一赛段」显示倒计时；赛程表里列出接下来 4 个赛段。单场或单个周末的大型赛事不要标 `series`。

页面按日期自动判断状态：今天早于 `start` 为「即将开始」，在 `start`–`end` 之间为「进行中」，结束后有 `champion` 为已结束，没有则显示「结果待更新」。已结束的赛事不显示 `watch`。

## meta/status

| 字段 | 说明 |
|---|---|
| `lastUpdated` | `"YYYY-MM-DD HH:MM"`，日本时间 |
| `brief` | 今日要点，1–2 句 |
| `ccNote` | Capcom Cup 13 名额构成说明 |
| `totalSlots` | 名额总数，48 |
| `qualified` | 数组 `{player, via, tbd?}`，`tbd: true` 为待确认名额 |
| `log` | 数组 `{date, text}`，最新在最前，最多 30 条；页面只显示最近 3 条，其余折叠 |
| `roadmap` | 下一次角色追加与版本调整，见下 |

### meta/status.roadmap

显示在页面顶部「下一站」卡片下方。

| 字段 | 说明 |
|---|---|
| `character` | 下一位追加角色 `{name, date, note, link}`。`date` 为官方公布的上线日期，未公布时为 `null`，页面只显示角色名 |
| `balance` | 下一次平衡性/版本调整 `{name?, date, note, link}`。只有 `date` 是官方公布的具体日期时页面才显示这一项 |
| `checked` | 最后核对日期 `YYYY-MM-DD` |

`date` 按日本时间写 `YYYY-MM-DD`；`link` 必须是 `https://` 链接。上线当天显示「今天上线」，过期后显示「已上线」，应在下次更新时换成下一位。

### meta/status.ewc

页面「EWC 2027 · 日程与名额」板块的数据，放在 Capcom Cup 名额板块之后。整个字段不存在时页面不显示这一块。

| 字段 | 说明 |
|---|---|
| `edition` | 届次，如 `"EWC 2027"`，显示在板块标题 |
| `facts` | 数组 `{k, v, s?}`：顶部三张小卡片（地点 / 整体日程 / SF6 项目），`k` 标签、`v` 主文字、`s` 一句补充 |
| `schedule` | 数组 `{when, what, state, note?}`：日程时间线，按时间先后排列。`when` 是自由文字（如 `"2026 年 9 月"`、`"7/24–26"`、`"待公布"`）；`state` 为 `set`（已公布）/ `tbd`（待公布）/ `est`（参照往年）/ `done`（已结束） |
| `slotsTotal` | 名额总数（整数），官方未公布时为 `null`，页面显示「总名额待公布」且不显示进度条 |
| `qualified` | 数组 `{player, via, tbd?}`：已获 EWC 名额的选手，`via` 写获得途径（如 `"EVO Japan 2027 冠军"`） |
| `emptyNote` | 还没有名额时显示的一句说明 |
| `ref` | `{title, items: [{slots, via, note?}]}`：名额构成。2027 规则公布前放 2026 的构成作参照，公布后换成 2027 的实际分配并改 `title` |
| `note` | 板块底部说明 |
| `checked` | 最后核对日期 `YYYY-MM-DD` |

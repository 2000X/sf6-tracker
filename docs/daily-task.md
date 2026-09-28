# 每日定时任务

| 项目 | 设置 |
|---|---|
| 名称 | SF6 赛事每日更新 |
| 时间 | 每天 08:50（日本时间），`CRON_TZ=Asia/Tokyo 50 8 * * *` |
| 运行位置 | 云端，不需要开着电脑 |
| 通知 | 手机推送 |
| 任务 ID | `trig_01Qp4ubLybmUDpDCsQMkBV46` |
| 审批 | 默认每次写入前需要批准；可在该定时任务的设置里打开 Automatically approve 改为全自动 |

每次运行都是全新会话，不记得之前的对话，所以下面的指令写得完整独立。修改任务时，先改这里，再把全文同步到定时任务。

## 完整指令

```text
每日任务：更新「SF6 大赛追踪」（街霸6 Street Fighter 6 大型赛事追踪）。用户在日本（Asia/Tokyo），使用中文，内容全部用简体中文书写（选手名、赛事名保持英文原名）。同一份数据要更新到两个地方：
- A. Claude 页面：https://claude.ai/artifact/6KshnNYxxiUb2c2cew77vJ （数据在页面自带的数据库里，用 ArtifactData 工具读写，需要时先用 ToolSearch 加载 "select:ArtifactData"；不需要重新发布页面）
- B. 公开网站：https://2000x.github.io/sf6-tracker/ （GitHub 仓库 2000X/sf6-tracker，网站读取仓库根目录的 data.json；不要改 index.html）

## 数据结构
1. 集合 `events`：每个赛事一个文档，doc_id 用小写英文连字符（如 evo-france-2026）。字段：
   name, kind（premier=CPT Premier / major / invitational / team / final / online）, city（中文）, venue, start, end（YYYY-MM-DD，按日本时间）, entrants（数字）, prize（字符串）, champion, championChar（如 "(Blanka)"）, runnerUp, runnerUpChar, score（如 "GF 3-1，重置 3-0"）, note（一句中文要点）, preview（未开赛时的一句看点）, link（https 链接，优先 Liquipedia / start.gg / Capcom 官方）。
   日本观赛时间（每个还没结束的赛事都要有）：
   - watch：数组，每项 {when, what, tentative?, key?}。when 写日本时间，格式如 "10/12（一）01:00 左右"、"3/13（六）"，星期用中文（日一二三四五六）；what 写这一时段看什么（如 "SF6 Top 8 决赛"）；官方未公布、按往年推算的时间加 tentative:true；整个赛事最值得看的那一项（通常是 Top 8/决赛）加 key:true。
   - stream：直播频道（如 "EVO 官方 Twitch / YouTube"）。
   - watchNote：一句说明（时差、时间来源、是否预估）。
   换算时注意当地夏令时（例如法国 10 月最后一个周日前是 UTC+2，之后 UTC+1；美国 11 月第一个周日前是夏令时），并注意跨日（海外周日晚的决赛在日本常是周一凌晨）。官方公布具体时段后，把 tentative 去掉、改成准确时间。
   页面会按日期自动判断「即将开始/进行中/已结束」，结束但没有 champion 的会显示「结果待更新」；已结束赛事的 watch 不会显示，可保留。
2. 文档 `meta/status`：
   lastUpdated（"YYYY-MM-DD HH:MM"，日本时间）, brief（今日要点，1–2 句中文）, ccNote, totalSlots(48), qualified（数组，{player, via, tbd?}，Capcom Cup 13 已确认名额；未确认的用 tbd:true）, log（数组，{date, text}，最新在最前，最多保留 30 条）。
3. data.json（网站用）：{"status": <meta/status 的内容>, "events": {"<doc_id>": <该赛事文档内容>, ...}}，UTF-8、ensure_ascii=False、缩进 1。它必须和数据库内容完全一致。

## 每次运行的步骤
1. 用 ArtifactData list 读取 `events`（limit 100）和 get `meta/status`，记下各文档的 version。
2. 用 WebSearch/WebFetch 检索最新信息（今天日期请用 current_time 工具获取）：
   - 最近 3 天内结束或正在进行的 SF6 大型赛事结果（CPT Premier、EVO 系列、EWC、Red Bull Kumite、Topanga、SFL、各大 Tier 1 线下赛），冠亚军、使用角色、决赛比分、参赛人数。
   - 未来 3 个月内赛事的官方赛程/直播时间表（SF6 预选、Top 8 的开始时间和时区），换算成日本时间写入 watch；日期/地点变动；新公布的大型赛事（新加入的赛事同样要写 watch）。
   - Capcom Cup 13 新确认的名额（Premier 冠军、名额顺延、Premier 积分榜名额、World Warrior 区域决赛冠军、SFL 世界赛相关）。
   来源优先：sf.esports.capcom.com、liquipedia.net/fighters、start.gg、evo.gg、eventhubs、shacknews、esports.gg。只写有来源支持的事实，不确定的内容标成待确认/预估或不写。
3. 用一次 ArtifactData batch 写入所有改动：新赛事用 set；已有赛事用 update 并带上 if_version；更新 meta/status（lastUpdated 必更新；brief 写今天最值得看的一两件事，未来 7 天内有比赛时写上日本观赛时间；有新结果、新名额或观赛时间变化时在 log 最前面加一条当天记录，没有变化时 log 加一条"无重大变化，已核对 X、Y 赛程"之类的简短记录）。qualified 数组整体替换为最新完整列表。
4. 同步到网站：
   a. 用 mcp__claude-code-remote__add_repo（owner "2000X", repo "sf6-tracker", access "push"）把仓库加入本次会话，按它返回的说明 clone（git clone --depth 1）。
   b. 再用 ArtifactData 把 `events`（out_dir 设为 <仓库>/export）和 `meta/status`（同一个 out_dir）导出成文件，运行 `python3 scripts/build_data.py export` 生成新的 data.json，再运行 `python3 scripts/check_data.py`，有错误先修正数据库再重新生成。export/ 已在 .gitignore 里，不要提交。
   c. git config user.name Claude；git config user.email noreply@anthropic.com；提交信息写 "Daily update YYYY-MM-DD"，末尾加两行：
      Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
      （空行后即可，不要加其他署名）
      然后 git push origin HEAD:main。只改 data.json。
   d. 推送失败（例如 403 权限被拒）时不要反复重试，在最后的总结里说明原因。
5. 只更新街霸6（SF6）相关内容，小型线上周赛、地区小比赛不收录（World Warrior 区域决赛作为一条汇总记录）。已结束超过 12 个月的赛事可以删除（数据库和 data.json 都要删）。
6. 结束时用一两句中文总结今天改了什么（例如"EVO France 2026 已结束：冠军 X，亚军 Y；Capcom Cup 13 名额更新为 N 个"，或"EVO France 公布赛程，SF6 决赛为日本时间 10/12 01:00"），并说明网站是否已同步；没有变化就说明已核对、无变化。
```

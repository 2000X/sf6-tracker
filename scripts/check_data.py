"""检查 data.json 的字段和格式，发现问题时以非零状态退出。

用法：
    python3 scripts/check_data.py [data.json 路径]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KINDS = {"premier", "major", "invitational", "team", "final", "online"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DOC_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def check(data):
    errors, warnings = [], []
    status, events = data.get("status"), data.get("events")
    if not isinstance(status, dict):
        errors.append("缺少 status")
        status = {}
    if not isinstance(events, dict) or not events:
        errors.append("缺少 events")
        events = {}

    for key in ("lastUpdated", "brief", "qualified", "log"):
        if key not in status:
            errors.append(f"status 缺少 {key}")
    if len(status.get("log", [])) > 30:
        warnings.append("status.log 超过 30 条")
    for q in status.get("qualified", []):
        if not q.get("player"):
            errors.append(f"qualified 有一项缺少 player：{q}")

    roadmap = status.get("roadmap")
    if roadmap is not None:
        if not isinstance(roadmap, dict):
            errors.append("status.roadmap 应为对象")
            roadmap = {}
        for key in ("character", "balance"):
            item = roadmap.get(key)
            if item is None:
                continue
            if not isinstance(item, dict):
                errors.append(f"roadmap.{key} 应为对象")
                continue
            if item.get("date") is not None and not DATE.match(str(item["date"])):
                errors.append(f"roadmap.{key}.date 应为 YYYY-MM-DD 或 null")
            if item.get("link") and not str(item["link"]).startswith("https://"):
                errors.append(f"roadmap.{key}.link 必须是 https:// 链接")
        if isinstance(roadmap.get("character"), dict) and not roadmap["character"].get("name"):
            errors.append("roadmap.character 缺少 name")

    for doc_id, ev in events.items():
        where = f"events/{doc_id}"
        if not DOC_ID.match(doc_id):
            errors.append(f"{where}：doc_id 应为小写英文加连字符")
        if not ev.get("name"):
            errors.append(f"{where}：缺少 name")
        if ev.get("kind") not in KINDS:
            errors.append(f"{where}：kind 不在 {sorted(KINDS)} 中")
        for f in ("start", "end"):
            if f in ev and not DATE.match(str(ev[f])):
                errors.append(f"{where}：{f} 不是 YYYY-MM-DD")
        if "start" not in ev:
            errors.append(f"{where}：缺少 start")
        if ev.get("start") and ev.get("end") and ev["end"] < ev["start"]:
            errors.append(f"{where}：end 早于 start")
        if ev.get("link") and not str(ev["link"]).startswith("https://"):
            errors.append(f"{where}：link 必须是 https:// 链接")
        if "entrants" in ev and not isinstance(ev["entrants"], (int, float)):
            errors.append(f"{where}：entrants 应为数字")
        watch = ev.get("watch")
        if watch is not None:
            if not isinstance(watch, list) or not all(isinstance(w, dict) and w.get("when") for w in watch):
                errors.append(f"{where}：watch 每项都要有 when")
        if ev.get("runnerUp") and not ev.get("champion"):
            warnings.append(f"{where}：有亚军但没有冠军")
    return errors, warnings


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    errors, warnings = check(data)
    for w in warnings:
        print("提醒：" + w)
    for e in errors:
        print("错误：" + e)
    print(f"共 {len(data.get('events', {}))} 个赛事，{len(errors)} 个错误，{len(warnings)} 个提醒")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

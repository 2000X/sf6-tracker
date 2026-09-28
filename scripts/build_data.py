"""把从 Claude 页面数据库导出的 JSON 文件合并成网站用的 data.json。

用法：
    python3 scripts/build_data.py <导出目录> [输出文件]

<导出目录> 的结构与 ArtifactData 的 out_dir 导出一致：
    <导出目录>/events/<doc_id>.json
    <导出目录>/meta/status.json
每个文件可以是文档本身，也可以是带 "data" 字段的包装格式。
输出文件默认是仓库根目录的 data.json。
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def body(path):
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    if isinstance(doc, dict) and isinstance(doc.get("data"), dict) and "version" in doc:
        return doc["data"]
    return doc


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "data.json")

    events = {}
    for path in sorted(glob.glob(os.path.join(src, "events", "*.json"))):
        events[os.path.splitext(os.path.basename(path))[0]] = body(path)
    status_path = os.path.join(src, "meta", "status.json")
    if not events or not os.path.exists(status_path):
        sys.exit(f"导出目录里缺少 events/*.json 或 meta/status.json：{src}")

    data = {"status": body(status_path), "events": events}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"已写入 {out}：{len(events)} 个赛事")


if __name__ == "__main__":
    main()

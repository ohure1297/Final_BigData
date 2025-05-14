import json

with open("topcv.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("topcv.jsonl", "w", encoding="utf-8") as f:
    for item in data:
        json.dump(item, f, ensure_ascii=False)
        f.write('\n')

import json
from pathlib import Path


total_data = {}
input_files = list(Path("raw_data").glob("*.json"))
num_pages = len(input_files)
for file in input_files:
    with open(file) as f:
        data = json.load(f)
    # check for collisions
    existing_keys = set(total_data.keys())
    new_keys = set(data.keys())
    inter = new_keys.intersection(existing_keys)
    assert len(inter) == 0, inter

    data_simple = {k: v["text"] for k, v in data.items()}

    total_data.update(data_simple)


meta={
    "length":len(total_data),
    "num_pages":num_pages,
    "per_page":len(total_data) / num_pages,
    "longest_key":len(max(total_data.keys(),key=len)),
}
print(meta)

with open("total_data.json", "w") as f:
    json.dump({
        "meta":meta,
        "data":total_data,
    }, f, indent=2, ensure_ascii=False, sort_keys=True)

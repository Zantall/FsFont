import json
import random

# -------------------------------
# 配置
# -------------------------------
train_file = "/root/test/other/FsFont/meta/train_unis.json"
val_file = "/root/test/other/FsFont/meta/val_unis.json"
decompose_file = "/root/test/other/FsFont/MyWork/chn_decompose.json"
output_file = "/root/test/other/FsFont/MyWork/cr_mapping.json"
refs_num = 5
seed = 42

random.seed(seed)

# -------------------------------
# 1. 读取 train/val Unicode
# -------------------------------
with open(train_file, "r", encoding="utf-8") as f:
    train_unis = json.load(f)
with open(val_file, "r", encoding="utf-8") as f:
    val_unis = json.load(f)

all_unis = sorted(set(train_unis + val_unis))  # 已经是 Unicode hex 字符串

# -------------------------------
# 2. 读取 chn_decompose.json
# -------------------------------
with open(decompose_file, "r", encoding="utf-8") as f:
    decompose_dict = json.load(f)  # key = Unicode hex, value = 部件索引列表

# -------------------------------
# 3. Jaccard 相似度函数
# -------------------------------
def jaccard_sim(u1, u2):
    # u1, u2 是 Unicode 字符编码字符串，如 "4E00"
    comp1 = set(decompose_dict.get(u1, []))
    comp2 = set(decompose_dict.get(u2, []))
    if not comp1 or not comp2:
        return 0.0
    return len(comp1 & comp2) / len(comp1 | comp2)

# -------------------------------
# 4. 生成 CRMapping
# -------------------------------
CRMapping = {}

for u in all_unis:
    sim_scores = []
    for other in all_unis:
        if other == u:
            continue
        score = jaccard_sim(u, other)
        sim_scores.append((other, score))
    
    # 按相似度降序
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    
    top_refs = [ch for ch,_ in sim_scores[:refs_num]]  # 已经是 Unicode
    
    # 不足 refs_num 时，用随机补齐
    if len(top_refs) < refs_num:
        need = refs_num - len(top_refs)
        candidates = [ch for ch in all_unis if ch != u and ch not in top_refs]
        if candidates:
            top_refs += random.choices(candidates, k=need)
        else:
            top_refs += [u]*need  # 最后手段重复自己
    
    CRMapping[u] = top_refs

# -------------------------------
# 5. 保存 JSON
# -------------------------------
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(CRMapping, f, ensure_ascii=False, indent=2)

print(f"✅ CRMapping generated, total chars={len(CRMapping)}, refs per char={refs_num}")

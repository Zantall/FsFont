import os
import json
import random

img_dir = "/root/test/other/FsFont/songti/imgs"
img_exts = (".png", ".jpg", ".jpeg", ".bmp")
seed = 42   # 固定随机种子，保证可复现

# 1. 读取字符
chars = []
for name in os.listdir(img_dir):
    if name.lower().endswith(img_exts):
        char = os.path.splitext(name)[0]
        assert len(char) == 1, f"非法文件名: {name}"
        chars.append(char)

# 2. 去重
chars = list(set(chars))

# 3. 随机打乱（可复现）
random.seed(seed)
random.shuffle(chars)

# 4. 转 Unicode hex（大写，不带前缀）
unis = [f"{ord(c):04X}" for c in chars]

# 5. 4:1 划分
split_idx = int(len(unis) * 0.8)
train_unis = unis[:split_idx]
val_unis   = unis[split_idx:]

# 6. （可选）各自内部再排序，便于阅读 & 对齐工程
train_unis = sorted(train_unis)
val_unis   = sorted(val_unis)

# 7. 写 JSON
with open("train_unis.json", "w", encoding="utf-8") as f:
    json.dump(train_unis, f, ensure_ascii=False, indent=2)

with open("val_unis.json", "w", encoding="utf-8") as f:
    json.dump(val_unis, f, ensure_ascii=False, indent=2)

print(f"Total={len(unis)}, Train={len(train_unis)}, Val={len(val_unis)}")

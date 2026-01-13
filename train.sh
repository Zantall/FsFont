# #export CUDA_VISIBLE_DEVICES=4
# python3 train.py \
#     FsFont_5_Train \
#     cfgs/custom.yaml \
#     #--resume \path\to\pretrain.pdparams

# === Step0: 配置环境 ===
pip install paddlepaddle-gpu==2.6.2
pip install torch torchvision
pip install sconf>=0.2.3 lmdb>=1.2.1
pip install numpy tqdm pillow opencv-python

# === Step1: 解压数据集 ===
tar -xzf /share/home/tm945458209690000/a945500620/Zzh-FsFont/font.tar.gz -C /share/home/tm945458209690000/a945500620/Zzh-FsFont

# === Step2: 构建数据库 ===
ROOT_DIR=/share/home/tm945458209690000/a945500620/Zzh-FsFont

echo "Building dataset..."
python3 ./build_dataset/build_meta4train.py \
  --saving_dir $ROOT_DIR/results/result \
  --content_font $ROOT_DIR/songti/imgs \
  --train_font_dir $ROOT_DIR/png_style_format5/Pot1.0Train \
  --val_font_dir $ROOT_DIR/png_style_format5/Pot1.0Test \
  --seen_unis_file ./meta/train_unis.json \
  --unseen_unis_file ./meta/val_unis.json

# === Step2: 启动训练 ===
echo "Start training..."
# export CUDA_VISIBLE_DEVICES=0
python3 train.py \
    FsFont_5_Train \
    cfgs/custom.yaml
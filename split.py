import os
import csv
import mdtraj as md
import numpy as np


def save_md_pairwise_csv(pdb_list, xtc_list, out_csv):
    """
    對每個 protein 計算單一數值 md_pairwise，
    並輸出成 csv，欄位為:
        name, pairwise_rmsd

    邏輯:
    1. 讀入 xtc (stride=40)
    2. 只取 CA
    3. 對齊到 frame 0
    4. 計算所有 frame-pair 的 RMSD
    5. 取平均，作為這個 protein 的 md_pairwise
    """

    if len(pdb_list) != len(xtc_list):
        raise ValueError("pdb_list 和 xtc_list 長度必須一致")

    rows = []

    for pdb, xtc in zip(pdb_list, xtc_list):
        name = os.path.splitext(os.path.basename(pdb))[0]

        # 載入 trajectory，固定 stride=40
        traj = md.load_xtc(xtc, top=pdb, stride=40)

        # 只取 CA
        ca_idx = traj.top.select("name CA")
        if len(ca_idx) == 0:
            raise ValueError(f"{name}: 找不到 CA 原子")
        traj = traj.atom_slice(ca_idx)

        # frame 太少沒辦法算 pairwise
        if traj.n_frames < 2:
            rows.append({
                "name": name,
                "pairwise_rmsd": np.nan
            })
            continue

        # 對齊到 frame 0
        traj.superpose(traj, frame=0)

        pairwise_vals = []

        # 計算所有 frame 間的 pairwise RMSD，只取上三角
        for i in range(traj.n_frames):
            rmsd_to_i = md.rmsd(traj, traj, frame=i) * 10.0  # nm -> Å
            pairwise_vals.extend(rmsd_to_i[i+1:])

        md_pairwise = float(np.mean(pairwise_vals))

        rows.append({
            "name": name,
            "pairwise_rmsd": md_pairwise
        })

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "pairwise_rmsd"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done. Output written to: {out_csv}")


import pandas as pd
import os 
train_csv = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/kkk/main-csv/train.csv'
test_csv = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/kkk/main-csv/test.csv'
raw_dir = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/pdbxtc/chain-r1'
pdb_list = []
xtc_list = []
#
df_train = pd.read_csv(train_csv)
df_test = pd.read_csv(test_csv)
# train
for _, row in df_train.iterrows():
    protein = row["proteins"]
    fragment = row["fragments"]
    for letter in ["A", "B", "C"]:
        pdb_list.append(os.path.join(raw_dir, f"{protein}-{fragment}-{letter}.pdb"))
        xtc_list.append(os.path.join(raw_dir, f"{protein}-{fragment}-{letter}.xtc"))
out_csv = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/kkk/analysis/rmsd/train.csv'
save_md_pairwise_csv(pdb_list, xtc_list, out_csv)

# test
for _, row in df_test.iterrows():
    protein = row["proteins"]
    fragment = row["fragments"]
    for letter in ["A", "B", "C"]:
        pdb_list.append(os.path.join(raw_dir, f"{protein}-{fragment}-{letter}.pdb"))
        xtc_list.append(os.path.join(raw_dir, f"{protein}-{fragment}-{letter}.xtc"))
out_csv = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/kkk/analysis/rmsd/test.csv'
save_md_pairwise_csv(pdb_list, xtc_list, out_csv)
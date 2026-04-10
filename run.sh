#r1
cd /mnt/hdd/jeff/MDGen/model/0-scratch/scratch-if-chain
python -m scripts.prep_sims-chain \
    --split /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/main-csv/name.csv \
    --sim_dir /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/pdbxtc/chain-r1 \
    --outdir /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/npy/chain-r1 \
    --csv_dir /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/csv \
    --num_workers 8 \
    --stride 40 \
    --atlas

#r2
cd /mnt/hdd/jeff/MDGen/model/0-scratch/scratch-if-chain
python -m scripts.prep_sims-chain \
    --split /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/main-csv/name.csv \
    --sim_dir /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/pdbxtc/chain-r2 \
    --outdir /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/npy/chain-r2 \
    --num_workers 8 \
    --stride 40 \
    --atlas

#r3
cd /mnt/hdd/jeff/MDGen/model/0-scratch/scratch-if-chain
python -m scripts.prep_sims-chain \
    --split /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/main-csv/name.csv \
    --sim_dir /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/pdbxtc/chain-r3 \
    --outdir /mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/npy/chain-r3 \
    --num_workers 8 \
    --stride 40 \
    --atlas
import os
import re
import csv

def delete_files_not_in_csv(csv_file, dir_path):
    keep_pairs = set()
    keep_fragments = set()

    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            protein = row["proteins"].strip()
            fragment = str(row["fragments"]).strip()
            keep_pairs.add((protein, fragment))
            keep_fragments.add(fragment)

    def should_keep(filename):
        # 例如 wt-1-A.pdb / wt-1-B.xtc
        m1 = re.match(r"^([^-]+)-(\d+)-[A-Z]\.(pdb|xtc)$", filename)
        if m1:
            protein, fragment, _ = m1.groups()
            return (protein, fragment) in keep_pairs

        # 例如 1.pdb / 1.xtc
        m2 = re.match(r"^(\d+)\.(pdb|xtc)$", filename)
        if m2:
            fragment, _ = m2.groups()
            return fragment in keep_fragments

        # 其他格式直接刪
        return False

    deleted = []
    kept = []

    for name in os.listdir(dir_path):
        path = os.path.join(dir_path, name)
        if not os.path.isfile(path):
            continue

        if should_keep(name):
            kept.append(path)
        else:
            os.remove(path)
            deleted.append(path)
            print("Deleted:", path)

    print(f"\n保留 {len(kept)} 個檔案")
    print(f"刪除 {len(deleted)} 個檔案")


csv_file = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/main-csv/name.csv'
dir_path = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/pdbxtc/protein-r2'
delete_files_not_in_csv(csv_file, dir_path)

csv_file = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/main-csv/name.csv'
dir_path = '/mnt/hdd/jeff/MDGen/data/dataset/wt-collagen-B/raw/pdbxtc/protein-r3'
delete_files_not_in_csv(csv_file, dir_path)
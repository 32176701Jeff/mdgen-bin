base_csv_dir="/mnt/hdd/jeff/MDGen/data/dataset/mdgen-atlas/small/main-csv"
out_root="/mnt/hdd/jeff/MDGen/data/dataset/mdgen-atlas/raw/protein"

for split in train val test; do
    csv_file="${base_csv_dir}/${split}.csv"

    tail -n +2 "$csv_file" | awk -F ',' '{print $1}' | while read -r name; do
        out_dir="${out_root}/${name}"
        zip_file="${out_dir}/${name}_protein.zip"
        url="https://www.dsimb.inserm.fr/ATLAS/database/ATLAS/${name}/${name}_protein.zip"

        mkdir -p "$out_dir"

        wget "$url" -O "$zip_file"

        unzip "$zip_file" -d "$out_dir"

        rm -f "$zip_file"
    done
done
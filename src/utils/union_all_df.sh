#!/bin/bash

file1="data/sinan_dengue_sample_2021.csv"
file2="data/sinan_dengue_sample_2022.csv"
file3="data/sinan_dengue_sample_2023.csv"
file4="data/sinan_dengue_sample_2024.csv"

output="data/sinan_dengue_sample_complete.csv"

cp "$file1" "$output"

tail -n +2 "$file2" >> "$output"
tail -n +2 "$file3" >> "$output"
tail -n +2 "$file4" >> "$output"

linhas=$(wc -l < "$output")
echo $linhas


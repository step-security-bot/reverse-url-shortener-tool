#!/bin/bash

readarray -d '' files < <(find ../. -name "*.py" -not -name "__*" -not -path "*testing*" -print0)

rm ./one_file.py

for file in "${files[@]}"; do
  echo "# $file" >> ./one_file.py
  cat $file >> ./one_file.py
  echo "\n" >> ./one_file.py
done 


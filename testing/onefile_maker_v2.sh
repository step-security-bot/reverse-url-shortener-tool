#!/bin/bash

# Define el archivo de salida
output_file="./one_file.py"

# Elimina el archivo de salida si ya existe
rm -f "$output_file"

# Busca los archivos Python y concaténalos en el archivo de salida
find ../. -name "*.py" -not -name "__*" -not -path "*testing*" -print0 |
while IFS= read -r -d '' file; do
  echo "# $file" >> "$output_file"
  cat "$file" >> "$output_file"
  echo >> "$output_file"  # Agrega una línea en blanco después de cada archivo
done

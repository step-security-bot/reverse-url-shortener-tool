#!/bin/bash
# Cambiar directorio de ejecución a ../
cd ./service/data_generator_service/

# Define el archivo de salida
output_file="./testing/one_file.py"

# Elimina el archivo de salida si ya existe
rm -f "$output_file"

# Busca los archivos Python y concaténalos en el archivo de salida
find . -name "*.py" -not -name "__*" -not -path "*testing*" -print0 |
while IFS= read -r -d '' file; do
    echo "# $file"
    cat "$file"
  {
    echo "# $file"
    cat "$file"
    echo  # Agrega una línea en blanco después de cada archivo
  } >> "$output_file"
done
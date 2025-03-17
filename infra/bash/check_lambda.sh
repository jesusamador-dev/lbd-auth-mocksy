#!/bin/bash
set -e  # Detiene el script si hay un error

# Leer JSON desde Terraform
read input_json || { echo '{"exists": false}'; exit 1; }

# Extraer la variable `lambda_name`
LAMBDA_NAME=$(echo "$input_json" | jq -r '.lambda_name')

# Si la variable está vacía, devolver error
if [[ -z "$LAMBDA_NAME" ]]; then
  echo "❌ Error: 'lambda_name' no definido"
  echo '{"exists": false}'
  exit 1
fi

# Verificar si la Lambda existe
if aws lambda get-function --function-name "$LAMBDA_NAME" >/dev/null 2>&1; then
  echo '{"exists": true}'
else
  echo '{"exists": false}'
fi

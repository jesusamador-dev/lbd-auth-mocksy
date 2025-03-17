#!/bin/bash
set -e  # Detiene el script si hay un error

# Leer JSON desde Terraform
read input_json || { echo '{"exists": false}'; exit 1; }

# Extraer la variable `role_name`
ROLE_NAME=$(echo "$input_json" | jq -r '.role_name')

# Si la variable está vacía, devolver error
if [[ -z "$ROLE_NAME" ]]; then
  echo "❌ Error: 'role_name' no definido"
  echo '{"exists": false}'
  exit 1
fi

# Verificar si el IAM Role existe
if aws iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1; then
  echo '{"exists": true}'
else
  echo '{"exists": false}'
fi

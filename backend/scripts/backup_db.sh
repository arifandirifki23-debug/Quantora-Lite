#!/bin/bash
DB_PATH=${DB_PATH:-quantora_data.db}
OUT_DIR=${OUT_DIR:-/var/backups/quantora}
mkdir -p "$OUT_DIR"
TS=$(date +"%Y%m%d_%H%M%S")
cp "$DB_PATH" "$OUT_DIR/quantora_db_$TS.db"
echo "Backup created: $OUT_DIR/quantora_db_$TS.db"
find "$OUT_DIR" -type f -mtime +30 -delete

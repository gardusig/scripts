#!/usr/bin/env bash

# Check for required folder path
if [ -z "$1" ]; then
  echo "Usage: $0 <folder-path> [optional-output-file]"
  exit 1
fi

FOLDER="$1"
OUTFILE="${2:-$(mktemp)}"

# List of ignored paths or patterns
IGNORED_PATHS=(
  "*/node_modules/*"
  "*/build/*"
  "*/dist/*"
  "*/.git/*"
)
IGNORED_FILES=(
  "package-lock.json"
  "yarn.lock"
  "*.png"
  "*.jpg"
  "*.jpeg"
  "*.gif"
  "*.webp"
  "*.svg"
  "*.ico"
)

# Add header to output file
echo "# 📦 File dump from: ${PWD}" >"$OUTFILE"
echo "" >>"$OUTFILE"

# Build find command dynamically with ignored paths
FIND_CMD=(find "$FOLDER" -type f)

# Add path exclusions
for pattern in "${IGNORED_PATHS[@]}"; do
  FIND_CMD+=(! -path "$pattern")
done

# Add file exclusions
for name in "${IGNORED_FILES[@]}"; do
  FIND_CMD+=(! -name "$name")
done

# Finish command with print0 for safe reading
FIND_CMD+=(-print0)

# Run the command and process files
"${FIND_CMD[@]}" | while IFS= read -r -d '' FILE; do
  echo -e "\n${FILE}:\n\`\`\`\n$(cat "$FILE")\n\`\`\`\n" >>"$OUTFILE"
  echo "📄 Processed: $FILE"
done

# Copy to clipboard (macOS only)
if command -v pbcopy >/dev/null; then
  cat "$OUTFILE" | pbcopy
  echo -e "\n✅ All contents copied to clipboard"
fi

echo "📝 Output also saved at: $OUTFILE"

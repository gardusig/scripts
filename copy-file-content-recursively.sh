#!/usr/bin/env bash

# Check for required folder path
if [ -z "$1" ]; then
  echo "Usage: $0 <folder-path> [optional-output-file]"
  exit 1
fi

FOLDER="$1"
OUTFILE="${2:-$(mktemp)}"

# Add header to output file
echo "# 📦 File dump from: ${PWD}" >"$OUTFILE"
echo "" >>"$OUTFILE"

# Collect files, excluding unwanted paths
find "$FOLDER" \
  -type f \
  ! -path "*/node_modules/*" \
  ! -path "*/build/*" \
  ! -path "*/dist/*" \
  ! -path "*/.git/*" \
  ! -name "package-lock.json" \
  ! -name "yarn.lock" \
  -print0 | while IFS= read -r -d '' FILE; do
  echo -e "\n${FILE}:\n\`\`\`\n$(cat "$FILE")\n\`\`\`\n" >>"$OUTFILE"
  echo "📄 Processed: $FILE"
done

# Copy to clipboard
cat "$OUTFILE" | pbcopy

echo -e "\n✅ All contents copied to clipboard"
echo "📝 Output also saved at: $OUTFILE"

#!/bin/bash

# Check for required folder path
if [ -z "$1" ]; then
  echo "Usage: $0 <folder-path>"
  exit 1
fi

FOLDER="$1"
OUTPUT=""

# Use find to iterate recursively over regular files
while IFS= read -r -d '' FILE; do
  if [ -f "$FILE" ]; then
    EXT="${FILE##*.}"
    BASENAME=$(basename "$FILE")
    CONTENT=$(<"$FILE")

    OUTPUT+="\n${FILE}:\n"
    OUTPUT+="\`\`\`${EXT}\n${CONTENT}\n\`\`\`\n\n"
  fi
done < <(find "$FOLDER" -type f -print0)

# Copy to clipboard
echo -e "$OUTPUT" | pbcopy

echo "✅ Copied contents of all files in '$FOLDER' to clipboard as formatted code blocks."

# remove_bom.py

# Remove BOM from the JSON file
with open('db.json', 'rb') as f:
    content = f.read()

# Check for BOM and remove it if present
if content.startswith(b'\xef\xbb\xbf'):
    content = content[3:]

# Write back to the file without BOM
with open('db.json', 'wb') as f:
    f.write(content)

print("BOM removed successfully, if it was present.")

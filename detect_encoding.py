import chardet

# Open the file in binary mode to detect encoding
with open('db.json', 'rb') as file:
    raw_data = file.read()

# Detect encoding
result = chardet.detect(raw_data)
encoding = result['encoding']

print(f"Detected file encoding: {encoding}")
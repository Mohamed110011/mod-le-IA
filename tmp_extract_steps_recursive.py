import json
import sys

json_path = r"c:\Users\mohamed taher\Downloads\3.json"

def find_key(obj, key_name):
    if isinstance(obj, dict):
        if key_name in obj:
            return obj[key_name]
        for v in obj.values():
            res = find_key(v, key_name)
            if res is not None: return res
    elif isinstance(obj, list):
        for item in obj:
            res = find_key(item, key_name)
            if res is not None: return res
    return None

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
        start = content.find('{')
        data = json.loads(content[start:])
        
        steps = find_key(data, 'steps')
        if steps:
            print("FOUND STEPS:")
            print(json.dumps(steps, indent=2, ensure_ascii=False))
        else:
            print("No 'steps' key found anywhere in the JSON.")

except Exception as e:
    print(f"Error: {e}")

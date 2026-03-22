import json
import sys

json_path = r"c:\Users\mohamed taher\Downloads\3.json"

def find_first_with_steps(obj):
    if isinstance(obj, dict):
        if 'steps' in obj and obj['steps']:
            return obj
        for v in obj.values():
            res = find_first_with_steps(v)
            if res: return res
    elif isinstance(obj, list):
        for item in obj:
            res = find_first_with_steps(item)
            if res: return res
    return None

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
        start = content.find('{')
        data = json.loads(content[start:])
        
        result = find_first_with_steps(data)
        if result:
            print("FOUND OBJECT WITH STEPS:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("No object with 'steps' key found.")

except Exception as e:
    print(f"Error: {e}")

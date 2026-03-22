import json
import sys

json_path = r"c:\Users\mohamed taher\Downloads\3.json"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
        start = content.find('{')
        if start == -1:
            print("No JSON object found")
            sys.exit(1)
            
        data = json.loads(content[start:])
        
        # Look for a product that has "steps"
        for cat_id, cat_data in data.items():
            if not isinstance(cat_data, dict): continue
            
            # Check items
            items = cat_data.get('items', [])
            for item in items:
                if 'steps' in item and item['steps']:
                    print(f"FOUND STEPS in item: {item.get('displayName', {}).get('dflt', {}).get('nameDef', 'Unknown')}")
                    print(json.dumps(item['steps'], indent=2, ensure_ascii=False))
                    sys.exit(0)
            
            # Check if category itself has steps
            if 'steps' in cat_data and cat_data['steps']:
                print(f"FOUND STEPS in category: {cat_data.get('title', 'Unknown')}")
                print(json.dumps(cat_data['steps'], indent=2, ensure_ascii=False))
                sys.exit(0)

    print("No 'steps' object found in the items or categories.")

except Exception as e:
    print(f"Error: {e}")

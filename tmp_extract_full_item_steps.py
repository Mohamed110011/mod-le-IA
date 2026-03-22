import json
import sys

json_path = r"c:\Users\mohamed taher\Downloads\3.json"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
        start = content.find('{')
        data = json.loads(content[start:])
        
        # Look for a product that has "steps"
        for cat_id, cat_data in data.items():
            if not isinstance(cat_data, dict): continue
            
            items = cat_data.get('items', [])
            for item in items:
                if 'steps' in item and item['steps']:
                    print(f"FULL ITEM WITH STEPS:")
                    # Print only essential fields to avoid too much output
                    # but keep 'steps' full
                    clean_item = {k: v for k, v in item.items() if k != 'steps'}
                    print(json.dumps(clean_item, indent=2, ensure_ascii=False))
                    print("\nSTEPS OBJECT:")
                    print(json.dumps(item['steps'], indent=2, ensure_ascii=False))
                    sys.exit(0)

except Exception as e:
    print(f"Error: {e}")

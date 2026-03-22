"""
Script CLI pour générer un article de restauration via l'IA Python.
Usage :
    python generate_article_api.py --json "Pizza 4 fromages avec mozzarella"

Retourne un JSON sur stdout.
"""

import argparse
import sys
import json
import contextlib
import io
import os


def main():
    parser = argparse.ArgumentParser(description="Génère un article de restauration via IA.")
    parser.add_argument('description', nargs='?', default='', help="Description de l'article")
    parser.add_argument('--json', action='store_true', help="Sortie au format JSON strict")

    args, unknown = parser.parse_known_args()

    description = args.description
    if unknown:
        description = description + ' ' + ' '.join(unknown) if description else ' '.join(unknown)
    description = description.strip()

    if not description:
        print(json.dumps({"error": "Description manquante"}, ensure_ascii=False))
        sys.exit(1)

    JSON_DATA_PATH = r"c:\Users\mohamed taher\Downloads\3.json"

    try:
        # Supprimer tous les print() des modules internes
        with contextlib.redirect_stdout(io.StringIO()):
            from product_generator_ai import ProductGeneratorAI

            if os.path.exists(JSON_DATA_PATH):
                generator = ProductGeneratorAI(JSON_DATA_PATH)
            else:
                generator = ProductGeneratorAI()

            product = generator.generate(description)

        # Construire la réponse simplifiée compatible avec pfe-catalogue
        name_fr = product.get('displayName', {}).get('dflt', {}).get('nameDef', description)
        translations = product.get('displayName', {}).get('dflt', {}).get('translations', {})
        name_en = translations.get('en', name_fr) if isinstance(translations.get('en'), str) else name_fr

        desc_fr = product.get('description', {}).get('dflt', {}).get('nameDef', description)

        price_raw = product.get('price', 0)
        try:
            price_val = float(price_raw) if price_raw is not None else 0.0
        except (ValueError, TypeError):
            price_val = 0.0

        price_ht = round(price_val / 1.1, 2)
        tva = 10

        allergens = product.get('allergens', [])
        category_name = product.get('category', 'AUTRES')
        color = product.get('color', '#FDFD96')

        result = {
            "title": name_fr,
            "displayName": {
                "fr": name_fr,
                "en": name_en
            },
            "description": {
                "fr": desc_fr,
                "en": translations.get('en', desc_fr) if isinstance(translations.get('en'), str) else desc_fr
            },
            "price": {
                "ht": price_ht,
                "tva": tva,
                "dflt": price_val
            },
            "allergens": allergens,
            "categoryName": category_name,
            "color": color,
            "img": os.path.basename(product.get('img', {}).get('dflt', {}).get('img', '')),
        }

        print(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        import traceback
        print(json.dumps({
            "error": str(e),
            "traceback": traceback.format_exc()
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()

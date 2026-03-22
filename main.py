"""
Generateur de produit - interface simple.

Usage :
  python main.py                      # mode interactif (boucle)
  python main.py "milkshake chocolat" # genere directement
"""

import sys
import json
import os
import io
from product_generator_ai import ProductGeneratorAI

# Forcer UTF-8 pour l'affichage console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JSON_PATH = r"c:\Users\mohamed taher\Downloads\3.json"
OUTPUT_DIR = r"d:\model-IA-image\generated_products"


def display(product: dict):
    """Affiche le produit de facon lisible."""
    name = product['displayName']['dflt']['nameDef']
    print()
    print(f"  Nom        : {name}")
    print(f"  Categorie  : {product.get('category', '-')}")
    print(f"  Prix       : {product['price']} EUR")
    print(f"  Allergenes : {', '.join(product['allergens']) if product['allergens'] else 'aucun'}")
    print(f"  Source     : {product['_source']}")
    img = product.get('img', {}).get('dflt', {}).get('img', '')
    if img:
        print(f"  Image      : {img[:80]}")
    print()


def save(product: dict):
    """Sauvegarde le produit en JSON."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pid = product['id'][:8]
    path = os.path.join(OUTPUT_DIR, f"product_{pid}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(product, f, ensure_ascii=False, indent=2)
    print(f"  Sauvegarde : {path}")


def run(gen: ProductGeneratorAI, description: str):
    """Genere et affiche un produit depuis une description."""
    print()
    print(f"Recherche / generation : {description}")
    print("-" * 50)
    product = gen.generate(description)
    display(product)

    rep = input("Sauvegarder ? (o/n) : ").strip().lower()
    if rep == 'o':
        save(product)


def main():
    gen = ProductGeneratorAI(JSON_PATH)

    # Si description passee en argument
    if len(sys.argv) > 1:
        description = ' '.join(sys.argv[1:])
        run(gen, description)
        return

    # Sinon mode interactif direct
    print()
    print("Generateur de produits  |  'q' pour quitter")
    print("=" * 50)

    while True:
        try:
            desc = input("\nNom / description du produit : ").strip()
            if desc.lower() in ('q', 'quit', 'exit'):
                break
            if not desc:
                continue
            run(gen, desc)
        except KeyboardInterrupt:
            break

    print("Au revoir.")


if __name__ == '__main__':
    main()

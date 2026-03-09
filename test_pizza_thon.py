# -*- coding: utf-8 -*-
"""
Test de recherche d'image pour Pizza Thon
"""

import sys
import os

# Forcer l'encodage UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from main import ProductAISystem


def test_pizza_thon():
    """Test spécifique pour pizza thon"""
    print("\n" + "="*70)
    print("TEST: Pizza Thon avec images du JSON")
    print("="*70 + "\n")
    
    # Initialiser avec backend from_json
    print("[1/3] Initialisation...")
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='from_json'
    )
    
    # Test avec "pizza thon"
    print("\n[2/3] Generation de 'pizza thon'...")
    print("-" * 70)
    
    try:
        product = system.generate_product_from_description(
            "pizza thon",
            generate_image=True,
            force=True
        )
        
        print("\n" + "-" * 70)
        print("RESULTAT:")
        print("-" * 70)
        print(f"Nom genere: {product['displayName']['dflt']['nameDef']}")
        print(f"Categorie: {product.get('category', 'N/A')}")
        
        # Le prix peut être un dict ou un float
        prix = product.get('price', 0)
        if isinstance(prix, dict):
            prix = prix.get('dflt', 0)
        print(f"Prix: {prix}€")
        
        print(f"Image: {product.get('image_path', 'N/A')}")
        
        # Vérifier si c'est un placeholder
        image_path = product.get('image_path', '')
        if 'placeholder' in image_path:
            print("\n⚠️  ATTENTION: Image placeholder generee (pas trouvee dans JSON)")
        elif 'from_json' in image_path:
            print("\n✅ SUCCES: Image recuperee depuis le JSON!")
        
    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n[3/3] Test termine!\n")
    print("="*70)


if __name__ == "__main__":
    test_pizza_thon()

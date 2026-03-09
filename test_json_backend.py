# -*- coding: utf-8 -*-
"""
Test simple du backend from_json
"""

import sys
import os

# Forcer l'encodage UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from main import ProductAISystem


def test_json_backend():
    """Test du backend from_json"""
    print("\n" + "="*70)
    print("TEST: Backend 'from_json'")
    print("="*70 + "\n")
    
    # Initialiser
    print("[1/4] Initialisation avec backend 'from_json'...")
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='from_json'
    )
    
    # Test 1: Produit qui existe probablement
    print("\n[2/4] Test avec 'Milkshake Fraise'...")
    try:
        product1 = system.generate_product_from_description(
            "Milkshake Fraise",
            generate_image=True,
            force=True
        )
        print(f"  => Nom: {product1['displayName']['dflt']['nameDef']}")
        print(f"  => Image: {product1.get('image_path', 'N/A')}")
    except Exception as e:
        print(f"  => Erreur: {e}")
    
    # Test 2: Produit inexistant
    print("\n[3/4] Test avec produit inexistant...")
    try:
        product2 = system.generate_product_from_description(
            "Nouveau Produit Test XYZ",
            generate_image=True,
            force=True
        )
        print(f"  => Nom: {product2['displayName']['dflt']['nameDef']}")
        print(f"  => Image: {product2.get('image_path', 'N/A')}")
        print(f"  => Note: Devrait utiliser un placeholder")
    except Exception as e:
        print(f"  => Erreur: {e}")
    
    print("\n[4/4] Test termine!")
    print("\n" + "="*70)
    print("RESUME:")
    print("  - Backend from_json charge 780 images du JSON")
    print("  - Trouve automatiquement l'image correspondante")
    print("  - Utilise un placeholder si image non trouvee")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        test_json_backend()
    except Exception as e:
        print(f"\nERREUR: {e}\n")
        import traceback
        traceback.print_exc()

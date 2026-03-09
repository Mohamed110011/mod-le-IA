# -*- coding: utf-8 -*-
"""
Tests multiples pour valider l'algorithme amélioré
"""

import sys
import os

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from main import ProductAISystem


def test_multiple_products():
    """Test avec plusieurs types de produits"""
    print("\n" + "="*70)
    print("TEST MULTI-PRODUITS : Algorithme ameliore")
    print("="*70 + "\n")
    
    # Initialiser
    print("Initialisation du systeme...\n")
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='from_json'
    )
    
    # Liste de tests
    test_cases = [
        ("pizza thon", "SPECIALE THON"),
        ("pizza poulet", "SPECIALE POULET ou PIZZA...POULET"),
        ("milkshake fraise", "MILKSHAKE FRAISE"),
        ("frappe caramel", "FRAPPE CARAMEL"),
        ("pizza chorizo", "SPECIALE CHORIZO"),
    ]
    
    print("\n" + "="*70)
    print("TESTS")
    print("="*70 + "\n")
    
    results = []
    
    for i, (description, expected) in enumerate(test_cases, 1):
        print(f"\n[Test {i}/{len(test_cases)}] '{description}'")
        print("-" * 70)
        
        try:
            product = system.generate_product_from_description(
                description,
                generate_image=True,
                force=True
            )
            
            # Vérifier le résultat
            nom = product['displayName']['dflt']['nameDef']
            image_path = product.get('image_path', '')
            
            if 'from_json' in str(image_path):
                status = "✅ IMAGE JSON"
                results.append(True)
            elif 'placeholder' in str(image_path):
                status = "⚠️  PLACEHOLDER"
                results.append(False)
            else:
                # Vérifier si l'image existe
                if image_path and os.path.exists(image_path):
                    if 'from_json' in image_path:
                        status = "✅ IMAGE JSON"
                        results.append(True)
                    else:
                        status = "⚠️  PLACEHOLDER"
                        results.append(False)
                else:
                    status = "❌ ERREUR"
                    results.append(False)
            
            print(f"Resultat: {nom}")
            print(f"Statut: {status}")
            print(f"Attendu: {expected}")
            
        except Exception as e:
            print(f"ERREUR: {e}")
            results.append(False)
    
    # Récapitulatif
    print("\n" + "="*70)
    print("RECAPITULATIF")
    print("="*70)
    print(f"\nTests reussis: {sum(results)}/{len(results)}")
    print(f"Taux de reussite: {sum(results)/len(results)*100:.1f}%\n")
    
    if sum(results) == len(results):
        print("🎉 TOUS LES TESTS PASSES !")
    elif sum(results) >= len(results) * 0.8:
        print("✅ Majorité des tests passes")
    else:
        print("⚠️  Plusieurs tests ont echoue")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    test_multiple_products()

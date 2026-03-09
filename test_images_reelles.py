"""
Test Rapide - Génération avec Images Réelles du JSON
Démontre la solution 100% gratuite avec les 780 images professionnelles
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import ProductAISystem


def test_pizza_escalope():
    """Teste la génération de pizza escalope avec image réelle du JSON"""
    
    print("\n" + "=" * 70)
    print("🍕 TEST : Pizza Escalope")
    print("=" * 70)
    print()
    
    # Initialiser avec le backend 'from_json' (GRATUIT, 780 images réelles)
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='from_json',  # 780 images réelles GRATUITES
        image_api_key=None
    )
    
    print("📝 Génération : 'pizza escalope'\n")
    
    # Générer le produit
    product = system.generate_product_from_description(
        "pizza escalope",
        generate_image=True
    )
    
    # Afficher les résultats
    print("\n" + "=" * 70)
    print("📦 RÉSULTAT")
    print("=" * 70)
    
    print(f"\n🏷️  NOM : {product['displayName']['dflt']['nameDef']}")
    print(f"📂 CATÉGORIE : {product['category']}")
    print(f"💰 PRIX : {product['price']}€")
    
    print(f"\n📸 IMAGE : {os.path.basename(product['image_path'])}")
    
    if 'from_json' in product['image_path']:
        print("✅ IMAGE RÉELLE du JSON (professionnelle)")
        print("💰 Coût : 0.00€")
        print("⭐ Qualité : ⭐⭐⭐⭐⭐")
    elif 'placeholder' in product['image_path']:
        print("⚠️  Placeholder (cercle coloré)")
        print("💡 Si vous voulez une image réelle, utilisez image_backend='from_json'")
    
    print("\n" + "=" * 70)
    
    return product


def test_multiple():
    """Teste plusieurs produits"""
    
    print("\n" + "=" * 70)
    print("🧪 TEST : 5 Produits avec Images Réelles")
    print("=" * 70)
    print()
    
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='from_json',
        image_api_key=None
    )
    
    test_products = [
        "pizza escalope",
        "pizza thon",
        "burger bacon",
        "milkshake fraise",
        "frappe caramel"
    ]
    
    results = []
    
    for desc in test_products:
        print(f"\n{'─' * 70}")
        print(f"📝 {desc}")
        print('─' * 70)
        
        product = system.generate_product_from_description(
            desc,
            generate_image=True
        )
        
        image_source = "JSON réelle" if 'from_json' in product['image_path'] else "Placeholder"
        
        print(f"✅ {product['displayName']['dflt']['nameDef']}")
        print(f"📷 {image_source}")
        
        results.append({
            'desc': desc,
            'name': product['displayName']['dflt']['nameDef'],
            'image': os.path.basename(product['image_path']),
            'from_json': 'from_json' in product['image_path']
        })
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    json_count = sum(1 for r in results if r['from_json'])
    
    print(f"\n✅ Images réelles du JSON : {json_count}/{len(results)}")
    print(f"⚠️  Placeholders : {len(results) - json_count}/{len(results)}")
    print(f"💰 Coût total : 0.00€")
    print("⭐ Qualité : ⭐⭐⭐⭐⭐ (images réelles)")
    
    print("\n" + "=" * 70)


def show_instructions():
    """Affiche les instructions pour utiliser le système avec images réelles"""
    
    print("\n" + "=" * 70)
    print("📖 COMMENT AVOIR DES IMAGES RÉELLES (GRATUIT)")
    print("=" * 70)
    print()
    
    print("🎯 SOLUTION 1 : Modifier main.py (ligne ~314)")
    print("-" * 70)
    print()
    print("   Changez :")
    print("   IMAGE_BACKEND = 'placeholder'")
    print()
    print("   En :")
    print("   IMAGE_BACKEND = 'from_json'  # 780 images réelles GRATUITES")
    print()
    
    print("\n🎯 SOLUTION 2 : Utiliser ProductAISystem directement")
    print("-" * 70)
    print()
    print("   from main import ProductAISystem")
    print()
    print("   system = ProductAISystem(")
    print("       json_data_path=r'...\\3.json',")
    print("       image_backend='from_json',  # Au lieu de 'placeholder'")
    print("       image_api_key=None")
    print("   )")
    print()
    print("   product = system.generate_product_from_description(")
    print("       'pizza escalope',")
    print("       generate_image=True")
    print("   )")
    print()
    
    print("\n💡 BACKENDS DISPONIBLES :")
    print("-" * 70)
    print()
    print("   'from_json'     → 780 images réelles (GRATUIT) ⭐⭐⭐⭐⭐")
    print("   'hybrid_free'   → JSON + placeholder (GRATUIT) ⭐⭐⭐⭐")
    print("   'placeholder'   → Cercles colorés (GRATUIT) ⭐⭐")
    print("   'dall-e'        → DALL-E 3 (0.04€/image) ⭐⭐⭐⭐⭐")
    print("   'stable-diffusion' → SD API (0.002€/image) ⭐⭐⭐⭐")
    print()
    
    print("\n📁 Images disponibles dans le JSON : 780 produits")
    print("   - Pizzas : 152 images")
    print("   - Burgers : 84 images")
    print("   - Boissons : 118 images")
    print("   - Desserts : 96 images")
    print("   - Et plus encore...")
    print()
    
    print("=" * 70)


def main():
    """Menu principal"""
    
    print("\n" + "=" * 70)
    print("🧪 TEST IMAGES RÉELLES - Menu")
    print("=" * 70)
    print()
    print("1. Tester 'pizza escalope'")
    print("2. Tester 5 produits")
    print("3. Voir les instructions")
    print("4. Tout tester")
    print("0. Quitter")
    print()
    
    choice = input("Votre choix : ").strip()
    
    if choice == '1':
        test_pizza_escalope()
    elif choice == '2':
        test_multiple()
    elif choice == '3':
        show_instructions()
    elif choice == '4':
        show_instructions()
        test_pizza_escalope()
        test_multiple()
    elif choice == '0':
        print("\n👋 Au revoir !")
        return
    else:
        print("\n❌ Choix invalide")
        return
    
    print("\n💡 Pour utiliser les images réelles en mode interactif :")
    print("   Modifiez main.py ligne ~314 :")
    print("   IMAGE_BACKEND = 'from_json'")
    print()
    print("📖 Documentation : SOLUTION_GRATUITE.md")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt demandé")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

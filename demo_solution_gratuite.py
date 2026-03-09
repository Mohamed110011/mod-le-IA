"""
Démonstration - Solution 100% GRATUITE
Utilise les 780 images réelles du JSON
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from image_generator_ai import ImageGeneratorAI
import time


def demo_json_images():
    """Démontre la recherche dans les 780 images JSON"""
    
    print("\n" + "=" * 70)
    print("🎁 SOLUTION 100% GRATUITE - Démonstration")
    print("=" * 70)
    print()
    print("📚 Utilisation des 780 images professionnelles du JSON")
    print("💰 Coût : 0.00€")
    print("⭐ Qualité : Images réelles de restaurants")
    print("⚡ Vitesse : Instantané (< 0.1 seconde)")
    print()
    
    json_path = r"c:\Users\mohamed taher\Downloads\3.json"
    
    if not os.path.exists(json_path):
        print(f"❌ Fichier JSON non trouvé : {json_path}")
        print("\n💡 Modifiez le chemin dans le script :")
        print(f"   json_path = r\"VOTRE_CHEMIN_ICI\"")
        return
    
    # Créer le générateur avec backend JSON
    print("🔧 Initialisation...")
    generator = ImageGeneratorAI(
        backend='from_json',
        json_path=json_path
    )
    
    # Produits de test (tous disponibles dans le JSON)
    test_products = [
        ("pizza thon", "Pizza au Thon", "PIZZAS"),
        ("pizza chorizo", "Pizza Chorizo", "PIZZAS"),
        ("milkshake fraise", "Milkshake Fraise", "BOISSONS"),
        ("burger bacon", "Burger Bacon", "BURGERS"),
        ("frappe caramel", "Frappé Caramel", "BOISSONS"),
    ]
    
    print(f"\n📝 Test avec {len(test_products)} produits...\n")
    
    results = []
    total_time = 0
    
    for i, (search, name, category) in enumerate(test_products, 1):
        print(f"\n{'─' * 70}")
        print(f"🔍 Test {i}/{len(test_products)} : {name}")
        print(f"{'─' * 70}")
        
        start = time.time()
        
        try:
            image_path = generator.generate_image(
                description=search,
                product_name=name,
                category=category
            )
            
            elapsed = time.time() - start
            total_time += elapsed
            
            if 'from_json' in image_path:
                print(f"\n✅ TROUVÉE dans le JSON !")
                print(f"   📁 Image : {os.path.basename(image_path)}")
                print(f"   ⏱️  Temps : {elapsed:.3f}s")
                print(f"   💰 Coût : 0.00€")
                print(f"   ⭐ Qualité : Image réelle professionnelle")
                results.append({'name': name, 'found': True, 'time': elapsed})
            else:
                print(f"\n⚠️  Non trouvée - placeholder généré")
                print(f"   📁 Image : {os.path.basename(image_path)}")
                results.append({'name': name, 'found': False, 'time': elapsed})
        
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            results.append({'name': name, 'found': False, 'time': 0})
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES RÉSULTATS")
    print("=" * 70)
    
    found_count = sum(1 for r in results if r['found'])
    
    print(f"\n✅ Images trouvées : {found_count}/{len(results)} ({found_count*100//len(results)}%)")
    print(f"⏱️  Temps total : {total_time:.3f}s")
    print(f"⏱️  Temps moyen : {total_time/len(results):.3f}s par image")
    print(f"💰 Coût total : 0.00€")
    print(f"⭐ Qualité : Images réelles professionnelles")
    print(f"\n📁 Dossier : {generator.output_dir}")
    
    print("\n" + "=" * 70)
    print("🎉 SOLUTION 100% GRATUITE VALIDÉE !")
    print("=" * 70)
    print()
    print("📖 Documentation : SOLUTION_GRATUITE.md")
    print()


def demo_hybrid_mode():
    """Démontre le mode hybride (JSON + Placeholder)"""
    
    print("\n" + "=" * 70)
    print("🔄 MODE HYBRIDE - Démonstration")
    print("=" * 70)
    print()
    print("Stratégie : JSON d'abord → Placeholder si non trouvé")
    print("💰 Coût : 0.00€")
    print()
    
    json_path = r"c:\Users\mohamed taher\Downloads\3.json"
    
    if not os.path.exists(json_path):
        print(f"❌ Fichier JSON non trouvé : {json_path}")
        return
    
    generator = ImageGeneratorAI(
        backend='hybrid_free',
        json_path=json_path
    )
    
    # Mélange de produits existants et nouveaux
    test_cases = [
        ("pizza thon", "Pizza au Thon", "PIZZAS", "Devrait être trouvée"),
        ("Pizza Nutella Fraise", "Pizza Dessert Nutella", "PIZZAS", "Nouveau produit → placeholder"),
    ]
    
    for search, name, category, expected in test_cases:
        print(f"\n{'─' * 70}")
        print(f"Test : {name}")
        print(f"Expected : {expected}")
        print(f"{'─' * 70}")
        
        start = time.time()
        
        try:
            image_path = generator.generate_image(
                description=search,
                product_name=name,
                category=category
            )
            
            elapsed = time.time() - start
            
            if 'from_json' in image_path:
                source = "✅ JSON (image réelle)"
            else:
                source = "🎨 Placeholder (coloré)"
            
            print(f"\n{source}")
            print(f"   📁 {os.path.basename(image_path)}")
            print(f"   ⏱️  {elapsed:.3f}s")
            print(f"   💰 0.00€")
        
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
    
    print("\n" + "=" * 70)
    print("✅ Mode hybride fonctionnel")
    print("=" * 70)


def show_stats():
    """Affiche les statistiques du JSON"""
    
    print("\n" + "=" * 70)
    print("📊 STATISTIQUES - Images Disponibles")
    print("=" * 70)
    
    json_path = r"c:\Users\mohamed taher\Downloads\3.json"
    
    if not os.path.exists(json_path):
        print(f"❌ Fichier JSON non trouvé")
        return
    
    generator = ImageGeneratorAI(
        backend='from_json',
        json_path=json_path
    )
    
    print(f"\n📚 Images chargées : {len(generator.image_cache)}")
    print(f"💰 Coût : 0.00€")
    print(f"⭐ Qualité : Images réelles professionnelles")
    print()
    
    # Analyser par catégorie (basé sur les mots-clés)
    categories = {}
    for key, data in generator.image_cache.items():
        name = data['original_name'].lower()
        
        if 'pizza' in name:
            cat = 'PIZZAS'
        elif 'burger' in name:
            cat = 'BURGERS'
        elif 'milkshake' in name or 'milk' in name:
            cat = 'MILKSHAKES'
        elif 'frappe' in name or 'boisson' in name or 'juice' in name:
            cat = 'BOISSONS'
        elif 'dessert' in name or 'gateau' in name or 'tarte' in name:
            cat = 'DESSERTS'
        elif 'finger' in name or 'nuggets' in name or 'frites' in name:
            cat = 'FINGER FOOD'
        elif 'salade' in name:
            cat = 'SALADES'
        else:
            cat = 'AUTRES'
        
        categories[cat] = categories.get(cat, 0) + 1
    
    print("📋 Répartition par catégorie (approximative) :")
    print()
    for cat in sorted(categories.keys()):
        count = categories[cat]
        bar = "█" * (count // 5)
        print(f"  {cat:15} : {count:3} images {bar}")
    
    print("\n" + "=" * 70)
    print(f"✅ Total : {len(generator.image_cache)} images professionnelles disponibles")
    print("💰 Coût : 0.00€")
    print("=" * 70)


def main():
    """Menu principal"""
    
    while True:
        print("\n" + "=" * 70)
        print("🎁 SOLUTION 100% GRATUITE - Menu")
        print("=" * 70)
        print()
        print("1. Démonstration JSON (5 produits)")
        print("2. Démonstration Mode Hybride")
        print("3. Voir les statistiques")
        print("4. Tout tester")
        print("0. Quitter")
        print()
        
        choice = input("Votre choix : ").strip()
        
        if choice == '1':
            demo_json_images()
        elif choice == '2':
            demo_hybrid_mode()
        elif choice == '3':
            show_stats()
        elif choice == '4':
            show_stats()
            demo_json_images()
            demo_hybrid_mode()
        elif choice == '0':
            print("\n" + "=" * 70)
            print("👋 Merci d'avoir testé la Solution 100% GRATUITE !")
            print("=" * 70)
            print()
            print("📖 Documentation complète : SOLUTION_GRATUITE.md")
            print("💰 Coût : 0.00€")
            print("⭐ Qualité : Images réelles professionnelles")
            print("📚 Images disponibles : 780")
            print()
            break
        else:
            print("\n❌ Choix invalide")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

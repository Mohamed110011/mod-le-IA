"""
Script de Test - Solution 100% GRATUITE
Teste la génération d'images avec Hugging Face (gratuit)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from image_generator_ai import ImageGeneratorAI
import time


def test_huggingface_free():
    """Teste la génération gratuite avec Hugging Face"""
    
    print("=" * 70)
    print("🎁 TEST DE LA SOLUTION 100% GRATUITE")
    print("=" * 70)
    print()
    print("Backend : Hugging Face Inference API")
    print("Coût : 0€")
    print("Clé API : Non nécessaire")
    print()
    
    # Créer le générateur (aucune clé API nécessaire !)
    generator = ImageGeneratorAI(
        backend='huggingface',
        api_key=None  # Pas de clé nécessaire !
    )
    
    # Produits de test
    test_products = [
        {
            "name": "Pizza Margherita",
            "description": "Pizza margherita avec tomate fraîche et mozzarella",
            "category": "PIZZAS"
        },
        {
            "name": "Burger Classique",
            "description": "Burger avec steak, salade, tomate et sauce",
            "category": "BURGERS"
        },
        {
            "name": "Milkshake Chocolat",
            "description": "Milkshake au chocolat avec chantilly",
            "category": "BOISSONS"
        }
    ]
    
    print(f"📝 Génération de {len(test_products)} images GRATUITES...\n")
    
    results = []
    total_time = 0
    
    for i, product in enumerate(test_products, 1):
        print(f"\n{'='*70}")
        print(f"Produit {i}/{len(test_products)}: {product['name']}")
        print(f"{'='*70}")
        
        start = time.time()
        
        try:
            image_path = generator.generate_image(
                description=product['description'],
                product_name=product['name'],
                category=product['category']
            )
            
            elapsed = time.time() - start
            total_time += elapsed
            
            if image_path and 'placeholder' not in image_path:
                print(f"\n✅ SUCCÈS !")
                print(f"   📁 Image : {os.path.basename(image_path)}")
                print(f"   ⏱️  Temps : {elapsed:.1f}s")
                print(f"   💰 Coût : 0.00€")
                results.append({
                    'name': product['name'],
                    'path': image_path,
                    'time': elapsed,
                    'success': True
                })
            else:
                print(f"\n⚠️  Échec - placeholder généré")
                results.append({
                    'name': product['name'],
                    'path': image_path,
                    'time': elapsed,
                    'success': False
                })
        
        except Exception as e:
            elapsed = time.time() - start
            print(f"\n❌ ERREUR : {e}")
            results.append({
                'name': product['name'],
                'path': None,
                'time': elapsed,
                'success': False
            })
        
        # Petite pause pour éviter le rate limiting
        if i < len(test_products):
            print("\n⏳ Pause de 3 secondes...")
            time.sleep(3)
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES RÉSULTATS")
    print("=" * 70)
    
    success_count = sum(1 for r in results if r['success'])
    
    print(f"\n✅ Images générées avec succès : {success_count}/{len(results)}")
    print(f"⏱️  Temps total : {total_time:.1f}s")
    print(f"⏱️  Temps moyen : {total_time/len(results):.1f}s par image")
    print(f"💰 Coût total : 0.00€")
    print(f"\n📁 Dossier : {generator.output_dir}")
    
    print("\n" + "=" * 70)
    
    if success_count == len(results):
        print("🎉 SUCCÈS COMPLET ! Tous les produits ont été générés GRATUITEMENT !")
    elif success_count > 0:
        print(f"✅ {success_count} produits générés avec succès.")
        print("⚠️  Certains ont échoué (rate limit possible, réessayez dans quelques minutes)")
    else:
        print("❌ Aucune image générée.")
        print("💡 Vérifiez votre connexion internet.")
    
    print("=" * 70)
    
    return results


def test_hybrid_free():
    """Teste le mode hybride (JSON + Hugging Face)"""
    
    print("\n" + "=" * 70)
    print("🔄 TEST DU MODE HYBRIDE GRATUIT")
    print("=" * 70)
    print()
    print("Stratégie : JSON d'abord (instantané), puis Hugging Face (5-10s)")
    print("Coût : 0€")
    print()
    
    json_path = r"c:\Users\mohamed taher\Downloads\3.json"
    
    if not os.path.exists(json_path):
        print(f"⚠️  Fichier JSON non trouvé : {json_path}")
        print("   Modifiez le chemin dans le script ou utilisez test_huggingface_free()")
        return
    
    generator = ImageGeneratorAI(
        backend='hybrid_free',
        api_key=None,
        json_path=json_path
    )
    
    # Test avec produits existants et nouveaux
    test_cases = [
        ("pizza thon", "Pizza au thon", "PIZZAS", "Devrait être trouvée dans JSON"),
        ("pizza chorizo", "Pizza au chorizo", "PIZZAS", "Devrait être trouvée dans JSON"),
        ("Pizza Nutella Fraise", "Pizza dessert nutella et fraise", "PIZZAS", "Nouveau produit - génération IA"),
    ]
    
    print(f"📝 Test de {len(test_cases)} cas...\n")
    
    for search_term, name, category, expected in test_cases:
        print(f"\n{'='*70}")
        print(f"Test : {name}")
        print(f"Expected : {expected}")
        print(f"{'='*70}")
        
        start = time.time()
        
        try:
            image_path = generator.generate_image(
                description=search_term,
                product_name=name,
                category=category
            )
            
            elapsed = time.time() - start
            
            source = "JSON" if elapsed < 1 else "Hugging Face IA"
            
            print(f"\n✅ Image générée")
            print(f"   📁 {os.path.basename(image_path)}")
            print(f"   🔍 Source : {source}")
            print(f"   ⏱️  Temps : {elapsed:.1f}s")
            print(f"   💰 Coût : 0.00€")
        
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
        
        time.sleep(2)
    
    print("\n" + "=" * 70)
    print("✅ Test du mode hybride terminé")
    print("=" * 70)


def main():
    """Menu principal"""
    
    print("\n" + "=" * 70)
    print("🎁 SOLUTION 100% GRATUITE - Menu de Test")
    print("=" * 70)
    print()
    print("Choisissez un test :")
    print()
    print("1. Test Hugging Face (3 images IA gratuites)")
    print("2. Test Mode Hybride (JSON + Hugging Face)")
    print("3. Les deux tests")
    print("0. Quitter")
    print()
    
    choice = input("Votre choix (1-3) : ").strip()
    
    if choice == '1':
        test_huggingface_free()
    elif choice == '2':
        test_hybrid_free()
    elif choice == '3':
        test_huggingface_free()
        test_hybrid_free()
    elif choice == '0':
        print("\n👋 Au revoir !")
        return
    else:
        print("\n❌ Choix invalide")
        return
    
    print("\n" + "=" * 70)
    print("🎊 TOUS LES TESTS TERMINÉS")
    print("=" * 70)
    print()
    print("💡 Pour utiliser dans votre code :")
    print()
    print("   from main import ProductAISystem")
    print()
    print("   # Mode Hugging Face (100% gratuit)")
    print("   system = ProductAISystem(")
    print("       json_data_path=r'...',")
    print("       image_backend='huggingface',")
    print("       image_api_key=None")
    print("   )")
    print()
    print("   # Mode Hybride (recommandé - 100% gratuit)")
    print("   system = ProductAISystem(")
    print("       json_data_path=r'...',")
    print("       image_backend='hybrid_free',")
    print("       image_api_key=None")
    print("   )")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

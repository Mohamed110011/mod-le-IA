#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration de l'utilisation des images depuis le JSON
"""

from main import ProductAISystem


def demo_with_json_images():
    """Démo avec images extraites du JSON"""
    print("\n" + "=" * 70)
    print("🖼️  DÉMONSTRATION : IMAGES DEPUIS LE JSON")
    print("=" * 70)
    print()
    
    # Initialiser le système avec backend 'from_json'
    print("📋 Initialisation du système avec images depuis JSON...")
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='from_json'  # ← Nouveau backend !
    )
    print()
    
    # Liste de produits à tester
    test_products = [
        "Milkshake Fraise avec crème fouettée",
        "Pizza Norvégienne avec saumon",
        "Frappe Caramel glacé"
    ]
    
    print("=" * 70)
    print("📦 GÉNÉRATION DE PRODUITS AVEC IMAGES DU JSON")
    print("=" * 70)
    print()
    
    generated_products = []
    
    for i, description in enumerate(test_products, 1):
        print(f"\n{'='*70}")
        print(f"Produit {i}/{len(test_products)}: {description}")
        print('='*70)
        
        try:
            # Générer le produit
            product = system.generate_product_from_description(
                description=description,
                generate_image=True,
                force=False
            )
            
            # Afficher le résumé
            system.display_product_summary(product)
            generated_products.append(product)
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
            continue
    
    print("\n" + "=" * 70)
    print("💾 SAUVEGARDE DES PRODUITS")
    print("=" * 70)
    print()
    
    if generated_products:
        output_file = system.save_products_to_json(
            generated_products,
            'd:/model-IA-image/products_with_json_images.json'
        )
        print(f"✅ {len(generated_products)} produits sauvegardés")
        print(f"📁 Fichier: {output_file}")
    else:
        print("⚠️  Aucun produit généré")
    
    print("\n" + "=" * 70)
    print("📊 RÉCAPITULATIF")
    print("=" * 70)
    print()
    print(f"✅ Produits générés: {len(generated_products)}")
    print(f"🖼️  Images récupérées depuis le JSON")
    print(f"📂 Dossier images: d:/model-IA-image/generated_images/")
    print()
    print("🎯 AVANTAGES DU MODE 'from_json':")
    print("   ✅ Utilise les vraies images des produits existants")
    print("   ✅ Pas besoin d'API payante (DALL-E, Stable Diffusion)")
    print("   ✅ Cohérence avec votre catalogue existant")
    print("   ✅ Génération instantanée (simple téléchargement)")
    print()
    print("=" * 70)
    print("🎉 Démonstration terminée !")
    print("=" * 70)
    print()


def compare_backends():
    """Compare les différents backends d'images"""
    print("\n" + "=" * 70)
    print("📊 COMPARAISON DES BACKENDS D'IMAGES")
    print("=" * 70)
    print()
    
    backends_info = [
        {
            'name': 'from_json',
            'description': 'Images extraites du JSON existant',
            'pros': ['✅ Gratuites', '✅ Vraies images produits', '✅ Instantané', '✅ Cohérent avec catalogue'],
            'cons': ['⚠️  Nécessite que le produit existe dans le JSON'],
            'best_for': 'Utilisation avec catalogue existant'
        },
        {
            'name': 'placeholder',
            'description': 'Images générées localement (cercles colorés)',
            'pros': ['✅ Gratuit', '✅ Aucune dépendance externe', '✅ Rapide'],
            'cons': ['⚠️  Qualité basique', '⚠️  Non réaliste'],
            'best_for': 'Développement et tests'
        },
        {
            'name': 'dall-e',
            'description': 'IA générative OpenAI',
            'pros': ['✅ Haute qualité', '✅ Très réaliste', '✅ Personnalisable'],
            'cons': ['⚠️  Payant (~$0.02/image)', '⚠️  Nécessite API key'],
            'best_for': 'Nouveaux produits uniques'
        },
        {
            'name': 'stable-diffusion',
            'description': 'IA générative Stability AI',
            'pros': ['✅ Bonne qualité', '✅ Prix abordable', '✅ Flexible'],
            'cons': ['⚠️  Payant', '⚠️  Nécessite API key'],
            'best_for': 'Génération de masse'
        }
    ]
    
    for i, backend in enumerate(backends_info, 1):
        print(f"\n{i}. {backend['name'].upper()}")
        print(f"   📝 {backend['description']}")
        print()
        print("   Avantages:")
        for pro in backend['pros']:
            print(f"      {pro}")
        print()
        print("   Inconvénients:")
        for con in backend['cons']:
            print(f"      {con}")
        print()
        print(f"   🎯 Idéal pour: {backend['best_for']}")
        print("   " + "-" * 60)
    
    print("\n" + "=" * 70)
    print("💡 RECOMMANDATION")
    print("=" * 70)
    print()
    print("1. Pour enrichir un catalogue existant → 'from_json'")
    print("2. Pour développement/tests rapides → 'placeholder'")
    print("3. Pour de nouveaux produits uniques → 'dall-e'")
    print("4. Pour génération en masse abordable → 'stable-diffusion'")
    print()


def main():
    """Menu principal"""
    print("\n" + "=" * 70)
    print("🖼️  SYSTÈME D'IMAGES DEPUIS JSON")
    print("=" * 70)
    print()
    print("Ce script démontre l'utilisation du nouveau backend 'from_json'")
    print("qui permet d'utiliser les images déjà présentes dans votre JSON.")
    print()
    print("📋 Choisissez une option:")
    print()
    print("1. Démonstration complète (génération 3 produits)")
    print("2. Comparaison des backends d'images")
    print("3. Les deux")
    print("0. Quitter")
    print()
    
    choice = input("Votre choix (0-3): ").strip()
    
    if choice == '1':
        demo_with_json_images()
    elif choice == '2':
        compare_backends()
    elif choice == '3':
        compare_backends()
        input("\nAppuyez sur Entrée pour continuer vers la démo...")
        demo_with_json_images()
    else:
        print("\n✅ Au revoir !\n")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print("\n❌ ERREUR: Fichier JSON introuvable")
        print(f"   {e}")
        print("📍 Chemin attendu: c:\\Users\\mohamed taher\\Downloads\\3.json\n")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur\n")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}\n")
        import traceback
        traceback.print_exc()

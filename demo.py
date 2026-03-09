"""
Script de démonstration rapide du système IA
Exécuter: python demo.py
"""

from product_generator_ai import ProductGeneratorAI
from image_generator_ai import ImageGeneratorAI
import json
import os

def print_separator(title=""):
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)
    else:
        print()

def demo():
    print("\n🤖 DÉMONSTRATION DU SYSTÈME IA DE GÉNÉRATION DE PRODUITS")
    print_separator()
    
    # 1. Initialisation
    print("📋 Étape 1 : Initialisation du système...")
    try:
        generator = ProductGeneratorAI(r"c:\Users\mohamed taher\Downloads\3.json")
        image_gen = ImageGeneratorAI(backend='placeholder')
        print("   ✅ Système initialisé avec succès")
    except Exception as e:
        print(f"   ⚠️  Fichier JSON non trouvé, utilisation du mode autonome")
        generator = ProductGeneratorAI()
        image_gen = ImageGeneratorAI(backend='placeholder')
    
    # 2. Exemples de génération
    print_separator("📝 Étape 2 : Génération de produits")
    
    exemples = [
        "Pizza Margherita avec mozzarella et basilic frais",
        "Milkshake chocolat avec chantilly",
        "Chicken Nuggets croustillants 6 pièces"
    ]
    
    produits_generes = []
    
    for i, description in enumerate(exemples, 1):
        print(f"\n{i}. Description : {description}")
        print("   " + "-"*66)
        
        # Générer le produit
        produit = generator.generate_complete_product(description)
        produits_generes.append(produit)
        
        # Afficher les informations
        print(f"   ✅ Nom : {produit['displayName']['dflt']['nameDef']}")
        print(f"   📂 Catégorie : {produit['category']}")
        print(f"   💰 Prix : {produit['price']}€")
        print(f"   ⚠️  Allergènes : {', '.join(produit['allergens']) if produit['allergens'] else 'Aucun'}")
        
        # Afficher les traductions
        sales_support = produit['displayName']['dflt'].get('salesSupport', {})
        if sales_support:
            print(f"   🌍 Traductions :")
            for lang, trans in sales_support.items():
                if isinstance(trans, dict) and 'name' in trans:
                    print(f"      {lang.upper()}: {trans['name']}")
        
        # Générer l'image
        print(f"   🎨 Génération de l'image...")
        image_path = image_gen.generate_image(
            description=description,
            product_name=produit['displayName']['dflt']['nameDef'],
            category=produit['category']
        )
        produit['img']['dflt']['img'] = image_path
        print(f"      ✅ Image : {os.path.basename(image_path)}")
    
    # 3. Sauvegarde
    print_separator("💾 Étape 3 : Sauvegarde des produits")
    
    output_file = 'd:/model-IA-image/demo_products.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(produits_generes, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ {len(produits_generes)} produits sauvegardés")
    print(f"   📁 Fichier : {output_file}")
    
    # 4. Récapitulatif
    print_separator("📊 RÉCAPITULATIF")
    
    print(f"\n✅ Démonstration terminée avec succès !")
    print(f"\n📦 Produits générés : {len(produits_generes)}")
    print(f"🎨 Images générées : {len(produits_generes)}")
    print(f"💾 Fichier JSON : demo_products.json")
    print(f"📂 Images : ./generated_images/")
    
    print("\n🎯 CAPACITÉS DU SYSTÈME :")
    print("   ✅ Génération automatique de nom")
    print("   ✅ Détection de catégorie")
    print("   ✅ Estimation de prix")
    print("   ✅ Identification d'allergènes")
    print("   ✅ Génération d'options (tailles, etc.)")
    print("   ✅ Traductions multilingues (FR, EN, AR)")
    print("   ✅ Génération d'images")
    print("   ✅ Export JSON complet")
    
    print("\n🚀 PROCHAINES ÉTAPES :")
    print("   1. Lancer le mode interactif : python main.py")
    print("   2. Tester les exemples avancés : python examples.py")
    print("   3. Lire la documentation : README.md")
    
    print("\n" + "="*70)
    print("  Merci d'avoir testé le système ! 🎉")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n👋 Démonstration interrompue.")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

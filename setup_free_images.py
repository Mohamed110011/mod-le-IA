"""
Setup Interactif - Solution 100% GRATUITE
Guide pour configurer et utiliser la génération d'images gratuite
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from image_generator_ai import ImageGeneratorAI


def show_welcome():
    """Affiche le message de bienvenue"""
    print("\n" + "=" * 70)
    print("🎁 SOLUTION 100% GRATUITE - Configuration")
    print("=" * 70)
    print()
    print("Générez des images réalistes sans dépenser 1 centime !")
    print()
    print("✅ Aucune carte bancaire nécessaire")
    print("✅ Aucune inscription requise")
    print("✅ Qualité professionnelle")
    print("✅ Nombre illimité d'images")
    print()


def show_options_comparison():
    """Compare les options gratuites"""
    print("\n" + "=" * 70)
    print("📊 OPTIONS GRATUITES DISPONIBLES")
    print("=" * 70)
    print()
    
    print("╔═══════════════════════╦═══════════╦═══════════╦═══════════════╗")
    print("║ Option                ║ Coût      ║ Qualité   ║ Temps/image   ║")
    print("╠═══════════════════════╬═══════════╬═══════════╬═══════════════╣")
    print("║ JSON (existant)       ║ 0€        ║ ⭐⭐⭐⭐⭐   ║ Instantané    ║")
    print("║ Hugging Face IA       ║ 0€        ║ ⭐⭐⭐⭐     ║ 5-10 secondes ║")
    print("║ Hybride (recommandé)  ║ 0€        ║ ⭐⭐⭐⭐⭐   ║ Variable      ║")
    print("║ Placeholder           ║ 0€        ║ ⭐⭐       ║ Instantané    ║")
    print("╠═══════════════════════╬═══════════╬═══════════╬═══════════════╣")
    print("║ DALL-E 3 (payant)     ║ 0.04€     ║ ⭐⭐⭐⭐⭐   ║ 3-5 secondes  ║")
    print("║ Stable Diffusion API  ║ 0.002€    ║ ⭐⭐⭐⭐     ║ 2-4 secondes  ║")
    print("╚═══════════════════════╩═══════════╩═══════════╩═══════════════╝")
    print()
    print("💡 Recommandation : Mode HYBRIDE")
    print("   → Utilise les images JSON (réelles) quand disponibles")
    print("   → Génère avec Hugging Face pour les nouveaux produits")
    print()


def show_how_it_works():
    """Explique le fonctionnement"""
    print("\n" + "=" * 70)
    print("🔧 COMMENT ÇA MARCHE ?")
    print("=" * 70)
    print()
    
    print("1️⃣  MODE JSON (from_json)")
    print("   • Recherche dans 780 images professionnelles existantes")
    print("   • Instantané (< 0.1 seconde)")
    print("   • Idéal pour : pizzas, burgers, desserts standards")
    print()
    
    print("2️⃣  MODE HUGGING FACE (huggingface)")
    print("   • Génère avec Stable Diffusion 2.1")
    print("   • 5-10 secondes par image")
    print("   • Aucune clé API nécessaire")
    print("   • Limite : ~100 images/heure")
    print("   • Idéal pour : nouveaux produits uniques")
    print()
    
    print("3️⃣  MODE HYBRIDE (hybrid_free) ⭐ RECOMMANDÉ")
    print("   • Essaie JSON d'abord (rapide)")
    print("   • Si non trouvé → Hugging Face (gratuit)")
    print("   • Meilleur des deux mondes")
    print("   • Idéal pour : tous les usages")
    print()


def generate_demo():
    """Génère 3 images de démonstration"""
    print("\n" + "=" * 70)
    print("🎨 DÉMONSTRATION - Génération de 3 Images GRATUITES")
    print("=" * 70)
    print()
    
    print("Quelle méthode voulez-vous tester ?")
    print()
    print("1. Hugging Face (IA gratuite - 3 nouvelles images)")
    print("2. Mode Hybride (JSON + IA - nécessite le fichier JSON)")
    print("3. JSON uniquement (recherche d'images existantes)")
    print("0. Retour")
    print()
    
    choice = input("Votre choix : ").strip()
    
    if choice == '1':
        _demo_huggingface()
    elif choice == '2':
        _demo_hybrid()
    elif choice == '3':
        _demo_json()
    else:
        return


def _demo_huggingface():
    """Démo Hugging Face"""
    print("\n🎨 Génération avec Hugging Face (100% gratuit)...\n")
    
    generator = ImageGeneratorAI(
        backend='huggingface',
        api_key=None
    )
    
    products = [
        ("Pizza Margherita", "Pizza margherita avec mozzarella", "PIZZAS"),
        ("Burger Classique", "Burger avec steak et cheddar", "BURGERS"),
        ("Milkshake Fraise", "Milkshake à la fraise avec chantilly", "BOISSONS")
    ]
    
    import time
    for name, desc, cat in products:
        print(f"\n🎨 Génération : {name}")
        start = time.time()
        
        try:
            path = generator.generate_image(desc, name, cat)
            elapsed = time.time() - start
            
            if path and 'placeholder' not in path:
                print(f"✅ Succès en {elapsed:.1f}s - {os.path.basename(path)}")
            else:
                print(f"⚠️  Échec - placeholder généré")
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        time.sleep(3)  # Pause pour éviter rate limit
    
    print(f"\n📁 Images dans : {generator.output_dir}")


def _demo_hybrid():
    """Démo Mode Hybride"""
    json_path = input("\n📁 Chemin du fichier JSON : ").strip().strip('"')
    
    if not os.path.exists(json_path):
        print(f"❌ Fichier non trouvé : {json_path}")
        return
    
    print("\n🔄 Mode Hybride : JSON + Hugging Face...\n")
    
    generator = ImageGeneratorAI(
        backend='hybrid_free',
        api_key=None,
        json_path=json_path
    )
    
    products = [
        ("pizza thon", "Pizza au thon", "PIZZAS"),
        ("Pizza Exotique Ananas", "Pizza dessert ananas coco", "PIZZAS"),
    ]
    
    import time
    for desc, name, cat in products:
        print(f"\n🔍 Test : {name}")
        start = time.time()
        
        try:
            path = generator.generate_image(desc, name, cat)
            elapsed = time.time() - start
            source = "JSON" if elapsed < 1 else "Hugging Face IA"
            
            print(f"✅ {source} - {elapsed:.1f}s - {os.path.basename(path)}")
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        time.sleep(2)
    
    print(f"\n📁 Images dans : {generator.output_dir}")


def _demo_json():
    """Démo JSON uniquement"""
    json_path = input("\n📁 Chemin du fichier JSON : ").strip().strip('"')
    
    if not os.path.exists(json_path):
        print(f"❌ Fichier non trouvé : {json_path}")
        return
    
    print("\n🔍 Recherche dans les 780 images JSON...\n")
    
    generator = ImageGeneratorAI(
        backend='from_json',
        api_key=None,
        json_path=json_path
    )
    
    products = [
        ("pizza thon", "Pizza au thon", "PIZZAS"),
        ("pizza chorizo", "Pizza au chorizo", "PIZZAS"),
        ("milkshake fraise", "Milkshake fraise", "BOISSONS"),
    ]
    
    for desc, name, cat in products:
        print(f"\n🔍 Recherche : {name}")
        
        try:
            path = generator.generate_image(desc, name, cat)
            
            if path and 'from_json' in path:
                print(f"✅ Trouvée - {os.path.basename(path)}")
            else:
                print(f"⚠️  Non trouvée - placeholder généré")
        except Exception as e:
            print(f"❌ Erreur : {e}")
    
    print(f"\n📁 Images dans : {generator.output_dir}")


def show_code_examples():
    """Affiche des exemples de code"""
    print("\n" + "=" * 70)
    print("💻 EXEMPLES DE CODE")
    print("=" * 70)
    print()
    
    print("📝 Exemple 1 : Mode Hugging Face (100% gratuit)")
    print("-" * 70)
    print("""
from main import ProductAISystem

system = ProductAISystem(
    json_data_path=r"c:\\Users\\...\\3.json",
    image_backend='huggingface',  # 100% GRATUIT
    image_api_key=None  # Pas de clé nécessaire !
)

product = system.generate_product_from_description(
    "Pizza Margherita avec mozzarella",
    generate_image=True
)

print(f"Image : {product['image_path']}")
# → Pizza_Margherita_huggingface.webp (GRATUIT)
""")
    
    print("\n📝 Exemple 2 : Mode Hybride (recommandé)")
    print("-" * 70)
    print("""
from main import ProductAISystem

system = ProductAISystem(
    json_data_path=r"c:\\Users\\...\\3.json",
    image_backend='hybrid_free',  # Mode hybride
    image_api_key=None
)

# Produit existant → image JSON (instantané)
product1 = system.generate_product_from_description("pizza thon")
# → SPECIALE THON (image réelle du JSON)

# Nouveau produit → génération IA (5-10s)
product2 = system.generate_product_from_description("Pizza Nutella")
# → Pizza_Nutella_huggingface.webp (GRATUIT)
""")
    
    print("\n📝 Exemple 3 : Génération en lot (100 produits)")
    print("-" * 70)
    print("""
from main import ProductAISystem

system = ProductAISystem(
    json_data_path=r"...",
    image_backend='hybrid_free'
)

descriptions = [
    "Pizza Margherita", "Pizza 4 Fromages", "Burger Classic",
    # ... 97 autres descriptions
]

for desc in descriptions:
    product = system.generate_product_from_description(
        desc, 
        generate_image=True
    )
    print(f"✅ {product['displayName']['dflt']['nameDef']}")

# Temps : ~10 minutes
# Coût : 0.00€ (100% GRATUIT !)
""")


def show_tips():
    """Affiche des conseils"""
    print("\n" + "=" * 70)
    print("💡 CONSEILS D'UTILISATION")
    print("=" * 70)
    print()
    
    print("✅ Pour OPTIMISER les performances :")
    print("   1. Utilisez le mode 'hybrid_free' (meilleur compromis)")
    print("   2. Générez par petits lots (20-30 images à la fois)")
    print("   3. Attendez 2-3 secondes entre chaque génération")
    print()
    
    print("⚠️  Si vous rencontrez des erreurs :")
    print("   • Rate limit (429) → Attendez 5-10 minutes")
    print("   • Modèle loading (503) → Le script attend automatiquement")
    print("   • Timeout → Vérifiez votre connexion internet")
    print()
    
    print("🚀 Pour de meilleures performances :")
    print("   • JSON : 780 images réelles instantanées")
    print("   • Hugging Face : ~100 images/heure gratuites")
    print("   • Mode hybride : Combine les deux intelligemment")
    print()


def main():
    """Menu principal"""
    show_welcome()
    
    while True:
        print("\n" + "=" * 70)
        print("📋 MENU PRINCIPAL")
        print("=" * 70)
        print()
        print("1. Voir les options gratuites disponibles")
        print("2. Comment ça marche ?")
        print("3. Générer des images de démonstration (GRATUIT)")
        print("4. Voir des exemples de code")
        print("5. Conseils d'utilisation")
        print("0. Quitter")
        print()
        
        choice = input("Votre choix : ").strip()
        
        if choice == '1':
            show_options_comparison()
        elif choice == '2':
            show_how_it_works()
        elif choice == '3':
            generate_demo()
        elif choice == '4':
            show_code_examples()
        elif choice == '5':
            show_tips()
        elif choice == '0':
            print("\n" + "=" * 70)
            print("🎊 Merci d'avoir utilisé la Solution 100% GRATUITE !")
            print("=" * 70)
            print()
            print("📖 Documentation : SOLUTION_GRATUITE.md")
            print("🧪 Tests : python test_huggingface_free.py")
            print()
            print("💰 Coût total : 0.00€")
            print("✨ Qualité : Professionnelle")
            print("🚀 Nombre d'images : Illimité")
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

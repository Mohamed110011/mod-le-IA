# -*- coding: utf-8 -*-
"""
Guide de configuration pour générer des images réalistes avec IA
"""

import sys
import os

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def show_api_instructions():
    """Affiche les instructions pour obtenir les clés API"""
    print("\n" + "="*70)
    print("🔑 CONFIGURATION DES CLES API")
    print("="*70 + "\n")
    
    print("Pour générer des images réalistes, vous avez besoin d'une clé API:\n")
    
    print("1️⃣  DALL-E 3 (OpenAI) - RECOMMANDE")
    print("   " + "-"*65)
    print("   ✅ Qualité: EXCELLENTE (meilleure qualité)")
    print("   💰 Prix: ~0.040$ par image (1024x1024, HD)")
    print("   ⚡ Vitesse: ~10-30 secondes")
    print("   🌐 Site: https://platform.openai.com/api-keys")
    print("")
    print("   📋 Étapes:")
    print("      1. Créer un compte sur https://platform.openai.com/")
    print("      2. Ajouter des crédits (minimum 5$)")
    print("      3. Générer une clé API dans 'API Keys'")
    print("      4. Copier la clé (commence par 'sk-...')")
    print("")
    
    print("2️⃣  Stable Diffusion (Stability AI)")
    print("   " + "-"*65)
    print("   ✅ Qualité: TRES BONNE")
    print("   💰 Prix: ~0.002$ par image (moins cher)")
    print("   ⚡ Vitesse: ~5-15 secondes")
    print("   🌐 Site: https://platform.stability.ai/")
    print("")
    print("   📋 Étapes:")
    print("      1. Créer un compte sur https://platform.stability.ai/")
    print("      2. Ajouter des crédits")
    print("      3. Générer une clé API")
    print("")
    
    print("3️⃣  Replicate (Stable Diffusion gratuit/payant)")
    print("   " + "-"*65)
    print("   ✅ Qualité: BONNE")
    print("   💰 Prix: Version gratuite limitée + payant")
    print("   ⚡ Vitesse: ~10-20 secondes")
    print("   🌐 Site: https://replicate.com/")
    print("")
    
    print("="*70)
    print("💡 RECOMMANDATION")
    print("="*70)
    print("")
    print("Pour la MEILLEURE qualité → DALL-E 3 (OpenAI)")
    print("Pour le meilleur rapport qualité/prix → Stable Diffusion")
    print("Pour tester gratuitement → Replicate (limité)")
    print("")


def test_api_key(backend='dall-e', api_key=None):
    """Teste une clé API"""
    print("\n" + "="*70)
    print(f"🧪 TEST DE LA CLE API - {backend.upper()}")
    print("="*70 + "\n")
    
    if not api_key:
        api_key = input(f"Entrez votre clé API {backend}: ").strip()
    
    if not api_key:
        print("❌ Aucune clé fournie")
        return False
    
    print(f"🔄 Test de la clé avec {backend}...")
    
    try:
        from main import ProductAISystem
        
        # Créer le système avec la clé API
        system = ProductAISystem(
            json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
            image_backend=backend,
            image_api_key=api_key
        )
        
        # Test simple
        print("\n📝 Génération d'une image test: 'Pizza Margherita'...\n")
        
        product = system.generate_product_from_description(
            "Pizza Margherita avec tomate et mozzarella",
            generate_image=True,
            force=True
        )
        
        image_path = product.get('image_path', '')
        
        if os.path.exists(image_path):
            file_size = os.path.getsize(image_path) / 1024  # Ko
            print(f"\n✅ TEST REUSSI!")
            print(f"   📁 Image: {image_path}")
            print(f"   💾 Taille: {file_size:.1f} Ko")
            print(f"\n🎉 Votre clé API fonctionne parfaitement!")
            return True
        else:
            print(f"\n⚠️  Image non créée")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        print("\nVérifiez:")
        print("  - La clé API est valide")
        print("  - Vous avez des crédits sur votre compte")
        print("  - La connexion internet fonctionne")
        return False


def demo_realistic_images():
    """Démonstration avec images réalistes"""
    print("\n" + "="*70)
    print("🎨 DEMO: GENERATION D'IMAGES REALISTES")
    print("="*70 + "\n")
    
    print("Ce script va générer 3 images réalistes de produits.")
    print("Vous avez besoin d'une clé API (DALL-E ou Stable Diffusion).\n")
    
    # Choix du backend
    print("Choisissez votre backend IA:")
    print("1. DALL-E 3 (OpenAI) - Meilleure qualité")
    print("2. Stable Diffusion (Stability AI) - Moins cher")
    print("3. Replicate - Gratuit/Payant")
    print("4. Voir les instructions pour obtenir une clé API")
    print("0. Quitter\n")
    
    choice = input("Votre choix (0-4): ").strip()
    
    if choice == '4':
        show_api_instructions()
        return
    elif choice == '0':
        print("\n✅ Au revoir!\n")
        return
    
    # Mapper le choix au backend
    backend_map = {
        '1': 'dall-e',
        '2': 'stable-diffusion',
        '3': 'replicate'
    }
    
    backend = backend_map.get(choice)
    if not backend:
        print("\n❌ Choix invalide\n")
        return
    
    # Demander la clé API
    api_key = input(f"\nEntrez votre clé API {backend}: ").strip()
    
    if not api_key:
        print("\n❌ Clé API requise\n")
        return
    
    # Tester la clé
    print("\n🔄 Test de la clé API...\n")
    if not test_api_key(backend, api_key):
        print("\n❌ La clé API ne fonctionne pas\n")
        return
    
    # Génération des images
    print("\n" + "="*70)
    print("📦 GENERATION DES PRODUITS")
    print("="*70 + "\n")
    
    from main import ProductAISystem
    
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend=backend,
        image_api_key=api_key
    )
    
    products_to_generate = [
        "Pizza Margherita avec tomate fraîche et mozzarella fondante",
        "Milkshake chocolat avec chantilly et sauce caramel",
        "Burger gourmet avec bacon croustillant et cheddar"
    ]
    
    generated = []
    
    for i, desc in enumerate(products_to_generate, 1):
        print(f"\n[{i}/{len(products_to_generate)}] Génération: {desc}")
        print("-"*70)
        
        try:
            product = system.generate_product_from_description(
                desc,
                generate_image=True,
                force=True
            )
            
            generated.append(product)
            
            name = product['displayName']['dflt']['nameDef']
            image = product.get('image_path', '')
            
            print(f"✅ {name}")
            print(f"   Image: {image}")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    # Récapitulatif
    print("\n" + "="*70)
    print("📊 RECAPITULATIF")
    print("="*70)
    print(f"\n✅ {len(generated)}/{len(products_to_generate)} images générées")
    print(f"📁 Dossier: d:/model-IA-image/generated_images/")
    print(f"🎨 Backend: {backend}")
    print("\n🎉 Images réalistes générées avec succès!\n")
    print("="*70 + "\n")


def save_api_key_template():
    """Crée un fichier template pour sauvegarder les clés API"""
    template = """# Configuration des clés API
# Renommez ce fichier en 'api_keys.py' et ajoutez vos clés

# OpenAI (DALL-E 3)
OPENAI_API_KEY = "sk-..."  # Remplacez par votre clé

# Stability AI (Stable Diffusion)
STABILITY_API_KEY = "sk-..."  # Remplacez par votre clé

# Replicate
REPLICATE_API_KEY = "r8_..."  # Remplacez par votre clé

# Backend à utiliser par défaut
DEFAULT_BACKEND = "dall-e"  # Options: 'dall-e', 'stable-diffusion', 'replicate', 'from_json', 'placeholder'
"""
    
    filepath = "d:/model-IA-image/api_keys_template.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"\n✅ Template créé: {filepath}")
    print("   Renommez-le en 'api_keys.py' et ajoutez vos clés\n")


def main():
    """Menu principal"""
    print("\n" + "="*70)
    print("🎨 GENERATEUR D'IMAGES REALISTES AVEC IA")
    print("="*70 + "\n")
    
    while True:
        print("📋 Menu:")
        print("1. Voir les instructions pour obtenir une clé API")
        print("2. Tester ma clé API")
        print("3. Générer des images réalistes (démo)")
        print("4. Créer un fichier de configuration")
        print("0. Quitter\n")
        
        choice = input("Votre choix (0-4): ").strip()
        
        if choice == '1':
            show_api_instructions()
        elif choice == '2':
            backend = input("\nBackend (dall-e/stable-diffusion/replicate): ").strip()
            if backend in ['dall-e', 'stable-diffusion', 'replicate']:
                test_api_key(backend)
            else:
                print("\n❌ Backend invalide\n")
        elif choice == '3':
            demo_realistic_images()
        elif choice == '4':
            save_api_key_template()
        elif choice == '0':
            print("\n✅ Au revoir!\n")
            break
        else:
            print("\n❌ Choix invalide\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur\n")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}\n")
        import traceback
        traceback.print_exc()

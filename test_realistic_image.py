# -*- coding: utf-8 -*-
"""
Test rapide de génération d'image réaliste
Usage: python test_realistic_image.py <backend> <api_key>
"""

import sys
import os

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def test_realistic_generation(backend='dall-e', api_key=None):
    """Test de génération d'une image réaliste"""
    
    print("\n" + "="*70)
    print(f"🧪 TEST GENERATION IMAGE REALISTE - {backend.upper()}")
    print("="*70 + "\n")
    
    if not api_key:
        print("❌ Clé API requise\n")
        print("Usage: python test_realistic_image.py <backend> <api_key>")
        print("\nExemple:")
        print("  python test_realistic_image.py dall-e sk-proj-...")
        print("  python test_realistic_image.py stable-diffusion sk-...")
        return
    
    print(f"Backend: {backend}")
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    print("")
    
    try:
        from main import ProductAISystem
        from image_generator_ai import ImageGeneratorAI
        
        # Test 1: Vérifier que le générateur charge bien
        print("[1/4] Initialisation du générateur d'images...")
        img_gen = ImageGeneratorAI(api_key=api_key, backend=backend)
        print("   ✅ Générateur initialisé\n")
        
        # Test 2: Vérifier la création de prompt
        print("[2/4] Création d'un prompt optimisé...")
        prompt = img_gen._create_realistic_prompt(
            "pizza margherita avec tomate et mozzarella",
            "Pizza Margherita",
            style='dalle' if backend == 'dall-e' else 'sd'
        )
        print(f"   ✅ Prompt créé ({len(prompt)} caractères)")
        print(f"\n   Extrait du prompt:")
        print(f"   {prompt[:150]}...\n")
        
        # Test 3: Détection du type de produit
        print("[3/4] Détection du type de produit...")
        product_type = img_gen._detect_product_type(
            "Pizza Margherita",
            "pizza margherita avec tomate et mozzarella"
        )
        print(f"   ✅ Type détecté: {product_type}\n")
        
        # Test 4: Génération réelle
        print("[4/4] Génération de l'image (peut prendre 10-30 secondes)...")
        print("   🎨 Connexion à l'API...")
        
        system = ProductAISystem(
            json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
            image_backend=backend,
            image_api_key=api_key
        )
        
        product = system.generate_product_from_description(
            "Pizza Margherita avec tomate fraîche et mozzarella fondante",
            generate_image=True,
            force=True
        )
        
        # Vérifier le résultat
        image_path = product.get('image_path', '')
        
        if os.path.exists(image_path):
            file_size = os.path.getsize(image_path) / 1024
            
            print(f"\n   ✅ IMAGE GENEREE AVEC SUCCES!\n")
            print("   " + "-"*65)
            print(f"   📁 Fichier: {image_path}")
            print(f"   💾 Taille: {file_size:.1f} Ko")
            
            # Vérifier que ce n'est pas un placeholder
            if 'placeholder' in image_path.lower():
                print(f"   ⚠️  ATTENTION: Placeholder généré (échec API)\n")
                return False
            elif backend in image_path.lower() or 'dalle' in image_path.lower():
                print(f"   🎉 Image {backend.upper()} réaliste générée!\n")
                print("   " + "="*65)
                print(f"   🌟 QUALITE: Photo-réaliste professionnelle")
                print(f"   💰 COUT: ~0.04$ (DALL-E) ou ~0.002$ (SD)")
                print(f"   ⏱️  TEMPS: Variable selon l'API")
                print("   " + "="*65 + "\n")
                return True
            else:
                print(f"   ✅ Image générée avec succès\n")
                return True
        else:
            print(f"\n   ❌ Image non créée\n")
            return False
        
    except ImportError as e:
        print(f"\n❌ ERREUR D'IMPORT: {e}")
        print("\nInstallez les dépendances manquantes:")
        print("  pip install openai  # Pour DALL-E")
        print("  pip install replicate  # Pour Replicate\n")
        return False
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}\n")
        print("Vérifications:")
        print("  ✓ La clé API est-elle valide?")
        print("  ✓ Avez-vous des crédits sur votre compte?")
        print("  ✓ La connexion internet fonctionne?")
        print("  ✓ Le backend est-il correct? (dall-e/stable-diffusion/replicate)\n")
        return False


def show_examples():
    """Affiche des exemples d'utilisation"""
    print("\n" + "="*70)
    print("📚 EXEMPLES D'UTILISATION")
    print("="*70 + "\n")
    
    print("1. Test avec DALL-E 3 (OpenAI):")
    print("   python test_realistic_image.py dall-e sk-proj-...")
    print("")
    
    print("2. Test avec Stable Diffusion:")
    print("   python test_realistic_image.py stable-diffusion sk-...")
    print("")
    
    print("3. Test avec Replicate:")
    print("   python test_realistic_image.py replicate r8_...")
    print("")
    
    print("💡 Astuce:")
    print("   Sauvegardez votre clé dans un fichier api_keys.py")
    print("   puis importez-la dans vos scripts Python\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_examples()
        
        print("\n" + "="*70)
        print("Mode interactif")
        print("="*70 + "\n")
        
        backend = input("Backend (dall-e/stable-diffusion/replicate): ").strip()
        api_key = input("Clé API: ").strip()
        
        if backend and api_key:
            test_realistic_generation(backend, api_key)
        else:
            print("\n❌ Backend et clé API requis\n")
    
    elif len(sys.argv) == 3:
        backend = sys.argv[1]
        api_key = sys.argv[2]
        test_realistic_generation(backend, api_key)
    
    else:
        show_examples()

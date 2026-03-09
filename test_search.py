"""
Script de test pour la fonctionnalité de recherche de produits
"""

from main import ProductAISystem
from data_analyzer import DataAnalyzer

def test_search():
    """Test de la fonctionnalité de recherche"""
    print("\n" + "="*70)
    print("🔍 TEST DE RECHERCHE DE PRODUITS")
    print("="*70)
    
    # Initialiser le système
    try:
        system = ProductAISystem(
            json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
            image_backend='placeholder'
        )
        print("✅ Système initialisé avec succès\n")
    except Exception as e:
        print(f"⚠️  Erreur d'initialisation : {e}")
        print("Le système fonctionnera en mode limité.\n")
        return
    
    # Tests de recherche
    test_queries = [
        "pizza",
        "milkshake",
        "chicken",
        "coca",
        "margherita",
        "chocolat",
        "fromage"
    ]
    
    print("="*70)
    print("📝 TESTS DE RECHERCHE")
    print("="*70)
    
    for query in test_queries:
        print(f"\n🔍 Recherche : '{query}'")
        print("-" * 70)
        
        results = system.search_existing_products(query)
        
        if not results:
            print("❌ Aucun résultat\n")
        else:
            print(f"✅ {len(results)} résultat(s) trouvé(s)\n")


def test_product_check():
    """Test de vérification d'existence de produit"""
    print("\n" + "="*70)
    print("🔎 TEST DE VÉRIFICATION D'EXISTENCE")
    print("="*70)
    
    try:
        system = ProductAISystem(
            json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
            image_backend='placeholder'
        )
    except:
        print("⚠️  Fichier JSON non disponible, test annulé.")
        return
    
    # Tests de vérification
    test_descriptions = [
        "Pizza Margherita classique",
        "Milkshake au chocolat",
        "Produit totalement nouveau et unique 12345"
    ]
    
    for desc in test_descriptions:
        print(f"\n📝 Description : '{desc}'")
        print("-" * 70)
        
        exists, similar, message = system.product_generator.check_product_exists(desc)
        
        print(f"   {message}")
        print(f"   Existe déjà : {'Oui' if exists else 'Non'}")
        print(f"   Produits similaires : {len(similar)}")
        
        if similar:
            print(f"\n   Top 3 similaires :")
            for i, prod in enumerate(similar[:3], 1):
                print(f"      {i}. {prod['display_name']} (score: {prod['score']})")
        print()


def test_smart_generation():
    """Test de génération intelligente avec recherche"""
    print("\n" + "="*70)
    print("🤖 TEST DE GÉNÉRATION INTELLIGENTE")
    print("="*70)
    
    try:
        system = ProductAISystem(
            json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
            image_backend='placeholder'
        )
    except:
        print("⚠️  Fichier JSON non disponible.")
        return
    
    print("\n1️⃣ Test : Produit possiblement existant")
    print("-" * 70)
    
    # Tenter de générer un produit qui existe peut-être
    desc1 = "Pizza avec fromage mozzarella"
    print(f"\n📝 Description : '{desc1}'")
    
    exists, similar, message = system.product_generator.check_product_exists(desc1)
    print(f"   {message}")
    
    if similar:
        print(f"\n   Produits similaires trouvés :")
        for i, prod in enumerate(similar[:3], 1):
            print(f"      {i}. {prod['display_name']} (score: {prod['score']})")
        
        print(f"\n   💡 Le système détecte {len(similar)} produit(s) similaire(s).")
        print("   Il proposera à l'utilisateur d'utiliser un produit existant.")
    
    print("\n\n2️⃣ Test : Produit complètement nouveau")
    print("-" * 70)
    
    desc2 = "Burger végétarien avec quinoa et légumes grillés"
    print(f"\n📝 Description : '{desc2}'")
    
    exists, similar, message = system.product_generator.check_product_exists(desc2)
    print(f"   {message}")
    
    if not similar:
        print("   ✅ Aucun produit similaire - génération sûre")
    elif similar:
        print(f"\n   Produits potentiellement similaires :")
        for i, prod in enumerate(similar[:3], 1):
            print(f"      {i}. {prod['display_name']} (score: {prod['score']})")


def demo_interactive_search():
    """Démo de recherche interactive"""
    print("\n" + "="*70)
    print("🎮 MODE DÉMO - RECHERCHE INTERACTIVE")
    print("="*70)
    
    try:
        system = ProductAISystem(
            json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
            image_backend='placeholder'
        )
    except:
        print("⚠️  Fichier JSON non disponible.")
        return
    
    print("\nExemples de recherches que vous pouvez faire :")
    print("  - 'search pizza' : Tous les produits pizza")
    print("  - 'search chocolat' : Produits au chocolat")
    print("  - 'search chicken' : Produits à base de poulet")
    print("  - 'search boisson' : Toutes les boissons")
    
    print("\n" + "="*70)
    print("💡 ESSAI DE QUELQUES RECHERCHES")
    print("="*70)
    
    demo_queries = ["pizza", "chocolat", "chicken"]
    
    for query in demo_queries:
        input(f"\n⏸️  Appuyez sur Entrée pour rechercher '{query}'...")
        system.search_existing_products(query)


def main():
    """Menu principal des tests"""
    print("\n" + "="*70)
    print("🧪 TESTS DE RECHERCHE ET DÉTECTION DE DOUBLONS")
    print("="*70)
    print("\nChoisissez un test :")
    print("1. Test de recherche de produits")
    print("2. Test de vérification d'existence")
    print("3. Test de génération intelligente")
    print("4. Démo recherche interactive")
    print("5. Exécuter tous les tests")
    print("0. Quitter")
    
    choice = input("\nVotre choix (0-5) : ").strip()
    
    tests = {
        '1': test_search,
        '2': test_product_check,
        '3': test_smart_generation,
        '4': demo_interactive_search
    }
    
    if choice == '5':
        for i in range(1, 5):
            try:
                tests[str(i)]()
                if i < 4:
                    input("\n⏸️  Appuyez sur Entrée pour continuer...")
            except Exception as e:
                print(f"\n❌ Erreur dans le test {i}: {e}")
    elif choice in tests:
        try:
            tests[choice]()
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
    elif choice == '0':
        print("\n👋 Au revoir !")
    else:
        print("\n❌ Choix invalide.")
    
    print("\n" + "="*70)
    print("✅ FONCTIONNALITÉ DE RECHERCHE TESTÉE")
    print("="*70)
    print("\n💡 Pour utiliser la recherche dans le système principal :")
    print("   python main.py")
    print("   → Mode interactif")
    print("   → Tapez : search <terme>")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrompus.")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

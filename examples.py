"""
Exemple d'utilisation avancée du système IA
"""

from main import ProductAISystem
import json


def example_1_basic_usage():
    """Exemple 1 : Utilisation basique"""
    print("\n" + "="*70)
    print("EXEMPLE 1 : UTILISATION BASIQUE")
    print("="*70)
    
    # Initialiser le système
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='placeholder'
    )
    
    # Générer un produit
    product = system.generate_product_from_description(
        "Pizza 4 fromages avec mozzarella, chèvre, emmental et parmesan"
    )
    
    # Afficher le résumé
    system.display_product_summary(product)
    
    return product


def example_2_batch_generation():
    """Exemple 2 : Génération en lot"""
    print("\n" + "="*70)
    print("EXEMPLE 2 : GÉNÉRATION EN LOT")
    print("="*70)
    
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='placeholder'
    )
    
    # Liste de descriptions
    descriptions = [
        "Pizza Margherita classique",
        "Milkshake chocolat",
        "Chicken Nuggets 6 pièces",
        "Coca-Cola 33cl",
        "Tiramisu maison"
    ]
    
    # Générer tous les produits
    products = system.generate_multiple_products(descriptions)
    
    # Sauvegarder
    system.save_products_to_json(products, 'd:/model-IA-image/batch_products.json')
    
    return products


def example_3_custom_product():
    """Exemple 3 : Produit personnalisé avec modifications"""
    print("\n" + "="*70)
    print("EXEMPLE 3 : PRODUIT PERSONNALISÉ")
    print("="*70)
    
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='placeholder'
    )
    
    # Générer le produit de base
    product = system.generate_product_from_description(
        "Pizza Spéciale du Chef avec ingrédients premium"
    )
    
    # Personnaliser le produit généré
    product['price'] = 19.90  # Prix premium
    product['displayName']['dflt']['nameDef'] = "Pizza Chef Premium"
    product['allergens'].append('sésame')  # Ajouter un allergène
    
    # Ajouter une option supplémentaire
    product['options'].append({
        "label": "Supplément",
        "required": False,
        "choices": [
            {"name": "Extra mozzarella", "priceModifier": 2.0},
            {"name": "Extra viande", "priceModifier": 3.0},
            {"name": "Bord farci", "priceModifier": 2.5}
        ]
    })
    
    system.display_product_summary(product)
    
    return product


def example_4_category_analysis():
    """Exemple 4 : Analyse par catégorie"""
    print("\n" + "="*70)
    print("EXEMPLE 4 : ANALYSE PAR CATÉGORIE")
    print("="*70)
    
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='placeholder'
    )
    
    # Obtenir les statistiques
    stats = system.data_analyzer.get_statistics()
    
    print("\n📊 STATISTIQUES DES DONNÉES :")
    print(f"\nNombre total de catégories : {stats['total_categories']}")
    
    print("\nCatégories par type :")
    for category, count in list(stats['categories_by_type'].most_common(10)):
        print(f"  - {category}: {count}")
    
    # Tester la suggestion de catégories
    test_descriptions = [
        "Pizza aux 4 fromages",
        "Milkshake vanille",
        "Salade César",
        "Chicken Wings épicées",
        "Coca Cola",
        "Tiramisu"
    ]
    
    print("\n🔍 SUGGESTION DE CATÉGORIES :")
    for desc in test_descriptions:
        category = system.data_analyzer.get_category_suggestions(desc)
        print(f"  '{desc}' → {category}")


def example_5_price_estimation():
    """Exemple 5 : Estimation des prix"""
    print("\n" + "="*70)
    print("EXEMPLE 5 : ESTIMATION DES PRIX")
    print("="*70)
    
    from product_generator_ai import ProductGeneratorAI
    
    generator = ProductGeneratorAI(r"c:\Users\mohamed taher\Downloads\3.json")
    
    # Test d'estimation de prix pour différentes catégories
    test_cases = [
        ('PIZZAS', 'S'),
        ('PIZZAS', 'M'),
        ('PIZZAS', 'L'),
        ('PIZZAS', 'XL'),
        ('MILKSHAKE', 'Petit'),
        ('MILKSHAKE', 'Grand'),
        ('BOISSONS', '33cl'),
        ('BOISSONS', '50cl'),
        ('FINGER FOOD', '6 pcs'),
    ]
    
    print("\n💰 ESTIMATION DES PRIX :")
    for category, size in test_cases:
        price = generator.generate_price(category, size)
        print(f"  {category} - {size}: {price}€")


def example_6_allergen_detection():
    """Exemple 6 : Détection des allergènes"""
    print("\n" + "="*70)
    print("EXEMPLE 6 : DÉTECTION DES ALLERGÈNES")
    print("="*70)
    
    from product_generator_ai import ProductGeneratorAI
    
    generator = ProductGeneratorAI(r"c:\Users\mohamed taher\Downloads\3.json")
    
    # Test de détection d'allergènes
    test_products = [
        ("Pizza Margherita", "Pizza avec mozzarella et tomate"),
        ("Milkshake Chocolat", "Milkshake au chocolat avec crème fouettée"),
        ("Burger Poulet", "Burger avec pain, poulet pané et sauce"),
        ("Salade Verte", "Salade fraîche avec vinaigrette"),
        ("Brownie", "Brownie au chocolat avec noix")
    ]
    
    print("\n⚠️  DÉTECTION DES ALLERGÈNES :")
    for name, description in test_products:
        allergens = generator.generate_allergens(description, name)
        allergens_str = ', '.join(allergens) if allergens else 'Aucun'
        print(f"\n  {name}:")
        print(f"    Description: {description}")
        print(f"    Allergènes: {allergens_str}")


def example_7_translation_system():
    """Exemple 7 : Système de traduction"""
    print("\n" + "="*70)
    print("EXEMPLE 7 : SYSTÈME DE TRADUCTION")
    print("="*70)
    
    from product_generator_ai import ProductGeneratorAI
    
    generator = ProductGeneratorAI()
    
    # Test de traduction
    test_phrases = [
        "Pizza avec fromage et tomate",
        "Milkshake au chocolat",
        "Salade fraîche",
        "Menu petit avec boisson"
    ]
    
    print("\n🌍 TRADUCTIONS :")
    for phrase in test_phrases:
        print(f"\n  Français: {phrase}")
        print(f"  English: {generator.translate_text(phrase, 'en')}")
        print(f"  العربية: {generator.translate_text(phrase, 'ar')}")


def example_8_complete_menu():
    """Exemple 8 : Génération d'un menu complet"""
    print("\n" + "="*70)
    print("EXEMPLE 8 : GÉNÉRATION D'UN MENU COMPLET")
    print("="*70)
    
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='placeholder'
    )
    
    # Définir un menu complet
    menu_items = {
        "Entrées": [
            "Salade César avec poulet grillé et parmesan",
            "Mozza Sticks fondants avec sauce marinara"
        ],
        "Plats": [
            "Pizza Margherita avec mozzarella di bufala",
            "Pizza 4 Fromages avec fromages italiens",
            "Pizza Végétarienne avec légumes grillés",
            "Burger Poulet croustillant avec frites"
        ],
        "Desserts": [
            "Tiramisu traditionnel au café",
            "Brownie au chocolat avec glace vanille",
            "Cheesecake New York style"
        ],
        "Boissons": [
            "Coca-Cola 33cl",
            "Milkshake Chocolat",
            "Limonade maison fraîche"
        ]
    }
    
    all_products = []
    
    for category_name, items in menu_items.items():
        print(f"\n\n{'='*70}")
        print(f"📋 {category_name.upper()}")
        print('='*70)
        
        for item in items:
            product = system.generate_product_from_description(item)
            all_products.append(product)
            
            print(f"\n✅ {product['displayName']['dflt']['nameDef']}")
            print(f"   💰 {product['price']}€")
            print(f"   📂 {product['category']}")
    
    # Sauvegarder le menu complet
    system.save_products_to_json(all_products, 'd:/model-IA-image/menu_complet.json')
    
    print(f"\n\n✅ MENU COMPLET GÉNÉRÉ !")
    print(f"   Total: {len(all_products)} produits")
    print(f"   Sauvegardé dans: d:/model-IA-image/menu_complet.json")
    
    return all_products


def main():
    """Menu principal des exemples"""
    print("\n" + "="*70)
    print("🎓 EXEMPLES D'UTILISATION AVANCÉE")
    print("="*70)
    print("\nChoisissez un exemple :")
    print("1. Utilisation basique")
    print("2. Génération en lot")
    print("3. Produit personnalisé")
    print("4. Analyse par catégorie")
    print("5. Estimation des prix")
    print("6. Détection des allergènes")
    print("7. Système de traduction")
    print("8. Génération d'un menu complet")
    print("9. Exécuter tous les exemples")
    print("0. Quitter")
    
    choice = input("\nVotre choix (0-9) : ").strip()
    
    examples = {
        '1': example_1_basic_usage,
        '2': example_2_batch_generation,
        '3': example_3_custom_product,
        '4': example_4_category_analysis,
        '5': example_5_price_estimation,
        '6': example_6_allergen_detection,
        '7': example_7_translation_system,
        '8': example_8_complete_menu
    }
    
    if choice == '9':
        # Exécuter tous les exemples
        for i in range(1, 9):
            try:
                examples[str(i)]()
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            except Exception as e:
                print(f"\n❌ Erreur dans l'exemple {i}: {e}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
    elif choice == '0':
        print("\n👋 Au revoir !")
    else:
        print("\n❌ Choix invalide.")


if __name__ == "__main__":
    main()

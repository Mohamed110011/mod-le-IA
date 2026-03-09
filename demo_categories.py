"""
Script de démonstration pour la génération de catégories IA
"""

import json
from category_generator_ai import CategoryGeneratorAI

def run_demo():
    print("🎬 DÉMO : GÉNÉRATION DE CATÉGORIES IA")
    print("="*50)
    
    # Initialiser le générateur
    generator = CategoryGeneratorAI()
    
    # Exemples de descriptions de catégories
    demo_cats = [
        "Pizzas Artisanales au feu de bois",
        "Milkshakes et Boissons Fraîches",
        "Desserts Gourmands",
        "Salades de Saison",
        "Menus Étudiants"
    ]
    
    results = []
    
    for desc in demo_cats:
        print(f"\n🔄 Génération pour : '{desc}'...")
        category = generator.generate_complete_category(desc)
        
        print(f"   ✅ Titre généré : {category['title']}")
        print(f"   🎨 Couleur : {category['color']}")
        print(f"   🌍 EN: {category['displayName']['dflt']['salesSupport']['en']['name']}")
        print(f"   🌍 AR: {category['displayName']['dflt']['salesSupport']['ar']['name']}")
        
        results.append(category)
    
    # Sauvegarder les résultats
    output_path = "d:/model-IA-image/generated_categories_demo.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*50)
    print(f"✅ DÉMO TERMINÉE")
    print(f"📁 {len(results)} catégories sauvegardées dans : {output_path}")

if __name__ == "__main__":
    run_demo()

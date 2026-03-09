#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration rapide de la fonctionnalité de recherche
"""

from data_analyzer import DataAnalyzer
from product_generator_ai import ProductGeneratorAI

def demo_search_simple():
    """Démonstration de recherche simple"""
    print("=" * 70)
    print("🔍 DÉMONSTRATION DE LA RECHERCHE")
    print("=" * 70)
    print()
    
    # Initialisation
    print("📋 Initialisation du système...")
    analyzer = DataAnalyzer(r"c:\Users\mohamed taher\Downloads\3.json")
    analyzer.load_data()
    print(f"✅ {len(analyzer.categories)} catégories chargées")
    print()
    
    # Test 1 : Recherche "pizza"
    print("-" * 70)
    print("🔍 Test 1 : Rechercher 'pizza'")
    print("-" * 70)
    results = analyzer.search_products("pizza", max_results=3)
    
    if results:
        print(f"✅ {len(results)} résultat(s) trouvé(s) :")
        for score, product in results:
            name = product['displayName']['dflt']['nameDef']
            category = product.get('title', 'N/A')
            print(f"  [Score: {score}] {name} ({category})")
    else:
        print("❌ Aucun résultat trouvé")
    print()
    
    # Test 2 : Recherche "milkshake"
    print("-" * 70)
    print("🔍 Test 2 : Rechercher 'milkshake'")
    print("-" * 70)
    results = analyzer.search_products("milkshake", max_results=3)
    
    if results:
        print(f"✅ {len(results)} résultat(s) trouvé(s) :")
        for score, product in results:
            name = product['displayName']['dflt']['nameDef']
            category = product.get('title', 'N/A')
            print(f"  [Score: {score}] {name} ({category})")
    else:
        print("❌ Aucun résultat trouvé")
    print()
    
    # Test 3 : Vérification d'existence
    print("-" * 70)
    print("🔍 Test 3 : Vérifier si 'Pizza Margherita' existe")
    print("-" * 70)
    exists = analyzer.product_exists("Pizza Margherita", threshold=80)
    
    if exists:
        print("✅ Produit existant détecté (score ≥ 80)")
    else:
        print("❌ Aucun produit similaire trouvé")
    print()
    
    print("=" * 70)
    print("✅ Démonstration terminée !")
    print("=" * 70)
    print()
    print("📖 Pour plus de détails, consultez SEARCH_FEATURE.md")
    print("🚀 Lancez 'python main.py' pour essayer la recherche interactive")
    print()

if __name__ == "__main__":
    try:
        demo_search_simple()
    except FileNotFoundError:
        print()
        print("❌ ERREUR : Fichier 3.json introuvable")
        print("📍 Chemin attendu : c:\\Users\\mohamed taher\\Downloads\\3.json")
        print()
    except Exception as e:
        print()
        print(f"❌ ERREUR : {e}")
        print()

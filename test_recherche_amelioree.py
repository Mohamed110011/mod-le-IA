"""
Test Rapide - Recherche et Sélection de Produits Existants
Teste la nouvelle fonctionnalité de recherche améliorée
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import ProductAISystem


def test_couscous():
    """Teste la recherche pour 'couscous tunisienne'"""
    
    print("\n" + "=" * 70)
    print("🧪 TEST : Recherche de 'couscous tunisienne'")
    print("=" * 70)
    print()
    
    # Initialiser le système
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='from_json',
        image_api_key=None
    )
    
    print("📝 Test : Génération avec recherche automatique")
    print("   Description : 'couscous tunisienne'")
    print()
    print("Le système devrait :")
    print("   1. Rechercher des produits similaires dans le JSON")
    print("   2. Afficher tous les résultats (même avec score faible)")
    print("   3. Demander si vous voulez :")
    print("      - Utiliser un produit existant (numéro)")
    print("      - Créer un nouveau produit (n)")
    print("      - Annuler (q)")
    print()
    print("─" * 70)
    print()
    
    # Simuler la génération (en mode interactif, l'utilisateur entrera sa réponse)
    # Pour ce test, nous allons juste montrer ce qui se passerait
    print("💡 Pour tester en mode interactif, lancez :")
    print("   python main.py")
    print()
    print("   Puis tapez : couscous tunisienne")
    print()


def test_pizza_escalope():
    """Teste la recherche pour 'pizza escalope'"""
    
    print("\n" + "=" * 70)
    print("🧪 TEST : Recherche de 'pizza escalope'")
    print("=" * 70)
    print()
    
    system = ProductAISystem(
        json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
        image_backend='from_json',
        image_api_key=None
    )
    
    print("📝 Test : Génération avec recherche automatique")
    print("   Description : 'pizza escalope'")
    print()
    print("Le système devrait :")
    print("   1. Trouver des pizzas similaires (PIZZA ESCALOPE, etc.)")
    print("   2. Afficher la liste avec scores")
    print("   3. Vous permettre de sélectionner un produit existant")
    print()
    print("─" * 70)
    print()


def show_how_to_use():
    """Montre comment utiliser la nouvelle fonctionnalité"""
    
    print("\n" + "=" * 70)
    print("📖 COMMENT UTILISER LA NOUVELLE FONCTIONNALITÉ")
    print("=" * 70)
    print()
    
    print("🚀 LANCER LE SYSTÈME :")
    print("-" * 70)
    print()
    print("   python main.py")
    print()
    print("   Choisissez l'option 1 (Mode interactif)")
    print()
    
    print("\n📝 ENTRER UNE DESCRIPTION :")
    print("-" * 70)
    print()
    print("   📝 Commande : couscous tunisienne")
    print()
    
    print("\n✅ LE SYSTÈME RECHERCHE AUTOMATIQUEMENT :")
    print("-" * 70)
    print()
    print("   🔍 Recherche de produits existants similaires...")
    print()
    print("   ✅ 5 produit(s) similaire(s) trouvé(s) :")
    print()
    print("      1. COUSCOUS ROYAL (score: 95) ⭐⭐⭐")
    print("      2. COUSCOUS POULET (score: 85) ⭐⭐⭐")
    print("      3. COUSCOUS AGNEAU (score: 80) ⭐⭐⭐")
    print("      4. TAJINE TUNISIEN (score: 45) ⭐")
    print("      5. PLAT ORIENTAL (score: 30) ⭐")
    print()
    
    print("\n💡 CHOISIR UNE OPTION :")
    print("-" * 70)
    print()
    print("   OPTIONS DISPONIBLES :")
    print()
    print("      • Entrez un NUMÉRO (1-10) pour utiliser un produit existant")
    print("      • Tapez 'n' pour créer un NOUVEAU produit")
    print("      • Tapez 'q' pour ANNULER")
    print()
    print("   Votre choix : 1")
    print()
    print("   ✅ Produit sélectionné : COUSCOUS ROYAL")
    print()
    
    print("\n📦 LE SYSTÈME AFFICHE LE PRODUIT EXISTANT :")
    print("-" * 70)
    print()
    print("   🏷️  NOM : COUSCOUS ROYAL")
    print("   📂 CATÉGORIE : PLATS")
    print("   💰 PRIX : 14.90€")
    print("   📸 IMAGE : Image réelle du JSON")
    print()
    
    print("\n🎉 RÉSULTAT :")
    print("-" * 70)
    print()
    print("   ✅ Vous utilisez un produit EXISTANT du JSON")
    print("   ✅ Avec son IMAGE RÉELLE professionnelle")
    print("   ✅ Avec tous ses détails (prix, allergènes, options, etc.)")
    print("   ✅ SANS créer de doublon")
    print()
    
    print("\n💡 SI VOUS VOULEZ CRÉER UN NOUVEAU :")
    print("-" * 70)
    print()
    print("   Votre choix : n")
    print()
    print("   📝 Création d'un nouveau produit...")
    print("   ⚙️  Génération des informations...")
    print("   🎨 Génération de l'image...")
    print("   ✅ Nouveau produit créé !")
    print()


def main():
    """Menu principal"""
    
    print("\n" + "=" * 70)
    print("🧪 TEST - Nouvelle Fonctionnalité de Recherche")
    print("=" * 70)
    print()
    print("1. Tester 'couscous tunisienne'")
    print("2. Tester 'pizza escalope'")
    print("3. Voir comment utiliser")
    print("4. Tout afficher")
    print("0. Quitter")
    print()
    
    choice = input("Votre choix : ").strip()
    
    if choice == '1':
        test_couscous()
    elif choice == '2':
        test_pizza_escalope()
    elif choice == '3':
        show_how_to_use()
    elif choice == '4':
        test_couscous()
        test_pizza_escalope()
        show_how_to_use()
    elif choice == '0':
        print("\n👋 Au revoir !")
        return
    else:
        print("\n❌ Choix invalide")
        return
    
    print("\n" + "=" * 70)
    print("🎯 NOUVELLE FONCTIONNALITÉ EXPLIQUÉE")
    print("=" * 70)
    print()
    print("✅ Le système RECHERCHE automatiquement des produits similaires")
    print("✅ Affiche TOUS les résultats (même avec score faible)")
    print("✅ Vous permet de CHOISIR un produit existant")
    print("✅ OU créer un nouveau si aucun ne convient")
    print("✅ ÉVITE les doublons dans la base de données")
    print()
    print("📖 Documentation : Le système est maintenant plus intelligent !")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt demandé")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

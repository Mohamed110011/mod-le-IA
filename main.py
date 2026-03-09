"""
Interface principale du système IA de génération de produits
Permet de générer automatiquement tous les détails d'un produit
"""

import json
import os
import random
from typing import Optional, List, Dict, Any
from product_generator_ai import ProductGeneratorAI
from image_generator_ai import ImageGeneratorAI
from data_analyzer import DataAnalyzer


class ProductAISystem:
    """
    Système IA complet pour la génération automatique de produits
    """
    
    def __init__(self, 
                 json_data_path: str,
                 image_api_key: Optional[str] = None,
                 image_backend: str = 'placeholder'):
        """
        Args:
            json_data_path: Chemin vers le fichier JSON de données
            image_api_key: Clé API pour la génération d'images (optionnel)
            image_backend: Backend pour les images ('dall-e', 'stable-diffusion', 'placeholder', 'from_json')
        """
        self.json_data_path = json_data_path
        
        # Initialiser les modules
        print("🚀 Initialisation du système IA...")
        self.product_generator = ProductGeneratorAI(json_data_path)
        
        # Si backend nécessite le JSON ('from_json' ou 'hybrid_free'), passer le chemin
        if image_backend in ['from_json', 'hybrid_free']:
            self.image_generator = ImageGeneratorAI(
                api_key=image_api_key, 
                backend=image_backend,
                json_path=json_data_path
            )
        else:
            self.image_generator = ImageGeneratorAI(api_key=image_api_key, backend=image_backend)
        
        self.data_analyzer = DataAnalyzer(json_data_path)
        
        print("✅ Système IA initialisé avec succès !\n")
    
    def search_existing_products(self, query: str) -> List[Dict[str, Any]]:
        """Recherche des produits existants"""
        print(f"\n🔍 RECHERCHE : '{query}'")
        print("="*70)
        
        results = self.data_analyzer.search_products(query, max_results=10)
        
        if not results:
            print("\n❌ Aucun produit trouvé.\n")
            return []
        
        print(f"\n✅ {len(results)} produit(s) trouvé(s) :\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['display_name']}")
            print(f"   🏷️  Titre: {result['title']}")
            print(f"   📊 Score: {result['score']}")
            print(f"   📦 Articles: {result['items_count']}")
            print()
        
        return results
    
    def _get_existing_product(self, search_result: Dict[str, Any]) -> Dict[str, Any]:
        """Récupère un produit existant depuis le résultat de recherche et complète les champs manquants
        
        Args:
            search_result: Résultat de recherche contenant la catégorie
            
        Returns:
            Produit formaté et complété avec toutes les informations
        """
        category = search_result['category']
        
        # Extraire le nom du produit pour la génération
        display_name = category.get('displayName', {})
        if isinstance(display_name, dict) and 'dflt' in display_name:
            product_name = display_name['dflt'].get('nameDef', category.get('title', 'Produit'))
        else:
            product_name = category.get('title', 'Produit')
        
        print(f"\n📦 Récupération du produit existant : {product_name}")
        print("🔍 Vérification des données...\n")
        
        # Récupérer les données existantes
        product = {
            'id': category.get('id', ''),
            'ref': category.get('ref', ''),
            'title': category.get('title', ''),
            'displayName': category.get('displayName', {}),
            'description': category.get('description', {}),
            'category': category.get('category', ''),
            'price': category.get('price'),
            'img': category.get('img', {}),
            'options': category.get('options', []),
            'allergens': category.get('allergens', []),
            'available': category.get('available', True),
            'isAvailable': category.get('available', True),
            'translations': category.get('translations', {})
        }
        
        # Vérifier et compléter les champs manquants avec l'IA
        needs_completion = False
        missing_fields = []
        
        # Vérifier le prix
        if product['price'] is None:
            missing_fields.append("prix")
            needs_completion = True
        
        # Vérifier les allergènes
        if not product['allergens'] or len(product['allergens']) == 0:
            missing_fields.append("allergènes")
            needs_completion = True
        
        # Vérifier la description
        description = product.get('description', {})
        if not description or (isinstance(description, dict) and not description.get('dflt', {}).get('nameDef')):
            missing_fields.append("description")
            needs_completion = True
        
        # Si des champs sont manquants, compléter avec l'IA
        if needs_completion:
            print(f"⚠️  Champs manquants détectés : {', '.join(missing_fields)}")
            print("🤖 Complétion automatique avec l'IA...\n")
            
            # Générer un produit complet avec l'IA
            ai_product = self.product_generator.generate_complete_product(product_name, force=True)
            
            # Compléter uniquement les champs manquants
            if product['price'] is None and ai_product.get('price'):
                product['price'] = ai_product['price']
                print(f"   ✅ Prix généré : {product['price']}€")
            
            if not product['allergens'] and ai_product.get('allergens'):
                product['allergens'] = ai_product['allergens']
                print(f"   ✅ Allergènes générés : {', '.join(product['allergens'])}")
            
            if not product.get('description', {}).get('dflt', {}).get('nameDef'):
                product['description'] = ai_product['description']
                print(f"   ✅ Description générée")
            
            if not product.get('options') and ai_product.get('options'):
                product['options'] = ai_product['options']
                print(f"   ✅ Options générées")
            
            print()
        else:
            print("✅ Toutes les données sont complètes\n")
        
        # Gérer l'image
        image_url = None
        if 'img' in category and 'dflt' in category['img']:
            image_url = category['img']['dflt'].get('img', '')
        
        if image_url and 'no-pictures' not in image_url:
            # Image réelle du JSON
            print("🎨 Téléchargement de l'image du JSON...")
            # L'image sera téléchargée par le générateur d'images
            product['image_path'] = image_url
            
            # Télécharger l'image maintenant
            try:
                image_path = self.image_generator.generate_image(
                    description=product_name,
                    product_name=product_name,
                    category=product['category']
                )
                product['img']['dflt']['img'] = image_path
                product['image_path'] = image_path
                print(f"   ✅ Image téléchargée : {image_path}\n")
            except Exception as e:
                print(f"   ⚠️  Erreur téléchargement : {e}")
                print("   🎨 Génération d'une nouvelle image...\n")
                image_path = self.image_generator._generate_placeholder(product_name, product['category'])
                product['img']['dflt']['img'] = image_path
                product['image_path'] = image_path
        else:
            # Pas d'image dans le JSON, en générer une
            print("🎨 Génération d'une nouvelle image...")
            image_path = self.image_generator.generate_image(
                description=product_name,
                product_name=product_name,
                category=product['category']
            )
            product['img']['dflt']['img'] = image_path
            product['image_path'] = image_path
            print(f"   ✅ Image générée : {image_path}\n")
        
        return product
    
    def generate_product_from_description(self, 
                                         description: str,
                                         generate_image: bool = True,
                                         force: bool = False) -> Dict[str, Any]:
        """
        Génère un produit complet à partir d'une simple description
        
        Args:
            description: Description du produit (ex: "Milkshake chocolat avec chantilly")
            generate_image: Si True, génère aussi l'image
            force: Si True, génère même si un produit similaire existe
        
        Returns:
            Dictionnaire contenant toutes les informations du produit
        """
        print(f"\n📝 GÉNÉRATION DU PRODUIT...")
        print(f"   Description: {description}\n")
        
        # TOUJOURS vérifier si un produit similaire existe (même si force=True)
        if not force:
            print("🔍 Recherche de produits existants similaires...\n")
            exists, similar, message = self.product_generator.check_product_exists(description)
            
            # Afficher TOUS les résultats, même avec score faible
            if similar:
                print(f"✅ {len(similar)} produit(s) similaire(s) trouvé(s) :\n")
                
                # Afficher les 10 premiers résultats
                for i, prod in enumerate(similar[:10], 1):
                    score_indicator = "⭐⭐⭐" if prod['score'] >= 80 else "⭐⭐" if prod['score'] >= 50 else "⭐"
                    print(f"   {i}. {prod['display_name']} (score: {prod['score']}) {score_indicator}")
                
                # Demander à l'utilisateur ce qu'il veut faire
                print("\n" + "="*70)
                print("💡 OPTIONS DISPONIBLES :")
                print("="*70)
                print()
                print("   • Entrez un NUMÉRO (1-10) pour utiliser un produit existant")
                print("   • Tapez 'n' pour créer un NOUVEAU produit")
                print("   • Tapez 'q' pour ANNULER")
                print()
                
                choice = input("Votre choix : ").strip().lower()
                
                if choice == 'q':
                    print("\n🚫 Génération annulée.\n")
                    return None
                
                # Si l'utilisateur choisit un numéro
                if choice.isdigit():
                    num = int(choice)
                    if 1 <= num <= min(10, len(similar)):
                        selected = similar[num - 1]
                        print(f"\n✅ Produit sélectionné : {selected['display_name']}")
                        
                        # Retourner le produit existant depuis le JSON
                        return self._get_existing_product(selected)
                    else:
                        print(f"\n⚠️  Numéro invalide. Création d'un nouveau produit...\n")
                
                elif choice != 'n':
                    print(f"\n⚠️  Choix invalide. Création d'un nouveau produit...\n")
                
                # Si l'utilisateur a choisi 'n' ou choix invalide, continuer la création
                print("📝 Création d'un nouveau produit...\n")
            
            else:
                print("ℹ️  Aucun produit similaire trouvé dans la base de données.")
                print("📝 Création d'un nouveau produit...\n")
        
        # 1. Générer les informations du produit
        print("⚙️  Génération des informations avec l'IA...")
        product = self.product_generator.generate_complete_product(description, force=True)
        
        # Vérifier que tous les champs essentiels sont remplis
        print("🔍 Vérification de la complétude du produit...")
        
        # Vérifier le prix
        if product.get('price') is None:
            print("   ⚠️  Prix manquant, génération automatique...")
            # Générer un prix basé sur la catégorie
            category = product.get('category', 'AUTRES')
            if 'PIZZA' in category.upper():
                product['price'] = round(random.uniform(8.0, 15.0), 2)
            elif 'BURGER' in category.upper():
                product['price'] = round(random.uniform(7.0, 12.0), 2)
            elif 'BOISSON' in category.upper() or 'MILKSHAKE' in category.upper():
                product['price'] = round(random.uniform(3.0, 6.0), 2)
            elif 'DESSERT' in category.upper():
                product['price'] = round(random.uniform(4.0, 8.0), 2)
            else:
                product['price'] = round(random.uniform(5.0, 12.0), 2)
            print(f"   ✅ Prix généré : {product['price']}€")
        
        # Vérifier les allergènes
        if not product.get('allergens') or len(product['allergens']) == 0:
            print("   ⚠️  Allergènes manquants, génération automatique...")
            # Générer des allergènes basiques selon le type de produit
            product_name = product['displayName']['dflt']['nameDef'].lower()
            allergens = []
            if any(word in product_name for word in ['pain', 'pizza', 'burger', 'sandwich', 'baguette']):
                allergens.append('gluten')
            if any(word in product_name for word in ['fromage', 'mozzarella', 'cheddar', 'lait', 'crème']):
                allergens.append('lait')
            if any(word in product_name for word in ['oeuf', 'mayonnaise']):
                allergens.append('oeufs')
            if any(word in product_name for word in ['noix', 'noisette', 'amande']):
                allergens.append('fruits à coque')
            
            if allergens:
                product['allergens'] = allergens
                print(f"   ✅ Allergènes générés : {', '.join(allergens)}")
            else:
                print(f"   ℹ️  Aucun allergène détecté")
        
        # Vérifier la description
        if not product.get('description', {}).get('dflt', {}).get('nameDef'):
            print("   ⚠️  Description manquante, utilisation du nom...")
            if 'description' not in product:
                product['description'] = {}
            if 'dflt' not in product['description']:
                product['description']['dflt'] = {}
            product['description']['dflt']['nameDef'] = description
            print(f"   ✅ Description définie")
        
        print("✅ Tous les champs sont maintenant complets\n")
        
        # 2. Générer l'image si demandé
        if generate_image:
            print("🎨 Génération de l'image...")
            image_path = self.image_generator.generate_image(
                description=description,
                product_name=product['displayName']['dflt']['nameDef'],
                category=product['category']
            )
            product['img']['dflt']['img'] = image_path
            print(f"   ✅ Image générée : {image_path}")
        
        print(f"\n✅ PRODUIT GÉNÉRÉ AVEC SUCCÈS !\n")
        return product
    
    def generate_multiple_products(self, 
                                   descriptions: List[str],
                                   generate_images: bool = True) -> List[Dict[str, Any]]:
        """
        Génère plusieurs produits en lot
        
        Args:
            descriptions: Liste de descriptions de produits
            generate_images: Si True, génère aussi les images
        
        Returns:
            Liste de produits générés
        """
        products = []
        
        print(f"\n🔄 GÉNÉRATION DE {len(descriptions)} PRODUITS...\n")
        
        for i, desc in enumerate(descriptions, 1):
            print(f"\n{'='*70}")
            print(f"PRODUIT {i}/{len(descriptions)}")
            print('='*70)
            
            product = self.generate_product_from_description(desc, generate_images)
            products.append(product)
        
        print(f"\n\n✅ {len(products)} PRODUITS GÉNÉRÉS AVEC SUCCÈS !")
        return products
    
    def save_products_to_json(self, 
                             products: List[Dict[str, Any]], 
                             output_path: str = 'd:/model-IA-image/generated_products.json'):
        """
        Sauvegarde les produits générés dans un fichier JSON
        
        Args:
            products: Liste des produits à sauvegarder
            output_path: Chemin du fichier de sortie
        """
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Sauvegarder
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Produits sauvegardés dans : {output_path}")
        return output_path
    
    def display_product_summary(self, product: Dict[str, Any]):
        """Affiche un résumé du produit généré ou existant"""
        if not product:
            print("\n⚠️  Aucun produit à afficher\n")
            return
        
        print("\n" + "="*70)
        print("📦 RÉSUMÉ DU PRODUIT")
        print("="*70)
        
        # Nom
        display_name = product.get('displayName', {})
        if isinstance(display_name, dict) and 'dflt' in display_name:
            name = display_name['dflt'].get('nameDef', 'N/A')
        else:
            name = product.get('title', 'N/A')
        print(f"\n🏷️  NOM : {name}")
        
        # Catégorie
        print(f"📂 CATÉGORIE : {product.get('category', 'N/A')}")
        
        # Prix
        price = product.get('price')
        if price is not None:
            print(f"💰 PRIX : {price}€")
        else:
            print(f"💰 PRIX : Non défini")
        
        # Description
        description = product.get('description', {})
        if isinstance(description, dict) and 'dflt' in description:
            desc = description['dflt'].get('nameDef', 'N/A')
        else:
            desc = product.get('title', 'N/A')
        print(f"📄 DESCRIPTION : {desc}")
        
        # Allergènes
        print(f"\n⚠️  ALLERGÈNES : ", end="")
        allergens = product.get('allergens', [])
        if allergens:
            print(', '.join(allergens))
        else:
            print("Aucun")
        
        # Options
        print(f"\n🔧 OPTIONS :")
        options = product.get('options', [])
        if options:
            for opt in options:
                choices = ', '.join([c.get('name', '') for c in opt.get('choices', [])])
                print(f"   - {opt.get('label', 'Option')}: {choices}")
        else:
            print("   Aucune option")
        
        # Traductions
        print(f"\n🌍 TRADUCTIONS :")
        if isinstance(display_name, dict) and 'dflt' in display_name:
            sales_support = display_name['dflt'].get('salesSupport', {})
            if sales_support:
                for lang, trans in sales_support.items():
                    if isinstance(trans, dict) and 'name' in trans:
                        print(f"   {lang.upper()}: {trans['name']}")
            else:
                print(f"   FR: {name}")
        else:
            print(f"   FR: {name}")
        
        # Image
        img_path = None
        if 'image_path' in product:
            img_path = product['image_path']
        elif 'img' in product and isinstance(product['img'], dict):
            if 'dflt' in product['img'] and isinstance(product['img']['dflt'], dict):
                img_path = product['img']['dflt'].get('img', 'N/A')
        
        if img_path:
            print(f"\n📸 IMAGE : {img_path}")
        else:
            print(f"\n📸 IMAGE : Non disponible")
        
        # Disponibilité
        available = product.get('isAvailable', product.get('available', True))
        print(f"✔️  DISPONIBLE : {'Oui' if available else 'Non'}")
        
        # ID et REF
        print(f"🆔 ID : {product.get('id', 'N/A')}")
        print(f"🔖 REF : {product.get('ref', 'N/A')}")
        
        print("\n" + "="*70 + "\n")
    
    def interactive_mode(self):
        """Mode interactif pour tester le système"""
        print("\n" + "="*70)
        print("🤖 MODE INTERACTIF - SYSTÈME IA DE GÉNÉRATION DE PRODUITS")
        print("="*70)
        print("\nCommandes disponibles :")
        print("  - Entrez une description pour générer un produit")
        print("  - 'search <terme>' pour rechercher des produits existants")
        print("  - 'quit' pour quitter\n")
        
        while True:
            try:
                user_input = input("📝 Commande : ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Au revoir !")
                    break
                
                if not user_input:
                    print("⚠️  Veuillez entrer une commande.\n")
                    continue
                
                # Commande de recherche
                if user_input.lower().startswith('search '):
                    query = user_input[7:].strip()
                    if query:
                        self.search_existing_products(query)
                    else:
                        print("⚠️  Veuillez spécifier un terme de recherche.\n")
                    continue
                
                # Générer un produit
                description = user_input
                product = self.generate_product_from_description(description, generate_image=True)
                
                # Si la génération a été annulée
                if product is None:
                    continue
                
                # Afficher le résumé
                self.display_product_summary(product)
                
                # Demander s'il faut sauvegarder
                save = input("💾 Sauvegarder ce produit ? (o/n) : ").strip().lower()
                if save == 'o':
                    output_path = f"d:/model-IA-image/product_{product['id'][:8]}.json"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(product, f, ensure_ascii=False, indent=2)
                    print(f"✅ Produit sauvegardé : {output_path}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir !")
                break
            except Exception as e:
                print(f"\n❌ Erreur : {e}\n")
    
    def demo_mode(self):
        """Mode démo avec exemples prédéfinis"""
        print("\n" + "="*70)
        print("🎬 MODE DÉMO - EXEMPLES DE GÉNÉRATION")
        print("="*70)
        
        demo_products = [
            "Pizza Margherita classique avec mozzarella di bufala et basilic frais",
            "Milkshake au chocolat belge avec chantilly maison et sauce caramel",
            "Chicken Tenders croustillants servis avec sauce BBQ fumée",
            "Salade César fraîche avec poulet grillé, parmesan et croûtons",
            "Tiramisu italien traditionnel au café et mascarpone"
        ]
        
        products = self.generate_multiple_products(demo_products, generate_images=True)
        
        # Afficher les résumés
        print("\n\n" + "="*70)
        print("📊 RÉSUMÉS DES PRODUITS GÉNÉRÉS")
        print("="*70)
        
        for product in products:
            self.display_product_summary(product)
        
        # Sauvegarder tous les produits
        output_path = self.save_products_to_json(products)
        
        print(f"\n✅ DÉMO TERMINÉE")
        print(f"📁 {len(products)} produits générés et sauvegardés !")
        print(f"📂 Fichier : {output_path}")


def main():
    """Point d'entrée principal"""
    import sys
    
    # Configuration
    JSON_DATA_PATH = r"c:\Users\mohamed taher\Downloads\3.json"
    IMAGE_API_KEY = None  # Mettre votre clé API ici si vous voulez utiliser DALL-E ou Stable Diffusion
    IMAGE_BACKEND = 'from_json'  # Options: 'from_json' (GRATUIT, 780 images réelles), 'hybrid_free' (JSON + placeholder), 'placeholder', 'dall-e', 'stable-diffusion'
    
    # Initialiser le système
    system = ProductAISystem(
        json_data_path=JSON_DATA_PATH,
        image_api_key=IMAGE_API_KEY,
        image_backend=IMAGE_BACKEND
    )
    
    # Menu principal
    print("\n" + "="*70)
    print("🤖 SYSTÈME IA DE GÉNÉRATION DE PRODUITS")
    print("="*70)
    print("\nChoisissez un mode :")
    print("1. Mode interactif (entrez vos propres descriptions)")
    print("2. Mode démo (exemples prédéfinis)")
    print("3. Quitter")
    
    choice = input("\nVotre choix (1/2/3) : ").strip()
    
    if choice == '1':
        system.interactive_mode()
    elif choice == '2':
        system.demo_mode()
    elif choice == '3':
        print("\n👋 Au revoir !")
    else:
        print("\n❌ Choix invalide.")


if __name__ == "__main__":
    main()

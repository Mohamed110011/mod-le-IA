"""
Modèle IA de génération automatique de produits
Génère : nom, prix, catégorie, allergènes, options, traductions, etc.
"""

import re
import uuid
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from data_analyzer import DataAnalyzer


class ProductGeneratorAI:
    """
    Modèle IA qui génère automatiquement tous les détails d'un produit
    à partir d'une simple description
    """
    
    def __init__(self, json_data_path: str = None):
        self.analyzer = DataAnalyzer(json_data_path) if json_data_path else None
        if self.analyzer:
            self.analyzer.load_data()
            self.analyzer.extract_patterns()
        
        # Base de connaissances du modèle IA
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Construit la base de connaissances du modèle IA"""
        return {
            'translations': {
                'fr_to_en': {
                    'pizza': 'pizza',
                    'fromage': 'cheese',
                    'poulet': 'chicken',
                    'tomate': 'tomato',
                    'champignon': 'mushroom',
                    'oignon': 'onion',
                    'olives': 'olives',
                    'jambon': 'ham',
                    'chorizo': 'chorizo',
                    'viande': 'meat',
                    'végétarien': 'vegetarian',
                    'épicé': 'spicy',
                    'crème': 'cream',
                    'sauce': 'sauce',
                    'milkshake': 'milkshake',
                    'chocolat': 'chocolate',
                    'vanille': 'vanilla',
                    'fraise': 'strawberry',
                    'caramel': 'caramel',
                    'boisson': 'drink',
                    'dessert': 'dessert',
                    'salade': 'salad',
                    'menu': 'menu',
                    'petit': 'small',
                    'moyen': 'medium',
                    'grand': 'large',
                    'géant': 'extra large',
                    'chantilly': 'whipped cream',
                    'glace': 'ice cream'
                },
                'fr_to_ar': {
                    'pizza': 'بيتزا',
                    'fromage': 'جبن',
                    'poulet': 'دجاج',
                    'tomate': 'طماطم',
                    'champignon': 'فطر',
                    'oignon': 'بصل',
                    'olives': 'زيتون',
                    'jambon': 'لحم خنزير',
                    'chorizo': 'شوريزو',
                    'viande': 'لحم',
                    'végétarien': 'نباتي',
                    'épicé': 'حار',
                    'crème': 'كريمة',
                    'sauce': 'صلصة',
                    'milkshake': 'ميلك شيك',
                    'chocolat': 'شوكولاتة',
                    'vanille': 'فانيليا',
                    'fraise': 'فراولة',
                    'caramel': 'كراميل',
                    'boisson': 'مشروب',
                    'dessert': 'حلوى',
                    'salade': 'سلطة',
                    'menu': 'قائمة',
                    'petit': 'صغير',
                    'moyen': 'متوسط',
                    'grand': 'كبير',
                    'chantilly': 'كريمة مخفوقة',
                    'glace': 'مثلجات'
                }
            },
            'allergens_by_ingredient': {
                'fromage': ['lait', 'fromage'],
                'mozzarella': ['lait', 'fromage'],
                'crème': ['lait'],
                'lait': ['lait'],
                'beurre': ['lait'],
                'poulet': [],
                'viande': [],
                'jambon': [],
                'chorizo': [],
                'pâte': ['gluten'],
                'pain': ['gluten'],
                'farine': ['gluten'],
                'oeuf': ['oeufs'],
                'noix': ['fruits à coque'],
                'amande': ['fruits à coque'],
                'noisette': ['fruits à coque']
            },
            'size_options': {
                'PIZZA': ['S', 'M', 'L', 'XL'],
                'BOISSON': ['33cl', '50cl', '1L'],
                'MILKSHAKE': ['Petit', 'Grand'],
                'DESSERT': ['Individuel'],
                'MENU': ['S', 'M', 'L', 'XL'],
                'FINGER_FOOD': ['4 pcs', '6 pcs', '9 pcs'],
                'ROLL': ['Individuel']
            }
        }
    
    def generate_name_from_description(self, description: str) -> str:
        """Génère un nom cohérent à partir de la description"""
        # Nettoyer et capitaliser
        description = description.strip()
        
        # Extraire les mots-clés importants
        words = description.split()
        
        # Règles pour générer un nom
        if 'pizza' in description.lower():
            # Pour pizza, extraire les ingrédients principaux
            ingredients = []
            keywords = ['poulet', 'fromage', 'chorizo', 'végétarienne', 'margherita', 
                       '4 fromages', 'reine', 'royale', 'pepperoni', 'calzone']
            for kw in keywords:
                if kw.lower() in description.lower():
                    ingredients.append(kw.capitalize())
            if ingredients:
                return f"Pizza {' '.join(ingredients)}"
            return "Pizza Spéciale"
        
        elif 'milkshake' in description.lower():
            # Pour milkshake, extraire le parfum
            flavors = ['chocolat', 'vanille', 'fraise', 'caramel', 'oreo', 'speculoos']
            for flavor in flavors:
                if flavor in description.lower():
                    return f"Milkshake {flavor.capitalize()}"
            return "Milkshake"
        
        elif any(word in description.lower() for word in ['chicken', 'nuggets', 'tenders', 'wings']):
            if 'nuggets' in description.lower():
                return "Chicken Nuggets"
            elif 'tenders' in description.lower():
                return "Chicken Tenders"
            elif 'wings' in description.lower():
                return "Chicken Wings"
            return "Chicken"
        
        elif 'coca' in description.lower() or 'cola' in description.lower():
            return "Coca-Cola"
        
        # Cas par défaut : capitaliser les premiers mots
        return ' '.join(word.capitalize() for word in words[:3])
    
    def generate_price(self, category: str, size: str = 'M') -> float:
        """Génère un prix probable basé sur la catégorie et la taille"""
        price_rules = {
            'PIZZAS': {'S': 9.5, 'M': 12.5, 'L': 15.5, 'XL': 18.5},
            'BOISSONS': {'33cl': 2.5, '50cl': 3.5, '1L': 5.0},
            'MILKSHAKE': {'Petit': 4.5, 'Grand': 6.5},
            'DESSERTS': {'Individuel': 4.5, 'Partage': 9.5},
            'MENU': {'S': 14.5, 'M': 17.5, 'L': 20.5, 'XL': 24.5},
            'FINGER FOOD': {'4 pcs': 6.5, '6 pcs': 8.5, '9 pcs': 11.5},
            'ROLL Z': {'Individuel': 8.5},
            'SALADES': {'Individuel': 9.5}
        }
        
        if category in price_rules and size in price_rules[category]:
            base_price = price_rules[category][size]
            # Ajouter une petite variation aléatoire
            variation = random.uniform(-0.5, 0.5)
            return round(base_price + variation, 2)
        
        # Prix par défautreturn 10.0
    
    def generate_allergens(self, description: str, name: str) -> List[str]:
        """Génère les allergènes probables basés sur les ingrédients"""
        allergens = set()
        text = (description + ' ' + name).lower()
        
        # Vérifier chaque ingrédient connu
        for ingredient, ingredient_allergens in self.knowledge_base['allergens_by_ingredient'].items():
            if ingredient in text:
                allergens.update(ingredient_allergens)
        
        # Règles spéciales pour certaines catégories
        if 'pizza' in text:
            allergens.update(['gluten', 'lait'])
        elif 'milkshake' in text or 'lait' in text:
            allergens.add('lait')
        elif 'pain' in text or 'burger' in text or 'roll' in text:
            allergens.add('gluten')
        
        return sorted(list(allergens))
    
    def generate_options(self, category: str) -> List[Dict[str, Any]]:
        """Génère les options disponibles (tailles, etc.)"""
        options = []
        
        if category in self.knowledge_base['size_options']:
            sizes = self.knowledge_base['size_options'][category]
            
            option = {
                "label": "Taille",
                "required": True,
                "choices": []
            }
            
            for size in sizes:
                option["choices"].append({
                    "name": size,
                    "priceModifier": 0.0
                })
            
            options.append(option)
        
        return options
    
    def translate_text(self, text: str, target_lang: str) -> str:
        """Traduit le texte vers la langue cible"""
        if target_lang == 'en':
            translations = self.knowledge_base['translations']['fr_to_en']
        elif target_lang == 'ar':
            translations = self.knowledge_base['translations']['fr_to_ar']
        else:
            return text
        
        # Traduire mot par mot (simple pour la démo)
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            # Enlever la ponctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            translated = translations.get(clean_word, word)
            translated_words.append(translated)
        
        return ' '.join(translated_words)
    
    def generate_translations(self, name: str, description: str) -> Dict[str, Dict[str, str]]:
        """Génère les traductions automatiques"""
        return {
            "fr": {
                "name": name,
                "description": description
            },
            "en": {
                "name": self.translate_text(name, 'en'),
                "description": self.translate_text(description, 'en')
            },
            "ar": {
                "name": self.translate_text(name, 'ar'),
                "description": self.translate_text(description, 'ar')
            }
        }
    
    def search_existing_products(self, description: str) -> List[Dict[str, Any]]:
        """Recherche des produits existants similaires"""
        if not self.analyzer:
            return []
        
        return self.analyzer.search_products(description, max_results=5)
    
    def check_product_exists(self, description: str) -> tuple:
        """Vérifie si un produit similaire existe déjà
        
        Returns:
            (bool, list, str): (existe, produits_similaires, message)
        """
        if not self.analyzer:
            return (False, [], "Analyseur non disponible")
        
        # Générer le nom pour la recherche
        name = self.generate_name_from_description(description)
        
        # Rechercher
        exists, similar = self.analyzer.product_exists(name)
        
        if exists:
            message = f"⚠️  Produit similaire trouvé : '{similar[0]['display_name']}'"
        elif similar:
            message = f"💡 Produits similaires trouvés ({len(similar)})"
        else:
            message = "✅ Aucun produit similaire trouvé"
        
        return (exists, similar, message)
    
    def generate_complete_product(self, description: str, force: bool = False) -> Dict[str, Any]:
        """
        Génère un produit complet à partir d'une simple description
        
        Args:
            description: Description du produit (ex: "Milkshake chocolat avec chantilly")
            force: Si True, génère même si un produit similaire existe
        
        Returns:
            Dictionnaire contenant toutes les informations du produit
        """
        # 0. Vérifier si le produit existe déjà (si analyzeur disponible)
        if not force and self.analyzer:
            exists, similar, message = self.check_product_exists(description)
            if exists and similar:
                # Ajouter l'info qu'un produit similaire existe
                print(f"\n{message}")
                if similar:
                    print("\n📋 Produits similaires existants :")
                    for i, prod in enumerate(similar[:3], 1):
                        print(f"   {i}. {prod['display_name']} (score: {prod['score']})")
                    print("\n💡 Utilisez force=True pour générer quand même\n")
        
        # 1. Générer le nom
        name = self.generate_name_from_description(description)
        
        # 2. Déterminer la catégorie
        if self.analyzer:
            category = self.analyzer.get_category_suggestions(description)
        else:
            category = self._basic_category_detection(description)
        
        # 3. Générer les options et prix
        options = self.generate_options(category)
        default_size = options[0]['choices'][0]['name'] if options and options[0]['choices'] else 'M'
        price = self.generate_price(category, default_size)
        
        # 4. Générer les allergènes
        allergens = self.generate_allergens(description, name)
        
        # 5. Générer les traductions
        translations = self.generate_translations(name, description)
        
        # 6. Générer un ID unique
        product_id = str(uuid.uuid4())
        
        # 7. Déterminer la disponibilité
        is_available = True  # Par défaut disponible
        
        # 8. Construire le produit complet
        product = {
            "id": product_id,
            "ref": f"REF{random.randint(100000, 999999)}",
            "rank": 0,
            "title": name.upper()[:12],
            "displayName": {
                "dflt": {
                    "nameDef": name,
                    "imp": [],
                    "salesSupport": translations
                }
            },
            "description": {
                "dflt": {
                    "nameDef": description,
                    "imp": [],
                    "salesSupport": {}
                }
            },
            "img": {
                "dflt": {
                    "img": "https://catalogue.etk360.com/placeholder-product.jpg",
                    "salesSupport": {}
                }
            },
            "video": {
                "url": "",
                "type": ""
            },
            "price": price,
            "category": category,
            "allergens": allergens,
            "options": options,
            "isAvailable": is_available,
            "items": [],
            "linkedItems": [],
            "linkedChild": [],
            "linkedTags": [],
            "visibilityInfo": {
                "dflt": {
                    "1": [2, 1, 0],
                    "2": [2, 1, 0],
                    "3": [2, 1, 0]
                },
                "isVisible": True,
                "basicCompVisibility": True
            },
            "isInfoModeActive": True,
            "archive": False,
            "color": "#FFFFFF",
            "idCard": [],
            "parent": "",
            "liaison": [],
            "isNameShow": True,
            "child": [],
            "dateCreation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "_generated_by_ai": True
        }
        
        return product
    
    def _basic_category_detection(self, description: str) -> str:
        """Détection basique de catégorie sans analyzer"""
        desc_lower = description.lower()
        
        if 'pizza' in desc_lower:
            return 'PIZZAS'
        elif 'milkshake' in desc_lower or 'milk shake' in desc_lower:
            return 'MILKSHAKE'
        elif any(word in desc_lower for word in ['coca', 'fanta', 'sprite', 'boisson']):
            return 'BOISSONS'
        elif any(word in desc_lower for word in ['dessert', 'gateau', 'tiramisu', 'brownie']):
            return 'DESSERTS'
        elif any(word in desc_lower for word in ['chicken', 'nuggets', 'tenders', 'wings']):
            return 'FINGER FOOD'
        elif 'salade' in desc_lower:
            return 'SALADES'
        elif 'menu' in desc_lower or 'formule' in desc_lower:
            return 'MENU'
        else:
            return 'AUTRES'


# Test du modèle
if __name__ == "__main__":
    print("🤖 SYSTÈME IA DE GÉNÉRATION DE PRODUITS\n")
    
    # Initialiser le générateur
    generator = ProductGeneratorAI(r"c:\Users\mohamed taher\Downloads\3.json")
    
    # Tests avec différentes descriptions
    test_cases = [
        "Milkshake chocolat avec chantilly et sauce caramel",
        "Pizza 4 fromages avec mozzarella, chèvre, emmental et parmesan",
        "Chicken nuggets croustillants servis avec sauce BBQ",
        "Coca-Cola fraîche",
        "Tiramisu maison avec café italien"
    ]
    
    print("📝 GÉNÉRATION AUTOMATIQUE DE PRODUITS :\n")
    
    for i, description in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i} : {description}")
        print('='*70)
        
        product = generator.generate_complete_product(description)
        
        print(f"\n✅ NOM GÉNÉRÉ : {product['displayName']['dflt']['nameDef']}")
        print(f"📂 CATÉGORIE : {product['category']}")
        print(f"💰 PRIX : {product['price']}€")
        print(f"⚠️  ALLERGÈNES : {', '.join(product['allergens']) if product['allergens'] else 'Aucun'}")
        print(f"🔧 OPTIONS : {len(product['options'])} option(s)")
        if product['options']:
            for opt in product['options']:
                choices = ', '.join([c['name'] for c in opt['choices']])
                print(f"   - {opt['label']}: {choices}")
        
        print(f"\n🌍 TRADUCTIONS :")
        for lang, trans in product['displayName']['dflt']['salesSupport'].items():
            print(f"   {lang.upper()}: {trans['name']}")
        
        print(f"\n📸 IMAGE : {product['img']['dflt']['img']}")
        print(f"✔️  DISPONIBLE : {'Oui' if product['isAvailable'] else 'Non'}")
    
    print(f"\n\n{'='*70}")
    print("✅ SYSTÈME IA OPÉRATIONNEL")
    print('='*70)

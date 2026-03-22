"""
Modèle IA de génération automatique de catégories
Génère : titre, displayName (traductions), couleur, etc.
"""

import re
import uuid
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from data_analyzer import DataAnalyzer

class CategoryGeneratorAI:
    """
    Modèle IA qui génère automatiquement tous les détails d'une catégorie
    à partir d'une simple description
    """
    
    def __init__(self, json_data_path: str = None):
        self.analyzer = DataAnalyzer(json_data_path) if json_data_path else None
        if self.analyzer:
            self.analyzer.load_data()
            self.analyzer.extract_patterns()
        
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Construit la base de connaissances pour les catégories"""
        return {
            'translations': {
                'fr_to_en': {
                    'pizzas': 'pizzas',
                    'boissons': 'drinks',
                    'desserts': 'desserts',
                    'milkshakes': 'milkshakes',
                    'salades': 'salads',
                    'menus': 'menus',
                    'entrées': 'starters',
                    'plats': 'main courses',
                    'accompagnements': 'sides',
                    'burger': 'burgers',
                    'pâtes': 'pasta',
                    'glaces': 'ice creams',
                    'vins': 'wines',
                    'bières': 'beers',
                    'cafés': 'coffees'
                },
                'fr_to_ar': {
                    'pizzas': 'بيتزا',
                    'boissons': 'مشروبات',
                    'desserts': 'حلويات',
                    'milkshakes': 'ميلك شيك',
                    'salades': 'سلطات',
                    'menus': 'قوائم',
                    'entrées': 'مقبلات',
                    'plats': 'أطباق رئيسية',
                    'accompagnements': 'مقبلات',
                    'burger': 'برجر',
                    'pâtes': 'باستا',
                    'glaces': 'مثلجات',
                    'vins': 'خمور',
                    'bières': 'بببيرة',
                    'cafés': 'قهوة'
                }
            },
            'color_schemes': {
                'PIZZAS': '#E74C3C',        # Rouge
                'BOISSONS': '#3498DB',     # Bleu
                'DESSERTS': '#9B59B6',     # Violet
                'MILKSHAKE': '#F1C40F',    # Jaune
                'SALADES': '#2ECC71',      # Vert
                'MENU': '#E67E22',         # Orange
                'FINGER FOOD': '#D35400',  # Orange foncé
                'ROLL Z': '#1ABC9C',       # Turquoise
                'BOISSONS CHAUDES': '#8D6E63' # Brun
            }
        }

    def generate_title_from_description(self, description: str) -> str:
        """Génère un titre (ID) court et en majuscules"""
        title = description.strip().upper()
        # Enlever les articles et mots inutiles
        title = re.sub(r'^(LA |LE |LES |DES |UN |UNE )', '', title)
        # Prendre max 2-3 mots et les joindre avec un espace
        words = title.split()
        return ' '.join(words[:2])

    def generate_color_from_category(self, title: str) -> str:
        """Suggère une couleur héxa selon le type de catégorie"""
        for cat_type, color in self.knowledge_base['color_schemes'].items():
            if cat_type in title.upper():
                return color
        # Couleur par défaut aléatoire si non trouvé
        return random.choice(['#34495E', '#7F8C8D', '#16A085', '#27AE60', '#2980B9', '#8E44AD'])

    def translate_text(self, text: str, target_lang: str) -> str:
        """Traduit le texte vers la langue cible"""
        if target_lang == 'en':
            translations = self.knowledge_base['translations']['fr_to_en']
        elif target_lang == 'ar':
            translations = self.knowledge_base['translations']['fr_to_ar']
        else:
            return text
        
        words = text.lower().split()
        translated_words = []
        
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word)
            translated = translations.get(clean_word, word)
            translated_words.append(translated)
        
        return ' '.join(translated_words)

    # Descriptions marketing par type de catégorie (FR / EN / AR)
    DESCRIPTIONS = {
        'PIZZA': {
            'fr': "Découvrez nos pizzas artisanales préparées avec des ingrédients frais et une pâte croustillante.",
            'en': "Discover our artisan pizzas made with fresh ingredients and a crispy crust.",
            'ar': "اكتشف بيتزاتنا الحرفية المحضرة بمكونات طازجة وعجينة مقرمشة."
        },
        'MILKSHAKE': {
            'fr': "Craquez pour nos milkshakes onctueux et gourmands, disponibles en de nombreux parfums.",
            'en': "Treat yourself to our creamy and indulgent milkshakes, available in many flavors.",
            'ar': "استمتع بميلك شيك كريمي ولذيذ، متوفر بنكهات متعددة."
        },
        'BOISSON': {
            'fr': "Rafraîchissez-vous avec notre sélection de boissons fraîches, jus et sodas.",
            'en': "Refresh yourself with our selection of cold drinks, juices and sodas.",
            'ar': "انتعش بتشكيلتنا من المشروبات الباردة والعصائر والمشروبات الغازية."
        },
        'DESSERT': {
            'fr': "Terminez votre repas en beauté avec nos desserts maison gourmands et généreux.",
            'en': "End your meal with a treat from our generous homemade dessert selection.",
            'ar': "اختم وجبتك بحلويات منزلية سخية ولذيذة."
        },
        'BURGER': {
            'fr': "Savourez nos burgers juteux préparés avec des viandes fraîches et des pains moelleux.",
            'en': "Enjoy our juicy burgers made with fresh meat and soft buns.",
            'ar': "استمتع ببرجرنا العصير المحضر بلحوم طازجة وخبز طري."
        },
        'SALADE': {
            'fr': "Optez pour la légèreté avec nos salades fraîches et colorées, riches en saveurs.",
            'en': "Choose lightness with our fresh and colorful salads, rich in flavors.",
            'ar': "اختر الخفة مع سلطاتنا الطازجة والملونة الغنية بالنكهات."
        },
        'MENU': {
            'fr': "Profitez de nos menus complets et équilibrés pour une expérience gourmande complète.",
            'en': "Enjoy our complete and balanced menus for a full gourmet experience.",
            'ar': "استمتع بقوائمنا المتكاملة والمتوازنة لتجربة ذواقة كاملة."
        },
        'FINGER FOOD': {
            'fr': "Partagez nos finger foods croustillants, parfaits pour l'apéritif ou une collation.",
            'en': "Share our crispy finger foods, perfect for appetizers or a snack.",
            'ar': "شارك أصابع الطعام المقرمشة لدينا، مثالية للمقبلات أو وجبة خفيفة."
        },
        'CAFE': {
            'fr': "Savourez nos boissons chaudes préparées avec soin pour vous réchauffer et vous réconforter.",
            'en': "Enjoy our hot beverages carefully prepared to warm and comfort you.",
            'ar': "استمتع بمشروباتنا الساخنة المحضرة بعناية لتدفئتك وراحتك."
        },
        'ROLL': {
            'fr': "Découvrez nos rolls généreux, garnis d'ingrédients frais pour un repas savoureux.",
            'en': "Discover our generous rolls, filled with fresh ingredients for a tasty meal.",
            'ar': "اكتشف لفائفنا السخية المحشوة بمكونات طازجة لوجبة شهية."
        },
    }

    DEFAULT_DESCRIPTION = {
        'fr': "Découvrez notre sélection de produits préparés avec soin pour satisfaire toutes vos envies.",
        'en': "Discover our selection of carefully prepared products to satisfy all your cravings.",
        'ar': "اكتشف تشكيلتنا من المنتجات المحضرة بعناية لإرضاء جميع رغباتك."
    }

    def generate_description(self, title: str) -> Dict:
        """Génère une description marketing trilingue selon le type de catégorie."""
        title_upper = title.upper()
        desc = self.DEFAULT_DESCRIPTION
        for key, texts in self.DESCRIPTIONS.items():
            if key in title_upper:
                desc = texts
                break
        return {
            "dflt": {
                "imp": [],
                "nameDef": desc['fr'],
                "salesSupport": {
                    "en": {"name": desc['en']},
                    "ar": {"name": desc['ar']}
                }
            }
        }

    def generate_display_name(self, description: str, title: str) -> Dict:
        """Génère le displayName avec traductions propres."""
        # Nom affiché : capitaliser chaque mot significatif
        name_fr = ' '.join(w.capitalize() for w in description.strip().split())

        # Traductions depuis la base de connaissances
        name_en = self.translate_text(description, 'en')
        name_ar = self.translate_text(description, 'ar')

        # Si la traduction n'a rien changé, utiliser l'anglais par défaut selon le type
        EN_NAMES = {
            'PIZZA': 'Pizzas', 'MILKSHAKE': 'Milkshakes', 'BOISSON': 'Drinks',
            'DESSERT': 'Desserts', 'BURGER': 'Burgers', 'SALADE': 'Salads',
            'MENU': 'Menus', 'FINGER FOOD': 'Finger Food', 'CAFE': 'Hot Drinks', 'ROLL': 'Rolls',
        }
        AR_NAMES = {
            'PIZZA': 'بيتزا', 'MILKSHAKE': 'ميلك شيك', 'BOISSON': 'مشروبات',
            'DESSERT': 'حلويات', 'BURGER': 'برجر', 'SALADE': 'سلطات',
            'MENU': 'قوائم', 'FINGER FOOD': 'مقبلات', 'CAFE': 'مشروبات ساخنة', 'ROLL': 'لفائف',
        }
        for key in EN_NAMES:
            if key in title.upper():
                name_en = EN_NAMES[key]
                name_ar = AR_NAMES[key]
                break

        return {
            "dflt": {
                "nameDef": name_fr,
                "salesSupport": {
                    "en": {"name": name_en},
                    "ar": {"name": name_ar}
                }
            }
        }

    def generate_complete_category(self, description: str) -> Dict[str, Any]:
        """Génère une catégorie complète prête pour le JSON"""
        title = self.generate_title_from_description(description)
        category_id = str(uuid.uuid4())

        category = {
            "id": category_id,
            "ref": f"CAT{random.randint(100, 999)}",
            "rank": 0,
            "title": title,
            "displayName": self.generate_display_name(description, title),
            "description": self.generate_description(title),
            "color": self.generate_color_from_category(title),
            "img": {
                "dflt": {
                    "img": "https://catalogue.etk360.com/placeholder-category.jpg",
                    "salesSupport": {}
                }
            },
            "video": {"url": "", "type": ""},
            "items": [],
            "child": [],
            "linkedChild": [],
            "linkedItems": [],
            "linkedTags": [],
            "visibilityInfo": {
                "dflt": {"1": [], "2": [], "3": [], "4": []},
                "isVisible": True,
                "basicCompVisibility": True
            },
            "isInfoModeActive": True,
            "idCard": [],
            "parent": "",
            "archive": False,
            "liaison": [],
            "isNameShow": True,
            "isVisible": True,
            "dateCreation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "_generated_by_ai": True
        }

        return category

    def generate_category_with_overrides(self, description: str, **overrides) -> Dict[str, Any]:
        """Generate a category then apply explicit field overrides.

        This is useful when you need a specific color, items list, visibility
        flags, etc. The overrides dictionary is deep-merged into the generated
        structure (top-level keys only). Example::

            gen = CategoryGeneratorAI()
            cat = gen.generate_category_with_overrides(
                "ESPRESSO",
                color="#FFFFE0",
                items=["id1", "id2"],
                visibilityInfo={"dflt": {"isVisible": False}}
            )

        """
        cat = self.generate_complete_category(description)
        # simple top-level merge; user can modify further as needed
        for k, v in overrides.items():
            cat[k] = v
        return cat

# Test rapide / interface CLI
if __name__ == "__main__":
    import sys

    generator = CategoryGeneratorAI()

    # if arguments were passed use them as descriptions, else start interactive loop
    if len(sys.argv) > 1:
        descriptions = sys.argv[1:]
    else:
        descriptions = []
        print("🔧 CategoryGeneratorAI interactive mode")
        print("  Tapez une description de catégorie et appuyez sur Entrée.")
        print("  Laissez vide puis appuyez sur Entrée pour quitter.")
        while True:
            desc = input("Description : ").strip()
            if not desc:
                break
            descriptions.append(desc)

    if not descriptions:
        # default examples if nothing was provided/interacted
        descriptions = ["Nos Pizzas Italiennes", "Boissons Fraîches", "Glace et Desserts"]

    for cat_desc in descriptions:
        c = generator.generate_complete_category(cat_desc)
        print(f"\n--- Catégorie: {cat_desc} ---")
        print(f"ID: {c['title']}")
        print(f"Ref: {c['ref']}")
        print(f"Couleur: {c['color']}")
        # Description and language support
        desc = c.get('description', {}).get('dflt', {}).get('nameDef', '')
        if desc:
            print(f"Description: {desc}")
        en_name = c['displayName']['dflt']['salesSupport'].get('en', {}).get('name','')
        ar_name = c['displayName']['dflt']['salesSupport'].get('ar', {}).get('name','')
        print(f"EN: {en_name}")
        print(f"AR: {ar_name}")
        # dump full structure for debugging if run in verbose mode
        if len(descriptions) == 1:  # when only one provided, show full JSON
            import json
            print("\nFull object:\n", json.dumps(c, ensure_ascii=False, indent=2))

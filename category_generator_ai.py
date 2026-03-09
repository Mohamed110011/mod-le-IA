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

    def generate_complete_category(self, description: str) -> Dict[str, Any]:
        """Génère une catégorie complète prête pour le JSON"""
        title = self.generate_title_from_description(description)
        display_name_fr = description.capitalize()
        
        category_id = str(uuid.uuid4())
        
        category = {
            "id": category_id,
            "ref": f"CAT{random.randint(100, 999)}",
            "title": title,
            "displayName": {
                "dflt": {
                    "nameDef": display_name_fr,
                    "salesSupport": {
                        "en": {"name": self.translate_text(description, 'en')},
                        "ar": {"name": self.translate_text(description, 'ar')}
                    }
                }
            },
            "color": self.generate_color_from_category(title),
            "img": {
                "dflt": {
                    "img": "https://catalogue.etk360.com/placeholder-category.jpg"
                }
            },
            "items": [],
            "isVisible": True,
            "dateCreation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "_generated_by_ai": True
        }
        
        return category

# Test rapide
if __name__ == "__main__":
    generator = CategoryGeneratorAI()
    test_cats = ["Nos Pizzas Italiennes", "Boissons Fraîches", "Glace et Desserts"]
    for cat_desc in test_cats:
        c = generator.generate_complete_category(cat_desc)
        print(f"\n--- Catégorie: {cat_desc} ---")
        print(f"ID: {c['title']}")
        print(f"Couleur: {c['color']}")
        print(f"EN: {c['displayName']['dflt']['salesSupport']['en']['name']}")
        print(f"AR: {c['displayName']['dflt']['salesSupport']['ar']['name']}")

"""
Système d'analyse des données JSON pour extraire les patterns
et préparer l'entraînement du modèle IA
"""

import json
import re
from collections import defaultdict, Counter
from typing import Dict, List, Any
import numpy as np


class DataAnalyzer:
    """Analyse le fichier JSON pour extraire les patterns de produits"""
    
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.data = None
        self.categories = []
        self.products = []
        self.patterns = {
            'prices': defaultdict(list),
            'allergens': defaultdict(list),
            'categories': defaultdict(int),
            'names': [],
            'descriptions': []
        }
    
    def load_data(self):
        """Charge les données JSON"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extraire uniquement les catégories (après la première accolade)
            start = content.find('{')
            self.data = json.loads(content[start:])
        print(f"✅ Données chargées : {len(self.data)} catégories trouvées")
        return self.data
    
    def extract_patterns(self):
        """Extrait tous les patterns des données"""
        if not self.data:
            self.load_data()
        
        for category_id, category_data in self.data.items():
            if not isinstance(category_data, dict):
                continue
            
            # Extraire les informations de catégorie
            category_info = {
                'id': category_data.get('id'),
                'title': category_data.get('title', ''),
                'displayName': category_data.get('displayName', {}),
                'items': category_data.get('items', []),
                'color': category_data.get('color', ''),
                'img': category_data.get('img', {})
            }
            
            self.categories.append(category_info)
            
            # Compter les catégories
            title = category_info['title']
            self.patterns['categories'][title] += 1
            
            # Extraire les noms
            if title:
                self.patterns['names'].append(title)
            
            # Extraire les descriptions
            display_name = category_info['displayName']
            if isinstance(display_name, dict) and 'dflt' in display_name:
                desc = display_name['dflt'].get('nameDef', '')
                if desc:
                    self.patterns['descriptions'].append(desc)
        
        print(f"✅ Patterns extraits :")
        print(f"   - {len(self.categories)} catégories")
        print(f"   - {len(self.patterns['names'])} noms")
        print(f"   - {len(self.patterns['descriptions'])} descriptions")
        
        return self.patterns
    
    def analyze_price_patterns(self, product_type: str = None):
        """Analyse les patterns de prix par type de produit"""
        # Règles basées sur l'observation des pizzas
        price_rules = {
            'PIZZA': {
                'S': (8.0, 12.0),
                'M': (10.0, 15.0),
                'L': (12.0, 18.0),
                'XL': (15.0, 22.0)
            },
            'BOISSON': {
                'SMALL': (2.0, 4.0),
                'MEDIUM': (3.0, 5.0),
                'LARGE': (4.0, 6.0)
            },
            'DESSERT': {
                'INDIVIDUAL': (3.0, 6.0),
                'SHARING': (8.0, 12.0)
            },
            'MENU': {
                'SMALL': (12.0, 16.0),
                'MEDIUM': (15.0, 20.0),
                'LARGE': (18.0, 25.0),
                'XL': (22.0, 30.0)
            },
            'FINGER_FOOD': {
                'SMALL': (5.0, 8.0),
                'MEDIUM': (7.0, 10.0),
                'LARGE': (9.0, 14.0)
            }
        }
        
        return price_rules
    
    def analyze_allergen_patterns(self):
        """Analyse les patterns d'allergènes par type de produit"""
        allergen_rules = {
            'PIZZA': ['gluten', 'lait', 'fromage'],
            'BOISSON': [],
            'MILKSHAKE': ['lait'],
            'DESSERT': ['gluten', 'lait', 'oeufs'],
            'ROLL': ['gluten'],
            'SALAD': [],
            'CHICKEN': [],
            'CAFE': ['lait']
        }
        return allergen_rules
    
    def get_category_suggestions(self, description: str):
        """Suggère des catégories basées sur la description"""
        description_lower = description.lower()
        
        # Mots-clés pour identifier les catégories
        category_keywords = {
            'PIZZAS': ['pizza', 'margherita', 'fromage', 'tomate', 'mozzarella'],
            'BOISSONS': ['boisson', 'coca', 'fanta', 'sprite', 'jus', 'eau'],
            'DESSERTS': ['dessert', 'tiramisu', 'brownie', 'glace', 'sundae'],
            'MILKSHAKE': ['milkshake', 'milk shake', 'frappé'],
            'MENU': ['menu', 'formule', 'offre'],
            'ROLL Z': ['roll', 'roulé'],
            'SALADES': ['salade', 'végétarien'],
            'FINGER FOOD': ['chicken', 'nuggets', 'tenders', 'wings', 'mozza sticks'],
            'BOISSONS CHAUDES': ['café', 'cappuccino', 'espresso', 'latte']
        }
        
        scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for kw in keywords if kw in description_lower)
            if score > 0:
                scores[category] = score
        
        # Retourner la catégorie avec le meilleur score
        if scores:
            best_category = max(scores, key=scores.get)
            return best_category
        
        return "AUTRES"
    
    def search_products(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Recherche des produits similaires dans les données existantes"""
        if not self.categories:
            self.extract_patterns()
        
        query_lower = query.lower()
        results = []
        
        for category in self.categories:
            # Chercher dans le titre
            title = category.get('title', '').lower()
            display_name = category.get('displayName', {})
            
            if isinstance(display_name, dict) and 'dflt' in display_name:
                name_def = display_name['dflt'].get('nameDef', '').lower()
            else:
                name_def = ''
            
            # Calculer un score de similarité simple
            score = 0
            query_words = set(query_lower.split())
            title_words = set(title.split())
            name_words = set(name_def.split())
            
            # Correspondance exacte bonus
            if query_lower in title or query_lower in name_def:
                score += 100
            
            # Mots en commun
            common_title = len(query_words.intersection(title_words))
            common_name = len(query_words.intersection(name_words))
            score += (common_title * 10) + (common_name * 10)
            
            # Mots partiels
            for q_word in query_words:
                if any(q_word in word for word in title_words):
                    score += 5
                if any(q_word in word for word in name_words):
                    score += 5
            
            if score > 0:
                results.append({
                    'category': category,
                    'score': score,
                    'title': category.get('title', ''),
                    'display_name': name_def or title,
                    'id': category.get('id', ''),
                    'items_count': len(category.get('items', []))
                })
        
        # Trier par score décroissant
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:max_results]
    
    def find_similar_products(self, description: str, category_type: str = None) -> List[Dict[str, Any]]:
        """Trouve des produits similaires basés sur la description et la catégorie"""
        results = self.search_products(description)
        
        if category_type:
            # Filtrer par type de catégorie si spécifié
            category_keywords = {
                'PIZZA': ['pizza'],
                'MILKSHAKE': ['milkshake', 'shake'],
                'BOISSON': ['boisson', 'coca', 'fanta', 'sprite'],
                'DESSERT': ['dessert', 'tiramisu', 'brownie'],
                'FINGER FOOD': ['chicken', 'nuggets', 'tenders', 'wings']
            }
            
            if category_type in category_keywords:
                keywords = category_keywords[category_type]
                results = [r for r in results 
                          if any(kw in r['title'].lower() or kw in r['display_name'].lower() 
                                for kw in keywords)]
        
        return results
    
    def product_exists(self, name: str, threshold: int = 80) -> tuple:
        """Vérifie si un produit similaire existe déjà
        
        Returns:
            (bool, list): (existe, liste des produits similaires)
        """
        results = self.search_products(name)
        
        if results and results[0]['score'] >= threshold:
            return (True, results)
        
        return (False, results)
    
    def get_statistics(self):
        """Retourne les statistiques des données"""
        if not self.categories:
            self.extract_patterns()
        
        stats = {
            'total_categories': len(self.categories),
            'categories_by_type': Counter([c['title'] for c in self.categories]),
            'total_names': len(self.patterns['names']),
            'total_descriptions': len(self.patterns['descriptions'])
        }
        
        return stats
    
    def export_training_data(self, output_path: str = 'd:/model-IA-image/training_data.json'):
        """Exporte les données pour l'entraînement"""
        if not self.categories:
            self.extract_patterns()
        
        training_data = {
            'categories': self.categories,
            'patterns': {
                'prices': self.analyze_price_patterns(),
                'allergens': self.analyze_allergen_patterns(),
                'category_keywords': self.get_category_suggestions.__doc__
            },
            'statistics': self.get_statistics()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Données d'entraînement exportées vers : {output_path}")
        return output_path


# Fonction utilitaire pour tester
if __name__ == "__main__":
    # Test du système
    analyzer = DataAnalyzer(r"c:\Users\mohamed taher\Downloads\3.json")
    analyzer.load_data()
    analyzer.extract_patterns()
    
    # Afficher les statistiques
    stats = analyzer.get_statistics()
    print("\n📊 STATISTIQUES :")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Tester la suggestion de catégories
    test_descriptions = [
        "Pizza margherita avec mozzarella",
        "Milkshake chocolat avec chantilly",
        "Chicken nuggets croustillants",
        "Coca Cola 33cl"
    ]
    
    print("\n🔍 TEST DE SUGGESTION DE CATÉGORIES :")
    for desc in test_descriptions:
        category = analyzer.get_category_suggestions(desc)
        print(f"   '{desc}' → {category}")
    
    # Exporter les données
    analyzer.export_training_data()

"""
Modèle IA de génération automatique d'options/étapes (steps) pour produits
Génère : options, modificateurs, sauces, accompagnements, etc.
"""

import re
import uuid
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from data_analyzer import DataAnalyzer

class StepsOptionsGeneratorAI:
    """
    Modèle IA qui génère automatiquement les options/étapes (steps)
    pour les produits culinaires (sauces, accompagnements, modificateurs)
    """

    def __init__(self, json_data_path: str = None):
        self.analyzer = DataAnalyzer(json_data_path) if json_data_path else None
        if self.analyzer:
            self.analyzer.load_data()
            self.analyzer.extract_patterns()

        self.knowledge_base = self._build_knowledge_base()

    def _build_knowledge_base(self):
        """Construit la base de connaissances pour les options/étapes"""
        return {
            'step_types': {
                'sauces_pizza': {
                    'name': 'SAUCES',
                    'displayName': {
                        'dflt': {
                            'imp': [],
                            'nameDef': 'SAUCES',
                            'salesSupport': {
                                '1': {'en': 'SAUCES', 'fr': ''},
                                '2': {'en': 'SAUCES', 'fr': ''}
                            }
                        }
                    },
                    'items': [
                        {
                            'name': 'Sauce Tomate',
                            'img': 'sauce_tomate.webp',
                            'color': '#FFCCFF',
                            'price': 0,
                            'priceStep': 0.3,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Sauce Crème',
                            'img': 'sauce_creme.webp',
                            'color': '#FFCCFF',
                            'price': 0,
                            'priceStep': 0.3,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Sauce Barbecue',
                            'img': 'sauce_barbecue.webp',
                            'color': '#FFCCFF',
                            'price': 0,
                            'priceStep': 0.3,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Sauce Curry',
                            'img': 'sauce_curry.webp',
                            'color': '#ffccff',
                            'price': 0,
                            'priceStep': 0.3,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Sauce Aigre-douce',
                            'img': 'sauce_aigre_douce.webp',
                            'color': '#ff80ff',
                            'price': 0,
                            'priceStep': 0.3,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Sauce Chili Thai',
                            'img': 'sauce_chili_thai.webp',
                            'color': '#FFCCFF',
                            'price': 0,
                            'priceStep': 0.3,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Sauce Fromage',
                            'img': 'sauce_fromage.webp',
                            'color': '#FFCCFF',
                            'price': 0.5,
                            'priceStep': 0.5,
                            'specialPrice': 0.2
                        },
                        {
                            'name': 'Sauce Balsamique',
                            'img': 'sauce_balsamique.webp',
                            'color': '#FFCCFF',
                            'price': 0.5,
                            'priceStep': 0.5,
                            'specialPrice': 0.2
                        },
                        {
                            'name': 'Sauce Miel',
                            'img': 'sauce_miel.webp',
                            'color': '#FFCCFF',
                            'price': 0.5,
                            'priceStep': 0.5,
                            'specialPrice': 0.2
                        }
                    ]
                },
                'tailles_pizza': {
                    'name': 'TAILLES',
                    'displayName': {
                        'dflt': {
                            'imp': [],
                            'nameDef': 'TAILLES',
                            'salesSupport': {
                                '1': {'en': 'SIZES', 'fr': ''},
                                '2': {'en': 'SIZES', 'fr': ''}
                            }
                        }
                    },
                    'items': [
                        {
                            'name': 'Petite',
                            'img': 'taille_s.webp',
                            'color': '#FFCCFF',
                            'price': 0,
                            'priceStep': 2.0,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Moyenne',
                            'img': 'taille_m.webp',
                            'color': '#FFCCFF',
                            'price': 2.0,
                            'priceStep': 3.0,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Large',
                            'img': 'taille_l.webp',
                            'color': '#FFCCFF',
                            'price': 4.0,
                            'priceStep': 4.0,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Extra Large',
                            'img': 'taille_xl.webp',
                            'color': '#FFCCFF',
                            'price': 6.0,
                            'priceStep': 5.0,
                            'specialPrice': 0
                        }
                    ]
                },
                'accompagnements': {
                    'name': 'ACCOMPAGNEMENTS',
                    'displayName': {
                        'dflt': {
                            'imp': [],
                            'nameDef': 'ACCOMPAGNEMENTS',
                            'salesSupport': {
                                '1': {'en': 'SIDES', 'fr': ''},
                                '2': {'en': 'SIDES', 'fr': ''}
                            }
                        }
                    },
                    'items': [
                        {
                            'name': 'Frites',
                            'img': 'frites.webp',
                            'color': '#FFCCFF',
                            'price': 2.5,
                            'priceStep': 1.0,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Salade',
                            'img': 'salade.webp',
                            'color': '#FFCCFF',
                            'price': 3.0,
                            'priceStep': 1.5,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Riz',
                            'img': 'riz.webp',
                            'color': '#FFCCFF',
                            'price': 2.0,
                            'priceStep': 1.0,
                            'specialPrice': 0
                        }
                    ]
                },
                'boissons': {
                    'name': 'BOISSONS',
                    'displayName': {
                        'dflt': {
                            'imp': [],
                            'nameDef': 'BOISSONS',
                            'salesSupport': {
                                '1': {'en': 'DRINKS', 'fr': ''},
                                '2': {'en': 'DRINKS', 'fr': ''}
                            }
                        }
                    },
                    'items': [
                        {
                            'name': 'Cola',
                            'img': 'cola.webp',
                            'color': '#CCE5FF',
                            'price': 2.0,
                            'priceStep': 1.0,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Limonade',
                            'img': 'limonade.webp',
                            'color': '#CCE5FF',
                            'price': 2.0,
                            'priceStep': 1.0,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Eau Minérale',
                            'img': 'eau_minerale.webp',
                            'color': '#CCE5FF',
                            'price': 1.5,
                            'priceStep': 1.0,
                            'specialPrice': 0
                        },
                        {
                            'name': 'Thé Glacé',
                            'img': 'the_glace.webp',
                            'color': '#CCE5FF',
                            'price': 2.5,
                            'priceStep': 1.0,
                            'specialPrice': 0
                        }
                    ]
                }
            },
            'translations': {
                'fr_to_en': {
                    'sauces': 'sauces',
                    'tailles': 'sizes',
                    'accompagnements': 'sides',
                    'petite': 'small',
                    'moyenne': 'medium',
                    'large': 'large',
                    'extra large': 'extra large',
                    'frites': 'fries',
                    'salade': 'salad',
                    'riz': 'rice'
                }
            }
        }

    def _identify_step_type(self, description: str) -> str:
        """Identifie le type d'étapes/options selon la description"""
        desc_lower = description.lower()

        # Ordre de priorité : du plus spécifique au plus général
        type_keywords = {
            'tailles_pizza': ['taille', 'size', 'petite', 'moyenne', 'large', 'xl', 'extra large'],
            'accompagnements': ['accompagnement', 'side', 'frites', 'salade', 'riz', 'fries'],
            'boissons': ['boisson', 'drink', 'cola', 'gazeuse', 'soda', 'eau'],
            'sauces_pizza': ['sauce', 'sauces']
        }

        for step_type, keywords in type_keywords.items():
            if any(keyword in desc_lower for keyword in keywords):
                return step_type

        return 'sauces_pizza'  # default

    def generate_step_item(self, item_data: Dict[str, Any], rank: int) -> Dict[str, Any]:
        """Génère un item d'étape avec toutes les propriétés"""
        item_id = str(uuid.uuid4())

        return {
            item_id: {
                "img": item_data.get('img', ''),
                "rank": rank,
                "color": item_data.get('color', '#FFCCFF'),
                "price": item_data.get('price', 0),
                "itemPrice": {
                    "price": {},
                    "isVisible": False
                },
                "priceStep": item_data.get('priceStep', 0.3),
                "maxChoices": None,
                "minChoices": 0,
                "nbrWithPrice": None,
                "specialPrice": item_data.get('specialPrice', 0),
                "basicCompVisibility": True,
                "nbrWithspecialPrice": None
            }
        }

    def generate_complete_steps(self, description: str) -> Dict[str, Any]:
        """Génère des étapes/options complètes"""
        step_type = self._identify_step_type(description)
        step_config = self.knowledge_base['step_types'][step_type]

        # Générer l'ID principal
        main_id = random.randint(100000, 999999)

        # Générer les stepItems
        step_items = {}
        items_with_price = 0
        items_with_special_price = 0

        for i, item in enumerate(step_config['items'], 1):
            item_data = self.generate_step_item(item, i)
            step_items.update(item_data)

            # Compter les items avec prix
            item_id = list(item_data.keys())[0]
            if item_data[item_id]['price'] > 0:
                items_with_price += 1
            if item_data[item_id]['specialPrice'] > 0:
                items_with_special_price += 1

        # Générer l'objet complet
        steps_object = {
            "id": main_id,
            "img": f"{datetime.now().strftime('%Y%m%d%H%M%S')}baselimitl.webp",
            "ref": "",
            "req": False,
            "title": step_config['name'] + " " + description.upper()[:20],
            "archive": False,
            "isBasic": False,
            "codeEcran": step_config['name'] + "_" + description.upper()[:10].replace(" ", "_"),
            "isComment": False,
            "stepItems": step_items,
            "maxChoices": min(9, len(step_config['items'])),
            "minChoices": 0,
            "displayName": step_config['displayName'],
            "isModifiable": False,
            "nbrWithPrice": items_with_price,
            "specificOpts": {
                "isNext": True,
                "noButton": True,
                "zeroPrice": False,
                "isCheapest": False,
                "nextButton": False,
                "isExpensive": False,
                "withoutStep": False
            },
            "nbrWithspecialPrice": items_with_special_price
        }

        return steps_object

    def generate_multiple_steps(self, descriptions: List[str]) -> List[Dict[str, Any]]:
        """Génère des étapes pour plusieurs descriptions"""
        return [self.generate_complete_steps(desc) for desc in descriptions]

# Test rapide / interface CLI
if __name__ == "__main__":
    import sys
    import json

    generator = StepsOptionsGeneratorAI()

    # Mode interactif ou arguments en ligne de commande
    if len(sys.argv) > 1:
        descriptions = sys.argv[1:]
    else:
        descriptions = []
        print("🔧 StepsOptionsGeneratorAI interactive mode")
        print("  Tapez une description d'options/étapes et appuyez sur Entrée.")
        print("  Laissez vide puis appuyez sur Entrée pour quitter.")
        while True:
            desc = input("Description : ").strip()
            if not desc:
                break
            descriptions.append(desc)

    if not descriptions:
        # Exemples par défaut
        descriptions = ["Sauces pour Pizza", "Tailles Pizza", "Accompagnements"]

    for desc in descriptions:
        steps_obj = generator.generate_complete_steps(desc)
        print(f"\n--- Options/Étapes pour: {desc} ---")
        print(f"Type identifié: {generator._identify_step_type(desc)}")
        print(f"Nombre d'options: {len(steps_obj['stepItems'])}")
        print(f"Options avec prix: {steps_obj['nbrWithPrice']}")
        print(f"Options avec prix spécial: {steps_obj['nbrWithspecialPrice']}")

        # Afficher quelques options
        print("\nPremières options:")
        items_list = list(steps_obj['stepItems'].items())[:3]
        for item_id, item_data in items_list:
            print(f"  - Rang {item_data['rank']}: {item_data.get('img', 'no_img')} (prix: {item_data['price']}€)")

        # Afficher l'objet JSON complet si une seule description
        if len(descriptions) == 1:
            print("\nObjet JSON complet:")
            print(json.dumps(steps_obj, ensure_ascii=False, indent=2))
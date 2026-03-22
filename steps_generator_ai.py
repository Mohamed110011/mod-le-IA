"""
Modèle IA de génération automatique d'étapes de préparation
Génère : étapes de préparation/cuisson pour les produits culinaires
"""

import re
import uuid
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from data_analyzer import DataAnalyzer

class StepsGeneratorAI:
    """
    Modèle IA qui génère automatiquement les étapes de préparation
    à partir d'une description de produit culinaire
    """

    def __init__(self, json_data_path: str = None):
        self.analyzer = DataAnalyzer(json_data_path) if json_data_path else None
        if self.analyzer:
            self.analyzer.load_data()
            self.analyzer.extract_patterns()

        self.knowledge_base = self._build_knowledge_base()

    def _build_knowledge_base(self):
        """Construit la base de connaissances pour les étapes de préparation"""
        return {
            'preparation_steps': {
                'pizza': [
                    "Étaler la pâte à pizza sur une plaque farinée",
                    "Étaler la sauce tomate uniformément",
                    "Ajouter le fromage râpé",
                    "Disposer les ingrédients choisis",
                    "Enfourner à 250°C pendant 12-15 minutes",
                    "Laisser reposer 2 minutes avant de servir"
                ],
                'milkshake': [
                    "Verser le lait froid dans le blender",
                    "Ajouter la glace vanille",
                    "Incorporer le sirop de saveur",
                    "Mixer à vitesse maximale pendant 30 secondes",
                    "Verser dans un verre haut",
                    "Décorer avec de la chantilly et un topping"
                ],
                'salade': [
                    "Laver soigneusement toutes les feuilles",
                    "Égoutter et essorer les légumes",
                    "Couper les ingrédients en morceaux réguliers",
                    "Préparer la vinaigrette dans un bol",
                    "Mélanger délicatement les ingrédients",
                    "Assaisonner et servir frais"
                ],
                'pasta': [
                    "Porter l'eau salée à ébullition",
                    "Cuire les pâtes al dente selon le temps indiqué",
                    "Égoutter les pâtes en gardant un peu d'eau de cuisson",
                    "Faire revenir l'ail et les ingrédients dans l'huile",
                    "Ajouter les pâtes et mélanger",
                    "Servir immédiatement avec du parmesan"
                ],
                'burger': [
                    "Former les steaks hachés en galettes",
                    "Assaisonner les deux faces",
                    "Faire chauffer la poêle ou la plancha",
                    "Cuire 3-4 minutes par face selon la cuisson souhaitée",
                    "Ajouter le fromage en fin de cuisson pour qu'il fonde",
                    "Assembler le burger avec les ingrédients"
                ],
                'dessert': [
                    "Préparer les ingrédients à température ambiante",
                    "Beurrer et fariner le moule",
                    "Mélanger les ingrédients secs",
                    "Incorporer progressivement les ingrédients liquides",
                    "Verser dans le moule et enfourner",
                    "Laisser refroidir avant de démouler"
                ]
            },
            'cooking_times': {
                'pizza': "12-15 minutes à 250°C",
                'pasta': "8-12 minutes selon le type",
                'burger': "6-8 minutes au total",
                'milkshake': "30 secondes de mixage",
                'salade': "5 minutes de préparation"
            },
            'translations': {
                'fr_to_en': {
                    'étaler': 'spread',
                    'cuire': 'cook',
                    'mélanger': 'mix',
                    'ajouter': 'add',
                    'enfourner': 'bake',
                    'servir': 'serve',
                    'verser': 'pour',
                    'laisser': 'let',
                    'préparer': 'prepare',
                    'réfrigérer': 'refrigerate'
                },
                'fr_to_ar': {
                    'étaler': 'نشر',
                    'cuire': 'طبخ',
                    'mélanger': 'خلط',
                    'ajouter': 'إضافة',
                    'enfourner': 'وضع في الفرن',
                    'servir': 'تقديم',
                    'verser': 'صب',
                    'laisser': 'ترك',
                    'préparer': 'تحضير',
                    'réfrigérer': 'تبريد'
                }
            }
        }

    def _identify_product_type(self, description: str) -> str:
        """Identifie le type de produit à partir de la description"""
        desc_lower = description.lower()

        type_keywords = {
            'pizza': ['pizza', 'margherita', 'calzone', 'napolitaine'],
            'milkshake': ['milkshake', 'milk-shake', 'milk shake'],
            'salade': ['salade', 'salad'],
            'pasta': ['pâtes', 'pasta', 'spaghetti', 'penne', 'fusilli'],
            'burger': ['burger', 'hamburger'],
            'dessert': ['dessert', 'tarte', 'gâteau', 'glace', 'crème']
        }

        for product_type, keywords in type_keywords.items():
            if any(keyword in desc_lower for keyword in keywords):
                return product_type

        return 'generic'

    def _customize_steps_for_description(self, base_steps: List[str], description: str) -> List[str]:
        """Personnalise les étapes selon les ingrédients mentionnés"""
        customized_steps = base_steps.copy()
        desc_lower = description.lower()

        # Personnalisation pour les ingrédients spécifiques
        if 'fromage' in desc_lower or 'mozzarella' in desc_lower:
            # Remplacer ou ajouter une étape pour le fromage
            for i, step in enumerate(customized_steps):
                if 'fromage' in step.lower():
                    customized_steps[i] = step
                    break

        if 'chantilly' in desc_lower:
            # Ajouter décoration avec chantilly
            if not any('chantilly' in step.lower() for step in customized_steps):
                customized_steps.append("Décorer généreusement de chantilly")

        if 'caramel' in desc_lower:
            if not any('caramel' in step.lower() for step in customized_steps):
                customized_steps.append("Napper de sauce caramel chaude")

        return customized_steps

    def generate_steps_from_description(self, description: str) -> Dict[str, Any]:
        """Génère les étapes de préparation complètes"""
        product_type = self._identify_product_type(description)

        # Récupérer les étapes de base selon le type
        base_steps = self.knowledge_base['preparation_steps'].get(
            product_type,
            self.knowledge_base['preparation_steps']['dessert']  # fallback
        )

        # Personnaliser les étapes
        steps = self._customize_steps_for_description(base_steps, description)

        # Générer l'objet steps complet
        steps_object = {
            "id": str(uuid.uuid4()),
            "title": f"Préparation - {description.capitalize()}",
            "description": f"Étapes de préparation pour {description.lower()}",
            "steps": [],
            "totalTime": self.knowledge_base['cooking_times'].get(product_type, "15-20 minutes"),
            "difficulty": random.choice(["Facile", "Moyen", "Difficile"]),
            "servings": random.randint(1, 4),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Générer chaque étape avec détails
        for i, step_text in enumerate(steps, 1):
            step = {
                "id": str(uuid.uuid4()),
                "order": i,
                "title": f"Étape {i}",
                "description": step_text,
                "duration": f"{random.randint(1, 5)} min",
                "instructions": step_text,
                "tips": self._generate_step_tips(step_text, product_type),
                "translations": {
                    "en": self.translate_step(step_text, 'en'),
                    "ar": self.translate_step(step_text, 'ar')
                }
            }
            steps_object["steps"].append(step)

        return steps_object

    def translate_step(self, step_text: str, target_lang: str) -> str:
        """Traduit une étape vers la langue cible"""
        translations = self.knowledge_base['translations'].get(f'fr_to_{target_lang}', {})

        # Traduction simple par mots-clés
        translated = step_text
        for fr_word, target_word in translations.items():
            translated = re.sub(r'\b' + re.escape(fr_word) + r'\b', target_word, translated, flags=re.IGNORECASE)

        return translated

    def _generate_step_tips(self, step_text: str, product_type: str) -> str:
        """Génère des conseils pour une étape donnée"""
        tips_by_type = {
            'pizza': {
                'enfourner': "Préchauffez toujours le four à température maximale",
                'étaler': "Utilisez un rouleau à pâtisserie pour une épaisseur uniforme",
                'fromage': "Le fromage doit être râpé finement pour une meilleure fonte"
            },
            'milkshake': {
                'mixer': "Ne dépassez pas 30 secondes pour éviter que la glace fonde trop",
                'verser': "Servez immédiatement pour conserver la texture onctueuse"
            },
            'salade': {
                'laver': "Utilisez une eau vinaigrée pour éliminer les pesticides",
                'mélanger': "Mélangez toujours avec les mains pour ne pas abîmer les feuilles"
            }
        }

        tips = tips_by_type.get(product_type, {})
        for keyword, tip in tips.items():
            if keyword in step_text.lower():
                return tip

        return "Travaillez proprement et précisément"

    def generate_multiple_steps(self, descriptions: List[str]) -> List[Dict[str, Any]]:
        """Génère des étapes pour plusieurs descriptions"""
        return [self.generate_steps_from_description(desc) for desc in descriptions]

# Test rapide / interface CLI
if __name__ == "__main__":
    import sys
    import json

    generator = StepsGeneratorAI()

    # Mode interactif ou arguments en ligne de commande
    if len(sys.argv) > 1:
        descriptions = sys.argv[1:]
    else:
        descriptions = []
        print("👨‍🍳 StepsGeneratorAI interactive mode")
        print("  Tapez une description de produit culinaire et appuyez sur Entrée.")
        print("  Laissez vide puis appuyez sur Entrée pour quitter.")
        while True:
            desc = input("Description : ").strip()
            if not desc:
                break
            descriptions.append(desc)

    if not descriptions:
        # Exemples par défaut
        descriptions = ["Pizza Margherita", "Milkshake Chocolat", "Salade César"]

    for product_desc in descriptions:
        steps_obj = generator.generate_steps_from_description(product_desc)
        print(f"\n--- Étapes pour: {product_desc} ---")
        print(f"Type identifié: {generator._identify_product_type(product_desc)}")
        print(f"Temps total: {steps_obj['totalTime']}")
        print(f"Difficulté: {steps_obj['difficulty']}")
        print(f"Nombre d'étapes: {len(steps_obj['steps'])}")

        print("\nÉtapes détaillées:")
        for step in steps_obj['steps']:
            print(f"  {step['order']}. {step['description']} ({step['duration']})")
            if step['tips'] != "Travaillez proprement et précisément":
                print(f"     💡 {step['tips']}")

        # Afficher l'objet JSON complet si une seule description
        if len(descriptions) == 1:
            print("\nObjet JSON complet:")
            print(json.dumps(steps_obj, ensure_ascii=False, indent=2))
"""
Interface principale du système IA de génération d'options/étapes (steps)
Permet de générer automatiquement les options/modificateurs pour les produits
"""

import json
import os
import io
import contextlib
from typing import Optional, List, Dict, Any
from steps_options_generator_ai import StepsOptionsGeneratorAI
from data_analyzer import DataAnalyzer


class StepsOptionsAISystem:
    """
    Système IA complet pour la génération automatique d'options/étapes
    """

    def __init__(self, json_data_path: str):
        """
        Args:
            json_data_path: Chemin vers le fichier JSON de données
        """
        self.json_data_path = json_data_path

        # Initialiser les modules
        print("🚀 Initialisation du système IA d'options/étapes...")
        self.steps_generator = StepsOptionsGeneratorAI(json_data_path)
        self.data_analyzer = DataAnalyzer(json_data_path)

        print("✅ Système IA d'options/étapes initialisé avec succès !\n")

    def generate_steps_from_description(self, description: str) -> Dict[str, Any]:
        """
        Génère des options/étapes à partir d'une description

        Args:
            description: Description des options (ex: "Sauces pour Pizza")

        Returns:
            Dictionnaire contenant toutes les options/étapes
        """
        print(f"\n🔧 GÉNÉRATION DES OPTIONS/ÉTAPES...")
        print(f"   Description: {description}\n")

        # Générer les options/étapes
        steps = self.steps_generator.generate_complete_steps(description)

        # Afficher le résumé
        self.display_steps_summary(steps)

        return steps

    def generate_multiple_steps(self, descriptions: List[str]) -> List[Dict[str, Any]]:
        """
        Génère des options/étapes pour plusieurs descriptions

        Args:
            descriptions: Liste de descriptions d'options

        Returns:
            Liste d'objets options/étapes générés
        """
        steps_list = []

        print(f"\n🔄 GÉNÉRATION D'OPTIONS/ÉTAPES POUR {len(descriptions)} DESCRIPTIONS...\n")

        for i, desc in enumerate(descriptions, 1):
            print(f"\n{'='*70}")
            print(f"OPTIONS/ÉTAPES {i}/{len(descriptions)}")
            print('='*70)

            steps = self.generate_steps_from_description(desc)
            steps_list.append(steps)

        print(f"\n\n✅ {len(steps_list)} SÉRIES D'OPTIONS/ÉTAPES GÉNÉRÉES AVEC SUCCÈS !")
        return steps_list

    def display_steps_summary(self, steps: Dict[str, Any]):
        """Affiche un résumé des options/étapes générées"""
        if not steps:
            print("\n⚠️  Aucune option/étape à afficher\n")
            return

        print("\n" + "="*70)
        print("🔧 RÉSUMÉ DES OPTIONS/ÉTAPES")
        print("="*70)

        # Informations principales
        print(f"🆔 ID : {steps.get('id', 'N/A')}")
        print(f"📝 TITRE : {steps.get('title', 'N/A')}")
        print(f"🏷️  NOM D'AFFICHAGE : {steps.get('displayName', {}).get('dflt', {}).get('nameDef', 'N/A')}")
        print(f"💻 CODE ÉCRAN : {steps.get('codeEcran', 'N/A')}")

        # Statistiques
        step_items = steps.get('stepItems', {})
        print(f"\n📊 STATISTIQUES :")
        print(f"   • Nombre total d'options : {len(step_items)}")
        print(f"   • Options avec prix : {steps.get('nbrWithPrice', 0)}")
        print(f"   • Options avec prix spécial : {steps.get('nbrWithspecialPrice', 0)}")
        print(f"   • Choix minimum : {steps.get('minChoices', 0)}")
        print(f"   • Choix maximum : {steps.get('maxChoices', 'illimité')}")

        # Propriétés
        print(f"\n⚙️  PROPRIÉTÉS :")
        print(f"   • Requis : {'Oui' if steps.get('req', False) else 'Non'}")
        print(f"   • Modifiable : {'Oui' if steps.get('isModifiable', False) else 'Non'}")
        print(f"   • Archivé : {'Oui' if steps.get('archive', False) else 'Non'}")
        print(f"   • De base : {'Oui' if steps.get('isBasic', False) else 'Non'}")

        # Afficher les premières options
        if step_items:
            print(f"\n🔢 PREMIÈRES OPTIONS ({min(5, len(step_items))} affichées) :")
            items_sorted = sorted(step_items.items(), key=lambda x: x[1].get('rank', 999))
            for item_id, item_data in items_sorted[:5]:
                rank = item_data.get('rank', '?')
                price = item_data.get('price', 0)
                special_price = item_data.get('specialPrice', 0)
                img = item_data.get('img', 'no_image')

                price_info = f"{price}€"
                if special_price > 0:
                    price_info += f" (spécial: {special_price}€)"

                print(f"   {rank}. {img} - Prix: {price_info}")

        # Options spécifiques
        specific_opts = steps.get('specificOpts', {})
        if specific_opts:
            print(f"\n🎛️  OPTIONS SPÉCIFIQUES :")
            for opt, value in specific_opts.items():
                print(f"   • {opt}: {value}")

        print("\n" + "="*70 + "\n")

    def save_steps_to_json(self,
                          steps_list: List[Dict[str, Any]],
                          output_path: str = 'd:/model-IA-image/generated_steps_options.json'):
        """
        Sauvegarde les options/étapes générées dans un fichier JSON

        Args:
            steps_list: Liste des options/étapes à sauvegarder
            output_path: Chemin du fichier de sortie
        """
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Sauvegarder
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(steps_list, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Options/Étapes sauvegardées dans : {output_path}")
        return output_path

    def interactive_mode(self):
        """Mode interactif pour tester le système d'options/étapes"""
        print("\n" + "="*70)
        print("🔧 MODE INTERACTIF - SYSTÈME IA D'OPTIONS/ÉTAPES")
        print("="*70)
        print("\nCommandes disponibles :")
        print("  - Entrez une description d'options/étapes")
        print("  - 'quit' pour quitter\n")

        while True:
            try:
                user_input = input("🔧 Commande : ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Au revoir !")
                    break

                if not user_input:
                    print("⚠️  Veuillez entrer une commande.\n")
                    continue

                # Générer des options/étapes
                description = user_input
                steps = self.generate_steps_from_description(description)

                # Demander s'il faut sauvegarder
                save = input("💾 Sauvegarder ces options/étapes ? (o/n) : ").strip().lower()
                if save == 'o':
                    output_path = f"d:/model-IA-image/steps_options_{steps['id']}.json"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(steps, f, ensure_ascii=False, indent=2)
                    print(f"✅ Options/Étapes sauvegardées : {output_path}\n")

            except KeyboardInterrupt:
                print("\n\n👋 Au revoir !")
                break
            except Exception as e:
                print(f"\n❌ Erreur : {e}\n")

    def demo_mode(self):
        """Mode démo avec exemples prédéfinis d'options/étapes"""
        print("\n" + "="*70)
        print("🎬 MODE DÉMO - EXEMPLES D'OPTIONS/ÉTAPES")
        print("="*70)

        demo_descriptions = [
            "Sauces pour Pizza",
            "Tailles de Pizza",
            "Accompagnements pour Burger",
            "Sauces pour Salade",
            "Options de Cuisson"
        ]

        steps_list = self.generate_multiple_steps(demo_descriptions)

        # Sauvegarder toutes les options/étapes
        output_path = self.save_steps_to_json(steps_list)

        print(f"\n✅ DÉMO TERMINÉE")
        print(f"📁 {len(steps_list)} séries d'options/étapes générées et sauvegardées !")
        print(f"📂 Fichier : {output_path}")


def main():
    """Point d'entrée principal"""
    import argparse

    # Configuration
    JSON_DATA_PATH = r"c:\Users\mohamed taher\Downloads\3.json"

    parser = argparse.ArgumentParser(description="Système IA de génération d'options/étapes")
    parser.add_argument("--description", type=str, help="Description des options/étapes à générer")
    parser.add_argument("--json", action="store_true", help="Retourner le résultat en JSON sur stdout")
    parser.add_argument("--demo", action="store_true", help="Lancer le mode démo")
    args = parser.parse_args()

    # Mode non interactif (API)
    if args.description and args.json:
        # Rediriger les prints vers un buffer pour ne pas polluer le JSON
        with contextlib.redirect_stdout(io.StringIO()):
            system = StepsOptionsAISystem(json_data_path=JSON_DATA_PATH)
            steps = system.generate_steps_from_description(args.description)
        print(json.dumps(steps, ensure_ascii=False))
        return

    # Initialiser le système en mode interactif ou démo
    system = StepsOptionsAISystem(json_data_path=JSON_DATA_PATH)

    if args.demo:
        system.demo_mode()
        return

    # Menu principal
    print("\n" + "="*70)
    print("🔧 SYSTÈME IA DE GÉNÉRATION D'OPTIONS/ÉTAPES")
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
        print("\n👋 Au revoir !")


if __name__ == "__main__":
    main()
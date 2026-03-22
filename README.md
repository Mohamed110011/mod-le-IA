# 🤖 Système IA de Génération Automatique de Produits

Un système d'intelligence artificielle complet qui génère automatiquement **tous les détails d'un produit** à partir d'une simple description :
- ✅ Nom cohérent
- ✅ Prix probable
- ✅ Catégorie
- ✅ Allergènes
- ✅ Options (tailles, etc.)
- ✅ Traductions (FR, EN, AR)
- ✅ Image générée
- ✅ Disponibilité

## 🎯 Fonctionnalités

### 1️⃣ Génération Automatique Complète
À partir d'une simple description comme :
```
"Milkshake chocolat avec chantilly et sauce caramel"
```

Le système génère automatiquement :
- **Nom** : Milkshake Chocolat
- **Catégorie** : MILKSHAKE
- **Prix** : 4.50€ (petit) / 6.50€ (grand)
- **Allergènes** : Lait
- **Options** : Taille (Petit, Grand)
- **Traductions** :
  - EN: Chocolate Milkshake
  - AR: ميلك شيك شوكولاتة
- **Image** : Générée automatiquement
- **Description marketing** : Générée et traduite

### 2️⃣ Analyse Intelligente des Données
- Analyse votre fichier JSON existant
- Extrait les patterns de prix par catégorie
- Identifie les allergènes courants
- Suggère des catégories basées sur le contenu

### 3️⃣ Génération d'Images
Plusieurs backends supportés :
- **Placeholder** : Génération locale (gratuit, pour les tests)
- **DALL-E** : OpenAI (haute qualité, payant)
- **Stable Diffusion** : Stability AI (haute qualité, payant)
- **Replicate** : Stable Diffusion gratuit

### 4️⃣ Traductions Automatiques
- Français (base)
- Anglais
- Arabe
- Extensible à d'autres langues

## 📦 Installation

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances
```bash
cd d:/model-IA-image
pip install -r requirements.txt
```

## 🚀 Utilisation

### Mode Interactif
```bash
python main.py
```
Choisissez l'option 1 et entrez vos descriptions de produits.

(Le menu a été simplifié ; les modes démo et étapes ne sont plus disponibles.)

### Génération de Catégories Indépendante
Le modèle de catégories fonctionne seul et peut être invoqué sans exécuter le système produit. En mode interactif chaque description génère également un résumé lisible et une image placeholder.
Deux options :

```bash
# mode interactif via le script dédié
python categories.py

# génération par arguments en ligne
actionner : python categories.py "Nos Pizzas" "Boissons"
```

ou en Python :
```python
from category_generator_ai import CategoryGeneratorAI

gen = CategoryGeneratorAI(r"c:\Users\mohamed taher\Downloads\3.json")
# génération standard
cat = gen.generate_complete_category("Boissons Fraîches")
print(cat)

# génération avec champs personnalisés (couleur, items, visibilité...)
cat2 = gen.generate_category_with_overrides(
    "ESPRESSO",
    color="#FFFFE0",
    items=[
        "8e7a650f-992b-49bb-aeef-58c24b597b60",
        "df3c2c5b-e057-4c52-baa4-34ed84c176ae"
    ],
    visibilityInfo={
        "dflt": {"isVisible": False},
        "isVisible": False,
        "basicCompVisibility": True
    }
)
print(cat2)
```

### Utilisation Programmatique
```python
from main import ProductAISystem

# Initialiser le système
system = ProductAISystem(
    json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
    image_backend='placeholder'  # ou 'dall-e', 'stable-diffusion'
)

# Générer un produit
product = system.generate_product_from_description(
    "Pizza 4 fromages avec mozzarella, chèvre, emmental et parmesan"
)

# Afficher le résumé
system.display_product_summary(product)

# Sauvegarder
system.save_products_to_json([product])
```

## 📁 Structure du Projet

```
d:/model-IA-image/
├── main.py                      # Interface principale
├── product_generator_ai.py      # Générateur de produits IA
├── image_generator_ai.py        # Générateur d'images IA
├── data_analyzer.py             # Analyseur de données
├── requirements.txt             # Dépendances Python
├── README.md                    # Documentation
├── generated_images/            # Images générées
└── generated_products.json      # Produits générés
```

## 🧠 Comment ça marche ?

### 1. Analyse des Données
Le système analyse votre fichier JSON pour comprendre :
- Les patterns de prix (ex: Pizza S = 9.5€, M = 12.5€, L = 15.5€)
- Les allergènes communs par type de produit
- Les catégories existantes
- Les structures de traduction

### 2. Génération du Produit
Lors de l'ajout d'un nouveau produit avec juste une description :

```
"Milkshake chocolat épais avec chantilly"
```

L'IA :
1. **Analyse la description** pour identifier :
   - Type de produit : Milkshake
   - Ingrédients : chocolat, chantilly
   - Caractéristiques : épais

2. **Génère le nom** : "Milkshake Chocolat"

3. **Détermine la catégorie** : MILKSHAKE

4. **Calcule le prix** basé sur les patterns :
   - Petit : 4.50€
   - Grand : 6.50€

5. **Identifie les allergènes** :
   - Lait (détecté via "chocolat" + "chantilly")

6. **Génère les options** :
   - Taille : Petit / Grand

7. **Traduit automatiquement** :
   - EN: Thick Chocolate Milkshake with Whipped Cream
   - AR: ميلك شيك شوكولاتة سميك مع كريمة مخفوقة

8. **Génère l'image** (si activé)

9. **Définit la disponibilité** : Disponible par défaut

### 3. Règles de Prix
Le système utilise des règles intelligentes par catégorie :

| Catégorie | Taille | Prix |
|-----------|--------|------|
| PIZZA | S | 9.50€ |
| PIZZA | M | 12.50€ |
| PIZZA | L | 15.50€ |
| PIZZA | XL | 18.50€ |
| MILKSHAKE | Petit | 4.50€ |
| MILKSHAKE | Grand | 6.50€ |
| BOISSON | 33cl | 2.50€ |
| BOISSON | 50cl | 3.50€ |
| DESSERT | Individuel | 4.50€ |

### 4. Détection des Allergènes
Base de connaissances intégrée :
- **Fromage** → Lait, Fromage
- **Mozzarella** → Lait, Fromage
- **Crème** → Lait
- **Pâte, Pain** → Gluten
- **Oeuf** → Oeufs
- **Noix, Amande** → Fruits à coque

## 🎨 Génération d'Images

### Option 1 : Placeholder (Gratuit)
Images placeholder colorées générées localement.
```python
system = ProductAISystem(
    json_data_path="...",
    image_backend='placeholder'
)
```

### Option 2 : DALL-E (OpenAI)
Images haute qualité avec DALL-E.
```python
system = ProductAISystem(
    json_data_path="...",
    image_api_key="sk-...",  # Votre clé OpenAI
    image_backend='dall-e'
)
```

### Option 3 : Stable Diffusion (Stability AI)
Images haute qualité avec Stable Diffusion.
```python
system = ProductAISystem(
    json_data_path="...",
    image_api_key="sk-...",  # Votre clé Stability AI
    image_backend='stable-diffusion'
)
```

### Option 4 : Replicate (Gratuit avec API)
```python
system = ProductAISystem(
    json_data_path="...",
    image_api_key="r8_...",  # Votre token Replicate (gratuit)
    image_backend='replicate'
)
```

## 🔧 Configuration Avancée

### Personnaliser les Règles de Prix
Éditez `product_generator_ai.py` :
```python
price_rules = {
    'PIZZAS': {'S': 10.0, 'M': 13.0, 'L': 16.0, 'XL': 19.0},
    # ... vos règles
}
```

### Ajouter des Traductions
Éditez `product_generator_ai.py` :
```python
'fr_to_es': {  # Ajouter l'espagnol
    'pizza': 'pizza',
    'fromage': 'queso',
    # ...
}
```

### Ajouter des Allergènes
Éditez `product_generator_ai.py` :
```python
'allergens_by_ingredient': {
    'soja': ['soja'],
    'céleri': ['céleri'],
    # ...
}
```

## 📊 Exemples de Génération

### Exemple 1 : Pizza
**Input** :
```
"Pizza 4 fromages avec mozzarella, chèvre, emmental et parmesan"
```

**Output** :
```json
{
  "id": "uuid-...",
  "displayName": {
    "dflt": {
      "nameDef": "Pizza 4 Fromages",
      "salesSupport": {
        "en": {"name": "4 Cheese Pizza"},
        "ar": {"name": "بيتزا 4 جبن"}
      }
    }
  },
  "category": "PIZZAS",
  "price": 12.5,
  "allergens": ["gluten", "lait", "fromage"],
  "options": [
    {
      "label": "Taille",
      "choices": [
        {"name": "S", "priceModifier": 0},
        {"name": "M", "priceModifier": 0},
        {"name": "L", "priceModifier": 0},
        {"name": "XL", "priceModifier": 0}
      ]
    }
  ],
  "isAvailable": true
}
```

### Exemple 2 : Milkshake
**Input** :
```
"Milkshake vanille avec sauce caramel et chantilly"
```

**Output** :
```json
{
  "displayName": {
    "dflt": {
      "nameDef": "Milkshake Vanille",
      "salesSupport": {
        "en": {"name": "Vanilla Milkshake"},
        "ar": {"name": "ميلك شيك فانيليا"}
      }
    }
  },
  "category": "MILKSHAKE",
  "price": 4.5,
  "allergens": ["lait"],
  "options": [
    {
      "label": "Taille",
      "choices": [
        {"name": "Petit"},
        {"name": "Grand"}
      ]
    }
  ]
}
```

## 🚀 Prochaines Étapes

### Améliorations Possibles :
1. **Fine-tuning du modèle** avec vos données spécifiques
2. **API REST** pour intégration dans votre système
3. **Interface Web** (React/Vue.js)
4. **Apprentissage continu** basé sur les produits validés
5. **Génération de descriptions marketing** enrichies
6. **Analyse nutritionnelle** automatique
7. **Suggestions de prix** basées sur la concurrence

## 📝 Licence

Ce projet est fourni tel quel pour votre usage personnel et commercial.

## 🤝 Support

Pour toute question ou amélioration, n'hésitez pas à :
- Modifier les fichiers selon vos besoins
- Adapter les règles de prix et d'allergènes
- Ajouter de nouvelles langues de traduction

## ⚡ Quick Start

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer le système
python main.py

# 3. Choisir le mode démo (option 2)

# 4. Voir les résultats dans :
#    - d:/model-IA-image/generated_products.json
#    - d:/model-IA-image/generated_images/
```

---

**Créé avec ❤️ pour automatiser la gestion de produits avec l'IA**
# mod-le-IA

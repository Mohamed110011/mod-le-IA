# 🔧 Système IA de Génération d'Options/Étapes (Steps)

Un système d'intelligence artificielle spécialisé dans la génération automatique **d'options et modificateurs** pour les produits culinaires.

## 🎯 Fonctionnalités

### 1️⃣ Génération Automatique d'Options
À partir d'une simple description comme :
```
"Sauces pour Pizza"
```

Le système génère automatiquement :
- **ID unique** et références
- **Liste d'options** avec rangs, prix, images
- **Propriétés avancées** (prix spéciaux, visibilité, etc.)
- **Configuration complète** (min/max choix, modificateur, etc.)

### 2️⃣ Types d'Options Supportés

#### 🍕 Sauces pour Pizza
- Sauce Tomate, Crème, Barbecue
- Sauce Curry, Aigre-douce, Chili Thai
- Sauce Fromage, Balsamique, Miel
- Prix et options spéciales

#### 📏 Tailles de Pizza
- Petite, Moyenne, Large, Extra Large
- Prix progressifs par taille

#### 🍟 Accompagnements
- Frites, Salade, Riz
- Options avec suppléments

## 🚀 Utilisation

### Interface Principale
```bash
python steps_main.py
```

**Menu principal :**
```
🔧 SYSTÈME IA DE GÉNÉRATION D'OPTIONS/ÉTAPES

Choisissez un mode :
1. Mode interactif (entrez vos propres descriptions)
2. Mode démo (exemples prédéfinis)
3. Quitter
```

### Mode Interactif
Tapez vos descriptions d'options :
```
🔧 Commande : Sauces pour Pizza
```

**Résultat :**
```
🔧 GÉNÉRATION DES OPTIONS/ÉTAPES...
   Description: Sauces pour Pizza

🔧 RÉSUMÉ DES OPTIONS/ÉTAPES
======================================================================

🆔 ID : 806809
📝 TITRE : SAUCES SAUCES POUR PIZZA
🏷️  NOM D'AFFICHAGE : SAUCES
💻 CODE ÉCRAN : SAUCES_SAUCES_POU

📊 STATISTIQUES :
   • Nombre total d'options : 9
   • Options avec prix : 3
   • Options avec prix spécial : 3
   • Choix minimum : 0
   • Choix maximum : 9

🔢 PREMIÈRES OPTIONS :
   1. sauce_tomate.webp - Prix: 0€
   2. sauce_creme.webp - Prix: 0€
   3. sauce_barbecue.webp - Prix: 0€
```

### Mode Démo
Génère des exemples prédéfinis :
- Sauces pour Pizza
- Tailles de Pizza
- Accompagnements pour Burger
- Sauces pour Salade
- Options de Cuisson

### Génération Directe
```bash
python steps_options_generator_ai.py "Sauces pour Pizza"
```

## 📋 Structure JSON Générée

Le système génère un objet JSON complet avec :

```json
{
  "id": 806809,
  "img": "20260309131926baselimitl.webp",
  "ref": "",
  "req": false,
  "title": "SAUCES SAUCES POUR PIZZA",
  "archive": false,
  "isBasic": false,
  "codeEcran": "SAUCES_SAUCES_POU",
  "isComment": false,
  "stepItems": {
    "item_id_1": {
      "img": "sauce_tomate.webp",
      "rank": 1,
      "color": "#FFCCFF",
      "price": 0,
      "priceStep": 0.3,
      "specialPrice": 0,
      "basicCompVisibility": true
    }
  },
  "maxChoices": 9,
  "minChoices": 0,
  "displayName": {...},
  "isModifiable": false,
  "nbrWithPrice": 3,
  "specificOpts": {...},
  "nbrWithspecialPrice": 3
}
```

## 🔧 Personnalisation

### Ajouter de Nouveaux Types d'Options

Modifiez `steps_options_generator_ai.py` :

```python
'step_types': {
    'nouveau_type': {
        'name': 'NOUVEAU',
        'displayName': {...},
        'items': [
            {
                'name': 'Option 1',
                'img': 'option1.webp',
                'price': 1.5,
                'priceStep': 0.5,
                'specialPrice': 0
            }
        ]
    }
}
```

### Modifier les Prix

Ajustez les prix dans la base de connaissances :
```python
'price': 2.5,        # Prix de base
'priceStep': 1.0,    # Incrément
'specialPrice': 0    # Prix spécial (0 = pas de spécial)
```

## 💾 Sauvegarde

Les options générées sont automatiquement sauvegardées dans :
- `d:/model-IA-image/steps_options_{id}.json` (interactif)
- `d:/model-IA-image/generated_steps_options.json` (démo)

## 🔗 Intégration

Ce système est complémentaire à :
- `main.py` : Génération de produits
- `category_generator_ai.py` : Génération de catégories

Utilisez-le pour créer des options/modificateurs à attacher aux produits générés.

## 📊 Statistiques

- **Types d'options** : 3 (sauces, tailles, accompagnements)
- **Options par défaut** : 9 sauces, 4 tailles, 3 accompagnements
- **Propriétés configurables** : Prix, visibilité, choix min/max
- **Format de sortie** : JSON compatible avec les systèmes existants
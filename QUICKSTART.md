# Guide d'Utilisation Rapide

## 🎯 Démarrage Rapide

### 1. Installation
```bash
cd d:/model-IA-image
pip install -r requirements.txt
```

### 2. Lancer le Système
```bash
python main.py
```

> **Générer des catégories indépendamment**
> ```bash
> # mode interactif
> python categories.py
>
> # ou via arguments
> python categories.py "Nos Pizzas" "Boissons"
> ```



### 3. Choisir un Mode

Le menu a été simplifié : seules deux options restent disponibles.

#### Mode Interactif
- Tapez `1` et appuyez sur Entrée
- Entrez une description de produit
- Exemple : `Pizza Margherita avec mozzarella et basilic`
- Le système génère tous les détails automatiquement

# (L'option 4 permet de quitter)

**🔍 Nouvelle Fonctionnalité : Recherche**
- Tapez `search pizza` pour rechercher tous les produits pizza
- Tapez `search milkshake` pour voir les boissons
- Le système détecte automatiquement les doublons avant création
- Voir [SEARCH_FEATURE.md](SEARCH_FEATURE.md) pour plus de détails

## 📝 Exemples de Descriptions

### Pizzas
```
Pizza Margherita avec mozzarella et basilic
Pizza 4 fromages avec chèvre, mozzarella, emmental et parmesan
Pizza Végétarienne avec champignons, poivrons et olives
Pizza Royale avec jambon, champignons et fromage
Pizza Pepperoni épicée avec chorizo et piments
```

### Milkshakes
```
Milkshake chocolat avec chantilly et sauce caramel
Milkshake vanille avec cookies Oreo
Milkshake fraise fraîche avec coulis de fruits rouges
Milkshake speculoos crémeux
Milkshake caramel salé avec biscuit croquant
```

### Finger Food
```
Chicken Nuggets croustillants avec sauce BBQ
Chicken Tenders panés servis avec sauce miel-moutarde
Chicken Wings épicées sauce buffalo
Mozza Sticks fondants avec sauce marinara
```

### Boissons
```
Coca-Cola 33cl bien fraîche
Fanta Orange 50cl
Sprite 1L
Jus d'orange pressé 25cl
Eau minérale 50cl
```

### Desserts
```
Tiramisu traditionnel au café italien
Brownie au chocolat avec glace vanille
Fondant au chocolat coulant
Cookie géant aux pépites de chocolat
Cheesecake New York style
```

## 🎨 Configuration des Images

### Par défaut (Placeholder - Gratuit)
Le système génère des images placeholder colorées localement.

### Avec DALL-E (Payant - OpenAI)
1. Obtenir une clé API sur https://platform.openai.com/api-keys
2. Éditer `main.py` :
```python
IMAGE_API_KEY = "sk-..."  # Votre clé
IMAGE_BACKEND = 'dall-e'
```

### Avec Replicate (Gratuit avec limite)
1. Créer un compte sur https://replicate.com
2. Obtenir un token API
3. Éditer `main.py` :
```python
IMAGE_API_KEY = "r8_..."  # Votre token
IMAGE_BACKEND = 'replicate'
```

## 📊 Résultats

### Fichiers Générés
- `generated_products.json` : Tous les produits en JSON
- `generated_images/` : Images générées
- `product_{id}.json` : Produits individuels sauvegardés

### Format JSON Généré
```json
{
  "id": "uuid-unique",
  "ref": "REF123456",
  "displayName": {
    "dflt": {
      "nameDef": "Pizza Margherita",
      "salesSupport": {
        "en": {"name": "Margherita Pizza"},
        "ar": {"name": "بيتزا مارغريتا"}
      }
    }
  },
  "category": "PIZZAS",
  "price": 12.5,
  "allergens": ["gluten", "lait"],
  "options": [...],
  "img": {...},
  "isAvailable": true
}
```

## 🔧 Personnalisation

### Changer les Prix
Éditez `product_generator_ai.py`, ligne ~150 :
```python
price_rules = {
    'PIZZAS': {'S': 9.5, 'M': 12.5, 'L': 15.5, 'XL': 18.5},
    # Modifiez ici
}
```

### Ajouter une Langue
Éditez `product_generator_ai.py`, ligne ~50 :
```python
'fr_to_es': {  # Espagnol
    'pizza': 'pizza',
    'fromage': 'queso',
    # ...
}
```

### Personnaliser les Allergènes
Éditez `product_generator_ai.py`, ligne ~90 :
```python
'allergens_by_ingredient': {
    'soja': ['soja'],
    'céleri': ['céleri'],
    # ...
}
```

## ⚡ Commandes Rapides

```bash
# Lancer le système
python main.py


# Tester l'analyseur de données
python data_analyzer.py

# Tester le générateur de produits
python product_generator_ai.py

# Tester le générateur d'images
python image_generator_ai.py
```

## 🐛 Résolution de Problèmes

### Erreur : Module not found
```bash
pip install -r requirements.txt
```

### Erreur : Fichier JSON introuvable
Vérifiez le chemin dans `main.py` ligne 100 :
```python
JSON_DATA_PATH = r"c:\Users\mohamed taher\Downloads\3.json"
```

### Images ne se génèrent pas
- Vérifiez que le dossier `generated_images/` existe
- Si vous utilisez une API, vérifiez votre clé API
- Utilisez le mode `placeholder` pour tester sans API

## 📞 Support

En cas de problème :
1. Vérifiez les prérequis (Python 3.8+)
2. Réinstallez les dépendances : `pip install -r requirements.txt --upgrade`
3. Vérifiez les chemins de fichiers
4. Testez avec le mode démo d'abord

## ✅ Checklist de Démarrage

- [ ] Python 3.8+ installé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier JSON source accessible
- [ ] `python main.py` fonctionne
- [ ] Mode démo (option 2) génère des produits
- [ ] Fichier `generated_products.json` créé
- [ ] Dossier `generated_images/` contient des images

**Tout fonctionne ? Vous êtes prêt ! 🚀**

---

Pour plus de détails, consultez `README.md`

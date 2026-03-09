# 🎨 Génération d'Images Réalistes avec IA

## 🎯 Objectif

Générer des **images ultra-réalistes** de produits alimentaires avec l'intelligence artificielle au lieu d'utiliser des placeholders ou les images du JSON.

## 🆚 Comparaison des Backends

| Backend | Qualité | Prix | Vitesse | Recommandation |
|---------|---------|------|---------|----------------|
| **DALL-E 3** | ⭐⭐⭐⭐⭐ | 0.040$/image | 10-30s | ✅ Meilleure qualité |
| **Stable Diffusion** | ⭐⭐⭐⭐ | 0.002$/image | 5-15s | 💰 Meilleur prix |
| **Replicate** | ⭐⭐⭐ | Gratuit limité | 10-20s | 🧪 Pour tester |
| from_json | ⭐⭐⭐ | Gratuit | Instantané | 📦 Produits existants |
| placeholder | ⭐ | Gratuit | Instantané | 🚧 Tests/dev |

## 🔑 Obtenir une Clé API

### Option 1 : DALL-E 3 (OpenAI) - RECOMMANDÉ

**Avantages** : Qualité exceptionnelle, comprend bien les prompts en français

1. Créer un compte sur https://platform.openai.com/signup
2. Ajouter des crédits (minimum 5$) : https://platform.openai.com/account/billing
3. Générer une clé API : https://platform.openai.com/api-keys
4. Copier la clé (commence par `sk-...`)

**Prix** : ~0.040$ par image (1024x1024 HD)  
**Qualité** : Images photo-réalistes de très haute qualité

### Option 2 : Stable Diffusion (Stability AI)

**Avantages** : Moins cher, bonne qualité

1. Créer un compte sur https://platform.stability.ai/
2. Ajouter des crédits
3. Générer une clé API dans le dashboard
4. Copier la clé (commence par `sk-...`)

**Prix** : ~0.002$ par image  
**Qualité** : Très bonne qualité, style plus artistique

### Option 3 : Replicate

**Avantages** : Version gratuite limitée

1. Créer un compte sur https://replicate.com/
2. Obtenir un token API
3. Version gratuite : quelques générations par jour

**Prix** : Gratuit limité, puis payant  
**Qualité** : Bonne qualité pour tester

## 🚀 Utilisation Rapide

### Méthode 1 : Configuration Interactive

```bash
python setup_realistic_images.py
```

Menu interactif qui vous guide :
- 🔑 Instructions pour obtenir une clé API
- 🧪 Tester votre clé API
- 🎨 Générer des images de démonstration
- 💾 Créer un fichier de configuration

### Méthode 2 : Code Python Direct

```python
from main import ProductAISystem

# Configuration
system = ProductAISystem(
    json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
    image_backend='dall-e',  # ou 'stable-diffusion', 'replicate'
    image_api_key='sk-...'   # Votre clé API
)

# Générer un produit avec image réaliste
product = system.generate_product_from_description(
    "Pizza Margherita avec tomate fraîche et mozzarella fondante",
    generate_image=True
)

# L'image est sauvegardée dans generated_images/
print(f"Image: {product['image_path']}")
```

### Méthode 3 : Fichier de Configuration

1. Créer `api_keys.py` à la racine du projet :

```python
# api_keys.py
OPENAI_API_KEY = "sk-proj-..."
STABILITY_API_KEY = "sk-..."
DEFAULT_BACKEND = "dall-e"
```

2. Utiliser dans votre code :

```python
import api_keys
from main import ProductAISystem

system = ProductAISystem(
    json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
    image_backend=api_keys.DEFAULT_BACKEND,
    image_api_key=api_keys.OPENAI_API_KEY
)
```

## 🎨 Amélioration des Prompts

Le système génère maintenant des **prompts optimisés** selon le type de produit :

### Pizza
```
Ultra realistic professional food photography of a delicious Pizza Margherita.
Fresh ingredients, melted cheese, crispy crust, 
studio lighting, white marble surface, appetizing steam rising,
high-end restaurant presentation, 8K resolution, sharp focus,
commercial photography, mouthwatering details
```

### Burger
```
Premium professional food photography of Burger Classic.
Juicy patty, fresh vegetables, golden bun,
studio lighting, wooden board presentation, gourmet burger style,
hyper-realistic details, 8K quality, appetizing composition
```

### Milkshake/Boisson
```
Professional beverage photography of Milkshake Chocolat.
Tall glass, cold condensation droplets,
white background, studio lighting, vibrant colors,
fresh ingredients visible, commercial drink photography,
8K resolution, instagram-worthy presentation
```

Le système **détecte automatiquement** le type de produit et adapte le prompt pour obtenir la meilleure qualité !

## 📊 Exemples de Résultats

### Avant (Placeholder)
```
📸 IMAGE : Pizza_Margherita_placeholder.webp
Type : Cercle coloré avec texte
Qualité : ⭐ Basique
```

### Après (DALL-E 3)
```
📸 IMAGE : Pizza_Margherita_dalle.webp
Type : Photo ultra-réaliste
Qualité : ⭐⭐⭐⭐⭐ Professionnelle
```

**Différence visuelle** :
- ❌ Placeholder : Simple cercle avec nom du produit
- ✅ DALL-E : Photo réaliste comme dans un menu de restaurant !

## 💰 Estimation des Coûts

### Pour générer 100 produits :

**DALL-E 3** :
- Prix : 100 images × 0.040$ = **4.00$**
- Qualité : ⭐⭐⭐⭐⭐
- Temps : ~20 minutes

**Stable Diffusion** :
- Prix : 100 images × 0.002$ = **0.20$**
- Qualité : ⭐⭐⭐⭐
- Temps : ~15 minutes

**Recommandation** : Commencez avec 5-10$ de crédits pour tester

## 🔧 Fonctionnalités Avancées

### 1. Batch Generation (Lots)

```python
descriptions = [
    "Pizza Margherita",
    "Burger Classic",
    "Milkshake Chocolat",
    "Tiramisu Italien"
]

for desc in descriptions:
    product = system.generate_product_from_description(
        desc,
        generate_image=True,
        force=True
    )
    print(f"✅ {product['displayName']['dflt']['nameDef']}")
```

### 2. Mode Hybride (JSON + IA)

```python
# Essayer d'abord le JSON, puis IA si non trouvé
system_json = ProductAISystem(
    json_data_path=r"...\3.json",
    image_backend='from_json'
)

product = system_json.generate_product_from_description("pizza thon")

# Si placeholder généré, regénérer avec IA
if 'placeholder' in product.get('image_path', ''):
    system_ai = ProductAISystem(
        json_data_path=r"...\3.json",
        image_backend='dall-e',
        image_api_key='sk-...'
    )
    product = system_ai.generate_product_from_description(
        "pizza thon",
        generate_image=True,
        force=True
    )
```

### 3. Personnalisation des Prompts

Modifier `_create_realistic_prompt()` dans `image_generator_ai.py` pour adapter le style :

```python
# Style restaurant haut de gamme
base_prompt += ", Michelin star plating, luxury presentation"

# Style street food
base_prompt += ", street food style, casual presentation, rustic"

# Style healthy/bio
base_prompt += ", organic ingredients, natural lighting, healthy food"
```

## 🐛 Résolution de Problèmes

### Erreur : "API key requise"
**Solution** : Vérifiez que vous avez bien passé la clé API :
```python
image_api_key='sk-...'  # N'oubliez pas ce paramètre !
```

### Erreur : "Insufficient credits"
**Solution** : Ajoutez des crédits sur votre compte :
- OpenAI : https://platform.openai.com/account/billing
- Stability AI : https://platform.stability.ai/account/billing

### Erreur : "Rate limit exceeded"
**Solution** : Vous générez trop d'images trop vite. Solutions :
```python
import time

for desc in descriptions:
    product = system.generate_product_from_description(desc)
    time.sleep(5)  # Pause de 5 secondes entre chaque génération
```

### Images de mauvaise qualité
**Solutions** :
1. Utilisez DALL-E 3 au lieu de Stable Diffusion
2. Améliorez votre description :
   - ❌ "pizza"
   - ✅ "Pizza Margherita avec tomate fraîche, mozzarella fondante et basilic"

### Timeout lors de la génération
**Solution** : Augmentez le timeout dans `image_generator_ai.py` :
```python
response = requests.get(url, timeout=60)  # 60 secondes au lieu de 30
```

## 📈 Optimisation des Coûts

### Stratégie 1 : Génération Sélective
Générez uniquement les produits importants avec IA, les autres avec le JSON :
```python
important_products = ["Pizza Signature", "Burger Premium"]

if product_name in important_products:
    backend = 'dall-e'
else:
    backend = 'from_json'
```

### Stratégie 2 : Cache des Images
Sauvegardez les images générées et réutilisez-les :
```python
# Première fois : génération IA (coûte de l'argent)
product = system.generate_product_from_description("Pizza Margherita")

# Fois suivantes : réutiliser l'image sauvegardée (gratuit)
```

### Stratégie 3 : Stable Diffusion au lieu de DALL-E
- 20× moins cher
- Qualité toujours excellente pour la plupart des usages

## 📚 Ressources Supplémentaires

### Documentation API
- **OpenAI DALL-E** : https://platform.openai.com/docs/guides/images
- **Stability AI** : https://platform.stability.ai/docs
- **Replicate** : https://replicate.com/docs

### Tutoriels
- Créer un compte OpenAI : https://www.youtube.com/watch?v=...
- Optimiser les prompts : https://learngpt.com/prompt-engineering

### Support
- Issues GitHub : [votre repo]
- Email : [votre email]

## 🎉 Résumé

Pour générer des images **ultra-réalistes** :

1. **Obtenir une clé API** (DALL-E recommandé)
2. **Exécuter** `python setup_realistic_images.py`
3. **Suivre le guide** interactif
4. **Générer** vos produits avec des images professionnelles !

**Résultat** : Images dignes d'un menu de restaurant étoilé ! ⭐⭐⭐⭐⭐

---

**Date** : 18 février 2026  
**Version** : 3.0  
**Statut** : ✅ Production Ready

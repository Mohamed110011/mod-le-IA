# 🚀 Démarrage Rapide - Images Réalistes

## ⚡ En 3 Étapes

### 1️⃣ Obtenir une Clé API (5 minutes)

**Option Recommandée : DALL-E 3 (OpenAI)**

1. Aller sur https://platform.openai.com/signup
2. Créer un compte
3. Ajouter 5$ de crédits : https://platform.openai.com/account/billing
4. Créer une clé API : https://platform.openai.com/api-keys
5. Copier la clé (commence par `sk-proj-...`)

💰 **Coût** : ~0.04$ par image (120 images pour 5$)

### 2️⃣ Installer les Dépendances

```bash
pip install openai>=1.12.0
```

### 3️⃣ Générer des Images !

**Méthode A : Script Interactif (Simple)**

```bash
python setup_realistic_images.py
```

Choisir option 3, entrer votre clé API, et générer !

**Méthode B : Code Python (Rapide)**

```python
from main import ProductAISystem

system = ProductAISystem(
    json_data_path=r"c:\Users\mohamed taher\Downloads\3.json",
    image_backend='dall-e',
    image_api_key='sk-proj-...'  # Votre clé ici
)

# Générer 1 produit avec image réaliste
product = system.generate_product_from_description(
    "Pizza Margherita avec tomate fraîche et mozzarella",
    generate_image=True
)

print(f"✅ Image créée : {product['image_path']}")
```

**Méthode C : Ligne de Commande (Test)**

```bash
python test_realistic_image.py dall-e sk-proj-...
```

## 📊 Résultats

### Avant
```
📸 Pizza_Margherita_placeholder.webp
Type : Cercle coloré ⭕
Qualité : ⭐ Basique
```

### Après
```
📸 Pizza_Margherita_dalle.webp
Type : Photo professionnelle 📷
Qualité : ⭐⭐⭐⭐⭐ Ultra-réaliste
```

## 💡 Exemples de Prompts Générés

Le système génère automatiquement des prompts optimisés :

**Pizza** →
```
Ultra realistic professional food photography of Pizza Margherita.
Fresh ingredients, melted cheese, crispy crust, 
studio lighting, white marble surface, 8K resolution
```

**Burger** →
```
Premium food photography of Burger Classic.
Juicy patty, golden bun, gourmet style,
hyper-realistic details, 8K quality
```

**Milkshake** →
```
Professional beverage photography of Milkshake Chocolat.
Tall glass, cold condensation droplets,
instagram-worthy presentation, 8K resolution
```

## 🆘 Problèmes Courants

### ❌ "API key requise"
```python
# Vérifiez que vous passez la clé :
image_api_key='sk-proj-...'  # ← Important !
```

### ❌ "Insufficient credits"
→ Ajoutez des crédits sur https://platform.openai.com/account/billing

### ❌ "Module 'openai' not found"
```bash
pip install openai>=1.12.0
```

## 💰 Optimisation des Coûts

### Stratégie 1 : JSON d'abord, IA ensuite
```python
# Essayer le JSON (gratuit)
system_json = ProductAISystem(
    json_data_path=r"...\3.json",
    image_backend='from_json'
)
product = system_json.generate_product_from_description("pizza")

# Si placeholder → IA (payant)
if 'placeholder' in product.get('image_path', ''):
    system_ai = ProductAISystem(
        json_data_path=r"...\3.json",
        image_backend='dall-e',
        image_api_key='sk-...'
    )
    product = system_ai.generate_product_from_description(
        "pizza", 
        force=True
    )
```

### Stratégie 2 : Stable Diffusion (20× moins cher)
```python
image_backend='stable-diffusion',  # 0.002$ vs 0.04$
image_api_key='sk-...'  # Clé Stability AI
```

**Économie** : 0.20$ pour 100 images au lieu de 4.00$ !

## 📚 Ressources

- **Guide Complet** : [IMAGES_REALISTES.md](IMAGES_REALISTES.md)
- **API OpenAI** : https://platform.openai.com/docs/guides/images
- **Script Setup** : `python setup_realistic_images.py`
- **Test Rapide** : `python test_realistic_image.py`

## 🎉 C'est Tout !

Vous pouvez maintenant générer des **images ultra-réalistes** dignes d'un menu de restaurant étoilé ! ⭐⭐⭐⭐⭐

---

💬 **Questions ?** Consultez [IMAGES_REALISTES.md](IMAGES_REALISTES.md) pour plus de détails.

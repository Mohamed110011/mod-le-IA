"""
Modele unique de generation de produit depuis une description.

Logique :
  1. Cherche dans data['items'] du JSON si un produit correspond
  2. Si trouve (score >= 50) → retourne le produit du JSON
  3. Sinon → genere un nouveau produit avec les regles integrees
"""

import json
import uuid
import random
import re
import os
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional
from PIL import Image, ImageDraw, ImageFont


# ---------------------------------------------------------------------------
# Regles integrees (prix, allergenes, categories, traductions)
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS = {
    'PIZZAS':          ['pizza', 'margherita', 'mozzarella', 'pepperoni', 'calzone'],
    'MILKSHAKE':       ['milkshake', 'milk shake', 'frappe', 'frappé'],
    'BOISSONS':        ['boisson', 'coca', 'fanta', 'sprite', 'jus', 'eau', 'soda'],
    'BOISSONS CHAUDES':['cafe', 'café', 'cappuccino', 'espresso', 'latte', 'thé', 'the'],
    'DESSERTS':        ['dessert', 'tiramisu', 'brownie', 'glace', 'sundae', 'gateau'],
    'MENU':            ['menu', 'formule', 'offre'],
    'SALADES':         ['salade', 'végétarien', 'vegetarien'],
    'FINGER FOOD':     ['chicken', 'nuggets', 'tenders', 'wings', 'mozza sticks'],
    'ROLL':            ['roll', 'roulé', 'roule'],
    'BURGER':          ['burger', 'hamburger', 'cheeseburger'],
}

PRICE_RULES = {
    'PIZZAS':          {'S': 9.5,  'M': 12.5, 'L': 15.5, 'XL': 18.5},
    'MILKSHAKE':       {'Petit': 4.5, 'Grand': 6.5},
    'BOISSONS':        {'33cl': 2.5, '50cl': 3.5, '1L': 5.0},
    'BOISSONS CHAUDES':{'Petit': 2.5, 'Grand': 3.5},
    'DESSERTS':        {'Individuel': 4.5},
    'MENU':            {'S': 14.5, 'M': 17.5, 'L': 20.5, 'XL': 24.5},
    'FINGER FOOD':     {'4 pcs': 6.5, '6 pcs': 8.5, '9 pcs': 11.5},
    'BURGER':          {'Simple': 8.5, 'Double': 11.5},
    'ROLL':            {'Individuel': 8.5},
    'SALADES':         {'Individuel': 9.5},
}

SIZE_OPTIONS = {
    'PIZZAS':          ['S', 'M', 'L', 'XL'],
    'MILKSHAKE':       ['Petit', 'Grand'],
    'BOISSONS':        ['33cl', '50cl', '1L'],
    'BOISSONS CHAUDES':['Petit', 'Grand'],
    'DESSERTS':        ['Individuel'],
    'MENU':            ['S', 'M', 'L', 'XL'],
    'FINGER FOOD':     ['4 pcs', '6 pcs', '9 pcs'],
    'BURGER':          ['Simple', 'Double'],
    'ROLL':            ['Individuel'],
}

ALLERGEN_RULES = {
    'fromage':    ['lait'],
    'mozzarella': ['lait'],
    'cheddar':    ['lait'],
    'crème':      ['lait'],
    'creme':      ['lait'],
    'lait':       ['lait'],
    'beurre':     ['lait'],
    'chocolat':   ['lait'],
    'chantilly':  ['lait'],
    'pizza':      ['gluten', 'lait'],
    'pâte':       ['gluten'],
    'pain':       ['gluten'],
    'burger':     ['gluten'],
    'roll':       ['gluten'],
    'farine':     ['gluten'],
    'oeuf':       ['oeufs'],
    'mayonnaise': ['oeufs'],
    'noix':       ['fruits a coque'],
    'amande':     ['fruits a coque'],
    'noisette':   ['fruits a coque'],
}

TRANSLATIONS_FR_EN = {
    'pizza': 'pizza', 'fromage': 'cheese', 'poulet': 'chicken',
    'tomate': 'tomato', 'champignon': 'mushroom', 'oignon': 'onion',
    'olives': 'olives', 'jambon': 'ham', 'viande': 'meat',
    'milkshake': 'milkshake', 'chocolat': 'chocolate', 'vanille': 'vanilla',
    'fraise': 'strawberry', 'caramel': 'caramel', 'boisson': 'drink',
    'dessert': 'dessert', 'salade': 'salad', 'petit': 'small',
    'grand': 'large', 'chantilly': 'whipped cream', 'glace': 'ice cream',
    'burger': 'burger', 'sauce': 'sauce', 'crème': 'cream',
}

TRANSLATIONS_FR_AR = {
    'pizza': 'بيتزا', 'fromage': 'جبن', 'poulet': 'دجاج',
    'tomate': 'طماطم', 'champignon': 'فطر', 'oignon': 'بصل',
    'olives': 'زيتون', 'jambon': 'لحم', 'viande': 'لحم',
    'milkshake': 'ميلك شيك', 'chocolat': 'شوكولاتة', 'vanille': 'فانيليا',
    'fraise': 'فراولة', 'caramel': 'كراميل', 'boisson': 'مشروب',
    'dessert': 'حلوى', 'salade': 'سلطة', 'petit': 'صغير',
    'grand': 'كبير', 'chantilly': 'كريمة مخفوقة', 'glace': 'مثلجات',
    'burger': 'برجر', 'sauce': 'صلصة', 'crème': 'كريمة',
}


# ---------------------------------------------------------------------------
# Generateur principal
# ---------------------------------------------------------------------------

class ProductGeneratorAI:
    """
    Genere un produit complet depuis une description.
    Cherche d'abord dans le JSON, sinon genere avec les regles integrees.
    """

    def __init__(self, json_path: str):
        self.json_path = json_path
        self.items: Dict[str, Any] = {}          # data['items']
        self.allergen_map: Dict[str, str] = {}   # uuid -> nom lisible
        self._load_json()

    # ------------------------------------------------------------------
    # Chargement JSON
    # ------------------------------------------------------------------

    def _load_json(self):
        """Charge les items et la carte d'allergenes depuis le JSON."""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.items = data.get('items', {})

        # Construire uuid -> nom allergene depuis allergenGroups
        # On mappe a la fois les UUIDs individuels ET l'UUID du groupe lui-meme
        for group_uuid, group in data.get('allergenGroups', {}).items():
            name = group.get('title', '').lower()
            self.allergen_map[group_uuid] = name           # UUID groupe
            for allergen_uuid in group.get('allergens', []):
                self.allergen_map[allergen_uuid] = name    # UUID individuel

        print(f"JSON charge : {len(self.items)} articles trouves.")

    # ------------------------------------------------------------------
    # Recherche dans le JSON
    # ------------------------------------------------------------------

    def _score(self, query: str, item: Dict[str, Any]) -> int:
        """Calcule un score de correspondance entre la requete et un item."""
        query_lower = query.lower()
        name = item.get('displayName', {}).get('dflt', {}).get('nameDef', '').lower()
        title = item.get('title', '').lower()

        score = 0
        q_words = set(query_lower.split())
        n_words = set(name.split())
        t_words = set(title.split())

        # Correspondance exacte
        if query_lower in name or query_lower in title:
            score += 100
        # Mots en commun
        score += len(q_words & n_words) * 15
        score += len(q_words & t_words) * 10
        # Mots partiels
        for w in q_words:
            if any(w in nw for nw in n_words):
                score += 5
        return score

    def search(self, description: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Retourne les items du JSON les plus proches de la description."""
        results = []
        for item_id, item in self.items.items():
            s = self._score(description, item)
            if s > 0:
                results.append({'item': item, 'score': s})
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:max_results]

    # ------------------------------------------------------------------
    # Construction depuis le JSON
    # ------------------------------------------------------------------

    def _allergen_names(self, uuids: List[str]) -> List[str]:
        """Convertit les UUIDs d'allergenes en noms lisibles."""
        seen = set()
        names = []
        for uid in uuids:
            name = self.allergen_map.get(uid)
            if name and name not in seen:
                seen.add(name)
                names.append(name)
        return names

    def _from_json(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Construit le produit final depuis un item du JSON."""
        name = item.get('displayName', {}).get('dflt', {}).get('nameDef', item.get('title', ''))

        # Categorie : detecter depuis le nom
        category = self._detect_category(name)

        # Prix : utiliser price.dflt, sinon generer
        raw_price = item.get('price', {})
        price = raw_price.get('dflt') if isinstance(raw_price, dict) else None
        if not price:
            price = self._make_price(category)

        # Allergenes : convertir UUIDs en noms
        allergen_uuids = item.get('allergens', [])
        allergens = self._allergen_names(allergen_uuids)
        if not allergens:
            allergens = self._make_allergens(name)

        # Image : telecharger depuis l'URL JSON, sinon chercher sur Openverse
        img_url = item.get('img', {}).get('dflt', {}).get('img', '')
        img_path = self._resolve_image(name, img_url, category)

        return {
            'id':          item.get('id', str(uuid.uuid4())),
            'ref':         item.get('ref', ''),
            'title':       item.get('title', name),
            'displayName': item.get('displayName', self._make_display_name(name)),
            'description': item.get('description', self._make_description(name)),
            'img':         {'dflt': {'img': img_path, 'salesSupport': {}}},
            'price':       price,
            'category':    category,
            'allergens':   allergens,
            'options':     item.get('opt', []),
            'isAvailable': not item.get('outStock', False),
            'visibilityInfo': item.get('visibilityInfo', {}),
            'archive':     item.get('archive', False),
            'color':       item.get('color', '#FFFFFF'),
            '_source':     'json',
        }

    # ------------------------------------------------------------------
    # Generation par regles IA
    # ------------------------------------------------------------------

    def _detect_category(self, text: str) -> str:
        text_lower = text.lower()
        best, best_score = 'AUTRES', 0
        for cat, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > best_score:
                best, best_score = cat, score
        return best

    def _make_price(self, category: str) -> float:
        rules = PRICE_RULES.get(category, {})
        if rules:
            base = list(rules.values())[0]
            return round(base + random.uniform(-0.5, 0.5), 2)
        return round(random.uniform(5.0, 12.0), 2)

    def _make_allergens(self, text: str) -> List[str]:
        text_lower = text.lower()
        found = set()
        for ingredient, names in ALLERGEN_RULES.items():
            if ingredient in text_lower:
                found.update(names)
        return sorted(found)

    def _translate(self, text: str, table: Dict[str, str]) -> str:
        words = re.sub(r'[^\w\s]', '', text.lower()).split()
        return ' '.join(table.get(w, w) for w in words)

    def _make_display_name(self, name: str) -> Dict:
        return {
            'dflt': {
                'nameDef': name,
                'imp': [],
                'salesSupport': {
                    'fr': {'name': name},
                    'en': {'name': self._translate(name, TRANSLATIONS_FR_EN)},
                    'ar': {'name': self._translate(name, TRANSLATIONS_FR_AR)},
                }
            }
        }

    def _make_description(self, text: str) -> Dict:
        return {'dflt': {'nameDef': text, 'imp': [], 'salesSupport': {}}}

    def _make_options(self, category: str) -> List[Dict]:
        sizes = SIZE_OPTIONS.get(category, [])
        if not sizes:
            return []
        return [{
            'label': 'Taille',
            'required': True,
            'choices': [{'name': s, 'priceModifier': 0.0} for s in sizes]
        }]

    def _make_name(self, description: str) -> str:
        """Genere un nom depuis la description en utilisant ses propres mots."""
        # Mots a ignorer (articles, prepositions, mots vides)
        STOP_WORDS = {'avec', 'aux', 'au', 'de', 'du', 'des', 'le', 'la', 'les',
                      'et', 'en', 'un', 'une', 'sur', 'sans', 'pour', 'par'}

        desc = description.strip()
        words = desc.split()

        # Identifier le mot principal (pizza, milkshake, burger, etc.)
        PREFIXES = {
            'pizza':     'Pizza',
            'milkshake': 'Milkshake',
            'frappe':    'Frappe',
            'frappé':    'Frappe',
            'burger':    'Burger',
            'salade':    'Salade',
            'roll':      'Roll',
            'menu':      'Menu',
        }

        prefix = None
        rest_words = []
        for w in words:
            w_low = w.lower()
            if w_low in PREFIXES:
                prefix = PREFIXES[w_low]
            elif w_low not in STOP_WORDS:
                rest_words.append(w.capitalize())

        if prefix and rest_words:
            return f"{prefix} {' '.join(rest_words)}"
        if prefix:
            return prefix
        # Cas generique : tous les mots significatifs
        significant = [w.capitalize() for w in words if w.lower() not in STOP_WORDS and len(w) > 1]
        return ' '.join(significant[:4]) or desc[:30]

    IMAGE_DIR = r'd:/model-IA-image/generated_images'

    def _resolve_image(self, name: str, url: str, category: str = '') -> str:
        """Tente de telecharger l'URL du JSON. Si echec, cherche sur Openverse."""
        import io as _io
        os.makedirs(self.IMAGE_DIR, exist_ok=True)
        safe = re.sub(r'[<>:"/\\|?*\s]', '_', name)
        headers = {'User-Agent': 'Mozilla/5.0'}

        if url and 'no-pictures' not in url:
            try:
                r = requests.get(url, headers=headers, timeout=12)
                if r.status_code == 200 and r.headers.get('content-type', '').startswith('image'):
                    path = os.path.join(self.IMAGE_DIR, f"{safe}.webp")
                    Image.open(_io.BytesIO(r.content)).convert('RGB').resize((800, 800), Image.LANCZOS).save(path, 'WEBP', quality=85)
                    print(f"  Image : {path}")
                    return path
            except Exception:
                pass

        # URL inaccessible → Openverse
        return self._generate_image(name, name, category)

    CATEGORY_COLORS = {
        'PIZZAS':          '#FF6B35',
        'MILKSHAKE':       '#FFE66D',
        'BOISSONS':        '#4ECDC4',
        'BOISSONS CHAUDES':'#C8956C',
        'DESSERTS':        '#FF69B4',
        'FINGER FOOD':     '#FFA500',
        'SALADES':         '#90EE90',
        'MENU':            '#9370DB',
        'BURGER':          '#D2691E',
        'ROLL':            '#20B2AA',
    }

    def _generate_image(self, name: str, description: str, category: str = '') -> str:
        """Cherche une image reelle via Openverse (libre de droits, sans cle API)."""
        import io as _io
        os.makedirs(self.IMAGE_DIR, exist_ok=True)
        safe = re.sub(r'[<>:"/\\|?*\s]', '_', name)
        headers = {'User-Agent': 'Mozilla/5.0'}

        # Construire la requete : nom du produit + type generique (food)
        query = urllib.parse.quote(f"{name} food")
        search_url = f"https://api.openverse.org/v1/images/?q={query}&page_size=10&license_type=commercial"

        try:
            print(f"  Image : recherche '{name}' sur Openverse...")
            resp = requests.get(search_url, headers=headers, timeout=15)
            if resp.status_code == 200:
                results = resp.json().get('results', [])
                # Essayer chaque resultat jusqu'a en telecharger un
                for item in results:
                    img_url = item.get('url', '')
                    if not img_url:
                        continue
                    try:
                        dl = requests.get(img_url, headers=headers, timeout=15)
                        if dl.status_code == 200 and dl.headers.get('content-type', '').startswith('image'):
                            path = os.path.join(self.IMAGE_DIR, f"{safe}.webp")
                            img = Image.open(_io.BytesIO(dl.content)).convert('RGB')
                            img = img.resize((800, 800), Image.LANCZOS)
                            img.save(path, 'WEBP', quality=85)
                            print(f"  Image : {path}")
                            return path
                    except Exception:
                        continue
        except Exception as e:
            print(f"  Image : erreur Openverse ({e})")

        # Fallback : placeholder PIL colore
        print(f"  Image : creation placeholder local...")
        color = self.CATEGORY_COLORS.get(category, '#AAAAAA')
        size = (800, 800)
        img = Image.new('RGB', size, color=color)
        draw = ImageDraw.Draw(img)
        m = 150
        draw.ellipse([m, m, size[0]-m, size[1]-m], fill='white', outline='#333333', width=6)
        try:
            font = ImageFont.truetype("arial.ttf", 52)
            small = ImageFont.truetype("arial.ttf", 28)
        except Exception:
            font = ImageFont.load_default()
            small = font
        lines = name.split()
        y = size[1] // 2 - len(lines) * 32
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            x = (size[0] - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), line, fill='#333333', font=font)
            y += (bbox[3] - bbox[1]) + 12
        if category:
            bbox = draw.textbbox((0, 0), category, font=small)
            x = (size[0] - (bbox[2] - bbox[0])) // 2
            draw.text((x, size[1] - 80), category, fill='#555555', font=small)
        path = os.path.join(self.IMAGE_DIR, f"{safe}_placeholder.webp")
        img.save(path, 'WEBP', quality=85)
        print(f"  Image : {path} (placeholder)")
        return path

    def _new_product(self, description: str) -> Dict[str, Any]:
        """Genere un produit entierement depuis les regles IA."""
        name = self._make_name(description)
        category = self._detect_category(description)
        price = self._make_price(category)
        allergens = self._make_allergens(description)
        options = self._make_options(category)
        img_path = self._generate_image(name, description, category)

        return {
            'id':          str(uuid.uuid4()),
            'ref':         f"REF{random.randint(100000, 999999)}",
            'title':       name.upper()[:20],
            'displayName': self._make_display_name(name),
            'description': self._make_description(description),
            'img':         {'dflt': {'img': img_path, 'salesSupport': {}}},
            'price':       price,
            'category':    category,
            'allergens':   allergens,
            'options':     options,
            'isAvailable': True,
            'visibilityInfo': {
                'dflt': {'1': [2, 1, 0], '2': [2, 1, 0], '3': [2, 1, 0]},
                'isVisible': True,
                'basicCompVisibility': True,
            },
            'archive':     False,
            'color':       '#FFFFFF',
            'dateCreation': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '_source':     'ai',
        }

    # ------------------------------------------------------------------
    # Point d'entree principal
    # ------------------------------------------------------------------

    def generate(self, description: str, force_new: bool = False) -> Dict[str, Any]:
        """
        Genere un produit depuis une description.

        Args:
            description : texte decrivant le produit
            force_new   : si True, ignore le JSON et genere toujours un nouveau produit

        Returns:
            Dictionnaire produit complet
        """
        if not force_new:
            results = self.search(description, max_results=1)
            if results and results[0]['score'] >= 50:
                best = results[0]
                name = best['item'].get('displayName', {}).get('dflt', {}).get('nameDef', '')
                print(f"Trouve dans le JSON (score {best['score']}) : {name}")
                return self._from_json(best['item'])

        print("Non trouve dans le JSON → generation par l'IA...")
        return self._new_product(description)


# ---------------------------------------------------------------------------
# Test rapide
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    gen = ProductGeneratorAI(r'c:\Users\mohamed taher\Downloads\3.json')

    tests = [
        'Milkshake fraise',
        'Pizza margherita avec mozzarella',
        'Frappe caramel',
        'Burger poulet croustillant',
        'Coca Cola 33cl',
    ]

    for desc in tests:
        print()
        print('=' * 60)
        print('Description :', desc)
        p = gen.generate(desc)
        name = p['displayName']['dflt']['nameDef']
        print(f"  Nom       : {name}")
        print(f"  Categorie : {p.get('category', p.get('title',''))}")
        print(f"  Prix      : {p['price']} EUR")
        print(f"  Allergenes: {p['allergens']}")
        print(f"  Source    : {p['_source']}")

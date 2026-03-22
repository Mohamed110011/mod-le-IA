"""
Script utilitaire pour générer des catégories sans passer par le menu principal.
Usage :
    python categories.py ["Description1" "Description2" ...]

Si aucun argument n'est fourni le script se met en mode interactif.
"""

import argparse
import sys
import json
import contextlib
import io
import os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import re
import base64
import requests
import urllib.parse
from PIL import Image, ImageDraw, ImageFont


IMAGE_DIR = r'd:/model-IA-image/generated_images'


def fetch_real_image(title: str) -> str:
    """Cherche une vraie image sur Openverse et la sauvegarde en WebP.
    Retourne le chemin local, ou '' si echec.
    """
    os.makedirs(IMAGE_DIR, exist_ok=True)
    safe = re.sub(r'[<>:"/\\|?*\s]', '_', title)
    headers = {'User-Agent': 'Mozilla/5.0'}

    query = urllib.parse.quote(f"{title} food")
    url = f"https://api.openverse.org/v1/images/?q={query}&page_size=10&license_type=commercial"

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            for item in results:
                img_url = item.get('url', '')
                if not img_url:
                    continue
                try:
                    dl = requests.get(img_url, headers=headers, timeout=15)
                    if dl.status_code == 200 and dl.headers.get('content-type', '').startswith('image'):
                        path = os.path.join(IMAGE_DIR, f"{safe}.webp")
                        img = Image.open(io.BytesIO(dl.content)).convert('RGB')
                        img = img.resize((800, 800), Image.LANCZOS)
                        img.save(path, 'WEBP', quality=85)
                        return path
                except Exception:
                    continue
    except Exception:
        pass
    return ''


def make_placeholder(title: str) -> str:
    """Cree une image placeholder PIL coloree."""
    os.makedirs(IMAGE_DIR, exist_ok=True)
    safe = re.sub(r'[<>:"/\\|?*\s]', '_', title)

    COLORS = {
        'PIZZA': '#FF6B35', 'MILKSHAKE': '#FFE66D', 'BOISSON': '#4ECDC4',
        'DESSERT': '#FF69B4', 'BURGER': '#D2691E', 'SALADE': '#90EE90',
        'MENU': '#9370DB', 'CAFE': '#C8956C',
    }
    color = next((v for k, v in COLORS.items() if k in title.upper()), '#AAAAAA')

    size = (800, 800)
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    m = 150
    draw.ellipse([m, m, size[0]-m, size[1]-m], fill='white', outline='#333333', width=6)
    try:
        font = ImageFont.truetype("arial.ttf", 52)
    except Exception:
        font = ImageFont.load_default()
    lines = title.split()
    y = size[1] // 2 - len(lines) * 32
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (size[0] - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill='#333333', font=font)
        y += (bbox[3] - bbox[1]) + 12

    path = os.path.join(IMAGE_DIR, f"{safe}_placeholder.webp")
    img.save(path, 'WEBP', quality=85)
    return path


def get_image(title: str) -> str:
    """Retourne le chemin d'une image reelle, sinon placeholder."""
    path = fetch_real_image(title)
    if path:
        print(f"  Image : {path}")
        return path
    path = make_placeholder(title)
    print(f"  Image : {path} (placeholder)")
    return path


def path_to_base64(path: str) -> str:
    """Convertit un fichier image en data URL base64."""
    if path and os.path.isfile(path):
        with open(path, 'rb') as f:
            return f"data:image/webp;base64,{base64.b64encode(f.read()).decode()}"
    return ''


def main():
    parser = argparse.ArgumentParser(description="Script utilitaire pour générer des catégories.")
    parser.add_argument('descriptions', nargs='*', help="Descriptions des catégories à générer")
    parser.add_argument('--json', action='store_true', help="Sortie au format JSON strict")

    args, unknown = parser.parse_known_args()

    if args.json:
        descriptions = args.descriptions
        if unknown:
            descriptions.extend(unknown)
        desc = descriptions[0] if descriptions else ""

        try:
            with contextlib.redirect_stdout(io.StringIO()):
                from category_generator_ai import CategoryGeneratorAI
                generator = CategoryGeneratorAI()
                cat = generator.generate_complete_category(desc)
                img_path = fetch_real_image(cat['title']) or make_placeholder(cat['title'])
                cat['imageUrl'] = path_to_base64(img_path)

            print(json.dumps(cat, ensure_ascii=False))
        except Exception as e:
            import traceback
            print(json.dumps({"error": str(e), "traceback": traceback.format_exc()}, ensure_ascii=False))
        return

    # Mode interactif / arguments
    from category_generator_ai import CategoryGeneratorAI
    generator = CategoryGeneratorAI()

    if len(sys.argv) > 1 and not any(a.startswith('-') for a in sys.argv[1:]):
        descriptions = sys.argv[1:]
    else:
        descriptions = []
        print("Mode interactif de generation de categories")
        print("  Saisissez une description puis Entree. Vide pour quitter.")
        while True:
            desc = input("Description : ").strip()
            if not desc:
                break
            descriptions.append(desc)

    if not descriptions:
        descriptions = ["Nos Pizzas Italiennes", "Boissons Fraiches", "Glace et Desserts"]

    for desc in descriptions:
        cat = generator.generate_complete_category(desc)
        img_path = get_image(cat['title'])
        cat['imageUrl'] = img_path
        cat['img']['dflt']['img'] = img_path

        print(f"\n--- Categorie : {desc} ---")
        print(f"  ID     : {cat['id']}")
        print(f"  Titre  : {cat['title']}")
        print(f"  Nom    : {cat.get('displayName',{}).get('dflt',{}).get('nameDef','')}")
        print(f"  Couleur: {cat['color']}")
        print(f"  Image  : {img_path}")
        print(json.dumps(cat, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

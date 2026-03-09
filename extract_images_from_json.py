#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extraction des URLs d'images depuis le fichier JSON
"""

import json
import re
from typing import List, Dict
import requests
import os
from pathlib import Path


class ImageExtractor:
    """Extrait et télécharge les images depuis le JSON"""
    
    def __init__(self, json_path: str, output_dir: str = "d:/model-IA-image/images_from_json"):
        self.json_path = json_path
        self.output_dir = output_dir
        self.data = None
        self.image_urls = []
        
        # Créer le dossier de sortie
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def load_data(self):
        """Charge le fichier JSON"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Compter les éléments
        items_count = len(self.data.get('items', {}))
        cat_count = len(self.data.get('cat', {}))
        
        print(f"✅ Données chargées : {items_count} produits, {cat_count} catégories")
        return self.data
    
    def extract_image_urls(self) -> List[Dict[str, str]]:
        """Extrait toutes les URLs d'images du JSON"""
        if not self.data:
            self.load_data()
        
        image_info = []
        
        # Extraire les images des items (produits)
        items = self.data.get('items', {})
        if isinstance(items, dict):
            for item_id, item_data in items.items():
                if not isinstance(item_data, dict):
                    continue
                
                # Récupérer le nom du produit
                display_name = item_data.get('displayName', {})
                if isinstance(display_name, dict) and 'dflt' in display_name:
                    product_name = display_name['dflt'].get('nameDef', 'Unknown')
                else:
                    product_name = item_data.get('title', 'Unknown')
                
                # Extraire l'image du produit
                img_data = item_data.get('img', {})
                if isinstance(img_data, dict):
                    dflt_img = img_data.get('dflt', {})
                    if isinstance(dflt_img, dict):
                        img_url = dflt_img.get('img', '')
                        if img_url and 'no-pictures' not in img_url:
                            image_info.append({
                                'item_id': item_id,
                                'product_name': product_name,
                                'url': img_url,
                                'type': 'product',
                                'ref': item_data.get('ref', ''),
                                'price': item_data.get('price', {}).get('dflt', 0)
                            })
        
        # Extraire les images des catégories
        categories = self.data.get('cat', {})
        if isinstance(categories, dict):
            for cat_id, cat_data in categories.items():
                if not isinstance(cat_data, dict):
                    continue
                
                category_title = cat_data.get('title', 'Unknown')
                
                # Extraire les images de la catégorie
                img_data = cat_data.get('img', {})
                if isinstance(img_data, dict):
                    dflt_img = img_data.get('dflt', {})
                    if isinstance(dflt_img, dict):
                        img_url = dflt_img.get('img', '')
                        if img_url and 'no-pictures' not in img_url:
                            image_info.append({
                                'category_id': cat_id,
                                'category_title': category_title,
                                'url': img_url,
                                'type': 'category'
                            })
                
                # Extraire les vidéos/images alternatives
                video_data = cat_data.get('video', {})
                if isinstance(video_data, dict):
                    video_url = video_data.get('url', '')
                    if video_url and video_url.strip() and 'no-pictures' not in video_url:
                        image_info.append({
                            'category_id': cat_id,
                            'category_title': category_title,
                            'url': video_url,
                            'type': 'category_banner'
                        })
        
        self.image_urls = image_info
        print(f"✅ {len(image_info)} URLs d'images trouvées")
        return image_info
    
    def display_image_summary(self):
        """Affiche un résumé des images trouvées"""
        if not self.image_urls:
            self.extract_image_urls()
        
        print("\n" + "=" * 70)
        print("📸 RÉSUMÉ DES IMAGES DANS LE JSON")
        print("=" * 70)
        
        # Compter par domaine
        domains = {}
        for img in self.image_urls:
            url = img['url']
            if url.startswith('http'):
                domain = url.split('/')[2]
            else:
                domain = 'local/relative'
            domains[domain] = domains.get(domain, 0) + 1
        
        print(f"\n📊 Total: {len(self.image_urls)} images")
        print(f"\n🌐 Par domaine:")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {domain}: {count} images")
        
        print(f"\n📋 Premiers exemples:")
        for i, img in enumerate(self.image_urls[:10], 1):
            if img['type'] == 'product':
                name = img['product_name']
                ref = img.get('ref', '')
                price = img.get('price', 0)
                print(f"   {i}. [Produit] {name} ({ref}) - {price}€")
            else:
                name = img.get('category_title', 'Unknown')
                print(f"   {i}. [Catégorie] {name}")
            print(f"      URL: {img['url'][:70]}...")
        
        if len(self.image_urls) > 10:
            print(f"   ... et {len(self.image_urls) - 10} autres")
        
        print("\n" + "=" * 70)
    
    def download_image(self, url: str, filename: str) -> bool:
        """Télécharge une image depuis une URL"""
        try:
            # Si c'est une URL relative ou locale, chercher dans un dossier
            if not url.startswith('http'):
                print(f"   ⚠️  URL relative/locale ignorée: {url}")
                return False
            
            response = requests.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            return False
    
    def download_all_images(self, max_downloads: int = None):
        """Télécharge toutes les images"""
        if not self.image_urls:
            self.extract_image_urls()
        
        print("\n" + "=" * 70)
        print("⬇️  TÉLÉCHARGEMENT DES IMAGES")
        print("=" * 70)
        
        images_to_download = self.image_urls[:max_downloads] if max_downloads else self.image_urls
        success_count = 0
        fail_count = 0
        
        for i, img in enumerate(images_to_download, 1):
            url = img['url']
            
            # Générer un nom de fichier propre
            if img['type'] == 'product':
                name = img['product_name']
                ref = img.get('ref', str(i))
                filename = f"{ref}_{name.replace(' ', '_')}.webp"
            else:
                name = img.get('category_title', f'image_{i}')
                filename = f"cat_{name.replace(' ', '_')}.webp"
            
            # Nettoyer le nom de fichier
            filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
            
            print(f"\n[{i}/{len(images_to_download)}] {name}")
            print(f"   📥 {url[:60]}...")
            
            if self.download_image(url, filename):
                print(f"   ✅ Sauvegardé: {filename}")
                success_count += 1
            else:
                fail_count += 1
        
        print("\n" + "=" * 70)
        print(f"✅ Téléchargement terminé: {success_count} réussis, {fail_count} échecs")
        print(f"📁 Dossier: {self.output_dir}")
        print("=" * 70)
    
    def export_image_list(self, output_file: str = "d:/model-IA-image/image_urls.json"):
        """Exporte la liste des URLs d'images en JSON"""
        if not self.image_urls:
            self.extract_image_urls()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.image_urls, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Liste exportée: {output_file}")


def main():
    """Fonction principale"""
    print("\n" + "=" * 70)
    print("🖼️  EXTRACTEUR D'IMAGES DEPUIS JSON")
    print("=" * 70)
    
    # Créer l'extracteur
    extractor = ImageExtractor(r"c:\Users\mohamed taher\Downloads\3.json")
    
    # Extraire et afficher les URLs
    extractor.extract_image_urls()
    extractor.display_image_summary()
    
    # Menu interactif
    print("\n📋 Options:")
    print("1. Télécharger toutes les images")
    print("2. Télécharger les 10 premières images (test)")
    print("3. Exporter la liste en JSON")
    print("4. Quitter sans télécharger")
    
    choice = input("\nVotre choix (1-4): ").strip()
    
    if choice == '1':
        print("\n⚠️  Attention: Cela peut prendre du temps...")
        confirm = input("Confirmer le téléchargement de toutes les images ? (oui/non): ")
        if confirm.lower() in ['oui', 'o', 'yes', 'y']:
            extractor.download_all_images()
    elif choice == '2':
        extractor.download_all_images(max_downloads=10)
    elif choice == '3':
        extractor.export_image_list()
    else:
        print("\n✅ Terminé sans téléchargement")
    
    print("\n🎉 Extraction terminée !\n")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print("\n❌ ERREUR: Fichier JSON introuvable")
        print("📍 Chemin attendu: c:\\Users\\mohamed taher\\Downloads\\3.json\n")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur\n")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}\n")

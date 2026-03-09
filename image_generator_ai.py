"""
Module de génération d'images avec IA
Intégration avec Stable Diffusion, DALL-E, simulation ou extraction depuis JSON
"""

import os
import requests
from typing import Optional, Dict, Any, List
from PIL import Image, ImageDraw, ImageFont
import io
import json
import re
import unicodedata


class ImageGeneratorAI:
    """
    Générateur d'images pour les produits
    Supporte plusieurs backends : Stable Diffusion, DALL-E, génération locale, ou extraction depuis JSON
    """
    
    def __init__(self, api_key: Optional[str] = None, backend: str = 'placeholder', json_path: Optional[str] = None):
        """
        Args:
            api_key: Clé API pour les services externes (OpenAI, Stability AI, etc.)
            backend: 'dall-e', 'stable-diffusion', 'placeholder', 'replicate', 'from_json'
            json_path: Chemin vers le fichier JSON contenant les images (requis si backend='from_json')
        """
        self.api_key = api_key
        self.backend = backend
        self.output_dir = 'd:/model-IA-image/generated_images'
        self.json_path = json_path
        self.json_data = None
        self.image_cache = {}  # Cache des URLs d'images par nom de produit
        
        # Créer le dossier de sortie
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Charger les images du JSON si backend = 'from_json'
        if self.backend == 'from_json' and self.json_path:
            self._load_images_from_json()
    
    def generate_image(self, 
                      description: str, 
                      product_name: str,
                      category: str,
                      size: tuple = (800, 800)) -> str:
        """
        Génère une image basée sur la description du produit
        
        Args:
            description: Description du produit
            product_name: Nom du produit
            category: Catégorie du produit
            size: Taille de l'image (width, height)
        
        Returns:
            Chemin vers l'image générée
        """
        if self.backend == 'dall-e':
            return self._generate_with_dalle(description, product_name)
        elif self.backend == 'stable-diffusion':
            return self._generate_with_stable_diffusion(description, product_name)
        elif self.backend == 'replicate':
            return self._generate_with_replicate(description, product_name)
        elif self.backend == 'huggingface':
            return self._generate_with_huggingface(description, product_name)
        elif self.backend == 'hybrid_free':
            return self._generate_hybrid_free(product_name, description, category, size)
        elif self.backend == 'from_json':
            return self._get_image_from_json(product_name, description, category, size)
        else:
            return self._generate_placeholder(product_name, category, size)
    
    def _load_images_from_json(self):
        """Charge les URLs d'images depuis le JSON"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)
            
            # Indexer les images par nom de produit
            items = self.json_data.get('items', {})
            for item_id, item_data in items.items():
                if not isinstance(item_data, dict):
                    continue
                
                # Récupérer le nom du produit
                display_name = item_data.get('displayName', {})
                if isinstance(display_name, dict) and 'dflt' in display_name:
                    product_name = display_name['dflt'].get('nameDef', '').strip()
                else:
                    product_name = item_data.get('title', '').strip()
                
                if not product_name:
                    continue
                
                # Extraire l'URL de l'image
                img_data = item_data.get('img', {})
                if isinstance(img_data, dict):
                    dflt_img = img_data.get('dflt', {})
                    if isinstance(dflt_img, dict):
                        img_url = dflt_img.get('img', '')
                        if img_url and 'no-pictures' not in img_url:
                            # Normaliser le nom pour la recherche
                            norm_name = product_name.lower().strip()
                            self.image_cache[norm_name] = {
                                'url': img_url,
                                'original_name': product_name,
                                'ref': item_data.get('ref', ''),
                                'item_id': item_id
                            }
            
            print(f"✅ {len(self.image_cache)} images chargées depuis le JSON")
        
        except Exception as e:
            print(f"⚠️  Erreur lors du chargement des images depuis le JSON: {e}")
            self.image_cache = {}
    
    def _remove_accents(self, text: str) -> str:
        """Enlève les accents d'une chaîne de caractères"""
        nfd = unicodedata.normalize('NFD', text)
        return ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')
    
    def _find_image_url(self, product_name: str, description: str = '') -> Optional[str]:
        """Trouve l'URL d'une image correspondant au produit
        
        Recherche par :
        1. Correspondance exacte du nom (sans accents)
        2. Correspondance partielle avec scoring intelligent
        3. Mots-clés dans la description (prioritaires)
        4. Marques et ingrédients spécifiques (priorité maximale)
        """
        if not self.image_cache:
            return None
        
        # Mots de marque (TRÈS haute priorité)
        brand_words = {
            'fanta', 'coca', 'cola', 'pepsi', 'sprite', 'orangina', 'schweppes', 
            'evian', 'vittel', 'perrier', 'oasis', 'tropicana', 'minute', 'maid',
            'lipton', 'nestea', 'redbull', 'monster', '7up'
        }
        
        # Mots de combo/menu à pénaliser quand non recherchés
        combo_words = {'menu', 'combo', 'formule', 'pack', 'box', 'coffret'}
        
        # Normaliser (minuscules + sans accents)
        search_name_norm = self._remove_accents(product_name.lower().strip())
        search_words = set(search_name_norm.split())
        
        # Ajouter aussi les mots de la description (priorité haute)
        desc_words = set()
        if description:
            desc_norm = self._remove_accents(description.lower().strip())
            desc_words = set(desc_norm.split())
            # Mots importants (ingrédients, types)
            important_words = desc_words - {'pizza', 'avec', 'et', 'de', 'la', 'le', 'un', 'une', 'burger', 'sandwich'}
        else:
            important_words = set()
        
        # Détecter les marques recherchées
        searched_brands = search_words.intersection(brand_words)
        searched_brands.update(desc_words.intersection(brand_words))
        is_combo_search = bool(search_words.intersection(combo_words))
        
        # 1. Recherche exacte (sans accents)
        for cached_name, img_info in self.image_cache.items():
            cached_norm = self._remove_accents(cached_name)
            if search_name_norm == cached_norm:
                print(f"   ✅ Correspondance exacte trouvée: {img_info['original_name']}")
                return img_info['url']
        
        # 2. Recherche avec scoring avancé
        best_match = None
        best_score = 0
        best_name = ""
        
        for cached_name, img_info in self.image_cache.items():
            cached_norm = self._remove_accents(cached_name)
            cached_words = set(cached_norm.split())
            
            score = 0
            
            # PRIORITÉ MAXIMALE: Correspondance de marque (+100 par marque)
            brand_matches = searched_brands.intersection(cached_words)
            if brand_matches:
                score += len(brand_matches) * 100
                print(f"   🎯 '{img_info['original_name']}' a les marques: {brand_matches} (score +{len(brand_matches)*100})")
            
            # PÉNALITÉ: Combo/menu non recherché (-50)
            cached_combos = cached_words.intersection(combo_words)
            if cached_combos and not is_combo_search:
                score -= 50
                print(f"   ⚠️  '{img_info['original_name']}' est un combo non recherché: {cached_combos} (score -50)")
            
            # Mots importants de la description (PRIORITÉ HAUTE)
            important_common = important_words.intersection(cached_words)
            if important_common:
                score += len(important_common) * 50
                print(f"   🎯 '{img_info['original_name']}' a les mots importants: {important_common} (score +{len(important_common)*50})")
            
            # Mots communs du nom
            common_words = search_words.intersection(cached_words)
            score += len(common_words) * 10
            
            # Mots communs de toute la description
            if desc_words:
                desc_common = desc_words.intersection(cached_words)
                score += len(desc_common) * 15
            
            # Bonus si le nom de recherche est contenu
            if search_name_norm in cached_norm:
                score += 30
            if cached_norm in search_name_norm:
                score += 30
            
            # Correspondance partielle de mots
            for search_word in search_words:
                if len(search_word) > 3:  # Éviter les mots trop courts
                    for cached_word in cached_words:
                        if search_word in cached_word or cached_word in search_word:
                            score += 5
            
            if score > best_score:
                best_score = score
                best_match = img_info['url']
                best_name = img_info['original_name']
        
        if best_score > 0:
            print(f"   ✅ Meilleure correspondance: '{best_name}' (score: {best_score})")
            return best_match
        
        print(f"   ❌ Aucune correspondance trouvée dans le cache ({len(self.image_cache)} images)")
        return None
    
    def _get_image_from_json(self, product_name: str, description: str, category: str, size: tuple) -> str:
        """Récupère et télécharge une image depuis le JSON"""
        print(f"   🔍 Recherche image pour '{product_name}' (description: '{description}')")
        
        # Trouver l'URL de l'image
        img_url = self._find_image_url(product_name, description)
        
        if not img_url:
            print(f"   ⚠️  Aucune image trouvée dans le JSON, génération placeholder")
            return self._generate_placeholder(product_name, category, size)
        
        try:
            # Télécharger l'image
            print(f"   📥 Téléchargement depuis: {img_url[:70]}...")
            response = requests.get(img_url, timeout=15)
            response.raise_for_status()
            
            # Sauvegarder l'image
            filename = f"{product_name.replace(' ', '_')}_from_json.webp"
            filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"   ✅ Image téléchargée: {filename}")
            return filepath
        
        except Exception as e:
            print(f"   ❌ Erreur lors du téléchargement: {e}")
            print(f"   → Génération d'un placeholder à la place")
            return self._generate_placeholder(product_name, category, size)
    
    def _generate_with_dalle(self, description: str, product_name: str) -> str:
        """Génère une image avec DALL-E (OpenAI)"""
        if not self.api_key:
            raise ValueError("API key requise pour DALL-E")
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            # Créer un prompt optimisé
            prompt = self._create_realistic_prompt(description, product_name, style='dalle')
            
            print(f"   🎨 Génération DALL-E avec prompt: {prompt[:100]}...")
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="hd",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Télécharger l'image
            print(f"   📥 Téléchargement de l'image DALL-E...")
            image_path = self._download_image(image_url, product_name, suffix="_dalle")
            print(f"   ✅ Image DALL-E générée: {image_path}")
            return image_path
            
        except Exception as e:
            print(f"   ❌ Erreur DALL-E : {e}")
            print(f"   → Génération d'un placeholder à la place")
            return self._generate_placeholder(product_name, "ERROR")
    
    def _generate_with_stable_diffusion(self, description: str, product_name: str) -> str:
        """Génère une image avec Stable Diffusion"""
        if not self.api_key:
            raise ValueError("API key requise pour Stable Diffusion")
        
        try:
            # Utiliser l'API Stability AI
            prompt = self._create_sd_prompt(description, product_name)
            
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "text_prompts": [
                        {
                            "text": prompt,
                            "weight": 1
                        }
                    ],
                    "cfg_scale": 7,
                    "height": 1024,
                    "width": 1024,
                    "samples": 1,
                    "steps": 30,
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                # Sauvegarder l'image
                image_data = data['artifacts'][0]['base64']
                image_path = os.path.join(self.output_dir, f"{product_name.replace(' ', '_')}.webp")
                
                import base64
                with open(image_path, 'wb') as f:
                    f.write(base64.b64decode(image_data))
                
                return image_path
            else:
                raise Exception(f"Erreur API: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur Stable Diffusion : {e}")
            return self._generate_placeholder(product_name, "ERROR")
    
    def _generate_with_replicate(self, description: str, product_name: str) -> str:
        """Génère une image avec Replicate API (Stable Diffusion gratuit)"""
        try:
            import replicate
            
            if self.api_key:
                os.environ["REPLICATE_API_TOKEN"] = self.api_key
            
            prompt = self._create_sd_prompt(description, product_name)
            
            output = replicate.run(
                "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                input={"prompt": prompt}
            )
            
            # Télécharger l'image
            if output and len(output) > 0:
                image_url = output[0]
                image_path = self._download_image(image_url, product_name)
                return image_path
            
        except Exception as e:
            print(f"❌ Erreur Replicate : {e}")
        
        return self._generate_placeholder(product_name, "ERROR")
    
    def _generate_with_huggingface(self, description: str, product_name: str) -> str:
        """Génère une image GRATUITEMENT avec plusieurs APIs gratuites
        
        Essaie dans l'ordre :
        1. Pollinations.AI (le plus fiable, sans limite)
        2. Hugging Face Inference API (backup)
        
        Avantages :
        - 100% GRATUIT (pas de clé API nécessaire)
        - Bonne qualité (Stable Diffusion)
        - Aucune limite de coût
        - Très fiable (plusieurs APIs de fallback)
        
        Limitations :
        - Temps de génération : 3-8 secondes
        """
        # Essayer d'abord Pollinations.AI (le plus fiable et rapide)
        try:
            result = self._generate_with_pollinations(description, product_name)
            if result and 'placeholder' not in result:
                return result
        except Exception as e:
            print(f"⚠️  Pollinations échoué, essai avec Hugging Face...")
        
        # Fallback sur Hugging Face
        return self._generate_with_huggingface_inference(description, product_name)
    
    def _generate_with_pollinations(self, description: str, product_name: str) -> str:
        """Génère avec Pollinations.AI - API GRATUITE et SANS LIMITE
        
        Pollinations.AI est un service gratuit qui génère des images via Stable Diffusion
        Sans authentification, sans rate limit, très fiable
        """
        try:
            prompt = self._create_realistic_prompt(description, product_name, style='sd')
            
            # API Pollinations.AI (complètement gratuit)
            # Simple URL avec le prompt encodé
            import urllib.parse
            encoded_prompt = urllib.parse.quote(prompt)
            api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            
            print(f"🎨 Génération gratuite avec Pollinations.AI...")
            
            response = requests.get(api_url, timeout=30)
            
            if response.status_code == 200:
                # Sauvegarder l'image
                image = Image.open(io.BytesIO(response.content))
                
                # Convertir en WebP
                safe_name = self._safe_filename(product_name)
                filename = f"{safe_name}_free.webp"
                filepath = os.path.join(self.output_dir, filename)
                
                image.save(filepath, 'WEBP', quality=85)
                print(f"✅ Image gratuite générée : {filename}")
                return filepath
            else:
                print(f"⚠️  Pollinations API erreur : {response.status_code}")
        
        except Exception as e:
            print(f"⚠️  Erreur Pollinations : {e}")
        
        return None
    
    def _generate_with_huggingface_inference(self, description: str, product_name: str) -> str:
        """Génère avec Hugging Face Inference API (fallback)"""
        try:
            # Créer un prompt réaliste
            prompt = self._create_realistic_prompt(description, product_name, style='sd')
            
            # Liste de modèles gratuits à essayer (par ordre de préférence)
            models = [
                "runwayml/stable-diffusion-v1-5",  # Le plus populaire et stable
                "CompVis/stable-diffusion-v1-4",   # Alternative stable
                "prompthero/openjourney-v4",       # Bonne qualité artistique
            ]
            
            headers = {}
            # Si une clé HF est fournie, l'utiliser (optionnel, augmente les limites)
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 30,
                    "guidance_scale": 7.5,
                }
            }
            
            print(f"🎨 Génération gratuite avec Hugging Face...")
            
            response = None
            # Essayer chaque modèle jusqu'à ce qu'un fonctionne
            for model in models:
                api_url = f"https://api-inference.huggingface.co/models/{model}"
                try:
                    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
                    if response.status_code == 200:
                        print(f"✅ Modèle utilisé : {model}")
                        break
                    elif response.status_code == 503:
                        print(f"⏳ {model} en chargement, essai suivant...")
                        continue
                except:
                    continue
            
            if not response:
                print("❌ Aucun modèle disponible")
                return self._generate_placeholder(product_name, "ERROR")
            
            if response.status_code == 200:
                # Sauvegarder l'image
                image = Image.open(io.BytesIO(response.content))
                
                # Convertir en WebP
                safe_name = self._safe_filename(product_name)
                filename = f"{safe_name}_huggingface.webp"
                filepath = os.path.join(self.output_dir, filename)
                
                image.save(filepath, 'WEBP', quality=85)
                print(f"✅ Image gratuite générée : {filename}")
                return filepath
            
            print(f"⚠️  Tous les modèles ont échoué (status: {response.status_code})")
            if response.status_code == 429:
                print("   Rate limit atteint. Attendez quelques minutes ou utilisez 'hybrid_free'")
            
        except Exception as e:
            print(f"❌ Erreur Hugging Face : {e}")
        
        return self._generate_placeholder(product_name, "ERROR")
    
    def _generate_hybrid_free(self, product_name: str, description: str, category: str, size: tuple) -> str:
        """Mode hybride GRATUIT : essaie JSON d'abord, puis placeholder amélioré
        
        Stratégie optimale 100% GRATUITE :
        1. Cherche dans les 780 images du JSON (gratuit, instantané, qualité ⭐⭐⭐⭐⭐)
        2. Si non trouvé, génère un placeholder coloré (gratuit, instantané, qualité ⭐⭐)
        
        Avantages :
        - 100% GRATUIT
        - 100% FIABLE (aucune dépendance externe)
        - RAPIDE (toujours instantané)
        - Toujours fonctionnel
        """
        # Essayer d'abord le JSON
        if self.json_path and self.image_cache:
            print(f"🔍 Recherche dans le JSON (780 images)...")
            image_path = self._get_image_from_json(product_name, description, category, size)
            
            # Si trouvé dans le JSON (pas un placeholder)
            if image_path and 'placeholder' not in image_path:
                print(f"✅ Image trouvée dans le JSON !")
                return image_path
            
            print(f"ℹ️  Produit non trouvé dans le JSON")
        
        # Si pas trouvé, générer un placeholder coloré (instantané, gratuit)
        print(f"🎨 Génération d'un placeholder coloré...")
        return self._generate_placeholder(product_name, category, size)
    
    def _create_realistic_prompt(self, description: str, product_name: str, style: str = 'dalle') -> str:
        """Crée un prompt ultra-réaliste optimisé pour la génération IA
        
        Args:
            description: Description du produit
            product_name: Nom du produit
            style: 'dalle' ou 'sd' pour adapter le style
        """
        # Nettoyer et analyser la description
        desc_lower = description.lower()
        
        # Détecter le type de produit
        product_type = self._detect_product_type(product_name, description)
        
        # Templates spécifiques par type
        if product_type == 'pizza':
            base_prompt = f"""Ultra realistic professional food photography of a delicious {product_name}. 
{description}. Fresh ingredients, melted cheese, crispy crust, 
studio lighting, white marble surface, appetizing steam rising, 
high-end restaurant presentation, 8K resolution, sharp focus, 
commercial photography, mouthwatering details"""
        
        elif product_type == 'burger':
            base_prompt = f"""Premium professional food photography of {product_name}. 
{description}. Juicy patty, fresh vegetables, golden bun, 
studio lighting, wooden board presentation, gourmet burger style, 
hyper-realistic details, 8K quality, appetizing composition, 
commercial product shot"""
        
        elif product_type == 'milkshake' or product_type == 'boisson':
            base_prompt = f"""Professional beverage photography of {product_name}. 
{description}. Tall glass, cold condensation droplets, 
white background, studio lighting, vibrant colors, 
fresh ingredients visible, commercial drink photography, 
8K resolution, instagram-worthy presentation"""
        
        elif product_type == 'dessert':
            base_prompt = f"""Elegant food photography of {product_name}. 
{description}. Beautiful plating, white porcelain plate, 
studio lighting, artistic presentation, luxury dessert style, 
hyper-realistic textures, 8K quality, commercial patisserie photo"""
        
        elif product_type == 'sandwich' or product_type == 'wrap':
            base_prompt = f"""Fresh food photography of {product_name}. 
{description}. Layered ingredients visible, fresh vegetables, 
wooden cutting board, natural lighting, healthy and appetizing, 
commercial sandwich photography, 8K resolution, detailed textures"""
        
        else:
            # Template générique mais professionnel
            base_prompt = f"""Professional high-quality food photography of {product_name}. 
{description}. Studio lighting, clean presentation, 
appetizing and fresh, commercial product photography, 
8K resolution, detailed and vibrant, restaurant quality"""
        
        # Ajouter des mots-clés négatifs pour Stable Diffusion
        if style == 'sd':
            base_prompt += "\nNegative prompt: blurry, low quality, cartoon, illustration, drawing, painting, unrealistic, distorted"
        
        return base_prompt
    
    def _detect_product_type(self, product_name: str, description: str) -> str:
        """Détecte le type de produit pour adapter le prompt"""
        text = (product_name + " " + description).lower()
        
        if any(word in text for word in ['pizza', 'margherita', 'calzone']):
            return 'pizza'
        elif any(word in text for word in ['burger', 'hamburger', 'cheeseburger']):
            return 'burger'
        elif any(word in text for word in ['milkshake', 'smoothie', 'frappe', 'shake']):
            return 'milkshake'
        elif any(word in text for word in ['coca', 'sprite', 'fanta', 'boisson', 'jus', 'soda']):
            return 'boisson'
        elif any(word in text for word in ['tiramisu', 'brownie', 'cookie', 'gateau', 'tarte', 'dessert']):
            return 'dessert'
        elif any(word in text for word in ['sandwich', 'panini', 'wrap', 'tacos']):
            return 'sandwich'
        elif any(word in text for word in ['nuggets', 'tenders', 'wings', 'frites', 'chicken']):
            return 'finger_food'
        elif any(word in text for word in ['salade', 'salad']):
            return 'salade'
        else:
            return 'generic'
    
    def _create_dalle_prompt(self, description: str, product_name: str) -> str:
        """Crée un prompt optimisé pour DALL-E (legacy)"""
        return self._create_realistic_prompt(description, product_name, style='dalle')
    
    def _create_sd_prompt(self, description: str, product_name: str) -> str:
        """Crée un prompt optimisé pour Stable Diffusion"""
        return self._create_realistic_prompt(description, product_name, style='sd')
    
    def _download_image(self, url: str, product_name: str, suffix: str = "") -> str:
        """Télécharge une image depuis une URL"""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                filename = f"{product_name.replace(' ', '_')}{suffix}.webp"
                filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
                image_path = os.path.join(self.output_dir, filename)
                
                # Convertir en WebP pour optimiser la taille
                img = Image.open(io.BytesIO(response.content))
                img.save(image_path, 'WEBP', quality=90)
                
                return image_path
        except Exception as e:
            print(f"   ❌ Erreur téléchargement : {e}")
        
        return self._generate_placeholder(product_name, "ERROR")
    
    def _generate_placeholder(self, product_name: str, category: str, size: tuple = (800, 800)) -> str:
        """Génère une image placeholder locale"""
        # Créer une image de base
        img = Image.new('RGB', size, color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Couleurs par catégorie
        category_colors = {
            'PIZZAS': '#FF6B35',
            'BOISSONS': '#4ECDC4',
            'MILKSHAKE': '#FFE66D',
            'DESSERTS': '#FF69B4',
            'FINGER FOOD': '#FFA500',
            'SALADES': '#90EE90',
            'MENU': '#9370DB',
            'ERROR': '#CCCCCC'
        }
        
        bg_color = category_colors.get(category, '#CCCCCC')
        
        # Dessiner un fond coloré
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Ajouter un cercle central
        circle_size = min(size) // 2
        circle_bbox = [
            (size[0] - circle_size) // 2,
            (size[1] - circle_size) // 2,
            (size[0] + circle_size) // 2,
            (size[1] + circle_size) // 2
        ]
        draw.ellipse(circle_bbox, fill='white', outline='#333333', width=5)
        
        # Ajouter le texte (nom du produit)
        try:
            # Essayer d'utiliser une police système
            font_size = 40
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Centrer le texte
        text_lines = product_name.split(' ')
        y_offset = size[1] // 2 - (len(text_lines) * 25)
        
        for line in text_lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size[0] - text_width) // 2
            draw.text((x, y_offset), line, fill='#333333', font=font)
            y_offset += text_height + 10
        
        # Ajouter le nom de la catégorie en bas
        category_text = f"[{category}]"
        try:
            small_font = ImageFont.truetype("arial.ttf", 20)
        except:
            small_font = font
        
        bbox = draw.textbbox((0, 0), category_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2
        y = size[1] - 60
        draw.text((x, y), category_text, fill='#666666', font=small_font)
        
        # Sauvegarder
        image_path = os.path.join(
            self.output_dir,
            f"{product_name.replace(' ', '_')}_placeholder.webp"
        )
        img.save(image_path, 'WEBP', quality=85)
        
        return image_path
    
    def generate_batch(self, products: list) -> Dict[str, str]:
        """
        Génère des images pour une liste de produits
        
        Args:
            products: Liste de dictionnaires de produits
        
        Returns:
            Dictionnaire {product_id: image_path}
        """
        results = {}
        
        for i, product in enumerate(products, 1):
            print(f"🖼️  Génération image {i}/{len(products)} : {product.get('displayName', {}).get('dflt', {}).get('nameDef', 'Unknown')}")
            
            try:
                image_path = self.generate_image(
                    description=product.get('description', {}).get('dflt', {}).get('nameDef', ''),
                    product_name=product.get('displayName', {}).get('dflt', {}).get('nameDef', 'Unknown'),
                    category=product.get('category', 'AUTRES')
                )
                
                results[product['id']] = image_path
                print(f"   ✅ Image sauvegardée : {image_path}")
                
            except Exception as e:
                print(f"   ❌ Erreur : {e}")
                results[product['id']] = None
        
        return results


# Test du générateur d'images
if __name__ == "__main__":
    print("🎨 MODULE DE GÉNÉRATION D'IMAGES\n")
    
    # Initialiser le générateur (mode placeholder pour la démo)
    generator = ImageGeneratorAI(backend='placeholder')
    
    # Tests
    test_products = [
        {
            "id": "test-1",
            "displayName": {"dflt": {"nameDef": "Pizza Margherita"}},
            "description": {"dflt": {"nameDef": "Pizza classique avec mozzarella"}},
            "category": "PIZZAS"
        },
        {
            "id": "test-2",
            "displayName": {"dflt": {"nameDef": "Milkshake Chocolat"}},
            "description": {"dflt": {"nameDef": "Milkshake crémeux au chocolat"}},
            "category": "MILKSHAKE"
        },
        {
            "id": "test-3",
            "displayName": {"dflt": {"nameDef": "Chicken Nuggets"}},
            "description": {"dflt": {"nameDef": "Nuggets de poulet croustillants"}},
            "category": "FINGER FOOD"
        }
    ]
    
    print("📝 Génération des images pour les produits de test...\n")
    results = generator.generate_batch(test_products)
    
    print("\n✅ RÉSULTATS :")
    for product_id, image_path in results.items():
        print(f"   {product_id}: {image_path}")
    
    print(f"\n📁 Images sauvegardées dans : {generator.output_dir}")

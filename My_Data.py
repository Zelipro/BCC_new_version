import requests
import json
import hashlib
from typing import List, Dict, Optional, Any, Union
from datetime import datetime
import time

class SupabaseDB:
    """
    Classe Supabase corrigée avec gestion d'erreurs améliorée
    """
    
    def __init__(self, 
                 supabase_url: str = "https://jutueskohextubwszbhv.supabase.co", 
                 supabase_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dHVlc2tvaGV4dHVid3N6Ymh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxMTQ5MDUsImV4cCI6MjA3MzY5MDkwNX0.q3uKtQ3EKdpv4MDuJE0pCrBOBdCbMf9pu36RmoDNGKw"):
        """
        Initialise la connexion Supabase avec la bonne clé
        """
        self.supabase_url = supabase_url.rstrip('/')
        self.supabase_key = supabase_key
        
        # Headers pour Supabase REST API
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        
        # Test de connexion au démarrage
        self.connection_status = self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test de connexion à Supabase"""
        try:
            url = f"{self.supabase_url}/rest/v1/"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.status_code in [200, 404]  # 404 est normal pour la racine
        except Exception as e:
            print(f"Erreur de connexion Supabase: {e}")
            return False
    
    def _build_url(self, collection: str) -> str:
        return f"{self.supabase_url}/rest/v1/{collection}"
    
    def _convert_to_strings(self, data: Union[List[str], Dict[str, str]]) -> Dict[str, str]:
        """Convertit les données en dictionnaire avec des chaînes de caractères"""
        if isinstance(data, list):
            return {str(i): str(value) for i, value in enumerate(data)}
        elif isinstance(data, dict):
            return {str(key): str(value) for key, value in data.items()}
        else:
            raise ValueError("Les données doivent être une liste ou un dictionnaire")
    
    def _generate_hash(self, data: Dict[str, str]) -> str:
        """Génère un hash pour les données"""
        hash_string = json.dumps(data, sort_keys=True)
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def ajouter_donnees(self, collection: str, data: Union[List[str], Dict[str, str]]) -> Dict[str, Any]:
        """
        Ajoute des données à une table Supabase avec retry
        """
        if not self.connection_status:
            return {
                'success': False, 
                'error': 'Pas de connexion internet ou Supabase inaccessible',
                'message': 'Vérifiez votre connexion internet'
            }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Convertir en strings
                string_data = self._convert_to_strings(data)
                
                # Préparer les données pour Supabase
                supabase_data = {
                    'date': string_data.get('0', ''),
                    'heur': string_data.get('1', ''), 
                    'operator': string_data.get('2', ''),
                    'o_f_dd': string_data.get('3', ''),
                    'operation': string_data.get('4', ''),
                    'mension': string_data.get('5', ''),
                    'hash_signature': self._generate_hash(string_data),
                    'device_info': 'CEET-BCC-Mobile',
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                
                url = self._build_url(collection)
                response = requests.post(url, json=supabase_data, headers=self.headers, timeout=30)
                
                if response.status_code == 201:
                    result_data = response.json()[0] if response.json() else {}
                    return {
                        'success': True, 
                        'data': result_data,
                        'message': 'Données ajoutées avec succès'
                    }
                elif response.status_code == 409:  # Conflit - données déjà existantes
                    return {
                        'success': False, 
                        'error': 'Données déjà existantes',
                        'message': 'Ces données existent déjà'
                    }
                else:
                    if attempt == max_retries - 1:  # Dernier essai
                        return {
                            'success': False, 
                            'error': f'Erreur HTTP {response.status_code}: {response.text}',
                            'message': 'Erreur lors de l\'ajout'
                        }
                    time.sleep(2 ** attempt)  # Backoff exponentiel
                    
            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    return {
                        'success': False, 
                        'error': 'Timeout - connexion trop lente',
                        'message': 'Vérifiez votre connexion internet'
                    }
                time.sleep(2 ** attempt)
                
            except requests.exceptions.ConnectionError:
                return {
                    'success': False, 
                    'error': 'Pas de connexion internet',
                    'message': 'Vérifiez votre connexion internet'
                }
                
            except Exception as e:
                if attempt == max_retries - 1:
                    return {
                        'success': False, 
                        'error': str(e),
                        'message': 'Erreur lors de l\'ajout des données'
                    }
                time.sleep(2 ** attempt)
        
        return {
            'success': False, 
            'error': 'Échec après plusieurs tentatives',
            'message': 'Erreur persistante'
        }
    
    def obtenir_toutes_donnees(self, collection: str) -> Dict[str, Any]:
        """
        Récupère toutes les données d'une table avec retry
        """
        if not self.connection_status:
            return {
                'success': False, 
                'error': 'Pas de connexion internet',
                'message': 'Mode hors ligne'
            }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                url = self._build_url(collection)
                response = requests.get(url, headers=self.headers, timeout=30)
                
                if response.status_code == 200:
                    raw_data = response.json()
                    
                    # Convertir au format Firebase (dict avec IDs comme clés)
                    formatted_data = {}
                    if raw_data:
                        for item in raw_data:
                            item_id = str(item.get('id', 'unknown'))
                            formatted_data[item_id] = item
                    
                    return {
                        'success': True, 
                        'data': formatted_data,
                        'message': f'Récupéré {len(formatted_data)} enregistrements'
                    }
                else:
                    if attempt == max_retries - 1:
                        return {
                            'success': False, 
                            'error': f'Erreur HTTP {response.status_code}',
                            'message': 'Erreur lors de la récupération'
                        }
                    time.sleep(2 ** attempt)
                    
            except requests.exceptions.Timeout:
                if attempt == max_retries - 1:
                    return {
                        'success': False, 
                        'error': 'Timeout',
                        'message': 'Connexion trop lente'
                    }
                time.sleep(2 ** attempt)
                
            except requests.exceptions.ConnectionError:
                return {
                    'success': False, 
                    'error': 'Pas de connexion internet',
                    'message': 'Mode hors ligne'
                }
                
            except Exception as e:
                if attempt == max_retries - 1:
                    return {
                        'success': False, 
                        'error': str(e),
                        'message': 'Erreur lors de la récupération'
                    }
                time.sleep(2 ** attempt)
        
        return {
            'success': False, 
            'error': 'Échec après plusieurs tentatives',
            'data': {}
        }
    
    def modifier_donnees(self, collection: str, doc_id: str, data: Union[List[str], Dict[str, str]]) -> Dict[str, Any]:
        """Modifie des données existantes dans Supabase"""
        try:
            string_data = self._convert_to_strings(data)
            
            update_data = {
                'date': string_data.get('0', ''),
                'heur': string_data.get('1', ''),
                'operator': string_data.get('2', ''),
                'o_f_dd': string_data.get('3', ''),
                'operation': string_data.get('4', ''),
                'mension': string_data.get('5', ''),
                'hash_signature': self._generate_hash(string_data),
                'updated_at': datetime.now().isoformat()
            }
            
            url = f"{self._build_url(collection)}?id=eq.{doc_id}"
            response = requests.patch(url, json=update_data, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                result_data = response.json()[0] if response.json() else {}
                return {
                    'success': True, 
                    'data': result_data,
                    'message': 'Données modifiées avec succès'
                }
            else:
                return {
                    'success': False, 
                    'error': f'Erreur HTTP {response.status_code}',
                    'message': 'Erreur lors de la modification'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de la modification'
            }
    
    def supprimer_donnees(self, collection: str, doc_id: str = None) -> Dict[str, Any]:
        """Supprime des données de Supabase"""
        try:
            if doc_id:
                url = f"{self._build_url(collection)}?id=eq.{doc_id}"
            else:
                url = self._build_url(collection)
            
            response = requests.delete(url, headers=self.headers, timeout=30)
            
            if response.status_code == 204:
                return {
                    'success': True, 
                    'message': 'Données supprimées avec succès'
                }
            else:
                return {
                    'success': False, 
                    'error': f'Erreur HTTP {response.status_code}',
                    'message': 'Erreur lors de la suppression'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de la suppression'
            }
    
    def rechercher_donnees(self, collection: str, key: str, value: str) -> Dict[str, Any]:
        """Recherche des données par clé-valeur"""
        try:
            url = f"{self._build_url(collection)}?{key}=eq.{value}"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                raw_data = response.json()
                
                results = {}
                if raw_data:
                    for item in raw_data:
                        item_id = str(item.get('id', 'unknown'))
                        results[item_id] = item
                
                return {
                    'success': True, 
                    'data': results,
                    'message': f'{len(results)} résultat(s) trouvé(s)'
                }
            else:
                return {
                    'success': False, 
                    'error': f'Erreur HTTP {response.status_code}',
                    'message': 'Erreur lors de la recherche'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de la recherche'
            }

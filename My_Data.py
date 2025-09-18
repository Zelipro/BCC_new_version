import requests
import json
import hashlib
from typing import List, Dict, Optional, Any, Union
from datetime import datetime

class SupabaseDB:
    """
    Classe Supabase réutilisable avec interface identique à FirebaseDB.
    Utilise la table bcc_operations configurée sur Supabase.
    
    Usage:
    supabase = SupabaseDB(
        supabase_url="https://jutueskohextubwszbhv.supabase.co",
        supabase_key="votre-cle-anon"
    )
    """
    
    def __init__(self, 
                 supabase_url: str = "https://jutueskohextubwszbhv.supabase.co", 
                 supabase_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dHVlc2tvaGV4dHVid3N6YmhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjYzMzEwNDgsImV4cCI6MjA0MTkwNzA0OH0.zYqyTxuNHxXw3xoxLxrLzQl-3Cj7QzNhQXvUnEywrJM"):
        """
        Initialise la connexion Supabase
        
        Args:
            supabase_url (str): URL de votre projet Supabase
            supabase_key (str): Clé anon public Supabase
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
    
    def _build_url(self, collection: str) -> str:
        # Construit l'URL complète pour une table Supabase
        return f"{self.supabase_url}/rest/v1/{collection}"
    
    def _build_url_with_filter(self, collection: str, column: str, value: str) -> str:
        """Construit l'URL avec filtre pour Supabase"""
        return f"{self.supabase_url}/rest/v1/{collection}?{column}=eq.{value}"
    
    def _convert_to_strings(self, data: Union[List[str], Dict[str, str]]) -> Dict[str, str]:
        """
        Convertit les données en dictionnaire avec des chaînes de caractères
        (Interface identique à FirebaseDB)
        """
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
        Ajoute des données à une table Supabase
        Interface identique à FirebaseDB.ajouter_donnees()
        
        Args:
            collection (str): Nom de la table (ex: "bcc_operations")
            data: Liste ou dictionnaire de données (converties en strings)
            
        Returns:
            Dict: Réponse avec l'ID généré et les données
        """
        try:
            # Convertir en strings (comme Firebase)
            string_data = self._convert_to_strings(data)
            
            # Préparer les données pour Supabase selon la structure bcc_operations
            supabase_data = {
                'date': string_data.get('0', ''),
                'heur': string_data.get('1', ''), 
                'operator': string_data.get('2', ''),
                'o_f_dd': string_data.get('3', ''),
                'operation': string_data.get('4', ''),
                'mension': string_data.get('5', ''),
                'hash_signature': self._generate_hash(string_data),
                'device_info': 'CEET-BCC-Supabase',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            url = self._build_url(collection)
            response = requests.post(url, json=supabase_data, headers=self.headers)
            
            if response.status_code == 201:
                result_data = response.json()[0] if response.json() else {}
                return {
                    'success': True, 
                    'data': result_data,
                    'message': 'Données ajoutées avec succès'
                }
            else:
                return {
                    'success': False, 
                    'error': f'Erreur HTTP {response.status_code}: {response.text}',
                    'message': 'Erreur lors de l\'ajout'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de l\'ajout des données'
            }
    
    def modifier_donnees(self, collection: str, doc_id: str, data: Union[List[str], Dict[str, str]]) -> Dict[str, Any]:
        """
        Modifie des données existantes dans Supabase
        Interface identique à FirebaseDB.modifier_donnees()
        
        Args:
            collection (str): Nom de la table
            doc_id (str): ID du document à modifier
            data: Nouvelles données (converties en strings)
            
        Returns:
            Dict: Statut de l'opération
        """
        try:
            # Convertir en strings
            string_data = self._convert_to_strings(data)
            
            # Préparer les données de mise à jour
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
            response = requests.patch(url, json=update_data, headers=self.headers)
            
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
                    'error': f'Erreur HTTP {response.status_code}: {response.text}',
                    'message': 'Erreur lors de la modification'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de la modification des données'
            }
    
    def supprimer_donnees(self, collection: str, doc_id: str = None) -> Dict[str, Any]:
        """
        Supprime des données de Supabase
        Interface identique à FirebaseDB.supprimer_donnees()
        
        Args:
            collection (str): Nom de la table
            doc_id (str): ID du document à supprimer (si None, supprime toute la table - DANGER!)
            
        Returns:
            Dict: Statut de l'opération
        """
        try:
            if doc_id:
                url = f"{self._build_url(collection)}?id=eq.{doc_id}"
            else:
                # ATTENTION: Ceci supprime TOUTE la table!
                url = self._build_url(collection)
            
            response = requests.delete(url, headers=self.headers)
            
            if response.status_code == 204:
                return {
                    'success': True, 
                    'message': 'Données supprimées avec succès'
                }
            else:
                return {
                    'success': False, 
                    'error': f'Erreur HTTP {response.status_code}: {response.text}',
                    'message': 'Erreur lors de la suppression'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de la suppression des données'
            }
    
    def obtenir_toutes_donnees(self, collection: str) -> Dict[str, Any]:
        """
        Récupère toutes les données d'une table
        Interface identique à FirebaseDB.obtenir_toutes_donnees()
        
        Args:
            collection (str): Nom de la table
            
        Returns:
            Dict: Toutes les données de la table
        """
        try:
            url = self._build_url(collection)
            response = requests.get(url, headers=self.headers)
            
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
                    'message': 'Données récupérées avec succès'
                }
            else:
                return {
                    'success': False, 
                    'error': f'Erreur HTTP {response.status_code}: {response.text}',
                    'message': 'Erreur lors de la récupération'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de la récupération des données'
            }
    
    def obtenir_donnee_par_id(self, collection: str, doc_id: str) -> Dict[str, Any]:
        """
        Récupère une donnée spécifique par son ID
        Interface identique à FirebaseDB.obtenir_donnee_par_id()
        
        Args:
            collection (str): Nom de la table
            doc_id (str): ID du document
            
        Returns:
            Dict: Les données du document
        """
        try:
            url = f"{self._build_url(collection)}?id=eq.{doc_id}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                result_data = data[0] if data else None
                return {
                    'success': True, 
                    'data': result_data,
                    'message': 'Donnée récupérée avec succès'
                }
            else:
                return {
                    'success': False, 
                    'error': f'Erreur HTTP {response.status_code}: {response.text}',
                    'message': 'Erreur lors de la récupération'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de la récupération de la donnée'
            }
    
    def rechercher_donnees(self, collection: str, key: str, value: str) -> Dict[str, Any]:
        """
        Recherche des données par clé-valeur
        Interface identique à FirebaseDB.rechercher_donnees()
        
        Args:
            collection (str): Nom de la table
            key (str): Colonne à rechercher
            value (str): Valeur à rechercher
            
        Returns:
            Dict: Résultats de la recherche
        """
        try:
            # Utiliser les filtres Supabase pour une recherche efficace
            url = f"{self._build_url(collection)}?{key}=eq.{value}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                raw_data = response.json()
                
                # Convertir au format Firebase
                results = {}
                if raw_data:
                    for item in raw_data:
                        item_id = str(item.get('id', 'unknown'))
                        results[item_id] = item
                
                return {
                    'success': True, 
                    'data': results,
                    'message': f'Recherche terminée. {len(results)} résultat(s) trouvé(s)'
                }
            else:
                return {
                    'success': False, 
                    'error': f'Erreur HTTP {response.status_code}: {response.text}',
                    'message': 'Erreur lors de la recherche'
                }
                
        except Exception as e:
            return {
                'success': False, 
                'error': str(e),
                'message': 'Erreur lors de la recherche'
            }
    
    def rechercher_par_date(self, collection: str, date: str) -> Dict[str, Any]:
        """
        Fonction bonus: recherche spécifique par date pour CEET
        
        Args:
            collection (str): Nom de la table 
            date (str): Date à rechercher
            
        Returns:
            Dict: Résultats filtrés par date
        """
        return self.rechercher_donnees(collection, 'date', date)
    
    def obtenir_statistiques(self, collection: str) -> Dict[str, Any]:
        """
        Fonction bonus: obtient des statistiques sur la table
        
        Args:
            collection (str): Nom de la table
            
        Returns:
            Dict: Statistiques de la table
        """
        try:
            # Récupérer toutes les données pour calculer les stats
            all_data = self.obtenir_toutes_donnees(collection)
            
            if not all_data['success']:
                return all_data
            
            data = all_data['data']
            total_records = len(data)
            
            # Compter par opérateur
            operators = {}
            operations = {}
            dates = set()
            
            for record in data.values():
                op = record.get('operator', 'Inconnu')
                operators[op] = operators.get(op, 0) + 1
                
                operation = record.get('operation', 'Inconnue')
                operations[operation] = operations.get(operation, 0) + 1
                
                dates.add(record.get('date', ''))
            
            return {
                'success': True,
                'data': {
                    'total_records': total_records,
                    'unique_operators': len(operators),
                    'unique_dates': len(dates),
                    'operators_stats': operators,
                    'operations_stats': operations
                },
                'message': f'Statistiques calculées pour {total_records} enregistrements'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Erreur lors du calcul des statistiques'
            }


# Exemple d'utilisation dans ton code CEET :
"""
# Remplacement direct de ta classe Firebase
#supabase_db = SupabaseDB()

# Ajouter une manœuvre CEET (même interface que Firebase)
#manoeuvre_data = ["09/17/25", "14:30:15", "Jean Doe", "O", "Ouverture disjoncteur", "Succès"]
#result = supabase_db.ajouter_donnees("bcc_operations", manoeuvre_data)

#if result['success']:
#    print(f"Manœuvre ajoutée: {result['data']['id']}")

# Récupérer toutes les manœuvres
#all_manoeuvres = supabase_db.obtenir_toutes_donnees("bcc_operations")

# Rechercher par date
#manoeuvres_du_jour = supabase_db.rechercher_par_date("bcc_operations", "09/17/25")

# Obtenir des statistiques
#stats = supabase_db.obtenir_statistiques("bcc_operations")
"""
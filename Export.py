import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime
from pathlib import Path
from kivy.utils import platform
import traceback

class MobilePDF(FPDF):
    """Classe PDF personnalisée optimisée pour Android"""
    
    def __init__(self, title="Rapport"):
        super().__init__()
        self.report_title = title
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """En-tête de page"""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, self.report_title.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'C')
        self.set_font('Arial', '', 10)
        date_str = datetime.now().strftime("%d/%m/%Y à %H:%M")
        self.cell(0, 5, f'Généré le: {date_str}', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        """Pied de page"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def add_safe_text(self, text, max_length=50):
        """Ajouter du texte en gérant l'encodage"""
        try:
            # Tronquer et nettoyer le texte
            clean_text = str(text)[:max_length]
            # Remplacer les caractères non-ASCII
            safe_text = clean_text.encode('latin-1', 'replace').decode('latin-1')
            return safe_text
        except:
            return str(text)[:max_length]
        
    def add_table(self, headers, data, col_widths=None):
        """Ajouter un tableau au PDF avec gestion d'erreurs"""
        if not headers or not data:
            self.set_font('Arial', '', 12)
            self.cell(0, 10, 'Aucune donnée à afficher', 0, 1, 'C')
            return
            
        try:
            # Calculer les largeurs de colonnes
            if not col_widths:
                available_width = self.w - 2 * self.l_margin
                col_widths = [available_width / len(headers)] * len(headers)
            
            # En-têtes
            self.set_font('Arial', 'B', 9)
            self.set_fill_color(54, 96, 146)
            self.set_text_color(255, 255, 255)
            
            for i, header in enumerate(headers):
                safe_header = self.add_safe_text(header, 20)
                self.cell(col_widths[i], 8, safe_header, 1, 0, 'C', True)
            self.ln()
            
            # Données
            self.set_font('Arial', '', 8)
            self.set_text_color(0, 0, 0)
            
            fill = False
            for row in data:
                if fill:
                    self.set_fill_color(240, 240, 240)
                else:
                    self.set_fill_color(255, 255, 255)
                    
                # Vérifier si on a besoin d'une nouvelle page
                if self.get_y() > self.h - 30:
                    self.add_page()
                    # Réafficher les en-têtes
                    self.set_font('Arial', 'B', 9)
                    self.set_fill_color(54, 96, 146)
                    self.set_text_color(255, 255, 255)
                    for i, header in enumerate(headers):
                        safe_header = self.add_safe_text(header, 20)
                        self.cell(col_widths[i], 8, safe_header, 1, 0, 'C', True)
                    self.ln()
                    self.set_font('Arial', '', 8)
                    self.set_text_color(0, 0, 0)
                
                for i, cell_data in enumerate(row):
                    if i < len(col_widths):
                        safe_text = self.add_safe_text(cell_data, 25)
                        self.cell(col_widths[i], 6, safe_text, 1, 0, 'C', fill)
                self.ln()
                fill = not fill
                
        except Exception as e:
            print(f"Erreur dans add_table: {e}")
            self.set_font('Arial', '', 12)
            self.cell(0, 10, 'Erreur lors de la création du tableau', 0, 1, 'C')

class DataExporter:
    """
    Classe pour exporter des données optimisée pour Android
    """
    
    def __init__(self, output_dir="exports"):
        """Initialiser l'exporteur avec gestion des permissions Android"""
        self.setup_output_directory(output_dir)
        
    def setup_output_directory(self, output_dir):
        """Configuration du répertoire de sortie selon la plateforme"""
        try:
            if platform == 'android':
                # Pour Android, utiliser le stockage externe accessible
                from android.storage import primary_external_storage_path
                try:
                    external_path = primary_external_storage_path()
                    self.output_dir = Path(external_path) / "BCC_Exports"
                except:
                    # Fallback si les permissions ne sont pas accordées
                    self.output_dir = Path("/storage/emulated/0/Download/BCC_Exports")
            else:
                # Pour desktop/autres plateformes
                self.output_dir = Path(output_dir)
            
            # Créer le dossier avec gestion d'erreurs
            self.output_dir.mkdir(parents=True, exist_ok=True)
            print(f"Répertoire d'export: {self.output_dir}")
            
        except Exception as e:
            print(f"Erreur création répertoire: {e}")
            # Fallback vers un répertoire local
            self.output_dir = Path("exports_bcc")
            self.output_dir.mkdir(exist_ok=True)
        
    def export_data(self, data, filename_base, formats=['pdf'], 
                   title="Rapport de données", headers=None):
        """
        Exporter des données avec gestion d'erreurs robuste
        """
        if not data:
            return {'error': 'Aucune donnée à exporter'}
        
        # Normaliser les données
        try:
            normalized_data = self._normalize_data(data, headers)
        except Exception as e:
            return {'error': f'Erreur normalisation données: {e}'}
        
        created_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for format_type in formats:
            try:
                filename = f"{filename_base}_{timestamp}.{format_type.lower()}"
                filepath = self.output_dir / filename
                
                if format_type.lower() == 'pdf':
                    success = self._export_to_pdf(normalized_data, filepath, title)
                elif format_type.lower() in ['xlsx', 'excel']:
                    success = self._export_to_excel(normalized_data, filepath, title)
                else:
                    print(f"Format {format_type} non supporté sur mobile")
                    continue
                
                if success:
                    created_files[format_type] = str(filepath)
                    print(f"✓ Fichier {format_type.upper()} créé: {filepath}")
                else:
                    print(f"✗ Erreur création {format_type}")
                
            except Exception as e:
                print(f"✗ Erreur export {format_type}: {e}")
                traceback.print_exc()
        
        return created_files
    
    def _normalize_data(self, data, headers=None):
        """Normaliser les données en format standard"""
        if not data:
            return {'headers': headers or [], 'rows': []}
        
        try:
            # Si c'est une liste de dictionnaires
            if isinstance(data[0], dict):
                headers = headers or list(data[0].keys())
                rows = [[str(row.get(col, '')) for col in headers] for row in data]
            
            # Si c'est une liste de listes
            elif isinstance(data[0], (list, tuple)):
                headers = headers or [f"Colonne {i+1}" for i in range(len(data[0]))]
                rows = [[str(cell) for cell in row] for row in data]
            
            # Si c'est une liste simple
            else:
                headers = headers or ['Valeur']
                rows = [[str(item)] for item in data]
            
            return {'headers': headers, 'rows': rows}
        
        except Exception as e:
            print(f"Erreur normalisation: {e}")
            return {'headers': headers or ['Erreur'], 'rows': [['Erreur de données']]}
    
    def _export_to_pdf(self, normalized_data, filepath, title):
        """Exporter en PDF avec gestion d'erreurs robuste"""
        try:
            pdf = MobilePDF(title=title)
            pdf.add_page()
            
            # Ajouter des informations
            pdf.set_font('Arial', 'B', 12)
            info_text = f"Nombre d'enregistrements: {len(normalized_data['rows'])}"
            pdf.cell(0, 10, info_text, 0, 1)
            pdf.ln(5)
            
            # Ajouter le tableau
            if normalized_data['rows']:
                headers = normalized_data['headers']
                available_width = pdf.w - 2 * pdf.l_margin
                
                if len(headers) > 0:
                    # Largeurs égales par défaut
                    col_widths = [available_width / len(headers)] * len(headers)
                    pdf.add_table(headers, normalized_data['rows'], col_widths)
            else:
                pdf.set_font('Arial', '', 14)
                pdf.cell(0, 10, 'Aucune donnée à afficher', 0, 1, 'C')
            
            # Sauvegarder avec gestion d'erreurs
            pdf.output(str(filepath))
            
            # Vérifier que le fichier a été créé
            if filepath.exists() and filepath.stat().st_size > 0:
                return True
            else:
                print(f"Fichier PDF vide ou non créé: {filepath}")
                return False
                
        except Exception as e:
            print(f"Erreur création PDF: {e}")
            traceback.print_exc()
            return False
    
    def _export_to_excel(self, normalized_data, filepath, title):
        """Exporter en Excel avec gestion d'erreurs"""
        try:
            # Créer le DataFrame
            if normalized_data['rows']:
                df = pd.DataFrame(normalized_data['rows'], columns=normalized_data['headers'])
            else:
                df = pd.DataFrame()
            
            # Écrire dans Excel
            with pd.ExcelWriter(str(filepath), engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Données', index=False)
                
                # Ajouter une feuille d'informations
                info_data = {
                    'Information': ['Titre', 'Date de création', 'Nombre de lignes'],
                    'Valeur': [title, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), len(normalized_data['rows'])]
                }
                info_df = pd.DataFrame(info_data)
                info_df.to_excel(writer, sheet_name='Informations', index=False)
            
            # Vérifier que le fichier a été créé
            if filepath.exists() and filepath.stat().st_size > 0:
                return True
            else:
                print(f"Fichier Excel vide ou non créé: {filepath}")
                return False
                
        except Exception as e:
            print(f"Erreur création Excel: {e}")
            traceback.print_exc()
            return False

# Fonctions utilitaires pour usage rapide
def export_to_pdf(data, filename, title="Rapport", headers=None):
    """Fonction simple pour exporter seulement en PDF"""
    try:
        exporter = DataExporter()
        return exporter.export_data(data, filename, formats=['pdf'], title=title, headers=headers)
    except Exception as e:
        print(f"Erreur export PDF: {e}")
        return {}

def export_to_excel(data, filename, title="Rapport", headers=None):
    """Fonction simple pour exporter seulement en Excel"""
    try:
        exporter = DataExporter()
        return exporter.export_data(data, filename, formats=['xlsx'], title=title, headers=headers)
    except Exception as e:
        print(f"Erreur export Excel: {e}")
        return {}

# Test pour vérifier que les modules sont disponibles
def test_export_modules():
    """Tester la disponibilité des modules d'export"""
    results = {
        'pandas': False,
        'fpdf': False,
        'openpyxl': False
    }
    
    try:
        import pandas
        results['pandas'] = True
        print("✓ Pandas disponible")
    except ImportError:
        print("✗ Pandas non disponible")
    
    try:
        from fpdf import FPDF
        results['fpdf'] = True
        print("✓ FPDF disponible")
    except ImportError:
        print("✗ FPDF non disponible")
    
    try:
        import openpyxl
        results['openpyxl'] = True
        print("✓ OpenPyXL disponible")
    except ImportError:
        print("✗ OpenPyXL non disponible")
    
    return results

if __name__ == "__main__":
    # Test des modules
    test_export_modules()
    
    # Données d'exemple pour test
    data_test = [
        ['12/09/2024', '14:30', 'Jean', 'O', 'Ouverture normale', 'Succès'],
        ['12/09/2024', '18:00', 'Marie', 'F', 'Fermeture', 'Succès'],
        ['13/09/2024', '08:15', 'Pierre', 'DD', 'Défaillance détectée', 'IC']
    ]
    headers_test = ['Date', 'Heure', 'Opérateur', 'O/F/DD', 'Opération', 'Mention']
    
    # Test d'export
    exporter = DataExporter()
    files = exporter.export_data(
        data_test,
        "test_bcc",
        formats=['pdf', 'xlsx'],
        title="Test BCC Export",
        headers=headers_test
    )
    
    print(f"Fichiers créés: {files}")

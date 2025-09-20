import os
from datetime import datetime
from pathlib import Path
from kivy.utils import platform
import traceback

# Imports conditionnels pour Android
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Pandas non disponible - Export Excel désactivé")

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False
    print("FPDF non disponible - Export PDF désactivé")

class AndroidPDF(FPDF):
    """Classe PDF optimisée pour Android avec gestion d'erreurs robuste"""
    
    def __init__(self, title="Rapport BCC"):
        super().__init__()
        self.report_title = title
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        """En-tête simplifié pour Android"""
        try:
            self.set_font('Arial', 'B', 14)
            # Nettoyer le titre pour éviter les erreurs d'encodage
            clean_title = str(self.report_title).encode('ascii', 'ignore').decode('ascii')
            self.cell(0, 10, clean_title, 0, 1, 'C')
            
            self.set_font('Arial', '', 9)
            date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.cell(0, 5, f'Genere le: {date_str}', 0, 1, 'C')
            self.ln(8)
        except Exception as e:
            print(f"Erreur header PDF: {e}")
            
    def footer(self):
        """Pied de page simplifié"""
        try:
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        except Exception as e:
            print(f"Erreur footer PDF: {e}")
        
    def add_safe_text(self, text, max_length=30):
        """Texte sécurisé pour Android"""
        try:
            clean_text = str(text)[:max_length]
            # Remplacer tous les caractères non-ASCII
            safe_text = clean_text.encode('ascii', 'ignore').decode('ascii')
            return safe_text if safe_text else "N/A"
        except:
            return "N/A"
        
    def add_table(self, headers, data):
        """Tableau simplifié pour Android"""
        if not headers or not data:
            self.set_font('Arial', '', 12)
            self.cell(0, 10, 'Aucune donnee a afficher', 0, 1, 'C')
            return
            
        try:
            # Calculer largeurs disponibles
            available_width = self.w - 2 * self.l_margin
            col_width = available_width / len(headers)
            
            # En-têtes
            self.set_font('Arial', 'B', 8)
            self.set_fill_color(100, 149, 237)  # Bleu
            self.set_text_color(255, 255, 255)  # Blanc
            
            for header in headers:
                safe_header = self.add_safe_text(header, 15)
                self.cell(col_width, 8, safe_header, 1, 0, 'C', True)
            self.ln()
            
            # Données
            self.set_font('Arial', '', 7)
            self.set_text_color(0, 0, 0)  # Noir
            
            row_count = 0
            for row in data:
                # Vérifier si nouvelle page nécessaire
                if self.get_y() > self.h - 30:
                    self.add_page()
                    # Répéter les en-têtes
                    self.set_font('Arial', 'B', 8)
                    self.set_fill_color(100, 149, 237)
                    self.set_text_color(255, 255, 255)
                    for header in headers:
                        safe_header = self.add_safe_text(header, 15)
                        self.cell(col_width, 8, safe_header, 1, 0, 'C', True)
                    self.ln()
                    self.set_font('Arial', '', 7)
                    self.set_text_color(0, 0, 0)
                
                # Couleur alternée
                if row_count % 2 == 0:
                    self.set_fill_color(245, 245, 245)
                else:
                    self.set_fill_color(255, 255, 255)
                
                for i, cell_data in enumerate(row):
                    if i < len(headers):
                        safe_text = self.add_safe_text(cell_data, 20)
                        self.cell(col_width, 6, safe_text, 1, 0, 'C', True)
                self.ln()
                row_count += 1
                
        except Exception as e:
            print(f"Erreur création tableau PDF: {e}")
            self.set_font('Arial', '', 12)
            self.cell(0, 10, 'Erreur affichage tableau', 0, 1, 'C')

class AndroidDataExporter:
    """
    Exporteur de données spécialement optimisé pour Android
    """
    
    def __init__(self, output_dir="BCC_Exports"):
        self.setup_android_directory(output_dir)
        
    def setup_android_directory(self, output_dir):
        """Configuration du répertoire Android avec gestion des permissions"""
        try:
            if platform == 'android':
                # Essayer différents emplacements Android
                possible_paths = [
                    f"/storage/emulated/0/Download/{output_dir}",
                    f"/storage/emulated/0/Documents/{output_dir}",
                    f"/sdcard/Download/{output_dir}",
                    f"/sdcard/{output_dir}",
                    output_dir  # Fallback
                ]
                
                self.output_dir = None
                for path in possible_paths:
                    try:
                        test_dir = Path(path)
                        test_dir.mkdir(parents=True, exist_ok=True)
                        # Test d'écriture
                        test_file = test_dir / "test_write.tmp"
                        test_file.write_text("test")
                        test_file.unlink()  # Supprimer le fichier test
                        self.output_dir = test_dir
                        print(f"Répertoire Android configuré: {self.output_dir}")
                        break
                    except Exception as e:
                        print(f"Échec répertoire {path}: {e}")
                        continue
                
                if not self.output_dir:
                    # Dernier recours - répertoire de l'app
                    self.output_dir = Path("exports_bcc")
                    self.output_dir.mkdir(exist_ok=True)
                    print(f"Utilisation répertoire local: {self.output_dir}")
            else:
                # Desktop
                self.output_dir = Path(output_dir)
                self.output_dir.mkdir(parents=True, exist_ok=True)
                
        except Exception as e:
            print(f"Erreur configuration répertoire: {e}")
            self.output_dir = Path("exports_bcc")
            self.output_dir.mkdir(exist_ok=True)
    
    def export_data(self, data, filename_base, formats=['pdf'], 
                   title="Rapport BCC", headers=None):
        """
        Export avec gestion d'erreurs robuste pour Android
        """
        if not data:
            return {'error': 'Aucune donnée à exporter'}
        
        # Vérifier les modules disponibles
        available_formats = []
        for fmt in formats:
            if fmt.lower() == 'pdf' and FPDF_AVAILABLE:
                available_formats.append('pdf')
            elif fmt.lower() in ['xlsx', 'excel'] and PANDAS_AVAILABLE:
                available_formats.append('xlsx')
        
        if not available_formats:
            return {'error': 'Aucun module d\'export disponible'}
        
        # Normaliser les données
        try:
            normalized_data = self._normalize_data(data, headers)
        except Exception as e:
            return {'error': f'Erreur normalisation: {e}'}
        
        created_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for format_type in available_formats:
            try:
                filename = f"{filename_base}_{timestamp}.{format_type}"
                filepath = self.output_dir / filename
                
                success = False
                if format_type == 'pdf':
                    success = self._export_to_pdf_android(normalized_data, filepath, title)
                elif format_type == 'xlsx':
                    success = self._export_to_excel_android(normalized_data, filepath, title)
                
                if success:
                    created_files[format_type] = str(filepath)
                    print(f"✓ Fichier {format_type.upper()} créé: {filepath}")
                else:
                    print(f"✗ Échec création {format_type}")
                
            except Exception as e:
                print(f"✗ Erreur export {format_type}: {e}")
                traceback.print_exc()
        
        return created_files
    
    def _normalize_data(self, data, headers=None):
        """Normalisation robuste des données"""
        if not data:
            return {'headers': headers or [], 'rows': []}
        
        try:
            # Liste de dictionnaires
            if isinstance(data[0], dict):
                headers = headers or list(data[0].keys())
                rows = []
                for row in data:
                    row_data = []
                    for col in headers:
                        value = row.get(col, '')
                        # Nettoyer la valeur
                        clean_value = str(value).replace('\n', ' ').replace('\r', '')
                        row_data.append(clean_value)
                    rows.append(row_data)
            
            # Liste de listes
            elif isinstance(data[0], (list, tuple)):
                headers = headers or [f"Col{i+1}" for i in range(len(data[0]))]
                rows = []
                for row in data:
                    row_data = []
                    for cell in row:
                        clean_cell = str(cell).replace('\n', ' ').replace('\r', '')
                        row_data.append(clean_cell)
                    rows.append(row_data)
            
            # Liste simple
            else:
                headers = headers or ['Valeur']
                rows = [[str(item).replace('\n', ' ').replace('\r', '')] for item in data]
            
            return {'headers': headers, 'rows': rows}
        
        except Exception as e:
            print(f"Erreur normalisation: {e}")
            return {'headers': ['Erreur'], 'rows': [['Erreur de données']]}
    
    def _export_to_pdf_android(self, normalized_data, filepath, title):
        """Export PDF optimisé pour Android"""
        try:
            pdf = AndroidPDF(title=title)
            pdf.add_page()
            
            # Informations
            pdf.set_font('Arial', 'B', 10)
            info_text = f"Nombre d'enregistrements: {len(normalized_data['rows'])}"
            pdf.cell(0, 8, info_text, 0, 1)
            pdf.ln(5)
            
            # Tableau
            if normalized_data['rows']:
                pdf.add_table(normalized_data['headers'], normalized_data['rows'])
            else:
                pdf.set_font('Arial', '', 14)
                pdf.cell(0, 10, 'Aucune donnee a afficher', 0, 1, 'C')
            
            # Sauvegarde avec vérification
            pdf.output(str(filepath))
            
            # Vérifier que le fichier existe et n'est pas vide
            if filepath.exists() and filepath.stat().st_size > 100:  # Au moins 100 bytes
                print(f"PDF créé avec succès: {filepath.stat().st_size} bytes")
                return True
            else:
                print(f"Fichier PDF invalide ou vide")
                return False
                
        except Exception as e:
            print(f"Erreur création PDF Android: {e}")
            traceback.print_exc()
            return False
    
    def _export_to_excel_android(self, normalized_data, filepath, title):
        """Export Excel optimisé pour Android"""
        try:
            if normalized_data['rows']:
                df = pd.DataFrame(normalized_data['rows'], columns=normalized_data['headers'])
            else:
                df = pd.DataFrame()
            
            # Export simple sans mise en forme complexe
            df.to_excel(str(filepath), index=False, engine='openpyxl')
            
            # Vérification
            if filepath.exists() and filepath.stat().st_size > 500:  # Au moins 500 bytes
                print(f"Excel créé avec succès: {filepath.stat().st_size} bytes")
                return True
            else:
                print("Fichier Excel invalide ou vide")
                return False
                
        except Exception as e:
            print(f"Erreur création Excel Android: {e}")
            traceback.print_exc()
            return False

# Fonction utilitaire pour tester les modules
def test_export_android():
    """Test des modules disponibles sur Android"""
    print("=== Test des modules d'export Android ===")
    
    modules = {
        'FPDF': FPDF_AVAILABLE,
        'Pandas': PANDAS_AVAILABLE,
    }
    
    available_modules = []
    for module, status in modules.items():
        if status:
            print(f"✓ {module} disponible")
            available_modules.append(module)
        else:
            print(f"✗ {module} non disponible")
    
    if available_modules:
        print(f"Modules disponibles: {', '.join(available_modules)}")
        return True
    else:
        print("Aucun module d'export disponible!")
        return False

# Export simplifié pour intégration
def export_to_android(data, filename, formats=['pdf'], title="Rapport BCC", headers=None):
    """
    Fonction d'export simplifiée pour Android
    
    Returns:
        dict: Fichiers créés ou message d'erreur
    """
    try:
        exporter = AndroidDataExporter()
        result = exporter.export_data(data, filename, formats, title, headers)
        return result
    except Exception as e:
        print(f"Erreur export Android: {e}")
        return {'error': str(e)}

if __name__ == "__main__":
    # Test automatique
    print("Test des modules d'export pour Android...")
    test_export_android()
    
    # Test d'export basique
    test_data = [
        ['20/09/2024', '14:30', 'Test User', 'O', 'Test Operation', 'Succes'],
        ['20/09/2024', '15:45', 'Test User2', 'F', 'Test Operation 2', 'IC']
    ]
    test_headers = ['Date', 'Heure', 'Operateur', 'O/F/DD', 'Operation', 'Mention']
    
    print("\nTest d'export...")
    result = export_to_android(test_data, "test_android", ['pdf'], "Test Android", test_headers)
    print(f"Résultat: {result}")

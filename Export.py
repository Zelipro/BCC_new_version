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
                    print(f"

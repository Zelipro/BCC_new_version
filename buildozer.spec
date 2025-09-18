# Configuration Buildozer pour BCC Control - GitHub Actions Ready
# Basée sur l'analyse complète de votre projet

[app]
# Informations de base de l'application
title = BCC Control
package.name = bcccontrol
package.domain = com.ceet.bcc

# Configuration source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

# Patterns d'inclusion spécifiques pour votre projet
source.include_patterns = Pages/*.kv,*.png,*.db,My_Data.py,Export.py

# Version de l'application
version = 2.0

# Dépendances analysées depuis votre code
# Ordre important : les dépendances de base en premier
#requirements = python3==3.10.12,kivy==2.2.0,kivymd==1.1.1,sqlite3,requests,hashlib,pathlib,datetime

# Dépendances pour les exports (peuvent être problématiques sur Android)
requirements = python3==3.10.12,kivy==2.2.0,kivymd==1.1.1,sqlite3,requests,hashlib,pathlib,datetime,pandas,openpyxl,python-docx,reportlab

# Icône et presplash
presplash.filename = %(source.dir)s/CEET.png
icon.filename = %(source.dir)s/CEET.png

# Orientation (basée sur Window.size = [340,620] dans votre code)
orientation = portrait

# Configuration OSX
osx.kivy_version = 2.2.0

#
# Configuration Android
#

# Application en plein écran ou non
fullscreen = 0

# Couleur du presplash (basée sur votre md_bg_color jaune)
android.presplash_color = #FFFF00

# Permissions nécessaires pour votre application
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# API levels
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# Architectures supportées
android.archs = arm64-v8a, armeabi-v7a

# Configuration automatique
android.accept_sdk_license = True

# Point d'entrée
android.entrypoint = org.kivy.android.PythonActivity

# Format des artifacts
android.release_artifact = aab
android.debug_artifact = apk

# Backup Android
android.allow_backup = True

#
# Configuration Python-for-Android (p4a)
#

# Bootstrap recommandé pour KivyMD
p4a.bootstrap = sdl2

# Branch stable
p4a.branch = master

#
# Configuration iOS (si nécessaire plus tard)
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false

#
# Configuration Buildozer
#

[buildozer]
# Niveau de log pour debugging
log_level = 2

# Warning si exécuté en root
warn_on_root = 1

#
# NOTES IMPORTANTES POUR VOTRE PROJET BCC
#

# STRUCTURE RECOMMANDÉE POUR GITHUB ACTIONS:
# votre_repo/
# ├── main.py (renommé de main3.py)
# ├── My_Data.py
# ├── Export.py (renommé de 1758234099646_Export.py)
# ├── CEET.png
# ├── My_Image.png
# ├── base.db
# ├── Pages/
# │   ├── Page1.kv
# │   ├── Page2.kv
# │   ├── Page3.kv
# │   └── Page4.kv
# ├── buildozer.spec
# └── .github/
#     └── workflows/
#         └── build-apk.yml

# CORRECTIONS NÉCESSAIRES DANS VOTRE CODE:

# 1. Dans main3.py, ligne 1367 environ, corrigez cette fonction:
# def lancer_export_avec_formats(self, formats):
#     self.menu_export.dismiss()
#     content_layout = MDBoxLayout(...)
#     btn_date_actuelle = MDRaisedButton(
#         text=f"Exporter le {self.DATE}",
#         on_release=lambda x: self.choisir_emplacement_export(formats, False)  # ← CHANGÉ
#     )
#     btn_tout = MDRaisedButton(
#         text="Exporter tout l'historique", 
#         on_release=lambda x: self.choisir_emplacement_export(formats, True)   # ← CHANGÉ
#     )

# 2. Ajoutez TOUTES les nouvelles fonctions de choix d'emplacement à la fin
#    de votre classe BCC() avant la ligne BCC().run()

# DÉPENDANCES PROBLÉMATIQUES:
# - pandas: Très lourd sur Android, peut causer des échecs de build
# - reportlab: Peut nécessiter des dépendances système supplémentaires  
# - python-docx: Compatible mais peut être lent
# - openpyxl: Généralement compatible

# STRATÉGIE DE BUILD:
# 1. Première build: Sans les dépendances d'export (requirements de base)
# 2. Si succès: Ajouter progressivement pandas, reportlab, etc.
# 3. Si échec avec pandas: Remplacer par du Python natif

# PERMISSIONS EXPLIQUÉES:
# - INTERNET: Connexion Supabase
# - WRITE_EXTERNAL_STORAGE: Export de fichiers
# - READ_EXTERNAL_STORAGE: Lecture de fichiers
# - ACCESS_NETWORK_STATE: Gestion réseau pour Supabase
# - ACCESS_WIFI_STATE: État du WiFi pour sync

# GITHUB ACTIONS:
# Ce fichier est optimisé pour GitHub Actions avec:
# - android.accept_sdk_license = True (pas d'interaction manuelle)
# - Architectures ARM modernes
# - Versions API récentes mais compatibles
# - Permissions correctes pour votre usage

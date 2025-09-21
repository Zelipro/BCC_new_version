[app]
title = BCC - CEET Control
package.name = bcc
package.domain = com.ceet.bcc
source.dir = .
version = 2.3

# Requirements avec versions spécifiques pour Android
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow,requests,pandas==1.5.3,openpyxl==3.0.10,fpdf2==3.0.0,pyjnius

orientation = portrait

# Icône et splash
icon.filename = CEET.png
presplash.filename = CEET.png
presplash.color = #FFFF00

# =============================================
# PERMISSIONS ANDROID POUR EXPORT
# =============================================

# Permissions de base
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Permissions Android 11+ pour l'export
android.add_permissions = MANAGE_EXTERNAL_STORAGE

# =============================================
# CONFIGURATION ANDROID EXPORT
# =============================================

# Architecture Android
android.archs = arm64-v8a, armeabi-v7a

# API Android optimisé pour les exports
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

# Configuration de compilation
android.accept_sdk_license = True

# Dépendances Gradle pour l'export de fichiers
android.gradle_dependencies = androidx.core:core:1.6.0, androidx.appcompat:appcompat:1.3.1, androidx.documentfile:documentfile:1.0.1

# =============================================
# CONFIGURATION POUR EXPORT DE FICHIERS
# =============================================

# Support pour l'accès aux fichiers Android
android.add_src = java_src
android.add_xml = android_xml

# Utiliser le stockage scoped pour Android 10+
android.use_androidx = True

# Configuration P4A
p4a.branch = master
p4a.bootstrap = sdl2

# Bootstrap hooks pour les exports
p4a.hook = hooks/

# =============================================
# OPTIMISATIONS POUR L'EXPORT
# =============================================

# Permissions runtime pour l'export
android.add_activity = org.kivy.android.PythonActivity

# Support des fichiers
android.add_java_dir = java_src
android.add_res_dir = res

# Configuration réseau et stockage
android.logcat_filters = *:S python:D

# Options de compilation
android.release_artifact = apk

# =============================================
# INSTRUCTIONS POUR L'EXPORT
# =============================================

# L'app va créer les exports dans:
# - /storage/emulated/0/Download/BCC_Exports (priorité)
# - /storage/emulated/0/Documents/BCC_Exports (backup)
# - Dossier privé de l'app (fallback)

# Permissions requises:
# - WRITE_EXTERNAL_STORAGE pour Android < 10
# - MANAGE_EXTERNAL_STORAGE pour Android 11+
# - L'utilisateur devra accorder ces permissions manuellement

[buildozer]
log_level = 2
warn_on_root = 1

# =============================================
# HOOKS POUR L'EXPORT (optionnel)
# =============================================

# Si vous créez un dossier hooks/ avec pre_build.py:
# - Vérifier la disponibilité des modules d'export
# - Configurer les permissions Android
# - Optimiser les bibliothèques pour la taille de l'APK

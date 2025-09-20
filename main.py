from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import NoTransition,ScreenManager
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.behaviors import MagicBehavior,HoverBehavior
from kivymd.uix.button import MDRaisedButton,MDIconButton,MDFlatButton
from kivymd.uix.tooltip import MDTooltip
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image

from time import strftime
import sqlite3
from kivymd.toast import toast
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView

from My_Data import SupabaseDB
Window.size = [340,620]

# Écran de chargement personnalisé
class LoadingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'loading'
        
        # Utiliser le même style que votre Page1
        self.md_bg_color = [1,1,0,1]  # Fond jaune
        
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Logo CEET
        logo = Image(
            source='CEET.png',
            size_hint=(None, None),
            size=(120, 120),
            pos_hint={'center_x': 0.5}
        )
        
        # Titre principal
        title = MDLabel(
            text='LOGICIEL DE CONTRÔLE DU BCC',
            font_style='H5',
            markup=True,
            halign='center',
            theme_text_color='Primary'
        )
        
        # Sous-titre
        subtitle = MDLabel(
            text='CEET-DRM-BCC',
            font_style='H6',
            markup=True,
            halign='center',
            theme_text_color='Secondary'
        )
        
        # Message de chargement
        loading_msg = MDLabel(
            text='Initialisation en cours...',
            font_style='Caption',
            halign='center',
            theme_text_color='Hint'
        )
        
        layout.add_widget(logo)
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(loading_msg)
        
        self.add_widget(layout)
        
        # Programmer le passage à Page1 après 2.5 secondes
        Clock.schedule_once(self.go_to_main, 2.5)
    
    def go_to_main(self, dt):
        self.manager.current = 'Page1'

Builder.load_file("Pages/Page1.kv")
Builder.load_file("Pages/Page2.kv")
Builder.load_file("Pages/Page3.kv")
Builder.load_file("Pages/Page4.kv")

###Pour les buttons styler

class But_styler(MDCard):
    def __init__(self, Liste, **kwargs):
        super().__init__(**kwargs)
        self.Liste = Liste
        Liste2 = ["H6"] + [ "Subtitle1"]*(len(self.Liste)-1)  # Du plus grand au plus petit
        
        # Configuration de la carte
        self.radius = 10
        #self.elevation = 2
        self.padding = "16dp"
        self.spacing = "8dp"
        #self.size_hint_y = None
        self.adaptive_height = True
        #self.height = "170dp"  # Hauteur fixe pour chaque carte
        self.md_bg_color = (0.95, 0.95, 0.95, 1)  # Couleur de fond légère
        
        # Activation des événements de clic
        self.ripple_effect = True  # Effet de ripple KivyMD
        
        # Layout vertical pour organiser les labels
        layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height = True,
            spacing="4dp"
        )
        
        # Ajout des labels avec les styles correspondants
        for i, (elmt1, elmt2) in enumerate(zip(self.Liste, Liste2)):
            lab = MDLabel(
                text=str(elmt1),
                font_style=elmt2,
                theme_text_color="Primary",
                size_hint_y=None,
                height="20dp" if i > 0 else "30dp"  # Plus d'espace pour le premier élément
            )
            layout.add_widget(lab)
        
        self.add_widget(layout)
        
        # Comportement au clic avec l'événement natif de MDCard
        self.bind(on_release=self.on_card_click)
    
    def on_card_click(self, instance):
        """Fonction appelée quand on clique sur la carte"""
        # Créer le contenu du dialog avec toutes les informations
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="250dp"
        )
        
        # Styles pour l'affichage dans le dialog
        styles_dialog = ["H5", "H6", "Subtitle1", "Body1"]+["Body1"]
        
        # Ajouter chaque élément de la liste avec son style
        for i, (info, style) in enumerate(zip(self.Liste, styles_dialog)):
            label = MDLabel(
                text=f"• {info}",
                font_style=style,
                theme_text_color="Primary",
                size_hint_y=None,
                height="40dp"
            )
            content_layout.add_widget(label)
        
        # Créer le dialog
        self.dialog = MDDialog(
            title="Informations de la carte",
            type="custom",
            content_cls=content_layout,
            buttons=[
                MDFlatButton(
                    text="FERMER",
                    theme_text_color="Custom",
                    text_color=(0.2, 0.6, 1, 1),
                    on_release=self.close_dialog
                ),
            ],
        )
        
        # Afficher le dialog
        self.dialog.open()
    
    def close_dialog(self, instance):
        """Fermer le dialog"""
        if hasattr(self, 'dialog'):
            self.dialog.dismiss()


### FIn _ buttons styler

class But(MDRaisedButton , MagicBehavior,HoverBehavior):
    def on_enter(self):
        self.size_hint = .3,.1
        self.Font = self.font_size
        self.font_size = 20
    
    def on_leave(self):
        self.size_hint= .15,.05
        self.font_size = self.Font

class Icon(MDIconButton,HoverBehavior):
    def __init__(self, text="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        # Menu qui s'affiche au survol
        self.tooltip_menu = MDDropdownMenu(
            width=dp(50),
            )
        
    def on_enter(self):
        self.tooltip_menu.caller = self
        self.tooltip_menu.items=[{"text": self.text}]
        self.tooltip_menu.open()
        
    def on_leave(self):
        self.tooltip_menu.dismiss()


class Page1(MDScreen):
    pass

class Page2(MDScreen):
    pass

class Page3(MDScreen):
    pass

class Page4(MDScreen):
    pass

class BCC(MDApp):
    Langue = {
    "fr": {
        "Page1": {
            "1": "[b]LOGICIEL DE CONTRÔLE DU BCC[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]Aller[/b]"
        },
        "Page2": {
            "1": "[b]BIENVENUE \n VEUILLEZ SÉLECTIONNER VOTRE ACTION[/b]",
            "2": "[b]HISTOIRE[/b]",
            "3": "[b]AJOUTER[/b]",
            "4": "Aide",
            "5": "Changer de fonds (Nuit/Jour)",
            "6": "Accueil",
            "7": "Saisir information",
            "8": "Choix",
            "9": "Histoire",
            "10": "Couleur"
        },
        "Page3": {
            "1": "[b]VEUILLEZ REMPLIR CETTE PAGE[/b]",
            "2": "Date",
            "3": "Operateur",
            "4": "Ouverture ou fermerture ou DD",
            "5": "Operation",
            "6": "Mension(succes ou Ic)",
            "7": "Si il n'y a pas on met rien",
            "8": "[b]Valider[/b]"
        }
    },
    "en": {
        "Page1": {
            "1": "[b]BCC CONTROL SOFTWARE[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]Go[/b]"
        },
        "Page2": {
            "1": "[b]WELCOME \n PLEASE SELECT YOUR ACTION[/b]",
            "2": "[b]HISTORY[/b]",
            "3": "[b]ADD[/b]",
            "4": "Help",
            "5": "Switch theme (Light/Dark)",
            "6": "Home",
            "7": "Enter information",
            "8": "Choose",
            "9": "History",
            "10": "Color"
        },
        "Page3": {
            "1": "[b]PLEASE FILL OUT THIS PAGE[/b]",
            "2": "Date",
            "3": "Operator",
            "4": "Opening or closing or DD",
            "5": "Operation",
            "6": "Mention(success or Ic)",
            "7": "If there is nothing, leave empty",
            "8": "[b]Validate[/b]"
        }
    },
    "es": {
        "Page1": {
            "1": "[b]SOFTWARE DE CONTROL BCC[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]Ir[/b]"
        },
        "Page2": {
            "1": "[b]BIENVENIDO \n POR FAVOR SELECCIONE SU ACCIÓN[/b]",
            "2": "[b]HISTORIAL[/b]",
            "3": "[b]AÑADIR[/b]",
            "4": "Ayuda",
            "5": "Cambiar tema (Claro/Oscuro)",
            "6": "Inicio",
            "7": "Ingresar información",
            "8": "Elegir",
            "9": "Historial",
            "10": "Color"
        },
        "Page3": {
            "1": "[b]POR FAVOR COMPLETE ESTA PÁGINA[/b]",
            "2": "Fecha",
            "3": "Operador",
            "4": "Apertura o cierre o DD",
            "5": "Operación",
            "6": "Mención(éxito o Ic)",
            "7": "Si no hay nada, dejarlo vacío",
            "8": "[b]Validar[/b]"
        }
    },
    "de": {
        "Page1": {
            "1": "[b]BCC STEUERUNGSSOFTWARE[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]Gehen[/b]"
        },
        "Page2": {
            "1": "[b]WILLKOMMEN \n BITTE WÄHLEN SIE IHRE AKTION[/b]",
            "2": "[b]VERLAUF[/b]",
            "3": "[b]HINZUFÜGEN[/b]",
            "4": "Hilfe",
            "5": "Thema wechseln (Hell/Dunkel)",
            "6": "Startseite",
            "7": "Informationen eingeben",
            "8": "Auswählen",
            "9": "Verlauf",
            "10": "Farbe"
        },
        "Page3": {
            "1": "[b]BITTE FÜLLEN SIE DIESE SEITE AUS[/b]",
            "2": "Datum",
            "3": "Bediener",
            "4": "Öffnung oder Schließung oder DD",
            "5": "Betrieb",
            "6": "Erwähnung(Erfolg oder Ic)",
            "7": "Wenn nichts vorhanden ist, leer lassen",
            "8": "[b]Bestätigen[/b]"
        }
    },
    "zh": {  # Chinois simplifié
        "Page1": {
            "1": "[b]BCC控制软件[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]前往[/b]"
        },
        "Page2": {
            "1": "[b]欢迎 \n 请选择您的操作[/b]",
            "2": "[b]历史[/b]",
            "3": "[b]添加[/b]",
            "4": "帮助",
            "5": "切换主题（亮/暗）",
            "6": "主页",
            "7": "输入信息",
            "8": "选择",
            "9": "历史",
            "10": "颜色"
        },
        "Page3": {
            "1": "[b]请填写此页面[/b]",
            "2": "日期",
            "3": "操作员",
            "4": "开启或关闭或DD",
            "5": "操作",
            "6": "提及（成功或Ic）",
            "7": "如果没有内容，留空",
            "8": "[b]验证[/b]"
        }
    },
    "zh-tw": {  #// Chinois traditionnel
        "Page1": {
            "1": "[b]BCC控制軟體[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]前往[/b]"
        },
        "Page2": {
            "1": "[b]歡迎 \n 請選擇您的操作[/b]",
            "2": "[b]歷史[/b]",
            "3": "[b]添加[/b]",
            "4": "幫助",
            "5": "切換主題（亮/暗）",
            "6": "首頁",
            "7": "輸入資訊",
            "8": "選擇",
            "9": "歷史",
            "10": "顏色"
        },
        "Page3": {
            "1": "[b]請填寫此頁面[/b]",
            "2": "日期",
            "3": "操作員",
            "4": "開啟或關閉或DD",
            "5": "操作",
            "6": "提及（成功或Ic）",
            "7": "如果沒有內容，留空",
            "8": "[b]驗證[/b]"
        }
    },
    "ja": {  #// Japonais
        "Page1": {
            "1": "[b]BCC制御ソフトウェア[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]移動[/b]"
        },
        "Page2": {
            "1": "[b]ようこそ \n アクションを選択してください[/b]",
            "2": "[b]履歴[/b]",
            "3": "[b]追加[/b]",
            "4": "ヘルプ",
            "5": "テーマの切り替え（ライト/ダーク）",
            "6": "ホーム",
            "7": "情報を入力",
            "8": "選択",
            "9": "履歴",
            "10": "色"
        },
        "Page3": {
            "1": "[b]このページに記入してください[/b]",
            "2": "日付",
            "3": "オペレーター",
            "4": "開始または終了またはDD",
            "5": "操作",
            "6": "言及（成功またはIc）",
            "7": "何もない場合は空のままにする",
            "8": "[b]検証[/b]"
        }
    },
    "ko": {  #// Coréen
        "Page1": {
            "1": "[b]BCC 제어 소프트웨어[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]이동[/b]"
        },
        "Page2": {
            "1": "[b]환영합니다 \n 작업을 선택하세요[/b]",
            "2": "[b]기록[/b]",
            "3": "[b]추가[/b]",
            "4": "도움말",
            "5": "테마 전환 (밝음/어두움)",
            "6": "홈",
            "7": "정보 입력",
            "8": "선택",
            "9": "기록",
            "10": "색상"
        },
        "Page3": {
            "1": "[b]이 페이지를 작성해주세요[/b]",
            "2": "날짜",
            "3": "운영자",
            "4": "열기 또는 닫기 또는 DD",
            "5": "작업",
            "6": "언급(성공 또는 Ic)",
            "7": "없으면 비워두세요",
            "8": "[b]확인[/b]"
        }
    },
    "ar": {  #// Arabe
        "Page1": {
            "1": "[b]برنامج التحكم في BCC[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]انتقال[/b]"
        },
        "Page2": {
            "1": "[b]مرحباً \n يرجى اختيار إجراءك[/b]",
            "2": "[b]التاريخ[/b]",
            "3": "[b]إضافة[/b]",
            "4": "مساعدة",
            "5": "تغيير الثيم (فاتح/داكن)",
            "6": "الصفحة الرئيسية",
            "7": "إدخال المعلومات",
            "8": "اختيار",
            "9": "تاريخ",
            "10": "لون"
        },
        "Page3": {
            "1": "[b]يرجى ملء هذه الصفحة[/b]",
            "2": "التاريخ",
            "3": "المشغل",
            "4": "فتح أو إغلاق أو DD",
            "5": "العملية",
            "6": "الذكر(نجاح أو Ic)",
            "7": "إذا لم يكن هناك شيء، اتركه فارغاً",
            "8": "[b]التحقق[/b]"
        }
    },
    "ru": {  #// Russe
        "Page1": {
            "1": "[b]ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ УПРАВЛЕНИЯ BCC[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]Перейти[/b]"
        },
        "Page2": {
            "1": "[b]ДОБРО ПОЖАЛОВАТЬ \n ПОЖАЛУЙСТА, ВЫБЕРИТЕ ДЕЙСТВИЕ[/b]",
            "2": "[b]ИСТОРИЯ[/b]",
            "3": "[b]ДОБАВИТЬ[/b]",
            "4": "Помощь",
            "5": "Сменить тему (Светлая/Тёмная)",
            "6": "Главная",
            "7": "Ввести информацию",
            "8": "Выбрать",
            "9": "История",
            "10": "Цвет"
        },
        "Page3": {
            "1": "[b]ПОЖАЛУЙСТА, ЗАПОЛНИТЕ ЭТУ СТРАНИЦУ[/b]",
            "2": "Дата",
            "3": "Оператор",
            "4": "Открытие или закрытие или DD",
            "5": "Операция",
            "6": "Упоминание(успех или Ic)",
            "7": "Если ничего нет, оставить пустым",
            "8": "[b]Проверить[/b]"
        }
    },
    "pt": {  #// Portugais
        "Page1": {
            "1": "[b]SOFTWARE DE CONTROLE BCC[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]Ir[/b]"
        },
        "Page2": {
            "1": "[b]BEM-VINDO \n POR FAVOR SELECIONE SUA AÇÃO[/b]",
            "2": "[b]HISTÓRICO[/b]",
            "3": "[b]ADICIONAR[/b]",
            "4": "Ajuda",
            "5": "Mudar tema (Claro/Escuro)",
            "6": "Início",
            "7": "Inserir informação",
            "8": "Escolher",
            "9": "Histórico",
            "10": "Cor"
        },
        "Page3": {
            "1": "[b]POR FAVOR PREENCHA ESTA PÁGINA[/b]",
            "2": "Data",
            "3": "Operador",
            "4": "Abertura ou fechamento ou DD",
            "5": "Operação",
            "6": "Menção(sucesso ou Ic)",
            "7": "Se não houver nada, deixar vazio",
            "8": "[b]Validar[/b]"
        }
    },
    "it": {  #// Italien
        "Page1": {
            "1": "[b]SOFTWARE DI CONTROLLO BCC[/b]",
            "2": "[b]CEET-DRM-BCC[/b]",
            "3": "[b]Vai[/b]"
        },
        "Page2": {
            "1": "[b]BENVENUTO \n PER FAVORE SELEZIONA LA TUA AZIONE[/b]",
            "2": "[b]CRONOLOGIA[/b]",
            "3": "[b]AGGIUNGI[/b]",
            "4": "Aiuto",
            "5": "Cambia tema (Chiaro/Scuro)",
            "6": "Home",
            "7": "Inserire informazioni",
            "8": "Scegliere",
            "9": "Cronologia",
            "10": "Colore"
        },
        "Page3": {
            "1": "[b]PER FAVORE COMPILA QUESTA PAGINA[/b]",
            "2": "Data",
            "3": "Operatore",
            "4": "Apertura o chiusura o DD",
            "5": "Operazione",
            "6": "Menzione(successo o Ic)",
            "7": "Se non c'è niente, lasciare vuoto",
            "8": "[b]Convalidare[/b]"
        }
    }
}
    def __init__(self):
        super().__init__()
        self.Current_lang = "fr"

    def on_start(self):
        """Démarrage corrigé avec gestion d'erreurs"""
        try:
            # Initialiser la base de données
            self.con = sqlite3.connect("base.db")
            cur = self.con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS BCC (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                Date TEXT, 
                Heur TEXT, 
                Operator TEXT, 
                O_F_DD TEXT, 
                Operation TEXT, 
                Mension TEXT
            )""")
            self.con.commit()
            
            # Variables d'initialisation
            self.DATE = strftime("%D")
            self.PAGE4_Liste = []
            self.Data_Donne = {}
            self.index_syn = 0
            self.is_syncing = False
            self.Choix_affichage2 = "Data"
            self.Choix_affichage = "Data"
            
            # Initialiser Supabase avec gestion d'erreurs
            try:
                self.Sup = SupabaseDB(
                    supabase_url="https://jutueskohextubwszbhv.supabase.co",
                    supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dHVlc2tvaGV4dHVid3N6Ymh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxMTQ5MDUsImV4cCI6MjA3MzY5MDkwNX0.q3uKtQ3EKdpv4MDuJE0pCrBOBdCbMf9pu36RmoDNGKw"
                )
                print(f"Supabase initialisé - Statut connexion: {self.Sup.connection_status}")
            except Exception as e:
                print(f"Erreur initialisation Supabase: {e}")
                self.Sup = None
            
            # Configuration mobile
            from kivy.core.window import Window
            from kivy.utils import platform
            
            if platform in ('android', 'ios'):
                Window.softinput_mode = 'below_target'
            
            Window.bind(on_resize=self.on_window_resize)
            
            # Démarrer la vérification des pages
            self.Verifi_moi_les_pages()
            
            # Première synchronisation (différée)
            Clock.schedule_once(lambda dt: self.synchroniser(), 5)
            
        except Exception as e:
            print(f"Erreur lors du démarrage: {e}")
            import traceback
            traceback.print_exc()
        
    
    def on_window_resize(self, window, width, height):
        """Appelé quand la fenêtre change de taille (clavier apparaît/disparaît)"""
        # Optionnel: ajuster le scroll automatiquement
        pass
        
    def on_close(self):
        self.con.close()
        
    def build(self):
        self.cr = ScreenManager()
        
        # Ajouter l'écran de chargement en premier
        loading = LoadingScreen()
        self.cr.add_widget(loading)
        
        # Ajouter les autres pages
        Liste = [Page1,Page2,Page3,Page4]
        for elmt in Liste:
            self.cr.add_widget(elmt())
        
        self.cr.transition = NoTransition()
        self.cr.current = 'loading'  # Commencer par le loading
        
        return self.cr
    
    def page1(self):
        Element = self.Langue.get(self.Current_lang).get("Page1")
        Pge = self.cr.current_screen.ids

        Liste = [Pge.Page1_1,Pge.Page1_2,Pge.Page1_3]

        for elmt,elmt2 in zip(Liste,Element.keys()):
            elmt.text = Element.get(elmt2)
    
    def Verifi_moi_les_pages(self):
        """Vérification des pages corrigée"""
        try:
            # Vérifier seulement si on n'est pas sur l'écran de chargement
            if hasattr(self, 'cr') and self.cr and self.cr.current != 'loading':
                dic = {
                    "Page1": self.page1, 
                    "Page2": self.page2, 
                    "Page3": self.page3,
                    "Page4": self.page4
                }
                page_func = dic.get(self.cr.current)
                if page_func:
                    page_func()
            
            # Synchronisation périodique
            if hasattr(self, 'index_syn'):
                if self.index_syn % 20 == 0:  # Toutes les 10 secondes au lieu de 5
                    if hasattr(self, 'Sup') and self.Sup:
                        self.synchroniser()
                self.index_syn += 1
        
        except Exception as e:
            print(f"Erreur Verifi_moi_les_pages: {e}")
        
        finally:
            # Reprogrammer la vérification
            Clock.schedule_once(lambda dt: self.Verifi_moi_les_pages(), 1)
    
    def synchroniser(self):
        """Synchronisation corrigée avec gestion d'erreurs"""
        if self.is_syncing or not hasattr(self, 'Sup') or not self.Sup:
            return
        
        self.is_syncing = True
        print("Début synchronisation...")
        
        try:
            # Test de connexion
            if not self.Sup.connection_status:
                print("Pas de connexion internet - synchronisation annulée")
                return
            
            # 1. Récupérer données Supabase
            result = self.Sup.obtenir_toutes_donnees("bcc_operations")
            
            if result['success'] and result.get("data"):
                self.Data_Donne = result["data"]
                print(f"Récupéré {len(self.Data_Donne)} enregistrements de Supabase")
                
                # 2. Synchroniser: Supabase vers Local
                self.sync_supabase_to_local()
            else:
                print("Aucune donnée Supabase ou erreur de connexion")
            
            # 3. Synchroniser: Local vers Supabase
            self.sync_local_to_supabase()
            
            print("Synchronisation terminée avec succès")
            
        except Exception as e:
            print(f"Erreur synchronisation: {e}")
            # Afficher le toast seulement si l'interface est prête
            if hasattr(self, 'cr') and self.cr:
                from kivymd.toast import toast
                toast("Erreur de synchronisation", duration=2)
        
        finally:
            self.is_syncing = False
    
    def sync_supabase_to_local(self):
        """Synchronise les données Supabase vers la base locale"""
        try:
            cur = self.con.cursor()
            
            for supabase_id, supabase_record in self.Data_Donne.items():
                # Vérifier si ce record existe en local
                cur.execute("""
                    SELECT COUNT(*) FROM BCC 
                    WHERE Date = ? AND Heur = ? AND Operator = ?
                """, (supabase_record['date'], supabase_record['heur'], supabase_record['operator']))
                
                if cur.fetchone()[0] == 0:
                    # Ajouter en local
                    cur.execute("""
                        INSERT INTO BCC (Date, Heur, Operator, O_F_DD, Operation, Mension)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        supabase_record['date'],
                        supabase_record['heur'],
                        supabase_record['operator'],
                        supabase_record['o_f_dd'],
                        supabase_record['operation'],
                        supabase_record['mension']
                    ))
                    print(f"Ajouté en local: {supabase_record['date']} - {supabase_record['operator']}")
            
            self.con.commit()
            
        except Exception as e:
            print(f"Erreur sync Supabase->Local: {e}")

    def sync_local_to_supabase(self):
        """Synchronise les données locales vers Supabase"""
        try:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM BCC")
            local_records = cur.fetchall()
            
            for local_record in local_records:
                local_data = list(local_record[1:])  # Sans l'ID local
                
                # Vérifier si ce record existe déjà sur Supabase
                exists_online = False
                for supabase_id, supabase_record in self.Data_Donne.items():
                    if (supabase_record['date'] == local_data[0] and 
                        supabase_record['heur'] == local_data[1] and
                        supabase_record['operator'] == local_data[2]):
                        exists_online = True
                        break
                
                if not exists_online:
                    # Ajouter à Supabase
                    add_result = self.Sup.ajouter_donnees("bcc_operations", local_data)
                    if add_result['success']:
                        print(f"Ajouté à Supabase: {local_data[0]} - {local_data[2]}")
                    else:
                        print(f"Erreur ajout Supabase: {add_result.get('error', 'Inconnue')}")
            
        except Exception as e:
            print(f"Erreur sync Local->Supabase: {e}")
 
    def Changer_font1(self,instance):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == 'Light' else "Light"
    
    def Changer_font2(self,instance):
        Liste = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        items = []
        for elmt in Liste:
            Add = {
                "text":elmt,
                "on_release":lambda x = elmt : self.COLOR(x)
            }
            items.append(Add)
        
        self.COLOR2 = MDDropdownMenu(
            caller = instance,
            items = items,
            width_mult = 3,
        )

        self.COLOR2.open()
    
    def COLOR(self,x):
        self.theme_cls.primary_palette = x
        self.COLOR2.dismiss()

    #====== Fonction pour les affichages intuitives de la page 3 ========
    def affichage_intuitive_page3(self):
        """Version avec double-tap pour ouvrir le menu, clic simple pour saisir"""
        Pge = self.cr.current_screen.ids
        cur = self.con.cursor()
        
        # Récupérer les données uniques
        cur.execute("SELECT DISTINCT Operator FROM BCC WHERE Operator IS NOT NULL AND Operator != '' ORDER BY Operator")
        operateurs_uniques = list(set([row[0] for row in cur.fetchall()]))
        
        #Ici Mension == Operation
        cur.execute("SELECT DISTINCT Operation FROM BCC WHERE Operation IS NOT NULL AND Operation != '' ORDER BY Mension")
        mentions_uniques = list(set([row[0] for row in cur.fetchall()]))
        
        # Créer le menu pour les opérateurs
        if operateurs_uniques:
            items_operateurs = []
            for op in operateurs_uniques:
                items_operateurs.append({
                    "text": op,
                    "on_release": lambda x=op: self.selection_depuis_menu(x, Pge.Page3_3)
                })
            
            self.menu_operateurs = MDDropdownMenu(
                caller=Pge.Page3_3,
                items=items_operateurs,
                width_mult=5
            )
        
        # Créer le menu pour les mentions
        if mentions_uniques:
            items_mentions = []
            for mention in mentions_uniques:
                items_mentions.append({
                    "text": mention,
                    "on_release": lambda x=mention: self.selection_depuis_menu(x, Pge.Page3_5)
                })
            
            self.menu_mentions = MDDropdownMenu(
                caller=Pge.Page3_5,
                items=items_mentions,
                width_mult=4
            )
        
        # Nettoyer les anciens binds
        try:
            Pge.Page3_3.unbind(on_touch_down=self.double_tap_operateur)
            Pge.Page3_5.unbind(on_touch_down=self.double_tap_mention)
        except:
            pass
        
        # Lier les nouveaux événements
        Pge.Page3_3.bind(on_touch_down=self.double_tap_operateur)
        Pge.Page3_5.bind(on_touch_down=self.double_tap_mention)
        
        # S'assurer que les champs sont modifiables
        Pge.Page3_3.readonly = False
        Pge.Page3_5.readonly = False

    def double_tap_operateur(self, instance, touch):
        """Gestion du double-tap pour les opérateurs"""
        if instance.collide_point(*touch.pos):
            if touch.is_double_tap and hasattr(self, 'menu_operateurs'):
                self.menu_operateurs.open()
                return True
            # Clic simple : permettre la saisie normale
            instance.focus = True
            instance.readonly = False
        return False

    def double_tap_mention(self, instance, touch):
        """Gestion du double-tap pour les mentions"""
        if instance.collide_point(*touch.pos):
            if touch.is_double_tap and hasattr(self, 'menu_mentions'):
                self.menu_mentions.open()
                return True
            # Clic simple : permettre la saisie normale
            instance.focus = True
            instance.readonly = False
        return False

    def selection_depuis_menu(self, valeur, champ):
        """Quand on sélectionne une valeur du menu"""
        champ.text = valeur
        champ.readonly = False  # Reste modifiable après sélection
        
        # Fermer le bon menu
        if hasattr(self, 'menu_operateurs') and champ == self.cr.current_screen.ids.Page3_3:
            self.menu_operateurs.dismiss()
        elif hasattr(self, 'menu_mentions') and champ == self.cr.current_screen.ids.Page3_5:
            self.menu_mentions.dismiss()
    #============= Fin ================================= FIn ============
    def page3(self):
        Element = self.Langue.get(self.Current_lang).get("Page3")
        Pge = self.cr.current_screen.ids


        Liste1 = [Pge.Page2_7,Pge.Page2_9,Pge.Page2_8,Pge.Page2_10,Pge.Page2_11]
        for elmt in Liste1:
            elmt.theme_text_color = "Custom"
            if Liste1.index(elmt) == 2:
                elmt.icon_color = [1,1,1,1]
            else:
                elmt.icon_color = [0,0,0,1]

        Liste = [Pge.Page3_1]
        Liste2 = [Pge.Page3_2,Pge.Page3_3,Pge.Page3_4,Pge.Page3_5,Pge.Page3_6,Pge.Page3_6]
        Liste3 = [Pge.Page3_7]
        Pge.Page2_4.text = self.Current_lang
        Val = None
        for elmt,elmt2 in zip(Liste+Liste2+Liste3,Element.keys()):
            if Val == elmt:
                elmt.helper_text = Element.get(elmt2)
            elif  elmt not in Liste+Liste3:
                elmt.hint_text = Element.get(elmt2)
            else:
                elmt.text = Element.get(elmt2)
            Val = elmt
            
        
        Date = strftime("%D")
        Pge.Page3_2.text = Date
        Pge.Page3_2.readonly = True
        Pge.Page3_4.readonly = True

        #Essay de fair la fonction rappelle 

        items = [{ #Ca c'est pour Ouverture ou fermerture ou DD
            "text":"O",
            "on_release":lambda x = "O" : self.Clic(x)
        },
        {
            "text":"F",
            "on_release":lambda x = "F" : self.Clic(x)
        },
        {
            "text":"DD",
            "on_release":lambda x = "DD" : self.Clic(x)
        }
        ]
        self.Operation = MDDropdownMenu(
            caller = Pge.Page3_4,
            items = items,
            width_mult = 3,
        )

        Pge.Page3_4.bind(on_touch_down = self.Open_Menu)
        self.affichage_intuitive_page3() #Pour les affichage intuitive
        
       
    def Open_Menu(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.Operation.open()
            return True
        return False
    
    def Clic(self,x):
        Pge = self.cr.current_screen.ids
        self.Operation.dismiss()
        Pge.Page3_4.text = x
        
    #Fonction valider pour la Page3
    def Valider_3(self,instance):
        Pge = self.cr.current_screen.ids
        Liste = [Pge.Page3_2,Pge.Page3_3,Pge.Page3_4,Pge.Page3_5]
        Error = False
        for elmt in Liste:
            if elmt.text =="":
                elmt.error = True
                Error = True
        
        if not Error:
            try:
                Pge = self.cr.current_screen.ids
                Liste2 = [Pge.Page3_2,Pge.Page3_3,Pge.Page3_4,Pge.Page3_5,Pge.Page3_6]
                cur = self.con.cursor()
                cur.execute("Insert into BCC (Date,Heur,Operator,O_F_DD,Operation,Mension) values (?,?,?,?,?,?)",tuple([Liste2[0].text , str(strftime("%T"))] + [elmt.text for elmt in Liste2[1:]]))
                self.con.commit()

                toast("Ajout effectué avec succes!")
                for elmt in Liste2[1:]:
                    elmt.text = ""

            except Exception as e:
                toast(text = f"Erreur : {e}",background=[1,0,0,1],duration=3.5)

    def Recharge_date(self,instance):
        cur = self.con.cursor()
        Tous = cur.execute("SELECT * FROM  BCC")

        Date = set()
        for elmt in Tous:
            Date.add(elmt[1])
        
        items = []
        for elmt in Date:
            dic = {
                "text":elmt,
                "on_release": lambda btn = instance,x = elmt : self.Select2(btn,x)
            }
            items.append(dic)

        self.Operation2 = MDDropdownMenu(
            caller = instance,
            items = items,
            width_mult = 5,
        )

        self.Operation2.open()

    def Select2(self,instance,x):
        instance.text = f"[b]{x}[/b]"
        self.DATE = x
        self.page4()
        self.Operation2.dismiss()

    def page4(self):
        cur = self.con.cursor()
        Tous = cur.execute("SELECT * FROM BCC")
        
        Pge = self.cr.current_screen.ids
        Liste1 = [Pge.Page2_7,Pge.Page2_9,Pge.Page2_8,Pge.Page2_10,Pge.Page2_11]
        for elmt in Liste1:
            elmt.theme_icon_color = "Custom"
            if Liste1.index(elmt) == 3:
                elmt.icon_color = [1,1,1,1]
            else:
                elmt.icon_color = [0,0,0,1]

        Pge.Page4_But.text = f"[b]{self.DATE}[/b]"
        Veux = []
        for elmt in Tous:
            if elmt[1] == self.DATE:
                Veux.append(list(elmt))
        
        #try:
        Ici = self.cr.current_screen.ids.Page4_2

        if Veux:  # Si on a des données
            if self.PAGE4_Liste == [] or self.PAGE4_Liste != Veux or self.Choix_affichage != self.Choix_affichage2:
                self.PAGE4_Liste = Veux
                self.Choix_affichage2 = self.Choix_affichage
                Ici.clear_widgets()
                if self.Choix_affichage == "Data": #Ca c'est pour les Buttons qui permet de faire le choix d'affichage
                    Ici.add_widget(self.create_data_table(Veux))
                elif self.Choix_affichage == "Card":
                    self.Afficher_moi_les_infos_en_card(Ici,Veux)
        
                
                
        else:  # Si pas de données
            Ici.clear_widgets()
            Ici.add_widget(self.create_empty_message())
        #except Exception as e:
        #toast(text = f"Erreur : {e}",background=[1,0,0,1],duration=3.5)
            #pass

    def Changer_show_page4(self,instance):
        self.Choix_affichage = "Data" if self.Choix_affichage == "Card" else "Card"
    
    
    def Help(self,instance):
        Box = MDBoxLayout(
            orientation = "vertical",
            adaptive_height = True,
            spacing = 30,
            padding = 10
        )

        Card = MDCard(
            radius = [110],
            size_hint = (None,None),
            size = (215,215),
            pos_hint = {"center_x":.5,"center_y":.5},
            md_bg_color = [1,1,0,1]

        )

        Img = Image(
            source = "My_Image.png",
            #size_hint = (None,None),
            #size = (80,80),
            pos_hint = {"center_x":.5,"center_y":.5}

        )

        Card.add_widget(Img)

        Box.add_widget(Card)

        Text = MDLabel(
            text = "Elisée ATIKPO",
            font_style = "H5",
            halign = "center",
            theme_text_color = "Primary",
        )

        Box.add_widget(Text)

        Text2 = MDLabel(
            text = "[b]Contact:[/b] +228 96 44 40 55",
            markup = True,
            font_style = "H6",
            theme_text_color = "Secondary",
        )

        Box.add_widget(Text2)

        Text3 = MDLabel(
            text = "[b]Mail:[/b] eliseeatikpo10@gmail.com",
            markup = True,
            font_style = "H6",
            theme_text_color = "Secondary",
        )

        Box.add_widget(Text3)

        Text4 = MDLabel(
            text = "Dieu Est Grand",
            markup = True,
            font_style = "Subtitle1",
            halign = "center",
        )

        Box.add_widget(Text4)

        self.MD_Help = MDDialog(
            title = "Aide/Help",
            type = "custom",
            content_cls = Box,
            buttons = [
                MDFlatButton(
                    text = "FERMER",
                    theme_text_color = "Custom",
                    text_color = (.2,.6,1,1),
                    on_release = self.Close_help,
                )
            ]
        )
        
        self.MD_Help.open()
    
    def Close_help(self,instance):
        self.MD_Help.dismiss()

    def Appui_Icon_page4(self, instance):
        Pge = self.cr.current_screen.ids
        Liste = [Pge.Page2_4, Pge.Page2_5, Pge.Page2_6, Pge.Page2_11]
        Liste = [elmt.text for elmt in Liste] + ["Mode affichage"]
        self.Liste = Liste
        Icons = ["web", 'information', "brightness-6", "palette","cog"]
        
        Items = []
        for elmt1, elmt2 in zip(Liste, Icons):
            Add = {
                "text": elmt1,
                "icon": elmt2,
                # CORRECTION: Utiliser une lambda pour passer les bons arguments
                "on_release": lambda btn = instance , text=elmt1: self.Faire_Icon_4(btn, text)
            }
            Items.append(Add)

        self.INSTANCE = instance
        
        self.Operation3 = MDDropdownMenu(
            caller=instance,
            items=Items,
            width_mult=3,
        )
        
        instance.icon = "close"
        self.Operation3.open()
    

    def Afficher_moi_les_infos_en_card(self,Lieu,data):
        Lieu.orientation =  'vertical'
        Lieu.padding="16dp"
        Lieu.spacing="16dp"

        scroll = MDScrollView(
            do_scroll_x = False,
            do_scroll_y = True
        )
        
        # Layout vertical pour les cartes dans la ScrollView
        cards_layout = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            #size_hint_y=None,
            adaptive_height = True,
            padding="8dp"
        )
        #cards_layout.bind(minimum_height=cards_layout.setter('height'))

        for donnees in data:
            carte = But_styler(donnees)
            cards_layout.add_widget(carte)
        
        # Ajout du layout des cartes dans la ScrollView
        scroll.add_widget(cards_layout)

        Lieu.clear_widgets()
        Lieu.add_widget(scroll)

    def create_data_table(self, data):
        # Définir les noms des colonnes (correspondant à la table BCC)
        column_data = [
            ("ID", dp(20)),
            ("Date", dp(30)),
            ("Heur", dp(30)),
            ("Opérateur", dp(30)),
            ("O/F/DD", dp(20)),
            ("Opération", dp(50)),
            ("Mention", dp(30))
        ]
        # Convertir les données en tuples pour MDDataTable
        row_data = [tuple(row) for row in data]
        # Créer le MDDataTable
        data_table = MDDataTable(
            size_hint=(1, 1),
            column_data=column_data,
            row_data=row_data,
            elevation=2,
            use_pagination=True,  # Activer la pagination si beaucoup de données
            rows_num=10,  # Nombre de lignes par page
            on_row_press=lambda *args: None,
            check=False  # Désactiver les cases à cocher (optionnel)
            
        )
        
        return data_table

    def Appui_Icon_page2(self, instance):
        Pge = self.cr.current_screen.ids
        Liste = [Pge.Page2_4, Pge.Page2_5, Pge.Page2_6, Pge.Page2_11]
        Liste = [elmt.text for elmt in Liste]
        self.Liste = Liste
        print(Liste)
        Icons = ["web", 'information', "brightness-6", "palette"]
        
        Items = []
        for elmt1, elmt2 in zip(Liste, Icons):
            Add = {
                "text": elmt1,
                "icon": elmt2,
                # CORRECTION: Utiliser une lambda pour passer les bons arguments
                "on_release": lambda btn = instance , text=elmt1: self.Faire_Icon(btn, text)
            }
            Items.append(Add)

        self.INSTANCE = instance
        
        self.Operation3 = MDDropdownMenu(
            caller=instance,
            items=Items,
            width_mult=3,
        )
        
        instance.icon = "close"
        self.Operation3.open()
    
    def create_empty_message(self):
        """Créer un message quand il n'y a pas de données"""
        
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            adaptive_height=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        # Message principal
        message = MDLabel(
            text=f"Aucune donnée pour le {self.DATE}",
            halign="center",
            theme_text_color="Primary",
            font_style="H6"
        )
        
        # Message secondaire
        submessage = MDLabel(
            text="Ajoutez des opérations pour voir les données ici",
            halign="center",
            theme_text_color="Secondary",
            font_style="Caption"
        )
        
        # Bouton pour ajouter des données (optionnel)
        add_button = MDRaisedButton(
            text="[b]Ajouter une opération[/b]",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.Next_But(None, 3)  # Aller à la page de saisie
        )
        
        layout.add_widget(message)
        layout.add_widget(submessage)
        layout.add_widget(add_button)
        
        return layout

    # Fonction corrigée pour accepter les bons paramètres
    def Faire_Icon(self, instance,x):
        """
        calling_button: Le bouton qui a ouvert le menu
        menu_item: L'item du menu qui a été cliqué
        selected_text: Le texte de l'item sélectionné
        """
        #x = selected_text  # ou menu_item.text si vous préférez
        
        dic = {
            self.Liste[0]: self.Changer_language,
            self.Liste[1]: self.Help,
            self.Liste[2]: self.Changer_font1,
            self.Liste[-1]: self.Changer_font2
        }
        
        func = dic.get(x)
        if func is not None:
            func(instance)  # Passer le bouton original
    
        # Fermer le menu et remettre l'icône
        self.Operation3.dismiss()
        self.INSTANCE.icon = "plus"

    def page2(self):
        Element = self.Langue.get(self.Current_lang).get("Page2")
        Pge = self.cr.current_screen.ids

        Liste1 = [Pge.Page2_7,Pge.Page2_9,Pge.Page2_8,Pge.Page2_10]
        for elmt in Liste1:
            elmt.theme_text_color = "Custom"
            if Liste1.index(elmt) == 1:
                elmt.icon_color = [1,1,1,1]
            else:
                elmt.icon_color = [0,0,0,1]

        Liste = [Pge.Page2_1,Pge.Page2_2,Pge.Page2_3,Pge.Page2_5,Pge.Page2_6,Pge.Page2_7,Pge.Page2_8,Pge.Page2_9,Pge.Page2_10]

        Pge.Page2_4.text = self.Current_lang

        for elmt,elmt2 in zip(Liste,Element.keys()):
            elmt.text = Element.get(elmt2)
    
    def Add(self,instance):
        self.Next(3)
    
    def history(self,instance):
        self.Next(4)
        
    def Changer_language(self, instance):
        self.langues_disponibles = [
            {"text": "Français", "code": "fr"},
            {"text": "English", "code": "en"},
            {"text": "Español", "code": "es"},
            {"text": "Deutsch", "code": "de"},
            {"text": "中文 (简体)", "code": "zh"},
            {"text": "中文 (繁體)", "code": "zh-tw"},
            {"text": "日本語", "code": "ja"},
            {"text": "한국어", "code": "ko"},
            {"text": "العربية", "code": "ar"},
            {"text": "Русский", "code": "ru"},
            {"text": "Português", "code": "pt"},
            {"text": "Italiano", "code": "it"},
        ]
        
        menu = []
        for elmt in self.langues_disponibles:
            menu.append(
                {
                    "text":elmt["text"],
                    "on_release":lambda x = elmt["code"],btn = instance : self.selecter_Lang(btn,x)
                }
            )
        
        self.Menu = MDDropdownMenu(
            caller=instance,
            items=menu,
            width_mult=4,  # ← Correction 6: width_mult, pas width_milt
            max_height=dp(200),
            border_margin=dp(8),
        )
        
        self.Menu.open()
    
    def selecter_Lang(self,instance,code):
        #dic = {"[b]fr[/b]":"en" , "[b]en[/b]":"fr"}
        self.Current_lang = code#dic.get(instance.text)
        instance.text = f"[b]{self.Current_lang}[/b]"
        self.Menu.dismiss()
    
    def Go(self,intance):
        self.Next()
    
    def Next(self,val = None):
        Pge = self.cr.current
        self.cr.current = f"Page{int(Pge.split('e')[-1])+1 if val == None else val}"
    
    def Next_But(self,intance,val = None):
        self.Next(val)
    
#======= Les nouveaux fonctions ======
# Ajoutez ces méthodes dans votre classe BCC() :

    def exporter_donnees_bcc(self, formats=['pdf']):
        """
        Exporter les données de la date sélectionnée dans Page4
        
        Args:
            formats (list): Liste des formats d'export ('pdf', 'xlsx', 'docx')
        
        Returns:
            dict: Dictionnaire des fichiers créés
        """
        try:
            # Récupérer les données pour la date actuelle
            cur = self.con.cursor()
            cur.execute("SELECT * FROM BCC WHERE Date = ?", (self.DATE,))
            donnees = cur.fetchall()
            
            if donnees:
                # Préparer les données (exclure l'ID de la base de données)
                data_export = [list(self.redreser_les_donne(row[1:])) for row in donnees]  # row[1:] exclut l'ID
                headers = ['Date', 'Heure', 'Opérateur', 'O/F/DD', 'Opération', 'Mention']
                
                # Créer l'exporteur
                from Export import DataExporter  # Assurez-vous que le nom du fichier est correct
                exporter = DataExporter(output_dir="exports_bcc")
                
                # Nettoyer le nom de fichier (remplacer les / par _)
                date_clean = self.DATE.replace('/', '_').replace(' ', '_')
                
                files = exporter.export_data(
                    data_export,
                    f"rapport_bcc_{date_clean}",
                    formats=formats,
                    title=f"Rapport BCC - Contrôle des Opérations du {self.DATE}",
                    headers=headers
                )
                
                # Notification de succès
                if files:
                    message = f"Export réussi ! {len(files)} fichier(s) créé(s)"
                    toast(message, duration=3)
                    print("Fichiers créés:", files)
                    return files
                else:
                    toast("Erreur lors de l'export", background=[1,0,0,1])
                    return {}
                    
            else:
                toast(f"Aucune donnée à exporter pour le {self.DATE}")
                return {}
                
        except ImportError as e:
            toast("Module d'export non trouvé", background=[1,0,0,1])
            print(f"Erreur import: {e}")
            return {}
        except Exception as e:
            toast("Erreur lors de l'export", background=[1,0,0,1])
            print(f"Erreur export: {e}")
            return {}
    
    def redreser_les_donne(self, elmt):
        """Fonction corrigée pour formater les données d'export"""
        ret = []
        for cell in elmt:
            # Convertir en string et limiter la longueur
            cell_str = str(cell)
            # Diviser en lignes si trop long (tous les 20 caractères)
            if len(cell_str) > 20:
                lines = [cell_str[i:i+20] for i in range(0, len(cell_str), 20)]
                formatted_cell = '\n'.join(lines)
            else:
                formatted_cell = cell_str
            ret.append(formatted_cell)
        return tuple(ret)
            
    def exporter_toutes_donnees_bcc(self, formats=['pdf']):
        """
        Exporter TOUTES les données BCC (toutes dates confondues)
        
        Args:
            formats (list): Liste des formats d'export
        
        Returns:
            dict: Dictionnaire des fichiers créés
        """
        try:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM BCC ORDER BY Date, Heur")
            toutes_donnees = cur.fetchall()
            
            if toutes_donnees:
                # Préparer les données
                data_export = [list(self.redreser_les_donne(row[1:])) for row in toutes_donnees]
                headers = ['Date', 'Heure', 'Opérateur', 'O/F/DD', 'Opération', 'Mention']
                
                # Créer l'exporteur
                from Export import DataExporter
                exporter = DataExporter(output_dir="exports_bcc")
                
                # Utiliser la date du jour pour le nom du fichier
                from datetime import datetime
                today = datetime.now().strftime("%Y%m%d")

                files = exporter.export_data(
                    data_export,
                    f"rapport_bcc_complet_{today}",
                    formats=formats,
                    title="Rapport BCC - Historique Complet des Opérations",
                    headers=headers
                )
                
                if files:
                    message = f"Export complet réussi ! {len(files)} fichier(s) - {len(toutes_donnees)} enregistrements"
                    toast(message, duration=4)
                    return files
                else:
                    toast("Erreur lors de l'export complet", background=[1,0,0,1])
                    return {}
                    
            else:
                toast("Aucune donnée dans la base")
                return {}
                
        except Exception as e:
            toast("Erreur lors de l'export complet", background=[1,0,0,1])
            print(f"Erreur: {e}")
            return {}

    def choisir_formats_export(self, instance):
        """
        Ouvrir un menu pour choisir les formats d'export
        """
        formats_disponibles = [
            {"text": "PDF seulement", "formats": ["pdf"], "icon": "file-pdf-box"},
            {"text": "Excel seulement", "formats": ["xlsx"], "icon": "file-excel-box"},
            {"text": "Word seulement", "formats": ["docx"], "icon": "file-word-box"},
            {"text": "PDF + Excel", "formats": ["pdf", "xlsx"], "icon": "file-multiple"},
            {"text": "Tous les formats", "formats": ["pdf", "xlsx", "docx"], "icon": "file-export"},
        ]
        
        menu_items = []
        for option in formats_disponibles:
            menu_items.append({
                "text": option["text"],
                "icon": option["icon"],
                "on_release": lambda x=option["formats"]: self.lancer_export_avec_formats(x)
            })
        
        self.menu_export = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
        )
        
        self.menu_export.open()

    def lancer_export_avec_formats(self, formats):
        """
        Lancer l'export avec les formats choisis
        """
        self.menu_export.dismiss()
        
        # Demander quel type d'export (date actuelle ou complet)
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            size_hint_y=None,
            height="90dp"
        )
        
        btn_date_actuelle = MDRaisedButton(
            text=f"Exporter le {self.DATE}",
            size_hint_y=None,
            height="40dp",
            on_release=lambda x: self.choisir_emplacement_export(formats, False)  # Passe par choix d'emplacement(formats, False)
        )
        
        btn_tout = MDRaisedButton(
            text="Exporter tout l'historique",
            size_hint_y=None,
            height="40dp",
            on_release=lambda x: self.choisir_emplacement_export(formats, True)
        )
        
        content_layout.add_widget(btn_date_actuelle)
        content_layout.add_widget(btn_tout)
        
        self.dialog_export = MDDialog(
            title="Type d'export",
            type="custom",
            content_cls=content_layout,
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    theme_text_color="Custom",
                    text_color=(.5, .5, .5, 1),
                    on_release=self.annuler_export
                ),
            ],
        )
        
        self.dialog_export.open()

    def confirmer_export(self, formats, export_complet):
        """
        Confirmer et lancer l'export
        """
        self.dialog_export.dismiss()
        
        if export_complet:
            self.exporter_toutes_donnees_bcc(formats)
        else:
            self.exporter_donnees_bcc(formats)

    def annuler_export(self, instance):
        """
        Annuler l'export
        """
        self.dialog_export.dismiss()

    # Modification de la fonction Faire_Icon_4 pour ajouter l'export
    def Faire_Icon_4(self, instance, x):
        """
        Version modifiée avec option d'export
        """
        # Ajouter l'export dans la liste des options
        dic = {
            self.Liste[0]: self.Changer_language,
            self.Liste[1]: self.Help,
            self.Liste[2]: self.Changer_font1,
            self.Liste[3]: self.Changer_font2,
            self.Liste[4]: self.Changer_show_page4,
            "Export": self.choisir_formats_export,  # Nouvelle option
        }
        
        func = dic.get(x)
        if func is not None:
            func(instance)

        # Fermer le menu et remettre l'icône
        self.Operation3.dismiss()
        self.INSTANCE.icon = "plus"

    # Modification de Appui_Icon_page4 pour inclure l'export
    def Appui_Icon_page4(self, instance):
        Pge = self.cr.current_screen.ids
        Liste = [Pge.Page2_4, Pge.Page2_5, Pge.Page2_6, Pge.Page2_11]
        Liste = [elmt.text for elmt in Liste] + ["Mode affichage", "Export"]
        self.Liste = Liste
        Icons = ["web", 'information', "brightness-6", "palette", "cog", "export"]
        
        Items = []
        for elmt1, elmt2 in zip(Liste, Icons):
            Add = {
                "text": elmt1,
                "icon": elmt2,
                "on_release": lambda btn=instance, text=elmt1: self.Faire_Icon_4(btn, text)
            }
            Items.append(Add)

        self.INSTANCE = instance
        
        self.Operation3 = MDDropdownMenu(
            caller=instance,
            items=Items,
            width_mult=3,
        )
        
        instance.icon = "close"
        self.Operation3.open()

    # Méthode pour ajouter un bouton d'export direct en Page4
    def ajouter_bouton_export_page4(self):
        """
        Ajouter un bouton d'export visible en Page4
        """
        Pge = self.cr.current_screen.ids
        
        # Vérifier si le bouton n'existe pas déjà
        if not hasattr(self, 'btn_export_ajouté'):
            btn_export = MDRaisedButton(
                text="📊 Export",
                pos_hint={"center_x": 0.15, "center_y": 0.05},
                size_hint=(0.25, 0.06),
                on_release=self.choisir_formats_export
            )
            
            # Ajouter le bouton à la page (ajustez selon votre layout)
            if hasattr(Pge, 'Page4_layout'):  # Si vous avez un layout principal
                Pge.Page4_layout.add_widget(btn_export)
            
            self.btn_export_ajouté = True
    # Ajoutez ces méthodes à votre classe BCC() après les fonctions d'export existantes

    def choisir_emplacement_export(self, formats, export_complet=False):
        """
        Permettre à l'utilisateur de choisir l'emplacement d'export
        """
        from kivy.utils import platform
        
        if platform == 'android':
            # Sur Android, proposer des emplacements prédéfinis
            self.proposer_emplacements_android(formats, export_complet)
        else:
            # Sur desktop, utiliser un file chooser
            self.proposer_emplacements_desktop(formats, export_complet)

    def proposer_emplacements_android(self, formats, export_complet):
        """
        Proposer des emplacements d'export pour Android
        """
        # Emplacements typiques sur Android
        emplacements = [
            {"text": "Dossier par défaut (exports_bcc)", "path": "exports_bcc", "icon": "folder"},
            {"text": "Documents", "path": "/storage/emulated/0/Documents/BCC_Exports", "icon": "file-document"},
            {"text": "Téléchargements", "path": "/storage/emulated/0/Download/BCC_Exports", "icon": "download"},
            {"text": "Stockage externe", "path": "/storage/emulated/0/BCC_Exports", "icon": "sd"},
            {"text": "Personnalisé...", "path": "custom", "icon": "folder-edit"}
        ]
        
        menu_items = []
        for emplacement in emplacements:
            menu_items.append({
                "text": emplacement["text"],
                "icon": emplacement["icon"],
                "on_release": lambda path=emplacement["path"]: self.confirmer_emplacement(path, formats, export_complet)
            })
        
        self.menu_emplacement = MDDropdownMenu(
            caller=None,  # Sera défini lors de l'appel
            items=menu_items,
            width_mult=5,
        )
        
        # Créer un dialog pour afficher le menu
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="300dp"
        )
        
        title_label = MDLabel(
            text="Choisissez l'emplacement d'export:",
            font_style="H6",
            size_hint_y=None,
            height="40dp"
        )
        content_layout.add_widget(title_label)
        
        # Ajouter les boutons d'emplacement
        for emplacement in emplacements:
            btn = MDRaisedButton(
                text=emplacement["text"],
                size_hint_y=None,
                height="40dp",
                on_release=lambda x, path=emplacement["path"]: self.confirmer_emplacement(path, formats, export_complet)
            )
            content_layout.add_widget(btn)
        
        self.dialog_emplacement = MDDialog(
            title="Emplacement d'export",
            type="custom",
            content_cls=content_layout,
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    theme_text_color="Custom",
                    text_color=(.5, .5, .5, 1),
                    on_release=self.annuler_emplacement
                ),
            ],
        )
        
        self.dialog_emplacement.open()

    def proposer_emplacements_desktop(self, formats, export_complet):
        """
        Proposer des emplacements d'export pour desktop
        """
        import os
        from pathlib import Path
        
        # Emplacements typiques sur desktop
        home = Path.home()
        emplacements = [
            {"text": "Dossier par défaut (exports_bcc)", "path": "exports_bcc"},
            {"text": "Bureau", "path": str(home / "Bureau" / "BCC_Exports")},
            {"text": "Documents", "path": str(home / "Documents" / "BCC_Exports")},
            {"text": "Téléchargements", "path": str(home / "Downloads" / "BCC_Exports")},
            {"text": "Personnalisé...", "path": "custom"}
        ]
        
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="250dp"
        )
        
        title_label = MDLabel(
            text="Choisissez l'emplacement d'export:",
            font_style="H6",
            size_hint_y=None,
            height="40dp"
        )
        content_layout.add_widget(title_label)
        
        for emplacement in emplacements:
            btn = MDRaisedButton(
                text=emplacement["text"],
                size_hint_y=None,
                height="40dp",
                on_release=lambda x, path=emplacement["path"]: self.confirmer_emplacement(path, formats, export_complet)
            )
            content_layout.add_widget(btn)
        
        self.dialog_emplacement = MDDialog(
            title="Emplacement d'export",
            type="custom",
            content_cls=content_layout,
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    theme_text_color="Custom",
                    text_color=(.5, .5, .5, 1),
                    on_release=self.annuler_emplacement
                ),
            ],
        )
        
        self.dialog_emplacement.open()

    def saisir_emplacement_personnalise(self, formats, export_complet):
        """
        Permettre la saisie d'un emplacement personnalisé
        """
        from kivymd.uix.textfield import MDTextField
        
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint_y=None,
            height="150dp"
        )
        
        info_label = MDLabel(
            text="Entrez le chemin complet du dossier:",
            font_style="Subtitle1",
            size_hint_y=None,
            height="40dp"
        )
        
        self.path_field = MDTextField(
            hint_text="Ex: /storage/emulated/0/MonDossier ou C:/Users/Username/MonDossier",
            text="/storage/emulated/0/BCC_Exports",  # Valeur par défaut
            multiline=False,
            size_hint_y=None,
            height="50dp"
        )
        
        exemple_label = MDLabel(
            text="Le dossier sera créé s'il n'existe pas.",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="30dp"
        )
        
        content_layout.add_widget(info_label)
        content_layout.add_widget(self.path_field)
        content_layout.add_widget(exemple_label)
        
        self.dialog_path = MDDialog(
            title="Emplacement personnalisé",
            type="custom",
            content_cls=content_layout,
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    theme_text_color="Custom",
                    text_color=(.5, .5, .5, 1),
                    on_release=self.annuler_path_personnalise
                ),
                MDFlatButton(
                    text="CONFIRMER",
                    theme_text_color="Custom",
                    text_color=(.2, .6, 1, 1),
                    on_release=lambda x: self.confirmer_path_personnalise(formats, export_complet)
                ),
            ],
        )
        
        self.dialog_path.open()

    def confirmer_emplacement(self, path, formats, export_complet):
        """
        Confirmer l'emplacement choisi et lancer l'export
        """
        self.dialog_emplacement.dismiss()
        
        if path == "custom":
            # Ouvrir la saisie personnalisée
            self.saisir_emplacement_personnalise(formats, export_complet)
        else:
            # Utiliser l'emplacement choisi
            self.lancer_export_avec_emplacement(path, formats, export_complet)

    def confirmer_path_personnalise(self, formats, export_complet):
        """
        Confirmer le chemin personnalisé
        """
        path = self.path_field.text.strip()
        self.dialog_path.dismiss()
        
        if path:
            self.lancer_export_avec_emplacement(path, formats, export_complet)
        else:
            toast("Veuillez entrer un chemin valide", background=[1,0,0,1])

    def annuler_emplacement(self, instance):
        """
        Annuler le choix d'emplacement
        """
        self.dialog_emplacement.dismiss()

    def annuler_path_personnalise(self, instance):
        """
        Annuler la saisie du chemin personnalisé
        """
        self.dialog_path.dismiss()

    def lancer_export_avec_emplacement(self, output_dir, formats, export_complet):
        """
        Lancer l'export avec l'emplacement spécifié
        """
        try:
            # Créer le dossier s'il n'existe pas
            from pathlib import Path
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            if export_complet:
                self.exporter_toutes_donnees_bcc_custom(formats, output_dir)
            else:
                self.exporter_donnees_bcc_custom(formats, output_dir)
                
        except Exception as e:
            toast(f"Erreur création dossier: {str(e)}", background=[1,0,0,1])

    def exporter_donnees_bcc_custom(self, formats=['pdf'], output_dir="exports_bcc"):
        """
        Version modifiée avec emplacement personnalisé
        """
        try:
            # Récupérer les données pour la date actuelle
            cur = self.con.cursor()
            cur.execute("SELECT * FROM BCC WHERE Date = ?", (self.DATE,))
            donnees = cur.fetchall()
            
            if donnees:
                # Préparer les données (exclure l'ID de la base de données)
                data_export = [list(self.redreser_les_donne(row[1:])) for row in donnees]
                headers = ['Date', 'Heure', 'Opérateur', 'O/F/DD', 'Opération', 'Mention']
                
                # Créer l'exporteur avec l'emplacement personnalisé
                from Export import DataExporter
                exporter = DataExporter(output_dir=output_dir)
                
                # Nettoyer le nom de fichier
                date_clean = self.DATE.replace('/', '_').replace(' ', '_')
                
                files = exporter.export_data(
                    data_export,
                    f"rapport_bcc_{date_clean}",
                    formats=formats,
                    title=f"Rapport BCC - Contrôle des Opérations du {self.DATE}",
                    headers=headers
                )
                
                # Notification de succès
                if files:
                    message = f"Export réussi dans {output_dir}!\n{len(files)} fichier(s) créé(s)"
                    toast(message, duration=4)
                    print("Fichiers créés:", files)
                    return files
                else:
                    toast("Erreur lors de l'export", background=[1,0,0,1])
                    return {}
                    
            else:
                toast(f"Aucune donnée à exporter pour le {self.DATE}")
                return {}
                
        except Exception as e:
            toast("Erreur lors de l'export", background=[1,0,0,1])
            print(f"Erreur export: {e}")
            return {}

    def exporter_toutes_donnees_bcc_custom(self, formats=['pdf'], output_dir="exports_bcc"):
        """
        Version modifiée avec emplacement personnalisé pour export complet
        """
        try:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM BCC ORDER BY Date, Heur")
            toutes_donnees = cur.fetchall()
            
            if toutes_donnees:
                # Préparer les données
                data_export = [list(self.redreser_les_donne(row[1:])) for row in toutes_donnees]
                headers = ['Date', 'Heure', 'Opérateur', 'O/F/DD', 'Opération', 'Mention']
                
                # Créer l'exporteur avec l'emplacement personnalisé
                from Export import DataExporter
                exporter = DataExporter(output_dir=output_dir)
                
                # Utiliser la date du jour pour le nom du fichier
                from datetime import datetime
                today = datetime.now().strftime("%Y%m%d")

                files = exporter.export_data(
                    data_export,
                    f"rapport_bcc_complet_{today}",
                    formats=formats,
                    title="Rapport BCC - Historique Complet des Opérations",
                    headers=headers
                )
                
                if files:
                    message = f"Export complet dans {output_dir}!\n{len(files)} fichier(s) - {len(toutes_donnees)} enregistrements"
                    toast(message, duration=4)
                    return files
                else:
                    toast("Erreur lors de l'export complet", background=[1,0,0,1])
                    return {}
                    
            else:
                toast("Aucune donnée dans la base")
                return {}
                
        except Exception as e:
            toast("Erreur lors de l'export complet", background=[1,0,0,1])
            print(f"Erreur: {e}")
            return {}

    # Modifiez votre fonction lancer_export_avec_formats existante
    def lancer_export_avec_formats(self, formats):
        """
        Version modifiée qui demande d'abord l'emplacement
        """
        self.menu_export.dismiss()
        
        # Demander quel type d'export (date actuelle ou complet)
        content_layout = MDBoxLayout(
            orientation="vertical",
            spacing="20dp",
            size_hint_y=None,
            height="120dp"
        )
        
        btn_date_actuelle = MDRaisedButton(
            text=f"Exporter le {self.DATE}",
            size_hint_y=None,
            height="40dp",
            on_release=lambda x: self.choisir_emplacement_export(formats, False)
        )
        
        btn_tout = MDRaisedButton(
            text="Exporter tout l'historique",
            size_hint_y=None,
            height="40dp",
            on_release=lambda x: self.choisir_emplacement_export(formats, True)
        )
        
        content_layout.add_widget(btn_date_actuelle)
        content_layout.add_widget(btn_tout)
        
        self.dialog_export = MDDialog(
            title="Type d'export",
            type="custom",
            content_cls=content_layout,
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    theme_text_color="Custom",
                    text_color=(.5, .5, .5, 1),
                    on_release=self.annuler_export
                ),
            ],
        )
        
        self.dialog_export.open()
#=========== Fin =====================

BCC().run()

from customtkinter import *
from PIL import Image
from language import Locale
import subprocess
import json
from gc import collect as gc_collect
from requests import get
from requests.exceptions import ConnectionError
import os
import threading
import re
import string
from hmac import compare_digest

timezones = {'Africa': ['Abidjan', 'Accra', 'Addis_Ababa', 'Algiers', 'Asmara', 'Bamako', 'Bangui', 'Banjul', 'Bissau', 'Blantyre', 'Brazzaville', 'Bujumbura', 'Cairo', 'Casablanca', 'Ceuta', 'Conakry', 'Dakar', 'Dar_es_Salaam', 'Djibouti', 'Douala', 'El_Aaiun', 'Freetown', 'Gaborone', 'Harare', 'Johannesburg', 'Juba', 'Kampala', 'Khartoum', 'Kigali', 'Kinshasa', 'Lagos', 'Libreville', 'Lome', 'Luanda', 'Lubumbashi', 'Lusaka', 'Malabo', 'Maputo', 'Maseru', 'Mbabane', 'Mogadishu', 'Monrovia', 'Nairobi', 'Ndjamena', 'Niamey', 'Nouakchott', 'Ouagadougou', 'Porto-Novo', 'Sao_Tome', 'Tripoli', 'Tunis', 'Windhoek'], 'America': ['Adak', 'Anchorage', 'Anguilla', 'Antigua', 'Araguaina', 'Argentina/Buenos_Aires', 'Argentina/Catamarca', 'Argentina/Cordoba', 'Argentina/Jujuy', 'Argentina/La_Rioja', 'Argentina/Mendoza', 'Argentina/Rio_Gallegos', 'Argentina/Salta', 'Argentina/San_Juan', 'Argentina/San_Luis', 'Argentina/Tucuman', 'Argentina/Ushuaia', 'Aruba', 'Asuncion', 'Atikokan', 'Bahia', 'Bahia_Banderas', 'Barbados', 'Belem', 'Belize', 'Blanc-Sablon', 'Boa_Vista', 'Bogota', 'Boise', 'Cambridge_Bay', 'Campo_Grande', 'Cancun', 'Caracas', 'Cayenne', 'Cayman', 'Chicago', 'Chihuahua', 'Costa_Rica', 'Creston', 'Cuiaba', 'Curacao', 'Danmarkshavn', 'Dawson', 'Dawson_Creek', 'Denver', 'Detroit', 'Dominica', 'Edmonton', 'Eirunepe', 'El_Salvador', 'Fort_Nelson', 'Fortaleza', 'Glace_Bay', 'Godthab', 'Goose_Bay', 'Grand_Turk', 'Grenada', 'Guadeloupe', 'Guatemala', 'Guayaquil', 'Guyana', 'Halifax', 'Havana', 'Hermosillo', 'Indiana/Indianapolis', 'Indiana/Knox', 'Indiana/Marengo', 'Indiana/Petersburg', 'Indiana/Tell_City', 'Indiana/Vevay', 'Indiana/Vincennes', 'Indiana/Winamac', 'Inuvik', 'Iqaluit', 'Jamaica', 'Juneau', 'Kentucky/Louisville', 'Kentucky/Monticello', 'Kralendijk', 'La_Paz', 'Lima', 'Los_Angeles', 'Lower_Princes', 'Maceio', 'Managua', 'Manaus', 'Marigot', 'Martinique', 'Matamoros', 'Mazatlan', 'Menominee', 'Merida', 'Metlakatla', 'Mexico_City', 'Miquelon', 'Moncton', 'Monterrey', 'Montevideo', 'Montserrat', 'Nassau', 'New_York', 'Nipigon', 'Nome', 'Noronha', 'North_Dakota/Beulah', 'North_Dakota/Center', 'North_Dakota/New_Salem', 'Ojinaga', 'Panama', 'Pangnirtung', 'Paramaribo', 'Phoenix', 'Port-au-Prince', 'Port_of_Spain', 'Porto_Velho', 'Puerto_Rico', 'Rainy_River', 'Rankin_Inlet', 'Recife', 'Regina', 'Resolute', 'Rio_Branco', 'Santarem', 'Santiago', 'Santo_Domingo', 'Sao_Paulo', 'Scoresbysund', 'Sitka', 'St_Barthelemy', 'St_Johns', 'St_Kitts', 'St_Lucia', 'St_Thomas', 'St_Vincent', 'Swift_Current', 'Tegucigalpa', 'Thule', 'Thunder_Bay', 'Tijuana', 'Toronto', 'Tortola', 'Vancouver', 'Whitehorse', 'Winnipeg', 'Yakutat', 'Yellowknife'], 'Antarctica': ['Casey', 'Davis', 'DumontDUrville', 'Macquarie', 'Mawson', 'McMurdo', 'Palmer', 'Rothera', 'Syowa', 'Troll', 'Vostok'], 'Arctic': ['Longyearbyen'], 'Asia': ['Aden', 'Almaty', 'Amman', 'Anadyr', 'Aqtau', 'Aqtobe', 'Ashgabat', 'Atyrau', 'Baghdad', 'Bahrain', 'Baku', 'Bangkok', 'Barnaul', 'Beirut', 'Bishkek', 'Brunei', 'Chita', 'Choibalsan', 'Colombo', 'Damascus', 'Dhaka', 'Dili', 'Dubai', 'Dushanbe', 'Famagusta', 'Gaza', 'Hebron', 'Ho_Chi_Minh', 'Hong_Kong', 'Hovd', 'Irkutsk', 'Jakarta', 'Jayapura', 'Jerusalem', 'Kabul', 'Kamchatka', 'Karachi', 'Kathmandu', 'Khandyga', 'Kolkata', 'Krasnoyarsk', 'Kuala_Lumpur', 'Kuching', 'Kuwait', 'Macau', 'Magadan', 'Makassar', 'Manila', 'Muscat', 'Nicosia', 'Novokuznetsk', 'Novosibirsk', 'Omsk', 'Oral', 'Phnom_Penh', 'Pontianak', 'Pyongyang', 'Qatar', 'Qyzylorda', 'Riyadh', 'Sakhalin', 'Samarkand', 'Seoul', 'Shanghai', 'Singapore', 'Srednekolymsk', 'Taipei', 'Tashkent', 'Tbilisi', 'Tehran', 'Thimphu', 'Tokyo', 'Tomsk', 'Ulaanbaatar', 'Urumqi', 'Ust-Nera', 'Vientiane', 'Vladivostok', 'Yakutsk', 'Yangon', 'Yekaterinburg', 'Yerevan'], 'Atlantic': ['Azores', 'Bermuda', 'Canary', 'Cape_Verde', 'Faroe', 'Madeira', 'Reykjavik', 'South_Georgia', 'St_Helena', 'Stanley'], 'Australia': ['Adelaide', 'Brisbane', 'Broken_Hill', 'Currie', 'Darwin', 'Eucla', 'Hobart', 'Lindeman', 'Lord_Howe', 'Melbourne', 'Perth', 'Sydney'], 'Europe': ['Amsterdam', 'Andorra', 'Astrakhan', 'Athens', 'Belgrade', 'Berlin', 'Bratislava', 'Brussels', 'Bucharest', 'Budapest', 'Busingen', 'Chisinau', 'Copenhagen', 'Dublin', 'Gibraltar', 'Guernsey', 'Helsinki', 'Isle_of_Man', 'Istanbul', 'Jersey', 'Kaliningrad', 'Kiev', 'Kirov', 'Lisbon', 'Ljubljana', 'London', 'Luxembourg', 'Madrid', 'Malta', 'Mariehamn', 'Minsk', 'Monaco', 'Moscow', 'Oslo', 'Paris', 'Podgorica', 'Prague', 'Riga', 'Rome', 'Samara', 'San_Marino', 'Sarajevo', 'Saratov', 'Simferopol', 'Skopje', 'Sofia', 'Stockholm', 'Tallinn', 'Tirane', 'Ulyanovsk', 'Uzhgorod', 'Vaduz', 'Vatican', 'Vienna', 'Vilnius', 'Volgograd', 'Warsaw', 'Zagreb', 'Zaporozhye', 'Zurich'], 'Indian': ['Antananarivo', 'Chagos', 'Christmas', 'Cocos', 'Comoro', 'Kerguelen', 'Mahe', 'Maldives', 'Mauritius', 'Mayotte', 'Reunion'], 'Pacific': ['Apia', 'Auckland', 'Bougainville', 'Chatham', 'Chuuk', 'Easter', 'Efate', 'Enderbury', 'Fakaofo', 'Fiji', 'Funafuti', 'Galapagos', 'Gambier', 'Guadalcanal', 'Guam', 'Honolulu', 'Johnston', 'Kiritimati', 'Kosrae', 'Kwajalein', 'Majuro', 'Marquesas', 'Midway', 'Nauru', 'Niue', 'Norfolk', 'Noumea', 'Pago_Pago', 'Palau', 'Pitcairn', 'Pohnpei', 'Port_Moresby', 'Rarotonga', 'Saipan', 'Tahiti', 'Tarawa', 'Tongatapu', 'Wake', 'Wallis']}

VERSION = "0.2.3"
DEBUG = True
DEBUG_SHOW_COMMANDS = False # Default: False
DEBUG_SHOW_COMMANDS_EFI_PARTITION = "/dev/vda1"
DEBUG_SHOW_COMMANDS_ROOTFS_PARTITION = "/dev/vda2"
DEBUG_AUTOENTRY = False # Default: False
DEBUG_AUTOENTRY_VALUES = ['asd', 'asdasdasd']

MIN_PASSWORD_LENGTH = 8

DISTRO_NAME="SECUX"

REPO_URL = "https://kolbanidze.github.io/secux-repo/x86_64/"

MOK_PASSWORD = "123"

WORKDIR = os.path.dirname(os.path.abspath(__file__))

if os.path.isfile(WORKDIR + "/production.conf"):
    DEBUG = False

OFFLINE = False
if os.path.isfile(WORKDIR + "/offline_installation.conf"):
    OFFLINE = True

class Notification(CTkToplevel):
    def __init__(self, title: str, icon: str, message: str, message_bold: bool, exit_btn_msg: str):
        super().__init__()
        self.title(title)
        image = CTkImage(light_image=Image.open(f'{WORKDIR}/images/{icon}'), dark_image=Image.open(f'{WORKDIR}/images/{icon}'), size=(80, 80))
        image_label = CTkLabel(self, text="", image=image)
        label = CTkLabel(self, text=message)
        if message_bold:
            label.configure(font=(None, 16, "bold"))
        exit_button = CTkButton(self, text=exit_btn_msg, command=self.destroy)
        self.bind(("<Return>"), lambda event: self.destroy())
        image_label.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")
        label.grid(row=0, column=1, padx=15, pady=5, sticky="nsew")
        exit_button.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title(DISTRO_NAME)
        self.language = "ru"
        self.setup_information = {}
        self.ui_scale = 1
        self.light_theme = False
        self.current_stage = 0
        self.total_amount_of_stages = 10
        set_appearance_mode("dark")

        self.welcome_menu = CTkFrame(self)
        self.welcome_menu.pack(fill='both', expand=True)

        self.clicks = 0
        welcome_image = CTkImage(light_image=Image.open(f'{WORKDIR}/images/waving_hand.png'), dark_image=Image.open(f'{WORKDIR}/images/waving_hand.png'), size=(80,80))
        welcome_image_label = CTkLabel(self.welcome_menu, text="", image=welcome_image)
        welcome_image_label.bind("<Button-1>", self.__clicks_handler)
        welcome_entry_label = CTkLabel(self.welcome_menu, text=f"Добро пожаловать в установщик дистрибутива {DISTRO_NAME}\nWelcome to {DISTRO_NAME} distribution installer")        
        select_language_label = CTkLabel(self.welcome_menu, text="Выберите язык | Select language")
        languages_optionmenu = CTkOptionMenu(self.welcome_menu, values=["Русский", "English"], command=self.__language_callback)
        next_button = CTkButton(self.welcome_menu, text="Далее | Next", command=self.__draw_timezone_stage, fg_color="green")
        ui_scaling_label = CTkLabel(self.welcome_menu, text="Масштабирование | UI Scaling")
        self.ui_scaling = CTkOptionMenu(self.welcome_menu, values=["80%", "100%", "125%", "150%", "200%"], command=self.__ui_scaling_handler)
        self.ui_scaling.set(str(int(self.ui_scale*100)) + "%")
        self.white_mode = CTkSwitch(self.welcome_menu, text="Светлая тема | White theme", command=self.__theme_handler)
        if self.light_theme:
            self.white_mode.select()
        info = CTkLabel(self.welcome_menu, text=f"Версия | Version : {VERSION}", font=(None, 8))

        self.welcome_menu.grid_columnconfigure((0, 1), weight=1)

        welcome_image_label.grid(row=0, columnspan=2, padx=15, pady=5)
        welcome_entry_label.grid(row=1, columnspan=2, padx=15, pady=5)
        select_language_label.grid(row=2, columnspan=2, padx=15, pady=(15, 5))
        languages_optionmenu.grid(row=3, columnspan=2, padx=15, pady=5)
        ui_scaling_label.grid(row=4, columnspan=2, padx=15, pady=5)
        self.ui_scaling.grid(row=5, columnspan=2, padx=15, pady=5)
        self.white_mode.grid(row=6, columnspan=2, padx=15, pady=5)
        next_button.grid(row=7, columnspan=2, padx=15, pady=(15, 5))
        self.bind(("<Return>"), lambda event: self.__draw_timezone_stage())
        info.grid(row=8, padx=15, columnspan=2, pady=(5, 0))
        if DEBUG: CTkLabel(self.welcome_menu, text="WARNING: DEBUG MODE", font=(None, 10), text_color=("red")).grid(row=9, columnspan=2, padx=15, pady=(5,0))
        
    def __ui_scaling_handler(self, new_scaling: str):
        self.ui_scale = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(self.ui_scale)
        self.__resize()
    
    def __theme_handler(self):
        if self.white_mode.get():
            set_appearance_mode("light")
            self.light_theme = True
        else:
            set_appearance_mode("dark")
            self.light_theme = False

    def __resize(self):
        self.update_idletasks()
        resolution = f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}"
        self.geometry(resolution)

    def __clicks_handler(self, event):
        self.clicks += 1
        if self.clicks == 3:
            self.clicks = 0
            self._updater()
    
    def _updater(self):
        for widget in self.winfo_children():
            widget.destroy()
        update_image = CTkImage(light_image=Image.open(f'{WORKDIR}/images/update.png'), dark_image=Image.open(f'{WORKDIR}/images/update.png'), size=(80, 80))
        update_image_label = CTkLabel(self, text="", image=update_image)
        updater_welcome = CTkLabel(self, text=f"{DISTRO_NAME} installer updater | Обновления установщика {DISTRO_NAME}")
        run_update = CTkButton(self, text="Update | Обновить", command=self.__update_repo)
        self.updater_textbox = CTkTextbox(self, state="disabled")
        after_update = CTkLabel(self, text="Для применения обновлений необходимо перезапустить программу.\nTo apply updates, you must restart the program.")
        exit_button = CTkButton(self, text="Закрыть программу | Close the program", command=self.destroy)

        update_image_label.pack(padx=15, pady=15)
        updater_welcome.pack(padx=15, pady=15)
        run_update.pack(padx=15, pady=(0, 15))
        self.updater_textbox.pack(padx=15, pady=15, expand=True, fill="both")
        after_update.pack(padx=15, pady=15)
        exit_button.pack(padx=15, pady=(0, 15))
    
    def __update_repo(self):
        self.updater_textbox.configure(state="normal")
        try:
            # Ensure the script is running from a Git repository
            repo_path = os.path.dirname(os.path.abspath(__file__))
            os.chdir(repo_path)
            
            process = subprocess.Popen(
                ["git", "pull", "origin", "main"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)
            stdout, stderr = process.communicate()
            if stdout:
                self.updater_textbox.insert("end", stdout)
            if stderr:
                self.updater_textbox.insert("end", stderr)
        except Exception as e:
            self.updater_textbox.insert("end", f"ERROR: {e}\n")
        self.updater_textbox.configure(state="disabled")

    def __language_callback(self, choice):
        match choice:
            case "English":
                self.language = "en"
            case "Русский":
                self.language = "ru"
        if len(self.winfo_children()) > 1:
            for widget in self.winfo_children():
                if widget != self.welcome_menu:
                    widget.destroy()
            self.ui_scaling.configure(state='disabled')
            if hasattr(self, "timezone_stage_frame"):
                del self.timezone_stage_frame
            if hasattr(self, 'installation_type_frame'):
                del self.installation_type_frame
            if hasattr(self, 'de_frame'):
                del self.de_frame
            if hasattr(self, 'kernel_frame'):
                del self.kernel_frame
            if hasattr(self, 'partitioning_frame'):
                del self.partitioning_frame
            if hasattr(self, 'encryption_frame'):
                del self.encryption_frame
            if hasattr(self, 'admin_frame'):
                del self.admin_frame
            if hasattr(self, 'network_frame'):
                del self.network_frame
            self.current_stage = 0

    def __draw_progress_bar(self, frame):
        progressbar = CTkProgressBar(frame, orientation='horizontal', width=500)
        value = self.current_stage / self.total_amount_of_stages
        progressbar.set(value)
        progressbar.grid(row=0, column=0, padx=15, pady=(5,15), sticky="nsew", columnspan=2)

    ##### BEGIN TIME ZONE #####
    def __timezone_handler(self, choice):
        self.zone_box.configure(values=timezones[choice])
        self.zone_box.set(timezones[choice][0])
        self.__time_zone_write_to_setup_info()
    
    def __time_zone_write_to_setup_info(self, none = None):
        region = self.region_box.get()
        zone = self.zone_box.get()
        if zone:
            timezone = f"{region}/{zone}"
        else:
            timezone = f"{region}"
        self.setup_information["Timezone"] = timezone

    def __draw_timezone_stage(self):
        self.bind(("<Return>"), lambda event: self.__draw_installation_type())
        self.welcome_menu.pack_forget()
        self.current_stage += 1
        self.lang = Locale(language=self.language)
        if not hasattr(self, "timezone_stage_frame"):
            self.timezone_stage()
        self.__draw_stage(self.timezone_stage_frame)
            
    def __return_to_welcome_menu(self):
        self.bind(("<Return>"), lambda event: self.__draw_timezone_stage())
        self.current_stage -= 1
        self.timezone_stage_frame.pack_forget()
        self.__draw_stage(self.welcome_menu)

    def timezone_stage(self):
        self.timezone_stage_frame = CTkFrame(self)
        self.__draw_progress_bar(self.timezone_stage_frame)
        title1 = CTkLabel(self.timezone_stage_frame, text=self.lang.select_time_zone, font=(None, 16, 'bold'))
        region_label = CTkLabel(self.timezone_stage_frame, text=self.lang.region)
        zone_label = CTkLabel(self.timezone_stage_frame, text=self.lang.timezone)
        self.region_box = CTkOptionMenu(self.timezone_stage_frame, values=list(timezones.keys()), command=self.__timezone_handler)
        self.zone_box = CTkOptionMenu(self.timezone_stage_frame, command=self.__time_zone_write_to_setup_info)
        back_btn = CTkButton(self.timezone_stage_frame, text=self.lang.back, command=self.__return_to_welcome_menu)
        next_btn = CTkButton(self.timezone_stage_frame, text=self.lang.next, command=self.__draw_installation_type)
        
        if "Timezone" not in self.setup_information:
            self.__timezone_handler("Europe")
            self.region_box.set("Europe")
            self.zone_box.set("Minsk")
            self.setup_information["Timezone"] = "Europe/Minsk"
        else:
            region = self.setup_information["Timezone"].split('/')[0]
            zone = self.setup_information["Timezone"].split("/")[1]
            self.region_box.set(region)
            self.zone_box.set(zone)
            self.zone_box.configure(values=timezones[region])

        title1.grid(row=1, column=0, padx=15, pady=5, sticky="ew", columnspan=2)
        region_label.grid(row=2, column=0, padx=15, pady=(5, 0), sticky="ew")
        zone_label.grid(row=2, column=1, padx=15, pady=(5, 0), sticky="ew")
        self.region_box.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        self.zone_box.grid(row=3, column=1, padx=15, pady=5, sticky="ew")
        back_btn.grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        next_btn.grid(row=4, column=1, padx=15, pady=5, sticky="ew")
        self.timezone_stage_frame.pack(expand=True, fill='both')
        self.__resize()
        
    ##### END TIME ZONE #####

    def __draw_installation_type(self):
        self.bind(("<Return>"), lambda event: self.__draw_de())
        self.timezone_stage_frame.pack_forget()
        self.current_stage += 1
        if not hasattr(self, "installation_type_frame"):
            self.installation_type_stage()
        self.__draw_stage(self.installation_type_frame)

    def __return_to_timezone(self):
        self.installation_type_frame.pack_forget()
        self.bind(("<Return>"), lambda event: self.__draw_installation_type())
        self.current_stage -= 1
        self.__draw_stage(self.timezone_stage_frame)

    def __draw_stage(self, frame):
        frame.pack(fill='both', expand=True)
        self.__resize()

    ##### BEGIN INSTALLATION TYPE #####
    def __installation_type_radio_button_handler(self):
        key = self.installation_type_variable.get()
        match key:
            case 0:
                self.setup_information["InstallationType"] = "Secure"
            case 1:
                self.setup_information["InstallationType"] = "LessSecure"
            case 2:
                self.setup_information["InstallationType"] = "InSecure"

    def installation_type_stage(self):
        self.installation_type_frame = CTkFrame(self)
        # self.installation_type_frame.pack(fill='both', expand=True)

        self.__draw_progress_bar(self.installation_type_frame)
        label = CTkLabel(self.installation_type_frame, text=self.lang.select_install_option, font=(None, 16, "bold"))
        self.installation_type_variable = IntVar(value=0)
        self.secure_type = CTkRadioButton(self.installation_type_frame, value=0, variable=self.installation_type_variable, text=self.lang.securetype, command=self.__installation_type_radio_button_handler)
        self.less_secure_type = CTkRadioButton(self.installation_type_frame, value=1, variable=self.installation_type_variable, text=self.lang.lessecuretype, command=self.__installation_type_radio_button_handler)
        self.insecure_type = CTkRadioButton(self.installation_type_frame, value=2, variable=self.installation_type_variable, text=self.lang.insecuretype, command=self.__installation_type_radio_button_handler)
        back_btn = CTkButton(self.installation_type_frame, text=self.lang.back, command=self.__return_to_timezone)
        next_btn = CTkButton(self.installation_type_frame, text=self.lang.next, command=self.__draw_de)

        if "InstallationType" in self.setup_information:
            match self.setup_information["InstallationType"]:
                case "Secure":
                    self.installation_type_variable.set(value=0)
                case "LessSecure":
                    self.installation_type_variable.set(value=1)
                case "InSecure":
                    self.installation_type_variable.set(value=2)
        else:
            self.__installation_type_radio_button_handler()

        label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.secure_type.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.less_secure_type.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.insecure_type.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        back_btn.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=5, column=1, padx=15, pady=5, sticky="nsew")
        # self.__resize()
    
    ##### END INSTALLATION TYPE #####

    ##### BEGIN DE #####
    def __de_handler(self):
        key = self.de_variable.get()
        match key:
            case 0:
                self.setup_information["DE"] = "GNOME"
            case 1:
                self.setup_information["DE"] = "KDE"
            case 2:
                self.setup_information["DE"] = "Console"
    
    def __draw_de(self):
        self.installation_type_frame.pack_forget()
        self.current_stage += 1
        self.bind(("<Return>"), lambda event: self.__draw_kernel_stage())
        if not hasattr(self, "de_frame"):
            self.desktop_environment_stage()
        self.__draw_stage(self.de_frame)
    
    def __return_to_installation_type(self):
        self.bind(("<Return>"), lambda event: self.__draw_de())
        self.current_stage -= 1
        self.de_frame.pack_forget()
        self.__draw_stage(self.installation_type_frame)

    def desktop_environment_stage(self):
        self.de_frame = CTkFrame(self)

        self.__draw_progress_bar(self.de_frame)
        self.de_variable = IntVar(value=0)
        label = CTkLabel(self.de_frame, text=self.lang.choose_de, font=(None, 16, "bold"))
        self.gnome_button = CTkRadioButton(self.de_frame, value=0, variable=self.de_variable, text="GNOME", command=self.__de_handler)
        self.kde_button = CTkRadioButton(self.de_frame, value=1, variable=self.de_variable, text="KDE", command=self.__de_handler)
        self.console_button = CTkRadioButton(self.de_frame, value=2, variable=self.de_variable, text=self.lang.console, command=self.__de_handler)
        back_btn = CTkButton(self.de_frame, text=self.lang.back, command=self.__return_to_installation_type)
        next_btn = CTkButton(self.de_frame, text=self.lang.next, command=self.__draw_kernel_stage)

        if "DE" in self.setup_information:
            match self.setup_information["DE"]:
                case "GNOME":
                    self.de_variable.set(0)
                case "KDE":
                    self.de_variable.set(1)
                case "Console":
                    self.de_variable.set(2)
        else:
            self.__de_handler()

        label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.gnome_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.kde_button.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.console_button.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        back_btn.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=5, column=1, sticky="nsew", padx=15, pady=5)
        self.__resize()
    
    ##### END DE #####

    ##### BEGIN KERNEL SELECT #####
    def __kernel_select_handler(self):
        if "Kernel" not in self.setup_information:
            self.setup_information["Kernel"] = []
        
        self.setup_information["Kernel"].clear()
        
        if self.linux_hardened.get():
            self.setup_information["Kernel"].append('linux-hardened')
        if self.linux_lts.get():
            self.setup_information["Kernel"].append('linux-lts')
        if self.linux.get():
            self.setup_information["Kernel"].append("linux")

    def __draw_kernel_stage(self):
        self.de_frame.pack_forget()
        self.bind(("<Return>"), lambda event: self.__draw_partitioning())
        self.current_stage += 1
        if not hasattr(self, "kernel_frame"):
            self.kernel_select_stage()
        self.__draw_stage(self.kernel_frame)
    
    def __return_to_de(self):
        self.kernel_frame.pack_forget()
        self.bind(("<Return>"), lambda event: self.__draw_kernel_stage())
        self.current_stage -= 1
        self.__draw_stage(self.de_frame)

    def kernel_select_stage(self):
        self.kernel_frame = CTkFrame(self)

        self.__draw_progress_bar(self.kernel_frame)
        label = CTkLabel(self.kernel_frame, text=self.lang.kernel_label, font=(None, 16, "bold"))
        self.linux_hardened = CTkCheckBox(self.kernel_frame, text="Linux hardened", command=self.__kernel_select_handler)
        self.linux_lts = CTkCheckBox(self.kernel_frame, text="Linux LTS", command=self.__kernel_select_handler)
        self.linux = CTkCheckBox(self.kernel_frame, text="Linux", command=self.__kernel_select_handler)
        back_btn = CTkButton(self.kernel_frame, text=self.lang.back, command=self.__return_to_de)
        next_btn = CTkButton(self.kernel_frame, text=self.lang.next, command=self.__draw_partitioning)

        if "Kernel" not in self.setup_information:
            self.linux_hardened.select()
            self.__kernel_select_handler()
        else:
            if 'linux-hardened' in self.setup_information["Kernel"]:
                self.linux_hardened.select()
            if 'linux-lts' in self.setup_information["Kernel"]:
                self.linux_lts.select()
            if 'linux' in self.setup_information["Kernel"]:
                self.linux.select()
            

        label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.linux_hardened.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.linux_lts.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.linux.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        back_btn.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=5, column=1, padx=15, pady=5, sticky="nsew")
        self.__resize()

    ##### END KERNEL SELECT #####

    ##### BEGIN PARTITIONING #####
    def __convert_bytes_to_human_readable(self, size_in_bytes):
        # Define the size units
        units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
        
        # Initialize the unit index
        unit_index = 0
        
        # Convert bytes to the appropriate unit
        while size_in_bytes >= 1024 and unit_index < len(units) - 1:
            size_in_bytes /= 1024
            unit_index += 1
        
        # Return the formatted string with 2 decimal places
        return f"{size_in_bytes:.2f} {units[unit_index]}"
    
    def __draw_partitioning(self):
        if len(self.setup_information["Kernel"]) == 0:
            Notification(title=self.lang.atleast_one_kernel, icon='warning.png', message=self.lang.pls_select_kernel, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        self.bind(("<Return>"), lambda event: self.__partitioning_next_button_handler())
        self.current_stage += 1
        self.kernel_frame.pack_forget()
        if not hasattr(self, "partitioning_frame"):
            self.partitioning_stage()
        self.__draw_stage(self.partitioning_frame)
    
    def __return_to_kernel(self):
        self.partitioning_frame.pack_forget()
        self.bind(("<Return>"), lambda event: self.__draw_partitioning())
        self.current_stage -= 1
        self.__draw_stage(self.kernel_frame)

    def partitioning_stage(self):
        self.partitioning_frame = CTkFrame(self)
        # self.partitioning_frame.pack(expand=True, fill='both')

        self.__draw_progress_bar(self.partitioning_frame)
        label = CTkLabel(self.partitioning_frame, text=self.lang.diskpart, font=(None, 16, "bold"))
        
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,TYPE', '--json', '-b'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        raw_disks = []
        for disk in disks:
            if disk['type'] == 'disk':
                raw_disks.append({disk['name']: disk['size']})
        sorted_raw_disks = sorted([(list(d.keys())[0], list(d.values())[0]) for d in raw_disks], key=lambda x: x[1], reverse=True)
        erase_all_disks = [f"/dev/{drive} | {self.__convert_bytes_to_human_readable(size)}" for drive, size in sorted_raw_disks]

        self.partitioning_type = IntVar(value=0)
        erase_all_partitioning = CTkRadioButton(self.partitioning_frame, text=self.lang.erase_all_and_install, variable=self.partitioning_type, value=0)
        self.erase_all_disk = CTkOptionMenu(self.partitioning_frame, values=erase_all_disks)
        manual_partitioning = CTkRadioButton(self.partitioning_frame, text=self.lang.manual, variable=self.partitioning_type, value=1)
        back_btn = CTkButton(self.partitioning_frame, text=self.lang.back, command=self.__return_to_kernel)
        next_btn = CTkButton(self.partitioning_frame, text=self.lang.next, command=self.__partitioning_next_button_handler)

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        erase_all_partitioning.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.erase_all_disk.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        manual_partitioning.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        back_btn.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=5, column=1, padx=15, pady=5, sticky="nsew")
        self.__resize()

    def __partitioning_next_button_handler(self):
        key = self.partitioning_type.get()
        match key:
            case 0:
                disk = self.erase_all_disk.get().split(" |")[0]
                self.setup_information["Partitioning"] = "Automatic"
                self.setup_information["DriveToFormat"] = disk
                self.setup_information["UseSwap"] = True
                self.setup_information["SwapSize"] = "1"
                self.partitioning_frame.pack_forget()
                self.current_stage += 1
                if not hasattr(self, "encryption_frame"):
                    self.encryption_key_stage()
                self.bind(("<Return>"), lambda event: self.__draw_admin_creation())
                self.__draw_stage(self.encryption_frame)
            case 1:
                self.setup_information["Partitioning"] = "Manual"
                self.partitioning_frame.pack_forget()
                if not hasattr(self, "manual_partitioning_frame"):
                    self.manual_partitioning()
                self.bind(("<Return>"), lambda event: self.__draw_encryption_stage_from_manual())
                self.__draw_stage(self.manual_partitioning_frame)

    def manual_partitioning(self):
        self.manual_partitioning_frame = CTkFrame(self)
        # self.manual_partitioning_frame.pack(fill='both', expand=True)
        
        self.partitions = []
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    self.partitions.append(f"{partition['name']} | {partition['size']} | {partition.get('fstype', 'N/A')}")

        self.__draw_progress_bar(self.manual_partitioning_frame)
        label = CTkLabel(self.manual_partitioning_frame, text=self.lang.selfpart, font=(None, 16, "bold"))
        run_gparted_btn = CTkButton(self.manual_partitioning_frame, text=self.lang.rungparted, command=lambda: os.system("/usr/bin/sudo /usr/bin/gparted"))
        update_disks = CTkButton(self.manual_partitioning_frame, text=self.lang.refreshparts, command=self.__update_partitions)
        efi_partition_label = CTkLabel(self.manual_partitioning_frame, text=self.lang.efipart)
        self.efi_partition_optionmenu = CTkOptionMenu(self.manual_partitioning_frame, values=self.partitions)
        root_partition_label = CTkLabel(self.manual_partitioning_frame, text=self.lang.rootfs)
        self.root_partition_optionmenu = CTkOptionMenu(self.manual_partitioning_frame, values=self.partitions, command=self.__change_max_swapfile)
        self.use_swap = StringVar(value="on")
        self.swap_checkbox = CTkCheckBox(self.manual_partitioning_frame, text=self.lang.useswap, variable=self.use_swap, onvalue="on", offvalue="off", command=self.__swapfile_handler)
        swap_label = CTkLabel(self.manual_partitioning_frame, text=self.lang.swapsize)
        self.swap_entry = CTkEntry(self.manual_partitioning_frame)
        self.swap_entry.insert(0, "1")
        self.swap_scrollbar = CTkSlider(self.manual_partitioning_frame, command=self.__scroll_handler, to=16)
        back_btn = CTkButton(self.manual_partitioning_frame, text=self.lang.back, command=lambda: self.__return_to_partitioning(self.manual_partitioning_frame))
        next_btn = CTkButton(self.manual_partitioning_frame, text=self.lang.next, command=self.__draw_encryption_stage_from_manual)

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        run_gparted_btn.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        update_disks.grid(row=2, column=1, padx=15, pady=5, sticky="nsew")
        efi_partition_label.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")
        self.efi_partition_optionmenu.grid(row=3, column=1, padx=15, pady=5, sticky="nsew")
        root_partition_label.grid(row=4, column=0, padx=15, pady=5, sticky="nsew")
        self.root_partition_optionmenu.grid(row=4, column=1, padx=15, pady=5, sticky="nsew")
        self.swap_checkbox.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        swap_label.grid(row=6, column=0, padx=15, pady=5, sticky="nsew")
        self.swap_entry.grid(row=7, column=0, padx=15, pady=5, sticky="nsew")
        self.swap_scrollbar.grid(row=7, column=1, padx=15, pady=5, sticky="nsew")
        back_btn.grid(row=8, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=8, column=1, padx=15, pady=5, sticky="nsew")
        # self.__resize()

    def __scroll_handler(self, newvalue):
        newvalue = round(newvalue, 1)
        self.swap_entry.delete(0, 'end')
        self.swap_entry.insert(0, str(newvalue))
    
    def __swapfile_handler(self):
        if self.swap_checkbox.get() == "off":
            self.swap_entry.configure(state="disabled")
            self.swap_scrollbar.configure(state="disabled")
        else:
            self.swap_entry.configure(state="normal")
            self.swap_scrollbar.configure(state="normal")
            self.__change_max_swapfile(None)

    def __update_partitions(self):
        self.partitions.clear()
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    self.partitions.append(f"{partition['name']} | {partition['size']} | {partition.get('fstype', 'N/A')}")
        self.efi_partition_optionmenu.configure(values=self.partitions)
        self.root_partition_optionmenu.configure(values=self.partitions)

    def __change_max_swapfile(self, newvalue):
        if self.swap_checkbox.get() == "off":
            return
        half_of_max_space = int(self.__get_max_swap_size() / (2**30))//2
        if half_of_max_space == 0:
            Notification(title=self.lang.swap_part_too_small, icon="warning.png", message=self.lang.swap_part_too_small, message_bold=False, exit_btn_msg=self.lang.exit)
            self.swap_scrollbar.configure(state="disabled")
            return 
        else:
            self.swap_scrollbar.configure(state="normal")
        self.swap_scrollbar.configure(to=half_of_max_space)

    def __get_max_swap_size(self):
        """by default returns 16 GiB in bytes"""
        current_partition = self.root_partition_optionmenu.get().split(" | ")[0]
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE', '--json', '-ba'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        current_partition_size = 17179869184 # bytes
        for disk in disks:
            if 'children'in disk:
                for partition in disk['children']:
                    if partition['name'] == current_partition:
                        current_partition_size = partition['size']
                        break
        return current_partition_size

    def __draw_encryption_stage_from_manual(self):
        efi_partition = self.efi_partition_optionmenu.get().split(" | ")[0]
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE', '--json', '-ba'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    if partition['name'] == efi_partition:
                        efi_partition_size = partition['size']
                        break
        if efi_partition_size < 209715200:
            Notification(title=self.lang.efi_small_title, icon="warning.png", message=self.lang.efi_small, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        system_partition = "/dev/" + self.root_partition_optionmenu.get().split(" | ")[0]
        use_swapfile = ("on" == self.swap_checkbox.get())
        self.setup_information["Partitioning"] = "Manual"
        self.setup_information["EfiPartition"] = "/dev/" + efi_partition
        self.setup_information["SystemPartition"] = system_partition
        self.setup_information["UseSwap"] = use_swapfile
        if use_swapfile:
            swapsize = self.swap_entry.get()
            self.setup_information["SwapSize"] = swapsize
        self.bind(("<Return>"), lambda event: self.__draw_admin_creation())
        self.manual_partitioning_frame.grid_forget()
        self.current_stage += 1

        if not hasattr(self, "encryption_frame"):
            self.encryption_key_stage()
        self.__draw_stage(self.encryption_frame)
    
    def __return_to_partitioning(self, frame, decrement_current_stage = False):
        frame.pack_forget()
        if decrement_current_stage:
            self.current_stage -= 1
        self.bind(("<Return>"), lambda event: self.__partitioning_next_button_handler())
        if not hasattr(self, "partitioning_frame"):
            self.partitioning_stage()
        self.__draw_stage(self.partitioning_frame)
    ##### END PARTITIONING #####

    ##### BEGIN ENCRYPTION KEY #####
    def __validate_english_keymap(self, password) -> bool:
        """True -> can be written with english keymap. False -> can't be written with english keymap"""
        valid_characters = string.ascii_letters + string.digits + string.punctuation + " "
        return all(char in valid_characters for char in password)

    def encryption_key_stage(self):
        self.encryption_frame = CTkFrame(self)

        self.__draw_progress_bar(self.encryption_frame)
        label = CTkLabel(self.encryption_frame, text=self.lang.os_encryption, font=(None, 16, "bold"))
        label1 = CTkLabel(self.encryption_frame, text=self.lang.enckey)
        self.system_partition_encryption_key_entry = CTkEntry(self.encryption_frame, show='*')
        label2 = CTkLabel(self.encryption_frame, text=self.lang.enckey2)
        self.system_partition_encryption_key_entry2 = CTkEntry(self.encryption_frame, show='*')
        back_btn = CTkButton(self.encryption_frame, text=self.lang.back, command=lambda: self.__return_to_partitioning(self.encryption_frame, decrement_current_stage=True))
        next_btn = CTkButton(self.encryption_frame, text=self.lang.next, command=self.__draw_admin_creation)

        if DEBUG_AUTOENTRY:
            self.system_partition_encryption_key_entry.insert(0, DEBUG_AUTOENTRY_VALUES[1])
            self.system_partition_encryption_key_entry2.insert(0, DEBUG_AUTOENTRY_VALUES[1])

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        label1.grid(row=2, column=0, padx=15, pady=5, sticky="nsew", columnspan=2)
        self.system_partition_encryption_key_entry.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        label2.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.system_partition_encryption_key_entry2.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        back_btn.grid(row=6, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=6, column=1, padx=15, pady=5, sticky="nsew")

    def __draw_admin_creation(self):
        if self.system_partition_encryption_key_entry.get() != self.system_partition_encryption_key_entry2.get():
            Notification(title=self.lang.passwordmismatch, icon="warning.png", message=self.lang.passwordmsg, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if len(self.system_partition_encryption_key_entry.get()) < MIN_PASSWORD_LENGTH:
            Notification(title=self.lang.pwd_length_title, icon="warning.png", message=self.lang.pwd_length, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if not self.__validate_english_keymap(self.system_partition_encryption_key_entry.get()):
            Notification(title=self.lang.encryption_password_title, icon="warning.png", message=self.lang.encryption_password, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        self.setup_information["EncryptionKey"] = self.system_partition_encryption_key_entry.get()
        self.current_stage += 1
        if not hasattr(self, "admin_frame"):
            self.admin_creation_stage()
        self.encryption_frame.pack_forget()
        self.bind(("<Return>"), lambda event: self.__draw_network_stage())
        self.__draw_stage(self.admin_frame)

    def __return_to_encryption_key_stage(self):
        self.admin_frame.pack_forget()
        self.current_stage -= 1
        self.bind(("<Return>"), lambda event: self.__draw_admin_creation())
        self.__draw_stage(self.encryption_frame)

    ##### END ENCRYPTION KEY #####

    ##### BEGIN ADMIN CREATION #####
    def __validate_input(self, input: str, russian=False, spaces=False):
        if russian and spaces:
            pattern = "^[a-zA-Zа-яА-ЯёЁ0-9 _-]{0,32}$"
        elif russian == False and spaces:
            pattern = "^[a-zA-Z0-9 _-]{0,32}$"
        elif russian:
            pattern = "^[a-zA-Zа-яА-ЯёЁ0-9_-]{0,32}$"
        else:
            pattern = "^[a-zA-Z0-9_-]{0,32}$"
        if re.match(pattern, input):
            return True
        else:
            return False

    def admin_creation_stage(self):
        self.admin_frame = CTkFrame(self)

        self.__draw_progress_bar(self.admin_frame)
        label = CTkLabel(self.admin_frame, text=self.lang.admin_creation, font=(None, 16, "bold"))
        your_name_label = CTkLabel(self.admin_frame, text=self.lang.yourname)
        self.your_name_entry = CTkEntry(self.admin_frame)
        hostname_label = CTkLabel(self.admin_frame, text=self.lang.hostname)
        self.hostname_entry = CTkEntry(self.admin_frame)
        username_label = CTkLabel(self.admin_frame, text=self.lang.username)
        self.username_entry = CTkEntry(self.admin_frame)
        password_label = CTkLabel(self.admin_frame, text=self.lang.password1)
        self.password_entry = CTkEntry(self.admin_frame, show='*')
        password_label2 = CTkLabel(self.admin_frame, text=self.lang.password2)
        self.password_entry2 = CTkEntry(self.admin_frame, show="*")
        back_btn = CTkButton(self.admin_frame, text=self.lang.back, command=self.__return_to_encryption_key_stage)
        next_btn = CTkButton(self.admin_frame, text=self.lang.next, command=self.__draw_network_stage)

        if DEBUG_AUTOENTRY:
            self.your_name_entry.insert(0, DEBUG_AUTOENTRY_VALUES[0])
            self.hostname_entry.insert(0, DEBUG_AUTOENTRY_VALUES[0])
            self.username_entry.insert(0, DEBUG_AUTOENTRY_VALUES[0])
            self.password_entry.insert(0, DEBUG_AUTOENTRY_VALUES[1])
            self.password_entry2.insert(0, DEBUG_AUTOENTRY_VALUES[1])

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        your_name_label.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        self.your_name_entry.grid(row=2, column=1, padx=15, pady=5, sticky="nsew")
        hostname_label.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")
        self.hostname_entry.grid(row=3, column=1, padx=15, pady=5, sticky="nsew")
        username_label.grid(row=4, column=0, padx=15, pady=5, sticky="nsew")
        self.username_entry.grid(row=4, column=1, padx=15, pady=5, sticky="nsew")
        password_label.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        self.password_entry.grid(row=5, column=1, padx=15, pady=5, sticky="nsew")
        password_label2.grid(row=6, column=0, padx=15, pady=5, sticky="nsew")
        self.password_entry2.grid(row=6, column=1, padx=15, pady=5, sticky="nsew")
        back_btn.grid(row=7, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=7, column=1, padx=15, pady=5, sticky="nsew")
    
    ##### END ADMIN CREATION #####

    #### NETWORK STAGE #####
    def __draw_network_stage(self):
        if not compare_digest(self.password_entry.get(), self.password_entry2.get()):
            Notification(title=self.lang.passwordmismatch, icon="warning.png", message=self.lang.passwordmsg, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if len(self.password_entry.get()) < MIN_PASSWORD_LENGTH:
            Notification(title=self.lang.pwd_length_title, icon="warning.png", message=self.lang.pwd_length, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if len(self.your_name_entry.get()) == 0:
            Notification(title=self.lang.empty_entry, icon="warning.png", message=self.lang.full_name_empty, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if len(self.hostname_entry.get()) == 0:
            Notification(title=self.lang.empty_entry, icon="warning.png", message=self.lang.hostname_empty, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if len(self.username_entry.get()) == 0:
            Notification(title=self.lang.username_empty, icon="warning.png", message=self.lang.username_empty, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        
        if not self.__validate_input(input=self.your_name_entry.get(), russian=True, spaces=True):
            Notification(title=self.lang.mismatch, icon="warning.png", message=self.lang.full_name_mismatch, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        if not self.__validate_input(input=self.hostname_entry.get(), russian=False, spaces=False):
            Notification(title=self.lang.mismatch, icon="warning.png", message=self.lang.hostname_mismatch, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        if not self.__validate_input(input=self.username_entry.get(), russian=False, spaces=False):
            Notification(title=self.lang.mismatch, icon="warning.png", message=self.lang.username_mismatch, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        self.setup_information["FullName"] = self.your_name_entry.get()
        self.setup_information["Hostname"] = self.hostname_entry.get()
        self.setup_information["Username"] = self.username_entry.get()
        self.setup_information["Password"] = self.password_entry.get()

        self.admin_frame.pack_forget()
        self.current_stage += 1
        if not hasattr(self, "network_frame"):
            self.network_stage()
        self.bind(("<Return>"), lambda event: self.__online_handler())

        self.__draw_stage(self.network_frame)
        self.__resize()
    
    def __return_to_admin(self):
        self.network_frame.pack_forget()
        self.current_stage -= 1
        self.bind(("<Return>"), lambda event: self.__draw_network_stage())
        self.__draw_stage(self.admin_frame)

    def network_stage(self):
        self.network_frame = CTkFrame(self)

        self.__draw_progress_bar(self.network_frame)
        title = CTkLabel(self.network_frame, text=self.lang.online_or_offline_title, font=(None, 16, 'bold'))
        image = CTkImage(light_image=Image.open(f"{WORKDIR}/images/wifi.png"), dark_image=Image.open(f"{WORKDIR}/images/wifi.png"), size=(80, 80))
        image_label = CTkLabel(self.network_frame, text="", image=image)
        label = CTkLabel(self.network_frame, text=self.lang.package_source)
        current_image = CTkLabel(self.network_frame, text=f"{self.lang.package_source_status}: {self.lang.offline if OFFLINE else self.lang.online}", font=(None, 14, 'bold'))
        back_button = CTkButton(self.network_frame, text=self.lang.back, command=self.__return_to_admin)
        offline_button = CTkButton(self.network_frame, text=self.lang.offline, command=self.__offline_handler)
        if not OFFLINE:
            offline_button.configure(state="disabled")
        online_button = CTkButton(self.network_frame, text=self.lang.online, command=self.__online_handler)

        title.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        image_label.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        label.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        offline_button.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        online_button.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")
        back_button.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        current_image.grid(row=4, column=1, padx=10, pady=5, sticky="nsew")


    def __online_handler(self):
        if not self.__check_network_connection():
            return
        self.online_installation = True
        self.__draw_apps_stage()
    
    def __offline_handler(self):
        self.online_installation = False
        self.__draw_apps_stage()

    def __draw_apps_stage(self):
        self.network_frame.pack_forget()
        self.current_stage += 1
        if not hasattr(self, "apps_frame"):
            self.apps_stage()
        self.bind(("<Return>"), lambda event: self.__draw_final())

        self.__draw_stage(self.apps_frame)

    #### END NETWORK STAGE #####

    #### BEGIN APPS STAGE ####

    def __return_to_network(self):
        self.apps_frame.pack_forget()
        self.current_stage -= 1
        self.bind(("<Return>"), lambda event: self.__draw_apps_stage())
        self.__draw_stage(self.network_frame)

    def apps_stage(self):
        self.apps_frame = CTkFrame(self)

        self.__draw_progress_bar(self.apps_frame)
        label = CTkLabel(self.apps_frame, text=self.lang.apps_label, font=(None, 16, 'bold'))
        tabview = CTkTabview(self.apps_frame)
        tabview.add("Secux")
        tabview.add("Pacman")

        tabview.set("Pacman")

        secux_tab = tabview.tab("Secux")
        pacman_tab = tabview.tab("Pacman")

        self.securitymanager = CTkCheckBox(secux_tab, text="Security Manager")
        self.kirt_app = CTkCheckBox(secux_tab, text=f"Kirt App")
        self.securitymanager.select()
        self.kirt_app.select()

        self.chromium = CTkCheckBox(pacman_tab, text="Chromium")
        self.firefox = CTkCheckBox(pacman_tab, text="Firefox")
        self.vlc = CTkCheckBox(pacman_tab, text="VLC")
        self.keepassxc = CTkCheckBox(pacman_tab, text="KeePassXC")
        self.libreoffice = CTkCheckBox(pacman_tab, text="Libreoffice")
        self.chromium.select()
        self.firefox.select()
        self.vlc.select()
        self.libreoffice.select()

        back_btn = CTkButton(self.apps_frame, text=self.lang.back, command=self.__return_to_network)
        next_btn = CTkButton(self.apps_frame, text=self.lang.next, command=self.__draw_final)

        self.apps_frame.grid_rowconfigure(2, weight=1)
        label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')
        tabview.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.securitymanager.pack(padx=10, pady=5, anchor='center')
        self.kirt_app.pack(padx=10, pady=5, anchor='center')

        self.chromium.pack(padx=10, pady=5, anchor='center')
        self.firefox.pack(padx=10, pady=5, anchor='center')
        self.vlc.pack(padx=10, pady=5, anchor='center')
        self.keepassxc.pack(padx=10, pady=5, anchor='center')
        self.libreoffice.pack(padx=10, pady=5, anchor='center')

        back_btn.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        next_btn.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")


    #### END APPS STAGE ####

    ##### BEGIN FINAL STAGE #####
    def __draw_final(self):
        self.setup_information["Apps"] = []
        # Secux tab
        if self.securitymanager.get():
            self.setup_information["Apps"].append("securitymanager")
        if self.kirt_app.get():
            self.setup_information["Apps"].append("kirt_app")
        
        # Pacman tab
        if self.chromium.get(): 
            self.setup_information["Apps"].append("chromium")
        if self.firefox.get(): 
            self.setup_information["Apps"].append("firefox")
        if self.vlc.get(): 
            self.setup_information["Apps"].append("vlc")
        if self.keepassxc.get(): 
            self.setup_information["Apps"].append("keepassxc")
        if self.libreoffice.get(): 
            self.setup_information["Apps"].append("libreoffice")
        
        self.apps_frame.pack_forget()
        self.current_stage += 1
        self.ui_scaling.configure(state='disabled')
        if hasattr(self, "final_frame"):
            for widget in self.final_frame.winfo_children():
                widget.destroy()
            del self.final_frame
        self.final_stage()
        self.bind(("<Return>"), lambda event: None)
        self.__draw_stage(self.final_frame)

    def __return_to_apps(self):
        self.final_frame.pack_forget()
        self.current_stage -= 1
        self.bind(("<Return>"), lambda event: self.__draw_final())
        self.__draw_stage(self.apps_frame)

    def final_stage(self):
        self.final_frame = CTkFrame(self)

        self.final_frame.grid_columnconfigure(1, weight=1)
        self.__draw_progress_bar(self.final_frame)
        label = CTkLabel(self.final_frame, text=self.lang.final, font=(None, 16, "bold"))
        timezone_label = CTkLabel(self.final_frame, text=self.lang.fulltimezone)
        timezone_entry = CTkEntry(self.final_frame)
        timezone_entry.insert(0, self.setup_information["Timezone"])
        timezone_entry.configure(state="disabled")

        installation_type_label = CTkLabel(self.final_frame, text=self.lang.installoption)
        installation_type_entry = CTkEntry(self.final_frame)
        match self.setup_information["InstallationType"]:
            case "Secure":
                installation_type_entry.insert(0, self.lang.securetype)
            case "InSecure":
                installation_type_entry.insert(0, self.lang.insecuretype)
            case "LessSecure":
                installation_type_entry.insert(0, self.lang.lessecuretype)
        installation_type_entry.configure(state="disabled")

        de_label = CTkLabel(self.final_frame, text=self.lang.de)
        de_entry = CTkEntry(self.final_frame)
        de_entry.insert(0, self.setup_information["DE"])
        de_entry.configure(state="disabled")

        partitioning_type_label = CTkLabel(self.final_frame, text=self.lang.partitioningtype)
        partitioning_type_entry = CTkEntry(self.final_frame)
        if self.setup_information["Partitioning"] == "Automatic":
            partitioning_type_entry.insert(0, self.lang.automatic)
            drive_to_format_label = CTkLabel(self.final_frame, text=self.lang.systeminstallto)
            drive_to_format_entry = CTkEntry(self.final_frame)
            drive_to_format_entry.insert(0, self.setup_information["DriveToFormat"])
            drive_to_format_entry.configure(state="disabled")
        else:
            partitioning_type_entry.insert(0, self.lang.manual)
            loader_label = CTkLabel(self.final_frame, text=self.lang.efipart)
            loader_entry = CTkEntry(self.final_frame)
            loader_entry.insert(0, self.setup_information["EfiPartition"])
            loader_entry.configure(state="disabled")

            system_label = CTkLabel(self.final_frame, text=self.lang.rootfs)
            system_entry = CTkEntry(self.final_frame)
            system_entry.insert(0, self.setup_information["SystemPartition"])
            system_entry.configure(state="disabled")
        partitioning_type_entry.configure(state="disabled")

        use_swap_label = CTkLabel(self.final_frame, text=self.lang.useswap)
        use_swap_entry = CTkEntry(self.final_frame)
        if self.setup_information["UseSwap"]:
            use_swap_entry.insert(0, self.lang.yes)
            swap_size_label = CTkLabel(self.final_frame, text=self.lang.swapsize_final)
            swap_size_entry = CTkEntry(self.final_frame)
            swap_size_entry.insert(0, self.setup_information["SwapSize"])
            swap_size_entry.configure(state="disabled")
        else:
            use_swap_entry.insert(0, self.lang.no)
        use_swap_entry.configure(state="disabled")

        hostname_label =CTkLabel(self.final_frame, text=self.lang.hostname)
        hostname_entry = CTkEntry(self.final_frame)
        hostname_entry.insert(0, self.setup_information["Hostname"])
        hostname_entry.configure(state="disabled")

        fullname_label = CTkLabel(self.final_frame, text=self.lang.yourname)
        fullname_entry = CTkEntry(self.final_frame)
        fullname_entry.insert(0, self.setup_information["FullName"])
        fullname_entry.configure(state="disabled")

        username_label = CTkLabel(self.final_frame, text=self.lang.username)
        username_entry = CTkEntry(self.final_frame)
        username_entry.insert(0, self.setup_information['Username'])
        username_entry.configure(state="disabled")

        back_button = CTkButton(self.final_frame, text=self.lang.back, command=self.__return_to_apps)
        begin_installation_button = CTkButton(self.final_frame, text=self.lang.begin_install, command=self.begin_installation_ui)

        i = 1
        label.grid(row=i, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        
        i += 1
        timezone_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        timezone_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")
        
        i += 1
        installation_type_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        installation_type_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")

        i += 1
        de_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        de_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")

        i += 1
        partitioning_type_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        partitioning_type_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")
        
        i += 1
        if self.setup_information["Partitioning"] == "Automatic":
            drive_to_format_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
            drive_to_format_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")
        else:
            loader_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
            loader_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")
            i += 1
            system_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
            system_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")

        i += 1
        use_swap_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        use_swap_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")

        if self.setup_information["UseSwap"]:
            i += 1
            swap_size_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
            swap_size_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")
        
        i += 1
        hostname_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        hostname_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")

        i += 1
        fullname_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        fullname_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")

        i += 1
        username_label.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        username_entry.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")

        i += 1
        back_button.grid(row=i, column=0, padx=15, pady=5, sticky="nsew")
        begin_installation_button.grid(row=i, column=1, padx=15, pady=5, sticky="nsew")
    
    ##### END FINAL STAGE #####

    ##### BEGIN INSTALLTION #####
    def __list_partitions(self, drive):
        result = subprocess.run(['lsblk', '-ln', '-o', 'NAME,TYPE'], stdout=subprocess.PIPE, text=True)
        partitions = []
        for line in result.stdout.splitlines():
            name, type_ = line.split()
            if type_ == 'part' and name.startswith(drive.replace('/dev/', '')):
                partitions.append(f"/dev/{name}")
        return partitions

    def _execute(self, command: str, input: str = None):
        cmd = {"command": command}
        if input:
            cmd["input"] = input
        self.commands.append(cmd)


    def _execute_commands(self, commands: list):
        def run_commands():
            for cmd in commands:
                try:
                    print(f"Executing: {cmd['command']}")
                    process = subprocess.Popen(
                        cmd["command"],
                        stdin=subprocess.PIPE if "input" in cmd else None,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True,
                        text=True,
                        executable="/bin/bash",
                        bufsize=1  # Line-buffered output
                    )
                    if "input" in cmd:
                        process.stdin.write(cmd["input"])
                        process.stdin.close()

                    def update_console(text):
                        self.console.configure(state="normal")
                        self.console.insert(END, text)
                        self.console.see(END)
                        self.console.configure(state="disabled")

                    for line in process.stdout:
                        print(line, end="")
                        self.console.after(0, update_console, line)

                    for line in process.stderr:
                        print(line, end="")
                        self.console.after(0, update_console, line)

                    process.wait()
                    print("\n")

                except Exception as e:
                    self.console.after(0, update_console, f"Error: {str(e)}\n")

        threading.Thread(target=run_commands, daemon=True).start()

    def __check_secure_boot_and_setup_mode(self):
        uefi_support = False
        secure_boot = False
        setup_mode = False
        secure_boot_path = "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c"
        setup_mode_path = "/sys/firmware/efi/efivars/SetupMode-8be4df61-93ca-11d2-aa0d-00e098032b8c"

        process = subprocess.run("[ -d /sys/firmware/efi ] && echo -n UEFI || echo -n BIOS", shell=True, capture_output=True)
        if process.stdout == b"UEFI":
            uefi_support = True

        def read_efi_var(path):
            try:
                with open(path, "rb") as f:
                    # EFI variable data starts after the first 4 bytes of metadata
                    return ord(f.read()[4:5])  # Convert byte to int
            except FileNotFoundError:
                return 0
        
        if uefi_support:
            secure_boot = read_efi_var(secure_boot_path)
            setup_mode = read_efi_var(setup_mode_path)

        return (uefi_support, secure_boot, setup_mode)
    
    def __get_ucode_package(self):
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "vendor_id" in line:
                        if "GenuineIntel" in line:
                            return "intel-ucode"
                        elif "AuthenticAMD" in line:
                            return "amd-ucode"
            return "amd-ucode intel-ucode"
        except FileNotFoundError:
            return "amd-ucode intel-ucode"

    def __check_network_connection(self) -> bool:
        try:
            answ = get("http://gstatic.com/generate_204", timeout=5)
        except ConnectionError:
            Notification(title=self.lang.network_title, icon="warning.png", message=self.lang.network, message_bold=True, exit_btn_msg=self.lang.exit)
            return False
        if answ.status_code != 204:
            Notification(title=self.lang.network_title, icon="warning.png", message=self.lang.network, message_bold=True, exit_btn_msg=self.lang.exit)
            return False
        return True


    def __begin_installation_ui(self):
        if DEBUG:
            Notification(title=self.lang.debug_title, icon="redcross.png", message=self.lang.debug_mode, message_bold=True, exit_btn_msg=self.lang.exit)
            return

        for widget in self.winfo_children():
            widget.destroy()
        
        self.geometry("600x400")

        calm_emoji = CTkImage(light_image=Image.open(f"{WORKDIR}/images/calm.png"), dark_image=Image.open(f"{WORKDIR}/images/calm.png"), size=(80, 80))
        calm_emoji_label = CTkLabel(self, text="", image=calm_emoji)
        calm_emoji_label.pack(padx=10, pady=10)
        label = CTkLabel(self, text=self.lang.installing)
        label.pack(padx=10, pady=10)
        self.console = CTkTextbox(self)
        self.console.pack(padx=10, pady=10, expand=True, fill="both")
        self.begin_installation()

    def begin_installation_ui(self):
        uefi_info = self.__check_secure_boot_and_setup_mode()
        if not uefi_info[0]:
            Notification(title=self.lang.not_uefi_title, icon="warning.png", message=self.lang.not_uefi, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        
        if self.setup_information["InstallationType"] == "Secure":
            if uefi_info[1] != 0 and uefi_info[2] != 1:
                Notification(title=self.lang.not_setup_mode_title, icon="warning.png", message=self.lang.not_setup_mode, message_bold=False, exit_btn_msg=self.lang.exit)
                return
        
        if self.online_installation:
            if not self.__check_network_connection():
                Notification(title=self.lang.network_title, icon="warning.png", message=self.lang.network, message_bold=True, exit_btn_msg=self.lang.exit)
                return
        self.__begin_installation_ui()
        

    def __split_device(self, device):
        match = re.match(r"(.+?)(p?\d+)$", device)
        if match:
            base, num = match.groups()
            if base.endswith("p"):  # Remove trailing 'p' for nvme devices
                base = base[:-1]
            return base, num.lstrip("p")  # Remove 'p' from number
        return device, ""

    def begin_installation(self):
        self.commands = []
        
        if not DEBUG_SHOW_COMMANDS:
            # Prepare partitions
            if self.setup_information["Partitioning"] == "Automatic":
                os.system(f"sgdisk -Z {self.setup_information["DriveToFormat"]}")
                os.system(f"sgdisk -n1:0:+1G -t1:ef00 -c1:EFI -N2 -t2:8304 {self.setup_information["DriveToFormat"]}")
                partitions = self.__list_partitions(self.setup_information["DriveToFormat"])
                efi_partition = partitions[0]
                rootfs_partition = partitions[1]
            else:
                efi_partition = self.setup_information["EfiPartition"]
                rootfs_partition = self.setup_information["SystemPartition"]
        else:
            efi_partition = DEBUG_SHOW_COMMANDS_EFI_PARTITION
            rootfs_partition = DEBUG_SHOW_COMMANDS_ROOTFS_PARTITION

        # Creating LUKS partition
        self._execute(f"cryptsetup luksFormat {rootfs_partition}", input=f"{self.setup_information["EncryptionKey"]}")
        self._execute(f"cryptsetup luksOpen {rootfs_partition} cryptlvm", input=f"{self.setup_information["EncryptionKey"]}")
        
        # Creating LVM
        self._execute("pvcreate /dev/mapper/cryptlvm")
        self._execute("vgcreate volumegroup /dev/mapper/cryptlvm")
        
        # Creating swap partition if needed
        if self.setup_information["UseSwap"] == False:
            self._execute("lvcreate -l 100%FREE volumegroup -n root")
        else:
            self._execute(f"lvcreate -L {self.setup_information["SwapSize"]}G volumegroup -n swap")
            self._execute("lvcreate -l 100%FREE volumegroup -n root")
        
        # Formatting root partition
        self._execute("mkfs.ext4 /dev/volumegroup/root")
        
        # Formatting swap partition
        if self.setup_information["UseSwap"]:
            self._execute("mkswap /dev/volumegroup/swap")
        
        # Formatting EFI partition if needed
        if self.setup_information["Partitioning"] == "Automatic":
            self._execute(f"mkfs.fat -F32 {efi_partition}")

        # Mounting root partition to /mnt and enabling swap if needed
        self._execute(f"mount /dev/volumegroup/root /mnt")
        if self.setup_information["UseSwap"]:
            self._execute("swapon /dev/volumegroup/swap")
        
        # Creating and mounting EFI partition
        self._execute(f"mount --mkdir -o uid=0,gid=0,fmask=0077,dmask=0077 {efi_partition} /mnt/efi")

        # Installing OS
        # NOTE: when installing linux-lts or linux-hardened DO NOT forget about linux-lts-headers and linux-hardened-headers
        if self.online_installation:
            self._execute("cp /etc/pacman_online.conf /etc/pacman.conf")
        else:
            self._execute("cp /etc/pacman_offline.conf /etc/pacman.conf")
        kernels = " ".join(self.setup_information["Kernel"]) + " " + " ".join([i+'-headers' for i in self.setup_information["Kernel"]])
        pacstrap_command = f"stdbuf -oL pacstrap -K /mnt base {kernels} linux-firmware {self.__get_ucode_package()} vim nano efibootmgr sudo plymouth python-pip lvm2 networkmanager systemd-ukify sbsigntools efitools less git ntfs-3g gvfs gvfs-mtp xdg-user-dirs fwupd apparmor ufw "

        if self.setup_information["InstallationType"] == "Secure":
            pacstrap_command += "sbctl "
        elif self.setup_information["InstallationType"] == "LessSecure":
            pacstrap_command += "shim-signed mokutil "
        
        if 'securitymanager' in self.setup_information["Apps"] or 'kirt_app' in self.setup_information["Apps"]:
            pacstrap_command += "base-devel cmake v4l-utils tk python-pexpect python-pillow "
        if 'vlc' in self.setup_information["Apps"]:
            pacstrap_command += "vlc "
        if 'firefox' in self.setup_information["Apps"]:
            pacstrap_command += "firefox "
        if 'chromium' in self.setup_information["Apps"]:
            pacstrap_command += "chromium "
        if 'libreoffice' in self.setup_information["Apps"]:
            pacstrap_command += "libreoffice "
        if 'keepassxc' in self.setup_information["Apps"]:
            pacstrap_command += "keepassxc "
        
        if self.setup_information["DE"] == "GNOME":
            pacstrap_command += "xorg gnome networkmanager-openvpn gnome-tweaks gdm "
        elif self.setup_information["DE"] == "KDE":
            pacstrap_command += "xorg plasma networkmanager-openvpn kde-applications "

        
        self._execute(pacstrap_command)
        
        self._execute("echo Packages were installed successfully.")
        # Adding custom repo
        self._execute(f'echo "[kolbanidze]\nServer = {REPO_URL}\n" >> /mnt/etc/pacman.conf')
        self._execute("cp /usr/share/pacman/keyrings/kolbanidze* /mnt/usr/share/pacman/keyrings")
        # self._execute("arch-chroot /mnt pacman-key --recv CE48F2CC9BE03B4EFAB02343AA0A42D146D35FCE")
        self._execute("arch-chroot /mnt pacman-key --add /usr/share/pacman/keyrings/kolbanidze.gpg")
        self._execute("arch-chroot /mnt pacman-key --lsign-key CE48F2CC9BE03B4EFAB02343AA0A42D146D35FCE")

        # Generating fstab
        self._execute("genfstab -U /mnt >> /mnt/etc/fstab")

        # Creating user
        self._execute(f"arch-chroot /mnt useradd -m {self.setup_information["Username"]} -c \"{self.setup_information["FullName"]}\"")
        
        # Setting password for user
        self._execute(f"arch-chroot /mnt passwd {self.setup_information["Username"]}", input=f"{self.setup_information["Password"]}\n{self.setup_information["Password"]}\n")

        # Making user admin
        self._execute("echo \"%wheel ALL=(ALL:ALL) ALL\" >> /mnt/etc/sudoers ")
        self._execute(f"arch-chroot /mnt usermod -aG wheel {self.setup_information["Username"]}")
        
        # Configuring timezone
        self._execute(f"arch-chroot /mnt ln -sf /usr/share/zoneinfo/{self.setup_information['Timezone']} /etc/localtime")
        
        # Creating mkinitcpio.conf
        self._execute('echo -e "MODULES=()\nBINARIES=()\nFILES=()\nHOOKS=(base systemd autodetect microcode modconf kms keyboard sd-vconsole plymouth block sd-encrypt lvm2 filesystems fsck)" > /mnt/etc/mkinitcpio.conf')
        
        # Creating cmdline
        self._execute("mkdir /mnt/etc/cmdline.d")
        self._execute(f"echo \"rd.luks.name=$(blkid -s UUID -o value {rootfs_partition})=cryptlvm root=/dev/volumegroup/root rw rootfstype=ext4 rd.shell=0 rd.emergency=reboot quiet oops=panic init_on_alloc=1 init_on_free=1 pti=on lockdown=confidentiality lsm=landlock,lockdown,yama,integrity,apparmor,bpf splash\" > /mnt/etc/cmdline.d/root.conf")

        # Creating UKI config
        self._execute('echo -e "[UKI]\nOSRelease=@/etc/os-release\nPCRBanks=sha256\n\n[PCRSignature:initrd]\nPhases=enter-initrd\nPCRPrivateKey=/etc/kernel/pcr-initrd.key.pem\nPCRPublicKey=/etc/kernel/pcr-initrd.pub.pem" > /mnt/etc/kernel/uki.conf')

        # Generate ukify keys
        self._execute("arch-chroot /mnt ukify genkey --config=/etc/kernel/uki.conf")

        # Configure UKI generation
        for kernel in self.setup_information["Kernel"]:
            self._execute(f"sed -i '/^default_config/s/^/#/' /mnt/etc/mkinitcpio.d/{kernel}.preset")
            self._execute(f"sed -i '/^default_image/s/^/#/' /mnt/etc/mkinitcpio.d/{kernel}.preset")
            self._execute(f"sed -i '/^#default_uki/s/^#//' /mnt/etc/mkinitcpio.d/{kernel}.preset")
            self._execute(f"sed -i '/^#default_options/s/^#//' /mnt/etc/mkinitcpio.d/{kernel}.preset")
            
            self._execute(f"sed -i '/^fallback_config/s/^/#/' /mnt/etc/mkinitcpio.d/{kernel}.preset")
            self._execute(f"sed -i '/^fallback_image/s/^/#/' /mnt/etc/mkinitcpio.d/{kernel}.preset")
            self._execute(f"sed -i '/^#fallback_uki/s/^#//' /mnt/etc/mkinitcpio.d/{kernel}.preset")
            self._execute(f"sed -i '/^#fallback_options/s/^#//' /mnt/etc/mkinitcpio.d/{kernel}.preset")

        # Set default plymouth theme
        self._execute("arch-chroot /mnt plymouth-set-default-theme")

        # Prepare EFI Partition
        self._execute("mkdir -p /mnt/efi/EFI/Linux")
        
        # Change distro info and logo
        self._execute("cp /etc/os-release /mnt/etc/os-release")
        self._execute("cp /usr/local/share/secux-installer/images/bootlogo.bmp /mnt/usr/share/icons")
        self._execute("cp /usr/local/share/secux-installer/images/secux.svg /mnt/usr/share/icons")
        for kernel in self.setup_information["Kernel"]:
            self._execute(f"sed -i 's|/usr/share/systemd/bootctl/splash-arch.bmp|/usr/share/icons/bootlogo.bmp|' /mnt/etc/mkinitcpio.d/{kernel}.preset")
        self._execute("rm /mnt/usr/share/factory/etc/ssh/sshd_config.d/99-archlinux.conf")
        self._execute("rm /mnt/etc/debuginfod/archlinux.urls")
        self._execute("rm /etc/ssh/sshd_config.d/99-archlinux.conf")
        self._execute("rm /mnt/etc/arch-release")
        self._execute("rm /mnt/usr/share/factory/etc/arch-release")
        self._execute("rm /mnt/usr/share/plymouth/themes/spinner/watermark.png")

        # Generate UKI
        for kernel in self.setup_information["Kernel"]:
            self._execute(f"arch-chroot /mnt mkinitcpio -p {kernel}")
        
        # Make NetworkManager run at boot
        self._execute("arch-chroot /mnt systemctl enable NetworkManager")

        # Add languages support
        if self.language == 'ru':
            self._execute('echo "ru_RU.UTF-8 UTF-8" >> /mnt/etc/locale.gen')
            self._execute('echo LANG=\"ru_RU.UTF-8\" > /mnt/etc/locale.conf')
        else:
            self._execute('echo "en_US.UTF-8 UTF-8" >> /mnt/etc/locale.gen')
            self._execute('echo LANG=\"en_US.UTF-8\" > /mnt/etc/locale.conf')
        self._execute("arch-chroot /mnt locale-gen")

        # Hostname
        self._execute(f'echo "{self.setup_information["Hostname"]}" > /mnt/etc/hostname')

        # Make GDM/SDDM run at boot
        if self.setup_information["DE"] == "GNOME":
            self._execute("arch-chroot /mnt systemctl enable gdm")
        elif self.setup_information["DE"] == "KDE":
            self._execute("arch-chroot /mnt systemctl enable sddm")
        
        # SDDM Theme
        if self.setup_information["DE"] == "KDE":
            self._execute("sed -i '/^\\# Current theme name/{n;s/^Current=.*/Current=breeze/}' /mnt/usr/lib/sddm/sddm.conf.d/default.conf")
        
        # GDM remove arch logo
        if self.setup_information["DE"] == "GNOME":
            self._execute("arch-chroot /mnt sudo -u gdm dbus-launch gsettings set org.gnome.login-screen logo ''")

        # Install bootloader
        self._execute("arch-chroot /mnt bootctl install --esp-path=/efi")
        
        # Generate sbctl keys
        if self.setup_information["InstallationType"] == "Secure":
            self._execute("arch-chroot /mnt sbctl create-keys")
            self._execute("arch-chroot /mnt sbctl enroll-keys --yes-this-might-brick-my-machine")
        
        # Signing EFI executables and storing them in the database for signing during updates
        if self.setup_information["InstallationType"] == "Secure":
            self._execute("arch-chroot /mnt sbctl sign --save /efi/EFI/BOOT/BOOTX64.EFI")
            self._execute("arch-chroot /mnt sbctl sign --save /efi/EFI/systemd/systemd-bootx64.efi")
            for kernel in self.setup_information["Kernel"]:
                self._execute(f"arch-chroot /mnt sbctl sign --save /efi/EFI/Linux/arch-{kernel}-fallback.efi")
                self._execute(f"arch-chroot /mnt sbctl sign --save /efi/EFI/Linux/arch-{kernel}.efi")
        
        # Creating trusted boot chain with microsoft keys
        if self.setup_information["InstallationType"] == "LessSecure":
            self._execute("cp /mnt/usr/share/shim-signed/shimx64.efi /mnt/efi/EFI/Linux/shimx64.efi")
            self._execute("cp /mnt/usr/share/shim-signed/mmx64.efi /mnt/efi/EFI/Linux/mmx64.efi")
            self._execute("mkdir -p /mnt/etc/secureboot")
            self._execute('openssl req -newkey rsa:4096 -nodes -keyout /mnt/etc/secureboot/sb.key -x509 -out /mnt/etc/secureboot/sb.crt -subj "/CN=SECUX MOK/"')
            self._execute("openssl x509 -outform DER -in /mnt/etc/secureboot/sb.crt -out /mnt/etc/secureboot/sb.cer")
            self._execute("arch-chroot /mnt sbsign --key /etc/secureboot/sb.key --cert /etc/secureboot/sb.crt --output /efi/EFI/systemd/systemd-bootx64.efi /usr/lib/systemd/boot/efi/systemd-bootx64.efi")
            self._execute("echo DEBUG thing.")
            for kernel in self.setup_information["Kernel"]:
                self._execute(f"echo Signing {kernel}")
                self._execute(f"arch-chroot /mnt sbsign --key /etc/secureboot/sb.key --cert /etc/secureboot/sb.crt --output /efi/EFI/Linux/arch-{kernel}.efi /efi/EFI/Linux/arch-{kernel}.efi")
                self._execute(f"arch-chroot /mnt sbsign --key /etc/secureboot/sb.key --cert /etc/secureboot/sb.crt --output /efi/EFI/Linux/arch-{kernel}-fallback.efi /efi/EFI/Linux/arch-{kernel}-fallback.efi")
                self._execute(f"echo Successfully signed {kernel}")
            self._execute('echo Importing MOK')
            self._execute("arch-chroot /mnt mokutil --import /etc/secureboot/sb.cer", input=f"{MOK_PASSWORD}\n{MOK_PASSWORD}\n")
            self._execute("cp /usr/local/share/secux-installer/scripts/92-shim-signed.hook /mnt/usr/share/libalpm/hooks/")
            self._execute("cp /usr/local/share/secux-installer/scripts/shim-copy.sh /mnt/usr/share/")
            self._execute("chmod +x /mnt/usr/share/shim-copy.sh")
            self._execute("cp /usr/local/share/secux-installer/scripts/91-systemd-boot.hook /mnt/usr/share/libalpm/hooks/")
            self._execute("cp /usr/local/share/secux-installer/scripts/systemd-boot-sign.sh /mnt/usr/share")
            self._execute("chmod +x /mnt/usr/share/systemd-boot-sign.sh")
            self._execute("cp /usr/local/share/secux-installer/scripts/sign-uki.sh /mnt/usr/lib/initcpio/post")
            self._execute("chmod +x /mnt/usr/lib/initcpio/post/sign-uki.sh")
            self._execute("cp /mnt/efi/EFI/systemd/systemd-bootx64.efi /mnt/efi/EFI/Linux/grubx64.efi")
            base, num = self.__split_device(efi_partition)
            self._execute("echo Adding bootentry.")
            self._execute(f'efibootmgr --create --disk {base} --part {num} --label "SECUX SHIM" --loader "\\EFI\\Linux\\shimx64.efi"')

        # Installing secux-apps
        if 'securitymanager' in self.setup_information["Apps"]:
            self._execute("mkdir -p /mnt/usr/local/bin/secux-apps")
            if self.online_installation:
                self._execute("git clone https://github.com/kolbanidze/secux-apps /mnt/usr/local/bin/secux-apps --depth=1")
            else:
                self._execute("cp /usr/local/share/secux-apps/* /mnt/usr/local/bin/secux-apps/ -r")
            self._execute("cp /usr/local/share/secux-installer/scripts/org.freedesktop.policykit.securitymanager.policy /mnt/usr/share/polkit-1/actions/")
            self._execute("touch /mnt/usr/local/bin/secux-apps/production.conf")
            self._execute("cp /usr/local/share/secux-installer/scripts/securitymanager.desktop /mnt/usr/share/applications")
            self._execute("chmod +x /mnt/usr/share/applications/securitymanager.desktop")
            self._execute("chmod +x /mnt/usr/local/bin/secux-apps/manager.py")

            # Dependencies
            self._execute("pacstrap /mnt tk python-pexpect python-pillow python-darkdetect python-packaging")
            if self.online_installation:
                self._execute("arch-chroot /mnt pip install customtkinter --break-system-packages")
            else:
                self._execute(f"cp {WORKDIR}/python_packages/customtkinter* /mnt/root/")
                self._execute(f"arch-chroot /mnt pip install customtkinter --find-links /root --no-index --break-system-packages")
                self._execute(f"rm -rf /mnt/root/customtkinter*")

        # Installing Kirt App
        if 'kirt_app' in self.setup_information["Apps"]:
            self._execute("mkdir -p /mnt/usr/local/bin/kirt-app")
            if self.online_installation:
                self._execute("git clone https://github.com/kirt-king/test_app /mnt/usr/local/bin/kirt-app --depth=1")
            else:
                self._execute("cp /usr/local/share/kirt-app/* /mnt/usr/local/bin/kirt-app/ -r")
            self._execute("cp /usr/local/share/secux-installer/scripts/org.freedesktop.policykit.kirt-app.policy /mnt/usr/share/polkit-1/actions/")
            self._execute("cp /usr/local/share/secux-installer/scripts/kirt-app.desktop /mnt/usr/share/applications")
            self._execute("chmod +x /mnt/usr/share/applications/kirt-app.desktop")
            self._execute("chmod +x /mnt/usr/local/bin/kirt-app/app_script/app.py")

            # Dependencies
            self._execute("pacstrap /mnt tk base-devel cmake python-pillow python-opencv python-numpy python-setuptools python-dotenv python-darkdetect python-packaging python-dlib")
            if self.online_installation:
                self._execute("arch-chroot /mnt pip install customtkinter face_recognition face_recognition_models --break-system-packages")
            else:
                self._execute(f"cp -r {WORKDIR}/python_packages/ /mnt/root/")
                self._execute(f"arch-chroot /mnt pip install customtkinter face_recognition face_recognition_models screeninfo --find-links /root/python_packages --no-index --break-system-packages")
                self._execute(f"rm -rf /mnt/root/python_packages")
                # self._execute(f"cp {WORKDIR}/python_packages /mnt/home/{self.setup_information["Username"]} -r")
                # # self._execute(f"arch-chroot /mnt pip install --find-links /tmp/python_packages customtkinter setuptools screeninfo python-dotenv face_recognition face_recognition_models --break-system-packages")
                # # self._execute(f"arch-chroot /mnt bash -c \"pip install /home/{self.setup_information['Username']}/python_packages/setuptools* --break-system-packages\"")
                # self._execute(f"arch-chroot /mnt bash -c \"pip install /home/{self.setup_information['Username']}/python_packages/* --break-system-packages\"")
                # self._execute(f"rm -rf /home/{self.setup_information['Username']}/python_packages")

        # Hardening
        self._execute("arch-chroot /mnt systemctl enable apparmor")
        self._execute("cp /usr/local/share/secux-installer/scripts/hardening.conf /mnt/etc/sysctl.d")
        self._execute("arch-chroot /mnt systemctl enable ufw")
        self._execute("arch-chroot /mnt ufw default deny")

        # Final message in console
        self._execute("echo [Installation finished!]")
        self._execute("echo [Now you can close this window and reboot into the system.]")
        self._execute("echo [Установка завершена!]")
        self._execute("echo [Теперь вы можете закрыть это окно и перезагрузиться в систему.]")

        # Execute commands
        if not DEBUG_SHOW_COMMANDS:
            self._execute_commands(self.commands)
        else:
            for i in self.commands:
                if 'input' in i:
                    print('#')
                    print(i['command'], "# ВНИМАНИЕ. ТРЕБУЕТ ВВОДА ДАННЫХ ПОЛЬЗОВАТЕЛЕМ")
                    print('#')
                else:
                    print(i['command'])
                print()


if __name__ == "__main__":
    App().mainloop()

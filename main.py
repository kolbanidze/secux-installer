from customtkinter import *
from PIL import Image
from language import Locale
from requests import get
from requests.exceptions import ConnectionError
from hmac import compare_digest
from psutil import virtual_memory
from contextlib import redirect_stdout, redirect_stderr
from collections.abc import Callable
from typing import Any, Optional, List, Dict, Tuple, Union
import subprocess
import json
import os
import re
import io
import string
import threading
import shlex
import queue

timezones = {'Africa': ['Abidjan', 'Accra', 'Addis_Ababa', 'Algiers', 'Asmara', 'Bamako', 'Bangui', 'Banjul', 'Bissau', 'Blantyre', 'Brazzaville', 'Bujumbura', 'Cairo', 'Casablanca', 'Ceuta', 'Conakry', 'Dakar', 'Dar_es_Salaam', 'Djibouti', 'Douala', 'El_Aaiun', 'Freetown', 'Gaborone', 'Harare', 'Johannesburg', 'Juba', 'Kampala', 'Khartoum', 'Kigali', 'Kinshasa', 'Lagos', 'Libreville', 'Lome', 'Luanda', 'Lubumbashi', 'Lusaka', 'Malabo', 'Maputo', 'Maseru', 'Mbabane', 'Mogadishu', 'Monrovia', 'Nairobi', 'Ndjamena', 'Niamey', 'Nouakchott', 'Ouagadougou', 'Porto-Novo', 'Sao_Tome', 'Tripoli', 'Tunis', 'Windhoek'], 'America': ['Adak', 'Anchorage', 'Anguilla', 'Antigua', 'Araguaina', 'Argentina/Buenos_Aires', 'Argentina/Catamarca', 'Argentina/Cordoba', 'Argentina/Jujuy', 'Argentina/La_Rioja', 'Argentina/Mendoza', 'Argentina/Rio_Gallegos', 'Argentina/Salta', 'Argentina/San_Juan', 'Argentina/San_Luis', 'Argentina/Tucuman', 'Argentina/Ushuaia', 'Aruba', 'Asuncion', 'Atikokan', 'Bahia', 'Bahia_Banderas', 'Barbados', 'Belem', 'Belize', 'Blanc-Sablon', 'Boa_Vista', 'Bogota', 'Boise', 'Cambridge_Bay', 'Campo_Grande', 'Cancun', 'Caracas', 'Cayenne', 'Cayman', 'Chicago', 'Chihuahua', 'Costa_Rica', 'Creston', 'Cuiaba', 'Curacao', 'Danmarkshavn', 'Dawson', 'Dawson_Creek', 'Denver', 'Detroit', 'Dominica', 'Edmonton', 'Eirunepe', 'El_Salvador', 'Fort_Nelson', 'Fortaleza', 'Glace_Bay', 'Godthab', 'Goose_Bay', 'Grand_Turk', 'Grenada', 'Guadeloupe', 'Guatemala', 'Guayaquil', 'Guyana', 'Halifax', 'Havana', 'Hermosillo', 'Indiana/Indianapolis', 'Indiana/Knox', 'Indiana/Marengo', 'Indiana/Petersburg', 'Indiana/Tell_City', 'Indiana/Vevay', 'Indiana/Vincennes', 'Indiana/Winamac', 'Inuvik', 'Iqaluit', 'Jamaica', 'Juneau', 'Kentucky/Louisville', 'Kentucky/Monticello', 'Kralendijk', 'La_Paz', 'Lima', 'Los_Angeles', 'Lower_Princes', 'Maceio', 'Managua', 'Manaus', 'Marigot', 'Martinique', 'Matamoros', 'Mazatlan', 'Menominee', 'Merida', 'Metlakatla', 'Mexico_City', 'Miquelon', 'Moncton', 'Monterrey', 'Montevideo', 'Montserrat', 'Nassau', 'New_York', 'Nipigon', 'Nome', 'Noronha', 'North_Dakota/Beulah', 'North_Dakota/Center', 'North_Dakota/New_Salem', 'Ojinaga', 'Panama', 'Pangnirtung', 'Paramaribo', 'Phoenix', 'Port-au-Prince', 'Port_of_Spain', 'Porto_Velho', 'Puerto_Rico', 'Rainy_River', 'Rankin_Inlet', 'Recife', 'Regina', 'Resolute', 'Rio_Branco', 'Santarem', 'Santiago', 'Santo_Domingo', 'Sao_Paulo', 'Scoresbysund', 'Sitka', 'St_Barthelemy', 'St_Johns', 'St_Kitts', 'St_Lucia', 'St_Thomas', 'St_Vincent', 'Swift_Current', 'Tegucigalpa', 'Thule', 'Thunder_Bay', 'Tijuana', 'Toronto', 'Tortola', 'Vancouver', 'Whitehorse', 'Winnipeg', 'Yakutat', 'Yellowknife'], 'Antarctica': ['Casey', 'Davis', 'DumontDUrville', 'Macquarie', 'Mawson', 'McMurdo', 'Palmer', 'Rothera', 'Syowa', 'Troll', 'Vostok'], 'Arctic': ['Longyearbyen'], 'Asia': ['Aden', 'Almaty', 'Amman', 'Anadyr', 'Aqtau', 'Aqtobe', 'Ashgabat', 'Atyrau', 'Baghdad', 'Bahrain', 'Baku', 'Bangkok', 'Barnaul', 'Beirut', 'Bishkek', 'Brunei', 'Chita', 'Choibalsan', 'Colombo', 'Damascus', 'Dhaka', 'Dili', 'Dubai', 'Dushanbe', 'Famagusta', 'Gaza', 'Hebron', 'Ho_Chi_Minh', 'Hong_Kong', 'Hovd', 'Irkutsk', 'Jakarta', 'Jayapura', 'Jerusalem', 'Kabul', 'Kamchatka', 'Karachi', 'Kathmandu', 'Khandyga', 'Kolkata', 'Krasnoyarsk', 'Kuala_Lumpur', 'Kuching', 'Kuwait', 'Macau', 'Magadan', 'Makassar', 'Manila', 'Muscat', 'Nicosia', 'Novokuznetsk', 'Novosibirsk', 'Omsk', 'Oral', 'Phnom_Penh', 'Pontianak', 'Pyongyang', 'Qatar', 'Qyzylorda', 'Riyadh', 'Sakhalin', 'Samarkand', 'Seoul', 'Shanghai', 'Singapore', 'Srednekolymsk', 'Taipei', 'Tashkent', 'Tbilisi', 'Tehran', 'Thimphu', 'Tokyo', 'Tomsk', 'Ulaanbaatar', 'Urumqi', 'Ust-Nera', 'Vientiane', 'Vladivostok', 'Yakutsk', 'Yangon', 'Yekaterinburg', 'Yerevan'], 'Atlantic': ['Azores', 'Bermuda', 'Canary', 'Cape_Verde', 'Faroe', 'Madeira', 'Reykjavik', 'South_Georgia', 'St_Helena', 'Stanley'], 'Australia': ['Adelaide', 'Brisbane', 'Broken_Hill', 'Currie', 'Darwin', 'Eucla', 'Hobart', 'Lindeman', 'Lord_Howe', 'Melbourne', 'Perth', 'Sydney'], 'Europe': ['Amsterdam', 'Andorra', 'Astrakhan', 'Athens', 'Belgrade', 'Berlin', 'Bratislava', 'Brussels', 'Bucharest', 'Budapest', 'Busingen', 'Chisinau', 'Copenhagen', 'Dublin', 'Gibraltar', 'Guernsey', 'Helsinki', 'Isle_of_Man', 'Istanbul', 'Jersey', 'Kaliningrad', 'Kiev', 'Kirov', 'Lisbon', 'Ljubljana', 'London', 'Luxembourg', 'Madrid', 'Malta', 'Mariehamn', 'Minsk', 'Monaco', 'Moscow', 'Oslo', 'Paris', 'Podgorica', 'Prague', 'Riga', 'Rome', 'Samara', 'San_Marino', 'Sarajevo', 'Saratov', 'Simferopol', 'Skopje', 'Sofia', 'Stockholm', 'Tallinn', 'Tirane', 'Ulyanovsk', 'Uzhgorod', 'Vaduz', 'Vatican', 'Vienna', 'Vilnius', 'Volgograd', 'Warsaw', 'Zagreb', 'Zaporozhye', 'Zurich'], 'Indian': ['Antananarivo', 'Chagos', 'Christmas', 'Cocos', 'Comoro', 'Kerguelen', 'Mahe', 'Maldives', 'Mauritius', 'Mayotte', 'Reunion'], 'Pacific': ['Apia', 'Auckland', 'Bougainville', 'Chatham', 'Chuuk', 'Easter', 'Efate', 'Enderbury', 'Fakaofo', 'Fiji', 'Funafuti', 'Galapagos', 'Gambier', 'Guadalcanal', 'Guam', 'Honolulu', 'Johnston', 'Kiritimati', 'Kosrae', 'Kwajalein', 'Majuro', 'Marquesas', 'Midway', 'Nauru', 'Niue', 'Norfolk', 'Noumea', 'Pago_Pago', 'Palau', 'Pitcairn', 'Pohnpei', 'Port_Moresby', 'Rarotonga', 'Saipan', 'Tahiti', 'Tarawa', 'Tongatapu', 'Wake', 'Wallis']}

VERSION = "0.3.1"
DEBUG = False
DEBUG_AUTOENTRY = False # Default: False
DEBUG_AUTOENTRY_VALUES = ['asd', 'asdasdasd']

MIN_PASSWORD_LENGTH = 8

REPO_URL = "https://kolbanidze.github.io/secux-repo/x86_64/"

MOK_PASSWORD = "123"

WORKDIR = os.path.dirname(os.path.abspath(__file__))

if os.path.isfile(WORKDIR + "/debug.conf"):
    DEBUG = True

OFFLINE = False
if os.path.isfile(WORKDIR + "/offline_installation.conf"):
    OFFLINE = True

class Notification(CTkToplevel):
    def __init__(self, title: str, icon: str, message: str, message_bold: bool, exit_btn_msg: str):
        super().__init__()
        self.title(title)
        img = Image.open(os.path.join(WORKDIR, "images", icon))
        image = CTkImage(light_image=img, dark_image=img, size=(80, 80))
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
        self.title("Secux Linux")
        self.language = "ru"
        self.setup_information = {}
        self.ui_scale = 1
        self.light_theme = False
        self.current_stage = 0
        self.total_amount_of_stages = 10
        set_appearance_mode("dark")
        self.installation_failed = False

        self.welcome_menu = CTkFrame(self)
        self.welcome_menu.pack(fill='both', expand=True)

        self.clicks = 0
        welcome_image = CTkImage(light_image=Image.open(f'{WORKDIR}/images/waving_hand.png'), dark_image=Image.open(f'{WORKDIR}/images/waving_hand.png'), size=(80,80))
        welcome_image_label = CTkLabel(self.welcome_menu, text="", image=welcome_image)
        welcome_image_label.bind("<Button-1>", self.__clicks_handler)
        welcome_entry_label = CTkLabel(self.welcome_menu, text=f"Добро пожаловать в установщик дистрибутива Secux Linux\nWelcome to Secux Linux distribution installer")        
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

        uefi_info = self.__check_secure_boot_and_setup_mode()
        if not uefi_info[0]:
            Notification(title="Отсутствие поддержки UEFI | No UEFI support", icon="warning.png", message="Система не поддерживает UEFI. Установка невозможна.\nThe system does not support UEFI. Installation is not possible.", message_bold=True, exit_btn_msg="Выйти | Exit")
        
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
        updater_welcome = CTkLabel(self, text=f"Secux Linux installer updater | Обновления установщика Secux Linux")
        run_update = CTkButton(self, text="Update | Обновить", command=self.__update_repo)
        self.updater_textbox = CTkTextbox(self, state="disabled")
        after_update = CTkLabel(self, text="Для применения обновлений необходимо перезапустить программу.\nTo apply updates, you must restart the program.")
        exit_button = CTkButton(self, text="Закрыть программу | Close the program", command=self.destroy)
        if DEBUG: print("I will remember this code forever. How much time was spent to fix this unfortunate segmentation fault... Interesting adventure: https://pastebin.com/ASiE2FVe")

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
                "git fetch; git reset --hard; git pull origin main",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
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
        secure_type_label = CTkLabel(self.installation_type_frame, text=self.lang.secure_label, font=("Arial", 12), text_color="light grey")
        self.less_secure_type = CTkRadioButton(self.installation_type_frame, value=1, variable=self.installation_type_variable, text=self.lang.lessecuretype, command=self.__installation_type_radio_button_handler)
        less_secure_type_label = CTkLabel(self.installation_type_frame, text=self.lang.less_secure_label, font=("Arial", 12), text_color="light grey")
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
        self.secure_type.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=(5, 0))
        secure_type_label.grid(row=3, column=0, columnspan=2, padx=45, pady=(0,10), sticky="w")
        self.less_secure_type.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=15, pady=0)
        less_secure_type_label.grid(row=5, column=0, columnspan=2, padx=45, pady=(0,10), sticky="w")
        self.insecure_type.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=15, pady=(0,5))

        back_btn.grid(row=7, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=7, column=1, padx=15, pady=5, sticky="nsew")
    
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
            self.setup_information["Kernel"].append('linux-hardened-headers')
        if self.linux_lts.get():
            self.setup_information["Kernel"].append('linux-lts')
            self.setup_information["Kernel"].append('linux-lts-headers')
        if self.linux.get():
            self.setup_information["Kernel"].append("linux")
            self.setup_information["Kernel"].append("linux-headers")

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
        self.linux_hardened = CTkCheckBox(self.kernel_frame, text=f"Linux Hardened ({self.lang.hardened_security})", command=self.__kernel_select_handler)
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
        if len(erase_all_disks) == 0:
            erase_all_disks = [self.lang.drives_not_found]
            self.bind(("<Return>"), lambda event: None)
        
        self.partitioning_type = IntVar(value=0)
        erase_all_partitioning = CTkRadioButton(self.partitioning_frame, text=self.lang.erase_all_and_install, variable=self.partitioning_type, value=0)
        self.erase_all_disk = CTkOptionMenu(self.partitioning_frame, values=erase_all_disks)
        manual_partitioning = CTkRadioButton(self.partitioning_frame, text=self.lang.manual, variable=self.partitioning_type, value=1)
        back_btn = CTkButton(self.partitioning_frame, text=self.lang.back, command=self.__return_to_kernel)
        next_btn = CTkButton(self.partitioning_frame, text=self.lang.next, command=self.__partitioning_next_button_handler)
        if erase_all_disks == [self.lang.drives_not_found]:
            next_btn.configure(state="disabled")

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

        self.partitions = []
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    self.partitions.append(f"{partition['name']} | {partition['size']} | {partition.get('fstype', 'N/A')}")

        # Max swap size: Total RAM (GiB) + 8 GiB
        max_swap = round(virtual_memory().total / (1024*1024*1024)) + 8

        self.__draw_progress_bar(self.manual_partitioning_frame)
        label = CTkLabel(self.manual_partitioning_frame, text=self.lang.selfpart, font=(None, 16, "bold"))
        run_gparted_btn = CTkButton(self.manual_partitioning_frame, text=self.lang.rungparted, command=lambda: os.system("/usr/bin/sudo /usr/bin/gparted"))
        update_disks = CTkButton(self.manual_partitioning_frame, text=self.lang.refreshparts, command=self.__update_partitions)
        efi_partition_label = CTkLabel(self.manual_partitioning_frame, text=self.lang.efipart)
        self.efi_partition_optionmenu = CTkOptionMenu(self.manual_partitioning_frame, values=self.partitions)
        efi_partition_explain_label = CTkLabel(self.manual_partitioning_frame, text="Раздел, в котором хранится загрузчик системы. Должен быть отформатирован в FAT32 и иметь размер не менее 200 МиБ (рекомендуется 1 ГиБ)", font=("Arial", 12), text_color="light grey")
        root_partition_label = CTkLabel(self.manual_partitioning_frame, text=self.lang.rootfs)
        self.root_partition_optionmenu = CTkOptionMenu(self.manual_partitioning_frame, values=self.partitions)
        root_partition_explain = CTkLabel(self.manual_partitioning_frame, text="Основной раздел для установки операционной системы и хранения данных. Используется LVM с файловой системой EXT4", font=("Arial", 12), text_color="light grey")
        self.use_swap = StringVar(value="on")
        self.swap_checkbox = CTkCheckBox(self.manual_partitioning_frame, text=self.lang.useswap, variable=self.use_swap, onvalue="on", offvalue="off", command=self.__swapfile_handler)
        swapfile_explain = CTkLabel(self.manual_partitioning_frame, text="Файл подкачки расширяет оперативную память за счёт диска", font=("Arial", 12), text_color="light grey")
        swap_label = CTkLabel(self.manual_partitioning_frame, text=self.lang.swapsize)
        self.swap_entry = CTkEntry(self.manual_partitioning_frame)
        self.swap_entry.insert(0, "1")
        self.swap_scrollbar = CTkSlider(self.manual_partitioning_frame, command=self.__scroll_handler, to=max_swap, number_of_steps=max_swap)
        back_btn = CTkButton(self.manual_partitioning_frame, text=self.lang.back, command=lambda: self.__return_to_partitioning(self.manual_partitioning_frame))
        next_btn = CTkButton(self.manual_partitioning_frame, text=self.lang.next, command=self.__draw_encryption_stage_from_manual)

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        run_gparted_btn.grid(row=2, column=0, padx=15, pady=(5, 10), sticky="nsew")
        update_disks.grid(row=2, column=1, padx=15, pady=(5, 10), sticky="nsew")
        efi_partition_label.grid(row=3, column=0, padx=15, pady=0, sticky="nsew")
        self.efi_partition_optionmenu.grid(row=3, column=1, padx=15, pady=0, sticky="nsew")
        efi_partition_explain_label.grid(row=4, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="nsew")

        root_partition_label.grid(row=5, column=0, padx=15, pady=(5,0), sticky="nsew")
        self.root_partition_optionmenu.grid(row=5, column=1, padx=15, pady=(5, 0), sticky="nsew")
        root_partition_explain.grid(row=6, column=0, columnspan=2, padx=15, pady=(0, 10), sticky="nsew")

        self.swap_checkbox.grid(row=7, column=0, padx=15, pady=(5,0), sticky="nsew")
        swapfile_explain.grid(row=8, column=1, padx=15, pady=(5,0), sticky="nsew")
        swap_label.grid(row=8, column=0, padx=15, pady=0, sticky="nsew")
        self.swap_entry.grid(row=9, column=0, padx=15, pady=(0,5), sticky="nsew")
        self.swap_scrollbar.grid(row=9, column=1, padx=15, pady=(0,5), sticky="nsew")
        back_btn.grid(row=10, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=10, column=1, padx=15, pady=5, sticky="nsew")

    def __scroll_handler(self, newvalue):
        newvalue = round(newvalue)
        self.swap_entry.delete(0, 'end')
        self.swap_entry.insert(0, str(int(newvalue)))
    
    def __swapfile_handler(self):
        if self.swap_checkbox.get() == "off":
            self.swap_entry.configure(state="disabled")
            self.swap_scrollbar.configure(state="disabled")
        else:
            self.swap_entry.configure(state="normal")
            self.swap_scrollbar.configure(state="normal")

    def __update_partitions(self):
        self.partitions.clear()
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    self.partitions.append(f"{partition['name']} | {partition['size']} | {partition.get('fstype', 'N/A')}")
        self.efi_partition_optionmenu.configure(values=self.partitions)
        self.root_partition_optionmenu.configure(values=self.partitions)

    # def __change_max_swapfile(self, newvalue):
    #     if self.swap_checkbox.get() == "off":
    #         return
    #     half_of_max_space = int(self.__get_max_swap_size() / (2**30))//2
    #     if half_of_max_space == 0:
    #         Notification(title=self.lang.swap_part_too_small, icon="warning.png", message=self.lang.swap_part_too_small, message_bold=False, exit_btn_msg=self.lang.exit)
    #         self.swap_scrollbar.configure(state="disabled")
    #         return 
    #     else:
    #         self.swap_scrollbar.configure(state="normal")
    #     self.swap_scrollbar.configure(to=half_of_max_space)

    # def __get_max_swap_size(self):
    #     """by default returns 16 GiB in bytes"""
    #     current_partition = self.root_partition_optionmenu.get().split(" | ")[0]
    #     disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE', '--json', '-ba'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
    #     current_partition_size = 17179869184 # bytes
    #     for disk in disks:
    #         if 'children'in disk:
    #             for partition in disk['children']:
    #                 if partition['name'] == current_partition:
    #                     current_partition_size = partition['size']
    #                     break
    #     return current_partition_size

    def __draw_encryption_stage_from_manual(self):
        efi_partition = self.efi_partition_optionmenu.get().split(" | ")[0]
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE', '--json', '-ba'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    if partition['name'] == efi_partition:
                        efi_partition_size = partition['size']
                        efi_fstype = partition['fstype']
                    if partition['name'] == self.root_partition_optionmenu.get().split(" | ")[0]:
                        system_partition_size = partition['size']
        if efi_partition_size < 209715200:
            Notification(title=self.lang.efi_small_title, icon="warning.png", message=self.lang.efi_small, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if efi_fstype != "vfat":
            Notification(title=self.lang.error, icon="warning.png", message=self.lang.efi_fstype_error, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        system_partition = "/dev/" + self.root_partition_optionmenu.get().split(" | ")[0]
        use_swapfile = ("on" == self.swap_checkbox.get())

        if use_swapfile:
            swapsize = self.swap_entry.get()
            try:
                if '.' in swapsize or ',' in swapsize:
                    raise ValueError
                swapsize = int(swapsize)
            except ValueError:
                Notification(title=self.lang.error, icon='warning.png', message=self.lang.swapsize_error, message_bold=False, exit_btn_msg=self.lang.exit)
                return
            if swapsize*(1024*1024*1024) > system_partition_size:
                Notification(title=self.lang.error, icon='warning.png', message=self.lang.swapsize_large, message_bold=False, exit_btn_msg=self.lang.exit)
                return
            self.setup_information["SwapSize"] = str(swapsize)
        if system_partition_size < (10*1024*1024*1024 + swapsize*1024*1024*1024):
            Notification(title=self.lang.error, icon='warning.png', message=self.lang.system_partition_small, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        self.setup_information["Partitioning"] = "Manual"
        self.setup_information["EfiPartition"] = "/dev/" + efi_partition
        self.setup_information["SystemPartition"] = system_partition
        self.setup_information["UseSwap"] = use_swapfile
        
        self.bind(("<Return>"), lambda event: self.__draw_admin_creation())
        self.manual_partitioning_frame.pack_forget()
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
        self.KIRTapp = CTkCheckBox(secux_tab, text=f"KIRTapp")
        self.securitymanager.select()
        self.KIRTapp.select()

        self.chromium = CTkCheckBox(pacman_tab, text="Chromium")
        self.firefox = CTkCheckBox(pacman_tab, text="Firefox")
        self.vlc = CTkCheckBox(pacman_tab, text="VLC")
        self.keepassxc = CTkCheckBox(pacman_tab, text="KeePassXC")
        self.libreoffice = CTkCheckBox(pacman_tab, text="Libreoffice")
        self.chromium.select()

        back_btn = CTkButton(self.apps_frame, text=self.lang.back, command=self.__return_to_network)
        next_btn = CTkButton(self.apps_frame, text=self.lang.next, command=self.__draw_final)

        self.apps_frame.grid_rowconfigure(2, weight=1)
        label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky='nsew')
        tabview.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.securitymanager.pack(padx=10, pady=5, anchor='center')
        self.KIRTapp.pack(padx=10, pady=5, anchor='center')

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
            self.setup_information["Apps"].append("Security Manager")
        if self.KIRTapp.get():
            self.setup_information["Apps"].append("KIRTapp")
        
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

    def __close(self, popup, close_self: bool, reboot: bool):
        popup.destroy()
        if close_self: 
            self.destroy()
        if reboot:
            os.system("systemctl reboot")

    def __installation_success(self):
        if not self.installation_failed:
            popup = CTkToplevel(self)
            popup.title(self.lang.success)
            image = CTkImage(light_image=Image.open(f"{WORKDIR}/images/greencheck.png"), dark_image=Image.open(f"{WORKDIR}/images/greencheck.png"), size=(80,80))
            image_label = CTkLabel(popup, text="", image=image)
            label = CTkLabel(popup, text=self.lang.installation_success, font=(None, 16, "bold"))
            continue_working = CTkButton(popup, text=self.lang.continue_working, command=lambda: self.__close(popup, close_self=True, reboot=False))
            reboot = CTkButton(popup, text=self.lang.reboot, command=lambda: self.__close(popup, close_self=True, reboot=True))

            image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            continue_working.grid(row=2, column=0, padx=(10,5), pady=10, sticky="nsew")
            reboot.grid(row=2, column=1, padx=(5, 10), pady=10, sticky="nsew")

    def __installation_failed(self):
        if not self.installation_failed:
            popup = CTkToplevel(self)
            popup.title(self.lang.success)
            image = CTkImage(light_image=Image.open(f"{WORKDIR}/images/redcross.png"), dark_image=Image.open(f"{WORKDIR}/images/redcross.png"), size=(80,80))
            image_label = CTkLabel(popup, text="", image=image)
            label = CTkLabel(popup, text=self.lang.installation_failed, font=(None, 16, "bold"))
            continue_working = CTkButton(popup, text=self.lang.continue_working, command=lambda: self.__close(popup, close_self=False, reboot=False))
            reboot = CTkButton(popup, text=self.lang.reboot, command=lambda: self.__close(popup, close_self=True, reboot=True))

            image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            continue_working.grid(row=2, column=0, padx=(10,5), pady=10, sticky="nsew")
            reboot.grid(row=2, column=1, padx=(5, 10), pady=10, sticky="nsew")
            self.installation_failed = True

    def __check_secure_boot_and_setup_mode(self):
        uefi_support = True
        secure_boot = False
        setup_mode = False

        process = subprocess.run(["/usr/bin/mokutil", "--sb-state"], capture_output=True)
        mokutil_output = process.stdout
        if b"not supported" in process.stderr or len(mokutil_output) == 0:
            uefi_support = False
        if b"enabled" in mokutil_output:
            secure_boot = True
        if b"Setup Mode" in mokutil_output:
            setup_mode = True

        return (uefi_support, secure_boot, setup_mode)
    
    def __get_ucode_package(self) -> list:
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "vendor_id" in line:
                        if "GenuineIntel" in line:
                            return ["intel-ucode"]
                        elif "AuthenticAMD" in line:
                            return ["amd-ucode"]
            return ["amd-ucode", "intel-ucode"]
        except FileNotFoundError:
            return ["amd-ucode", "intel-ucode"]

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

    def __mok_handler(self):
        if self.mok_entry_1.get() != self.mok_entry_2.get():
            Notification(title=self.lang.passwordmismatch, icon="warning.png", message=self.lang.passwordmsg, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if len(self.mok_entry_1.get()) < 3:
            Notification(title=self.lang.pwd_length_title, icon="warning.png", message=self.lang.pwd_length_mok, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if not self.__validate_english_keymap(self.mok_entry_1.get()):
            Notification(title=self.lang.encryption_password_title, icon="warning.png", message=self.lang.encryption_password, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        
        self.setup_information["MOK"] = self.mok_entry_1.get()
        self.__begin_installation_ui()

    def mok_stage(self):
        title = CTkLabel(self, text="Выберите одноразовый пароль MOK", font=(None, 16, "bold"))
        self.mok_entry_1 = CTkEntry(self, show='*')
        self.mok_entry_2 = CTkEntry(self, show='*')
        next_btn = CTkButton(self, text="Продолжить установку", command=self.__mok_handler)

        title.pack(padx=15, pady=5)
        self.mok_entry_1.pack(padx=15, pady=5)
        self.mok_entry_2.pack(padx=15, pady=5)
        next_btn.pack(padx=15, pady=5)


    def __begin_installation_ui(self):
        if DEBUG:
            Notification(title=self.lang.debug_title, icon="redcross.png", message=self.lang.debug_mode, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        
        for widget in self.winfo_children():
            widget.destroy()

        if self.setup_information["InstallationType"] == "LessSecure" and self.setup_information.get("MOK", True):
            self.mok_stage()
            return
        
        self.geometry("600x400")

        img = Image.open(f"{WORKDIR}/images/calm.png")
        calm_emoji = CTkImage(light_image=img, dark_image=img, size=(80, 80))
        calm_emoji_label = CTkLabel(self, text="", image=calm_emoji)
        calm_emoji_label.pack(padx=10, pady=10)
        label = CTkLabel(self, text=self.lang.installing)
        label.pack(padx=10, pady=10)
        self.console = CTkTextbox(self, wrap='word', state='disabled', font=("monospace", 12))
        self.console.pack(fill='both', expand=True, padx=10, pady=10)
        self.begin_installation()

    def begin_installation_ui(self):
        uefi_info = self.__check_secure_boot_and_setup_mode()
        if not uefi_info[0]:
            Notification(title=self.lang.not_uefi_title, icon="warning.png", message=self.lang.not_uefi, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        
        if self.setup_information["InstallationType"] == "Secure":
            if not uefi_info[2]:
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

    def update_console(self, text: str):
        """
        Safely updates the console Textbox from any thread by scheduling
        the update in the main thread's event loop.
        """
        # Use self.after(0, ...) to ensure this runs in the main GUI thread
        # This is thread-safe
        def _do_update():
            if self.console.winfo_exists(): # Check if widget exists
                try:
                    self.console.configure(state="normal")
                    self.console.insert(END, str(text)) # Ensure text is string
                    self.console.see(END) # Scroll to the end
                    self.console.configure(state="disabled")
                    # NO self.update_idletasks() here - rely on main loop / wait loop
                except Exception as e:
                    # Fallback if GUI update fails (e.g., during shutdown)
                    print(f"ERROR (update_console): {e}\n{text}", file=sys.stderr)

        # Schedule the actual update to run in the main thread
        self.after(0, _do_update)


    def _worker_loop(self):
        """The loop run by the background worker thread."""
        while True:
            try:
                # Wait for a task from the main thread
                task = self.task_queue.get()
                if task is None: # Sentinel for stopping the thread
                    # print("Worker thread received stop signal.")
                    break

                task_type, task_data, completion_event = task
                result = None
                exception = None

                try:
                    if task_type == 'execute':
                        command, input_str = task_data
                        result = self._run_command_in_worker(command, input_str)
                    elif task_type == 'execute_function':
                        func, args, kwargs = task_data
                        result = self._run_function_in_worker(func, args, kwargs)
                    else:
                        raise ValueError(f"Unknown task type: {task_type}")
                except Exception as e:
                    # Capture any exception during task execution
                    exception = e
                    self.update_console(f"✘ {self.lang.unexpected_error} {e}\n")
                    import traceback
                    self.update_console(traceback.format_exc() + "\n")
                    # Ensure result indicates failure if needed (e.g., return code for command)
                    if task_type == 'execute':
                        result = -2 # General error code
                finally:
                    # Store result and signal completion *regardless* of success/failure
                    # The main thread needs to know the task is done
                    self._current_task_result = result
                    self._current_task_exception = exception
                    completion_event.set() # Signal the waiting main thread

            except Exception as e:
                # Handle errors in the worker loop itself (e.g., queue issues)
                # Use print as update_console might rely on the main loop which could be blocked
                print(f"FATAL ERROR in worker loop: {e}", file=sys.stderr)
                # Optionally break or log more severely


    def _run_command_in_worker(self, command: List[str], input_str: Optional[str]) -> int:
        """Executed by the worker thread to run an external command."""
        display_cmd = ' '.join(shlex.quote(str(c)) for c in command)
        self.update_console(f"\n▶ {self.lang.executing_command} {display_cmd}\n")

        process = None
        return_code = -1 # Default to error

        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE if input_str is not None else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                encoding='utf-8',
                errors='replace'
            )

            # Handle stdin if provided
            if input_str is not None and process.stdin:
                try:
                    process.stdin.write(input_str)
                    process.stdin.close() # Signal end of input
                except OSError as e:
                    self.update_console(f"✘ {self.lang.error_writing_to_stdin} {e}\n")
                    try: process.kill()
                    except OSError: pass
                    process.wait() # Wait after killing
                    self.update_console(f"✘ {self.lang.command_failed_stdin}\n")
                    return process.returncode if process.returncode is not None else -1

            # --- Real-time Output Handling (Worker Thread) ---
            stdout_lines = []
            stderr_lines = []

            def read_stream(stream, output_list, prefix=""):
                """Reads lines from a stream and schedules updates."""
                try:
                    for line in iter(stream.readline, ''):
                        if line:
                            output_list.append(line)
                            self.update_console(f"{prefix}{line}") # Schedule GUI update
                        else:
                            break # End of stream
                except Exception as e:
                     self.update_console(f"\nError reading stream ({prefix}): {e}\n")
                finally:
                    try:
                        stream.close()
                    except OSError:
                        pass # Ignore errors on close

            # Use separate threads to read stdout and stderr concurrently
            # This prevents blocking if one pipe fills up while waiting for the other
            stdout_thread = None
            stderr_thread = None

            if process.stdout:
                stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, stdout_lines))
                stdout_thread.start()

            if process.stderr:
                stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, stderr_lines))
                stderr_thread.start()

            # Wait for reader threads to finish
            if stdout_thread:
                stdout_thread.join()
            if stderr_thread:
                stderr_thread.join()

            # Wait for the process to terminate and get the final return code
            return_code = process.wait()

            # Final status update
            if return_code == 0:
                self.update_console(f"✔ {self.lang.command_success} {return_code})\n")
            else:
                self.__installation_failed()
                self.update_console(f"✘ {self.lang.command_failed} {return_code})\n")

        except FileNotFoundError:
            self.__installation_failed()
            self.update_console(f"✘ {self.lang.command_not_found} '{command[0]}'\n")
            return_code = -1 # Specific error code
        except Exception as e:
            # Catch other Popen errors or issues before stream reading
            self.__installation_failed()
            self.update_console(f"✘ {self.lang.unexpected_error} executing command: {e}\n")
            return_code = -2 # General error code
        finally:
            # Ensure process is cleaned up if it's still running (e.g., due to early exit)
             if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception:
                    pass # Ignore cleanup errors
                if return_code == -1: # If not already set by error
                    return_code = -3 # Indicate killed process

        return return_code


    def _run_function_in_worker(self, func: Callable[..., Any], args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
        """Executed by the worker thread to run a Python function."""
        func_name = getattr(func, '__name__', repr(func))
        self.update_console(f"\n▶ {self.lang.executing_function} {func_name}\n")

        f_stdout = io.StringIO()
        f_stderr = io.StringIO()
        return_value = None
        success = False

        try:
            with redirect_stdout(f_stdout), redirect_stderr(f_stderr):
                return_value = func(*args, **kwargs)
            success = True # If no exception occurred during func call

        except Exception as e:
            # Exception already captured by the main worker loop's try/except
            # We just need to format the output here
            self.__installation_failed()
            self.update_console(f"✘ {self.lang.error_during_function_execution} {func_name}: {e}\n")
            # Traceback is handled by the outer exception handler in _worker_loop

        finally:
            # Get captured output
            stdout_val = f_stdout.getvalue()
            stderr_val = f_stderr.getvalue()
            f_stdout.close()
            f_stderr.close()

            # Display captured output via the main thread
            if stdout_val:
                self.update_console(stdout_val)
            if stderr_val:
                # Indicate it's stderr from the function itself
                self.update_console(f"{func_name}:\n{stderr_val}")

            # Final status update based on whether the function call itself succeeded
            if success:
                self.update_console(f"✔ {self.lang.function} '{func_name}' {self.lang.succeed}\n")
                # Display return value safely
                try:
                    return_repr = repr(return_value)
                    limit = 250
                    if len(return_repr) > limit:
                        return_repr = return_repr[:limit] + "..."
                    self.update_console(f"  {self.lang.return_value} {return_repr}\n")
                except Exception as repr_e:
                     self.update_console(f"  ({self.lang.couldnt_return_value}: {repr_e})\n")
            else:
                 # Error message already printed in except block or outer handler
                 self.__installation_failed()
                 self.update_console(f"✘ {self.lang.function} '{func_name}' {self.lang.failed}\n")

        # Return the value (or None if exception) to _worker_loop
        return return_value if success else None

    def _execute(self,
                 command: List[str],
                 input_str: Optional[str] = None) -> Optional[int]:
        """
        Schedules a shell command for execution in the background worker thread.
        Blocks *logically* until the command completes, while keeping the GUI responsive.
        Outputs stdout/stderr to the console in real-time via the worker.

        Args:
            command: A list of strings representing the command and its arguments.
            input_str: Optional string to be passed to the command's stdin.

        Returns:
            The exit code of the command (int) or None if task setup failed.
            Returns specific negative codes on internal errors.
        """
        if not command:
            self.update_console(f"{self.lang.empty_cli}\n")
            return None # Or a specific error code like -10
        
        if command[0] == '__INTERNAL_INSTALLATION_SUCCESS':
            self.__installation_success()
            return

        completion_event = threading.Event()
        task_data = (command, input_str)
        task = ('execute', task_data, completion_event)

        # Reset result/exception holders before submitting
        self._current_task_result = None
        self._current_task_exception = None

        self.task_queue.put(task)

        # Wait for the worker to signal completion, while processing GUI events
        while not completion_event.is_set():
            # self.update() processes pending Tkinter events, keeping UI alive
            # Add a small sleep to prevent pegging CPU in this loop
            self.update()

        # Task is done, retrieve the result stored by the worker
        # Check if an exception occurred in the worker *during* execution
        if self._current_task_exception:
             # Error messages should have been printed by worker
             # Return the failure code set by the worker's exception handler
             return self._current_task_result if isinstance(self._current_task_result, int) else -2

        # Return the actual result (exit code)
        return self._current_task_result


    def _execute_function(self,
                          func: Callable[..., Any],
                          args: Tuple[Any, ...] = (),
                          kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Schedules a Python function for execution in the background worker thread.
        Captures its stdout/stderr and return value.
        Blocks *logically* until the function completes, while keeping the GUI responsive.

        Args:
            func: The Python function to execute.
            args: Positional arguments for the function.
            kwargs: Keyword arguments for the function.

        Returns:
            The return value of the function, or None if an exception occurred
            during its execution in the worker thread.
        """
        if kwargs is None:
            kwargs = {}

        completion_event = threading.Event()
        task_data = (func, args, kwargs)
        task = ('execute_function', task_data, completion_event)

        # Reset result/exception holders
        self._current_task_result = None
        self._current_task_exception = None

        self.task_queue.put(task)

        # Wait for the worker to signal completion, keeping GUI responsive
        while not completion_event.is_set():
            self.update()

        # Task is done, retrieve result
        # If an exception was caught by the worker's main try/except for this task
        if self._current_task_exception:
             # Error messages printed by worker. Function effectively failed.
             return None # Indicate failure by returning None

        # Return the actual result stored by the worker
        return self._current_task_result


    def on_closing(self):
        """Handles window closing."""
        self.destroy()

    def begin_installation(self):
        self.commands = []
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.task_queue = queue.Queue()
        self._current_task_result = None
        self._current_task_exception = None
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

        efi_partition = ""
        rootfs_partition = ""
        if self.setup_information["Partitioning"] == "Automatic":
            drive = self.setup_information["DriveToFormat"]
            self.update_console(f"INFO: {self.lang.autopart} {drive}\n")
            if self._execute(['sgdisk', '-Z', drive]) != 0:
                self.update_console(f"ERROR: {self.lang.sgdisk_error}!\n")
                return

            if self._execute(['sgdisk', f'-n1:0:+1G', '-t1:ef00', '-c1:EFI', '-N2', '-t2:8304', drive]) != 0:
                self.update_console(f"ERROR: {self.lang.sgdisk_part_error}!\n")
                return

            partitions = self.__list_partitions(drive)
            if len(partitions) < 2:
                self.update_console(f"ERROR: {self.lang.failed_to_find} {drive}!\n")
                return
            
            efi_partition = partitions[0]
            rootfs_partition = partitions[1]
            self.update_console(f"INFO: EFI: {efi_partition}, OS: {rootfs_partition}\n")
        else: # Manual Partitioning
            efi_partition = self.setup_information["EfiPartition"]
            rootfs_partition = self.setup_information["SystemPartition"]
            self.update_console(f"INFO: {self.lang.selfpart}. EFI: {efi_partition}, OS: {rootfs_partition}\n")

            efi_base_drive, efi_number = self.__split_device(efi_partition)
            self._execute(['sgdisk', f'--typecode={efi_number}:ef00', efi_base_drive])

        if not efi_partition or not rootfs_partition:
             self.update_console(f"ERROR: {self.lang.failed_to_detect_parts}\n")
             return


        # Creating LUKS partition
        self._execute(['cryptsetup', 'luksFormat', rootfs_partition], input_str=self.setup_information["EncryptionKey"]) 
        self._execute(['cryptsetup', 'luksOpen', rootfs_partition, 'cryptlvm'], input_str=self.setup_information["EncryptionKey"])
        
        # Creating LVM
        self._execute(['pvcreate', '/dev/mapper/cryptlvm'])
        self._execute(['vgcreate', 'volumegroup', '/dev/mapper/cryptlvm'])
        
        self._execute(['lvcreate', '-l', '100%FREE', 'volumegroup', '-n', 'root']) 
        
        # Formatting root partition
        root_lv_path = "/dev/volumegroup/root"
        self._execute(['mkfs.ext4', root_lv_path])
                
        # Formatting EFI partition if needed
        if self.setup_information["Partitioning"] == "Automatic":
            self._execute(['mkfs.fat', '-F32', efi_partition])

        # Mounting root partition to /mnt and enabling swap if needed
        mount_point = '/mnt'
        efi_mount_point = os.path.join(mount_point, 'efi')

        self._execute(['mount', root_lv_path, mount_point])
        if self.setup_information["UseSwap"]:
            swap_path = f'{mount_point}/swapfile'
            swap_size_gb = self.setup_information["SwapSize"]
            self._execute(['fallocate', '-l', f'{swap_size_gb}G', swap_path])
            self._execute(['chmod', '600', swap_path]) 
            self._execute(['mkswap', swap_path])
            self._execute(['swapon', swap_path])


        # Creating and mounting EFI partition
        self._execute(['mount', '--mkdir', '-o', 'uid=0,gid=0,fmask=0077,dmask=0077', efi_partition, efi_mount_point])

        # Installing OS
        if self.online_installation:
            self._execute(['cp', '/etc/pacman_online.conf', '/etc/pacman.conf'])
        else:
            self._execute(['cp', '/etc/pacman_offline.conf', '/etc/pacman.conf'])
            self._execute(['pacman-key', '--init'])
            self._execute(['pacman-key', '--populate', 'archlinux'])
            self._execute(['pacman-key', '--populate', 'kolbanidze'])

        pacstrap_packages = ['base', 'base-devel', 'linux-firmware', 'vim', 'nano', 'efibootmgr', 'sudo', 'plymouth', 'python-pip', 'lvm2', 'networkmanager', 'systemd-ukify', 'sbsigntools', 'efitools', 'less', 'git', 'ntfs-3g', 'gvfs', 'gvfs-mtp', 'xdg-user-dirs', 'fwupd', 'apparmor', 'ufw', 'flatpak', 'mokutil']
        pacstrap_packages.extend(self.__get_ucode_package())
        kernels_no_headers = [k for k in self.setup_information["Kernel"] if 'headers' not in k]
        pacstrap_packages.extend(kernels_no_headers)

        if self.setup_information["InstallationType"] == "Secure":
            pacstrap_packages.append("sbctl")
        elif self.setup_information["InstallationType"] == "LessSecure":
            pacstrap_packages.append("shim-signed")
        
        if 'Security Manager' in self.setup_information["Apps"]:
            pacstrap_packages.extend(['tk', 'python-pexpect', 'python-pillow', 'python-darkdetect', 'python-packaging', 'libpam-google-authenticator', 'python-qrcode'])
        if 'KIRTapp' in self.setup_information["Apps"]:
            pacstrap_packages.extend(["tk", "v4l-utils", "python-pillow", "python-opencv", "python-numpy", "python-setuptools", "python-dotenv", "python-darkdetect", "python-packaging", "python-dlib", "python-sqlalchemy", "python-psycopg2"])
        
        if 'vlc' in self.setup_information["Apps"]:
            pacstrap_packages.append('vlc')
        if 'firefox' in self.setup_information["Apps"]:
            pacstrap_packages.append('firefox')
        if 'chromium' in self.setup_information["Apps"]:
            pacstrap_packages.append('chromium')
        if 'libreoffice' in self.setup_information["Apps"]:
            pacstrap_packages.append('libreoffice')
        if 'keepassxc' in self.setup_information["Apps"]:
            pacstrap_packages.append('keepassxc')
        
        if self.setup_information["DE"] == "GNOME":
            pacstrap_packages.extend(["xorg", "gnome", "networkmanager-openvpn", "gnome-tweaks", "gdm"])
        if self.setup_information["DE"] == "KDE":
            pacstrap_packages.extend(["xorg", "plasma", "networkmanager-openvpn", "kde-applications"])
        
        pacstrap_cmd = ['stdbuf', '-oL', 'pacstrap', '-K', mount_point] + pacstrap_packages

        # Leaving only kernels, not headers
        self._execute(pacstrap_cmd) 
        
        # Adding custom repo
        repo_conf_line = f'\n[kolbanidze]\nServer = {REPO_URL}\n'
        self._execute(['arch-chroot', mount_point, 'bash', '-c', f'echo -e "{repo_conf_line}" >> /etc/pacman.conf'])
        self._execute(['cp', '/usr/share/pacman/keyrings/kolbanidze.gpg', f'{mount_point}/usr/share/pacman/keyrings/'])
        self._execute(['cp', '/usr/share/pacman/keyrings/kolbanidze-trusted', f'{mount_point}/usr/share/pacman/keyrings/'])
        self._execute(['arch-chroot', mount_point, 'pacman-key', '--populate', 'kolbanidze'])


        # Generating fstab
        self._execute(['bash', '-c', 'genfstab -U /mnt >> /mnt/etc/fstab']) 

        # Creating user
        username = self.setup_information["Username"]
        fullname = self.setup_information["FullName"]
        self._execute(['arch-chroot', mount_point, 'useradd', '-m', username, '-c', fullname])
        
        # Setting password for user
        password = self.setup_information["Password"]
        passwd_input = f"{password}\n{password}\n"
        self._execute(['arch-chroot', mount_point, 'passwd', username], input_str=passwd_input) 

        # Making user admin
        sudoers_line = '"%wheel ALL=(ALL:ALL) ALL"'
        self._execute(['arch-chroot', mount_point, 'bash', '-c', f'echo {sudoers_line} >> /etc/sudoers']) 
        self._execute(['arch-chroot', mount_point, 'usermod', '-aG', 'wheel', username])
        
        # Configuring timezone
        self._execute(['arch-chroot', mount_point, 'ln', '-sf', f'/usr/share/zoneinfo/{self.setup_information['Timezone']}', '/etc/localtime'])

        
        # Creating mkinitcpio.conf
        mkinitcpio_conf_content = "MODULES=()\nBINARIES=()\nFILES=()\nHOOKS=(base systemd autodetect microcode modconf kms keyboard sd-vconsole plymouth block sd-encrypt lvm2 filesystems fsck)\n"
        self._execute(['arch-chroot', mount_point, 'bash', '-c', f'echo -e \'{mkinitcpio_conf_content}\' > /etc/mkinitcpio.conf'])
        
        # Creating cmdline
        self._execute(['arch-chroot', mount_point, 'mkdir', '-p', '/etc/cmdline.d'])
        process = subprocess.run(["blkid", '-s', 'UUID', '-o', 'value', rootfs_partition], check=True, capture_output=True)
        uuid = process.stdout.strip().decode()
        cmdline_content = f"rd.luks.name={uuid}=cryptlvm root={root_lv_path} rw rootfstype=ext4 rd.shell=0 rd.emergency=reboot audit=1 quiet oops=panic init_on_alloc=1 init_on_free=1 pti=on lockdown=confidentiality lsm=landlock,lockdown,yama,integrity,apparmor,bpf splash"
        self._execute(['arch-chroot', mount_point, 'bash', '-c', f'echo "{cmdline_content}" > /etc/cmdline.d/root.conf'])

        # Creating UKI config
        uki_conf_content = "[UKI]\nOSRelease=@/etc/os-release\nPCRBanks=sha256\n\n[PCRSignature:initrd]\nPhases=enter-initrd\nPCRPrivateKey=/etc/kernel/pcr-initrd.key.pem\nPCRPublicKey=/etc/kernel/pcr-initrd.pub.pem\n"
        self._execute(['arch-chroot', mount_point, 'bash', '-c', f'echo -e \'{uki_conf_content}\' > /etc/kernel/uki.conf'])

        # Generate ukify keys
        self._execute(['arch-chroot', mount_point, 'ukify', 'genkey', '--config=/etc/kernel/uki.conf'])

        # Configure UKI generation
        for kernel in kernels_no_headers:
            preset_file = f'{mount_point}/etc/mkinitcpio.d/{kernel}.preset'

            self._execute(['sed', '-i', '/^default_config/s/^/#/', preset_file])
            self._execute(['sed', '-i', '/^default_image/s/^/#/', preset_file])
            self._execute(['sed', '-i', '/^#default_uki/s/^#//', preset_file])
            self._execute(['sed', '-i', '/^#default_options/s/^#//', preset_file])

            self._execute(['sed', '-i', '/^fallback_config/s/^/#/', preset_file])
            self._execute(['sed', '-i', '/^fallback_image/s/^/#/', preset_file])
            self._execute(['sed', '-i', '/^#fallback_uki/s/^#//', preset_file])
            self._execute(['sed', '-i', '/^#fallback_options/s/^#//', preset_file])

            self._execute(['sed', '-i', 's/arch-/secux-/g', preset_file])
            self._execute(['sed', '-i', 's/Linux/secux/g', preset_file])

            self._execute(['sed', '-i', 's|--splash /usr/share/systemd/bootctl/splash-arch.bmp||', preset_file])

        # Add languages support
        locale_to_gen = "ru_RU.UTF-8 UTF-8" if self.language == 'ru' else "en_US.UTF-8 UTF-8"
        locale_conf = "LANG=ru_RU.UTF-8" if self.language == 'ru' else "LANG=en_US.UTF-8"
        self._execute(['arch-chroot', mount_point, 'bash', '-c', f'echo "{locale_to_gen}" >> /etc/locale.gen'])
        self._execute(['arch-chroot', mount_point, 'bash', '-c', f'echo "{locale_conf}" > /etc/locale.conf'])
        self._execute(['arch-chroot', mount_point, 'locale-gen'])

        self._execute(['arch-chroot', mount_point, 'bash', '-c', 'echo "FONT=cyr-sun16" >> /etc/vconsole.conf'])

        # Set plymouth theme
        self._execute(['rm', '-rf', f'{mount_point}/usr/share/plymouth/themes'])
        self._execute(['cp', '-r', '/usr/share/plymouth/themes/', f'{mount_point}/usr/share/plymouth/themes/'])
        self._execute(['arch-chroot', mount_point, 'plymouth-set-default-theme', 'bgrt-nologo']) 

        # Prepare EFI Partition
        self._execute(['mkdir', '-p', f'{mount_point}/efi/EFI/secux'])

        # Change distro info and logo
        installer_path = "/usr/local/share/secux-installer" # Пример пути к файлам инсталлятора
        self._execute(['cp', f'{installer_path}/scripts/os-release', f'{mount_point}/etc/os-release'])
        self._execute(['cp', f'{installer_path}/images/SecuxLinux.svg', f'{mount_point}/usr/share/icons/']) # Пример лого

        self._execute(['rm', '-f', f'{mount_point}/usr/share/factory/etc/ssh/sshd_config.d/99-archlinux.conf'])
        self._execute(['rm', '-f', f'{mount_point}/etc/debuginfod/archlinux.urls'])
        self._execute(['rm', '-f', f'{mount_point}/etc/ssh/sshd_config.d/99-archlinux.conf'])
        self._execute(['rm', '-f', f'{mount_point}/etc/arch-release'])
        self._execute(['rm', '-f', f'{mount_point}/usr/share/factory/etc/arch-release'])
        self._execute(['rm', '-f', f'{mount_point}/usr/share/plymouth/themes/spinner/watermark.png'])

        # Generate UKI
        for kernel in kernels_no_headers:
            self._execute(['arch-chroot', mount_point, 'mkinitcpio', '-p', kernel])
        
        self._execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'NetworkManager.service'])
        self._execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'systemd-timesyncd.service'])
        self._execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'auditd.service'])
        self._execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'apparmor.service'])
        self._execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'ufw.service'])

        if self.setup_information["DE"] == "GNOME":
            self._execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'gdm.service'])
            self._execute(['arch-chroot', mount_point, 'sudo', '-u', 'gdm', 'dbus-launch', 'gsettings', 'set', 'org.gnome.login-screen', 'logo', '""'])
        elif self.setup_information["DE"] == "KDE":
            self._execute(['arch-chroot', mount_point, 'systemctl', 'enable', 'sddm.service'])
            self._execute(['sed', '-i', '/^\\[Theme\\]/a Current=breeze', f'{mount_point}/usr/lib/sddm/sddm.conf.d/default.conf']) 

        # Hostname
        hostname = self.setup_information["Hostname"]
        self._execute(['arch-chroot', mount_point, 'bash', '-c', f'echo "{hostname}" > /etc/hostname'])
        
        self._execute(['arch-chroot', mount_point, 'bootctl', 'install', '--esp-path=/efi']) 

        default_kernel_conf = ""
        if 'linux-hardened' in kernels_no_headers: default_kernel_conf = "secux-linux-hardened.conf"
        elif 'linux-lts' in kernels_no_headers: default_kernel_conf = "secux-linux-lts.conf"
        elif 'linux' in kernels_no_headers: default_kernel_conf = "secux-linux.conf"

        loader_conf_content = f"timeout 3\ndefault {default_kernel_conf}\nconsole-mode keep\nreboot-for-bitlocker yes"
        self._execute(['bash', '-c', f'echo -e "{loader_conf_content}" > {mount_point}/efi/loader/loader.conf'])
        
        for kernel in kernels_no_headers:
            entry_content = f"title Secux Linux ({kernel})\nefi /EFI/secux/secux-{kernel}.efi\n"
            entry_fallback_content = f"title Secux Linux ({kernel}-fallback)\nefi /EFI/secux/secux-{kernel}-fallback.efi\n"
            self._execute(['bash', '-c', f'echo -e "{entry_content}" > {mount_point}/efi/loader/entries/secux-{kernel}.conf'])
            self._execute(['bash', '-c', f'echo -e "{entry_fallback_content}" > {mount_point}/efi/loader/entries/secux-{kernel}-fallback.conf'])

        # Generate sbctl keys
        if self.setup_information["InstallationType"] == "Secure":
            self._execute(['arch-chroot', mount_point, 'sbctl', 'create-keys'])
            self._execute(['arch-chroot', mount_point, 'sbctl', 'enroll-keys', '--yes-this-might-brick-my-machine'])
            self._execute(['arch-chroot', mount_point, 'sbctl', 'sign', '--save', '/efi/EFI/BOOT/BOOTX64.EFI'])
            self._execute(['arch-chroot', mount_point, 'sbctl', 'sign', '--save', '/efi/EFI/systemd/systemd-bootx64.efi'])
            for kernel in kernels_no_headers:
                 self._execute(['arch-chroot', mount_point, 'sbctl', 'sign', '--save', f'/efi/EFI/secux/secux-{kernel}.efi'])
                 self._execute(['arch-chroot', mount_point, 'sbctl', 'sign', '--save', f'/efi/EFI/secux/secux-{kernel}-fallback.efi'])

        elif self.setup_information["InstallationType"] == "LessSecure":
            self._execute(['cp', f'{mount_point}/usr/share/shim-signed/shimx64.efi', f'{mount_point}/efi/EFI/secux/shimx64.efi'])
            self._execute(['cp', f'{mount_point}/usr/share/shim-signed/mmx64.efi', f'{mount_point}/efi/EFI/secux/mmx64.efi'])
            self._execute(['mkdir', '-p', f'{mount_point}/etc/secureboot'])
            self._execute(['openssl', 'req', '-newkey', 'rsa:4096', '-nodes', '-keyout', f'{mount_point}/etc/secureboot/sb.key', '-new', '-x509', '-sha256', '-days', '3650', '-subj', '/CN=Secux Linux MOK/', '-out', f'{mount_point}/etc/secureboot/sb.crt'])
            self._execute(['openssl', 'x509', '-outform', 'DER', '-in', f'{mount_point}/etc/secureboot/sb.crt', '-out', f'{mount_point}/etc/secureboot/sb.cer'])
            self._execute(['arch-chroot', mount_point, 'sbsign', '--key', '/etc/secureboot/sb.key', '--cert', '/etc/secureboot/sb.crt', '--output', '/efi/EFI/systemd/systemd-bootx64.efi', '/usr/lib/systemd/boot/efi/systemd-bootx64.efi'])
            for kernel in kernels_no_headers:
                self._execute(['arch-chroot', mount_point, 'sbsign', '--key', '/etc/secureboot/sb.key', '--cert', '/etc/secureboot/sb.crt', '--output', f'/efi/EFI/secux/secux-{kernel}.efi', f'/efi/EFI/secux/secux-{kernel}.efi'])
                self._execute(['arch-chroot', mount_point, 'sbsign', '--key', '/etc/secureboot/sb.key', '--cert', '/etc/secureboot/sb.crt', '--output', f'/efi/EFI/secux/secux-{kernel}-fallback.efi', f'/efi/EFI/secux/secux-{kernel}-fallback.efi'])

            mok_input = f"{self.setup_information['MOK']}\n{self.setup_information['MOK']}\n"
            self._execute(['arch-chroot', mount_point, 'mokutil', '--import', '/etc/secureboot/sb.cer'], input_str=mok_input)

            self._execute(['cp', f'{installer_path}/scripts/92-shim-signed.hook', f'{mount_point}/usr/share/libalpm/hooks/'])
            self._execute(['cp', f'{installer_path}/scripts/shim-copy.sh', f'{mount_point}/usr/share/'])
            self._execute(['chmod', '+x', f'{mount_point}/usr/share/shim-copy.sh'])
            self._execute(['cp', f'{installer_path}/scripts/91-systemd-boot.hook', f'{mount_point}/usr/share/libalpm/hooks/'])
            self._execute(['cp', f'{installer_path}/scripts/systemd-boot-sign.sh', f'{mount_point}/usr/share'])
            self._execute(['chmod', '+x', f'{mount_point}/usr/share/systemd-boot-sign.sh'])
            self._execute(['cp', f'{installer_path}/scripts/sign-uki.sh', f'{mount_point}/usr/lib/initcpio/post/'])
            self._execute(['chmod', '+x', f'{mount_point}/usr/lib/initcpio/post/sign-uki.sh'])

            self._execute(['cp', f'{mount_point}/efi/EFI/systemd/systemd-bootx64.efi', f'{mount_point}/efi/EFI/secux/grubx64.efi'])

            efi_base_drive, efi_number_str = self.__split_device(efi_partition)
            efi_part_num = ''.join(filter(str.isdigit, efi_number_str))
            if efi_base_drive and efi_part_num:
                self._execute(['efibootmgr', '--create', '--disk', efi_base_drive, '--part', efi_part_num, '--label', "Secux Linux shim", '--loader', '\\EFI\\secux\\shimx64.efi'])

        apps_path = f'{mount_point}/usr/local/bin'
        polkit_path = f'{mount_point}/usr/share/polkit-1/actions'
        desktop_path = f'{mount_point}/usr/share/applications'

        if 'Security Manager' in self.setup_information["Apps"]:
             app_dir = f"{apps_path}/secux-apps"
             self._execute(['mkdir', '-p', app_dir])
             if self.online_installation:
                 self._execute(['git', 'clone', 'https://github.com/kolbanidze/secux-apps', app_dir, '--depth=1'])
             else:
                 self._execute(['cp', '-r', '/usr/local/share/secux-apps', apps_path])
             self._execute(['cp', f'{installer_path}/scripts/org.freedesktop.policykit.securitymanager.policy', polkit_path])
             self._execute(['cp', f'{installer_path}/scripts/securitymanager.desktop', desktop_path])
             self._execute(['chmod', '+x', f'{desktop_path}/securitymanager.desktop'])
             self._execute(['chmod', '+x', f'{app_dir}/manager.py'])
             if self.online_installation:
                 self._execute(['arch-chroot', mount_point, 'pip', 'install', 'customtkinter', '--break-system-packages'])
             else:
                 self._execute(['mkdir', '-p', f'{mount_point}/root/pip_cache'])
                 self._execute(['cp', f'{WORKDIR}/python_packages/', f'{mount_point}/root/pip_cache/', '-r'])
                 self._execute(['arch-chroot', mount_point, 'pip', 'install', 'customtkinter', '--no-index', f'--find-links=file:///root/pip_cache/python_packages', '--break-system-packages'])
                 self._execute(['rm', '-rf', f'{mount_point}/root/pip_cache'])

        if 'KIRTapp' in self.setup_information["Apps"]:
            app_dir = f"{apps_path}/KIRTapp"
            self._execute(['mkdir', '-p', app_dir])
            if self.online_installation:
                 self._execute(['git', 'clone', 'https://github.com/kirt-king/test_app', app_dir, '--depth=1'])
            else:
                 self._execute(['cp', '-r', '/usr/local/share/KIRTapp', apps_path])
            self._execute(['cp', f'{installer_path}/scripts/org.freedesktop.policykit.KIRTapp.policy', polkit_path])
            self._execute(['cp', f'{installer_path}/scripts/KIRTapp.desktop', desktop_path])
            self._execute(['chmod', '+x', f'{desktop_path}/KIRTapp.desktop'])
            self._execute(['chmod', '+x', f'{app_dir}/app_script/app.py'])
            pip_packages_kirt = ['customtkinter', 'face_recognition', 'face_recognition_models']
            if self.online_installation:
                self._execute(['arch-chroot', mount_point, 'pip', 'install'] + pip_packages_kirt + ['--break-system-packages'])
            else:
                self._execute(['mkdir', '-p', f'{mount_point}/root/pip_cache'])
                self._execute(['cp', f'{WORKDIR}/python_packages/', f'{mount_point}/root/pip_cache/', '-r'])
                self._execute(['arch-chroot', mount_point, 'pip', 'install'] + pip_packages_kirt + ['--no-index', f'--find-links=file:///root/pip_cache/python_packages', '--break-system-packages'])
                self._execute(['rm', '-rf', f'{mount_point}/root/pip_cache'])

        # Hardening
        self._execute(['cp', f'{installer_path}/scripts/hardening.conf', f'{mount_point}/etc/sysctl.d/'])
        self._execute(['arch-chroot', mount_point, 'ufw', 'default', 'deny'])
        self._execute(['cp', f'{installer_path}/scripts/secux.rules', f'{mount_point}/etc/audit/rules.d/secux.rules'])

        # Flatpak offline installation support
        self._execute(['arch-chroot', mount_point, 'flatpak', 'remote-modify', '--collection-id=org.flathub.Stable', 'flathub'])

        self._execute(["__INTERNAL_INSTALLATION_SUCCESS"])


if __name__ == "__main__":
    App().mainloop()

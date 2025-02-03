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

VERSION = "0.1.12"
DEBUG = True
DEBUG_SHOW_COMMANDS = False
DEBUG_SHOW_COMMANDS_EFI_PARTITION = "/dev/vda1"
DEBUG_SHOW_COMMANDS_ROOTFS_PARTITION = "/dev/vda2"

MIN_PASSWORD_LENGTH = 8

DISTRO_NAME="SECUX"

REPO_URL = "https://kolbanidze.github.io/secux-repo/x86_64/"

MOK_PASSWORD = "123"

WORKDIR = os.path.dirname(os.path.abspath(__file__))

if os.path.isfile(WORKDIR + "/production.conf"):
    DEBUG = False

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

        image_label.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")
        label.grid(row=0, column=1, padx=15, pady=5, sticky="nsew")
        exit_button.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")


class App(CTk):
    def __init__(self, first_execution = True):
        # Available languages: ["ru", "en"]
        if first_execution:
            super().__init__()
            self.title(DISTRO_NAME)
            self.language = "ru"
            self.setup_information = {}
            self.ui_scale = 1
            self.light_theme = False
            set_appearance_mode("dark")
            self.timezone_geometry_resized = False
            self.init_geometry_resized = False
        else:
            self.focus_set()
            for widget in self.winfo_children():
                widget.destroy()
        if self.init_geometry_resized:
            self.geometry(f"{self.winfo_width()//2}x{self.winfo_height()*2}")
            self.init_geometry_resized = False
            self.timezone_geometry_resized = False

        self.clicks = 0
        welcome_image = CTkImage(light_image=Image.open(f'{WORKDIR}/images/waving_hand.png'), dark_image=Image.open(f'{WORKDIR}/images/waving_hand.png'), size=(80,80))
        welcome_image_label = CTkLabel(self, text="", image=welcome_image)
        welcome_image_label.bind("<Button-1>", self.__clicks_handler)
        welcome_entry_label = CTkLabel(self, text=f"Добро пожаловать в установщик дистрибутива {DISTRO_NAME}\nWelcome to {DISTRO_NAME} distribution installer")        
        select_language_label = CTkLabel(self, text="Выберите язык | Select language")
        languages_optionmenu = CTkOptionMenu(self, values=["Русский", "English"], command=self.__language_callback)
        next_button = CTkButton(self, text="Далее | Next", command=self.timezone_stage, fg_color="green")
        ui_scaling_label = CTkLabel(self, text="Масштабирование | UI Scaling")
        ui_scaling = CTkOptionMenu(self, values=["80%", "100%", "125%", "150%", "200%"], command=self.__ui_scaling_handler)
        ui_scaling.set(str(int(self.ui_scale*100)) + "%")
        if not first_execution:
            ui_scaling.configure(state="disabled")
        self.white_mode = CTkSwitch(self, text="Светлая тема | White theme", command=self.__theme_handler)
        if self.light_theme:
            self.white_mode.select()
        info = CTkLabel(self, text=f"Версия | Version : {VERSION}", font=(None, 8))

        self.grid_columnconfigure((0, 1), weight=1)

        welcome_image_label.grid(row=0, columnspan=2, padx=15, pady=5)
        welcome_entry_label.grid(row=1, columnspan=2, padx=15, pady=5)
        select_language_label.grid(row=2, columnspan=2, padx=15, pady=(15, 5))
        languages_optionmenu.grid(row=3, columnspan=2, padx=15, pady=5)
        ui_scaling_label.grid(row=4, columnspan=2, padx=15, pady=5)
        ui_scaling.grid(row=5, columnspan=2, padx=15, pady=5)
        self.white_mode.grid(row=6, columnspan=2, padx=15, pady=5)
        next_button.grid(row=7, columnspan=2, padx=15, pady=(15, 5))
        info.grid(row=8, padx=15, columnspan=2, pady=(5, 0))
        if DEBUG: CTkLabel(self, text="WARNING: DEBUG MODE", font=(None, 10), text_color=("red")).grid(row=9, columnspan=2, padx=15, pady=(5,0))

    def __ui_scaling_handler(self, new_scaling: str):
        self.ui_scale = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(self.ui_scale)
        set_window_scaling(self.ui_scale)
    
    def __theme_handler(self):
        if self.white_mode.get():
            set_appearance_mode("light")
            self.light_theme = True
        else:
            set_appearance_mode("dark")
            self.light_theme = False

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
    
    def __delete_widgets(self):
        for widget in self.winfo_children():
            if type(widget) != windows.widgets.ctk_progressbar.CTkProgressBar:
                widget.destroy()


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

    def timezone_stage(self):
        self.lang = Locale(language=self.language)
        
        for widget in self.winfo_children():
            widget.destroy()
        if not self.timezone_geometry_resized:
            self.geometry(f"{self.winfo_width()*2}x{self.winfo_height()*0.5}")
            self.timezone_geometry_resized = True
            self.init_geometry_resized = True
        self.progressbar = CTkProgressBar(self, orientation='horizontal', width=500)
        self.progressbar.set(0.125)
        
        title1 = CTkLabel(self, text=self.lang.select_time_zone, font=(None, 16, 'bold'))
        region_label = CTkLabel(self, text=self.lang.region)
        zone_label = CTkLabel(self, text=self.lang.timezone)
        self.region_box = CTkOptionMenu(self, values=list(timezones.keys()), command=self.__timezone_handler)
        self.zone_box = CTkOptionMenu(self, command=self.__time_zone_write_to_setup_info)
        back_btn = CTkButton(self, text=self.lang.back, command=lambda: self.__init__(first_execution=False))
        next_btn = CTkButton(self, text=self.lang.next, command=self.installation_type_stage)

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
            
            
        self.progressbar.grid(row=0, column=0, padx=15, pady=(5,15), sticky="nsew", columnspan=2)
        title1.grid(row=1, column=0, padx=15, pady=5, sticky="ew", columnspan=2)
        region_label.grid(row=2, column=0, padx=15, pady=(5, 0), sticky="ew")
        zone_label.grid(row=2, column=1, padx=15, pady=(5, 0), sticky="ew")
        self.region_box.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        self.zone_box.grid(row=3, column=1, padx=15, pady=5, sticky="ew")
        back_btn.grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        next_btn.grid(row=4, column=1, padx=15, pady=5, sticky="ew")
    
    ##### END TIME ZONE #####

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
        self.progressbar.set(0.25)

        self.__delete_widgets()
        
        label = CTkLabel(self, text=self.lang.select_install_option, font=(None, 16, "bold"))
        self.installation_type_variable = IntVar(value=0)
        self.secure_type = CTkRadioButton(self, value=0, variable=self.installation_type_variable, text=self.lang.securetype, command=self.__installation_type_radio_button_handler)
        self.less_secure_type = CTkRadioButton(self, value=1, variable=self.installation_type_variable, text=self.lang.lessecuretype, command=self.__installation_type_radio_button_handler)
        self.insecure_type = CTkRadioButton(self, value=2, variable=self.installation_type_variable, text=self.lang.insecuretype, command=self.__installation_type_radio_button_handler)
        back_btn = CTkButton(self, text=self.lang.back, command=self.timezone_stage)
        next_btn = CTkButton(self, text=self.lang.next, command=self.desktop_environment_stage)

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
        
    def desktop_environment_stage(self):
        self.progressbar.set(0.375)

        self.__delete_widgets()
        
        self.de_variable = IntVar(value=0)
        label = CTkLabel(self, text=self.lang.choose_de, font=(None, 16, "bold"))
        self.gnome_button = CTkRadioButton(self, value=0, variable=self.de_variable, text="GNOME", command=self.__de_handler)
        self.kde_button = CTkRadioButton(self, value=1, variable=self.de_variable, text="KDE", command=self.__de_handler)
        self.console_button = CTkRadioButton(self, value=2, variable=self.de_variable, text=self.lang.console, command=self.__de_handler)
        back_btn = CTkButton(self, text=self.lang.back, command=self.installation_type_stage)
        next_btn = CTkButton(self, text=self.lang.next, command=self.kernel_select_stage)

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

    def __move_to_partitioning_stage(self):
        if len(self.setup_information["Kernel"]) == 0:
            Notification(title=self.lang.atleast_one_kernel, icon='warning.png', message=self.lang.pls_select_kernel, message_bold=False, exit_btn_msg=self.lang.exit)
            return
        self.partitioning_stage()

    def kernel_select_stage(self):
        self.progressbar.set(0.5)

        self.__delete_widgets()

        label = CTkLabel(self, text=self.lang.kernel_label, font=(None, 16, "bold"))
        
        self.linux_hardened = CTkCheckBox(self, text="Linux hardened", command=self.__kernel_select_handler)
        self.linux_lts = CTkCheckBox(self, text="Linux LTS", command=self.__kernel_select_handler)
        self.linux = CTkCheckBox(self, text="Linux", command=self.__kernel_select_handler)
        back_btn = CTkButton(self, text=self.lang.back, command=self.desktop_environment_stage)
        next_btn = CTkButton(self, text=self.lang.next, command=self.__move_to_partitioning_stage)

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
    
    def partitioning_stage(self):
        self.progressbar.set(0.625)

        self.__delete_widgets()
        
        label = CTkLabel(self, text=self.lang.diskpart, font=(None, 16, "bold"))
        
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,TYPE', '--json', '-b'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        raw_disks = []
        for disk in disks:
            if disk['type'] == 'disk':
                raw_disks.append({disk['name']: disk['size']})
        sorted_raw_disks = sorted([(list(d.keys())[0], list(d.values())[0]) for d in raw_disks], key=lambda x: x[1], reverse=True)
        erase_all_disks = [f"/dev/{drive} | {self.__convert_bytes_to_human_readable(size)}" for drive, size in sorted_raw_disks]

        self.partitioning_type = IntVar(value=0)
        erase_all_partitioning = CTkRadioButton(self, text=self.lang.erase_all_and_install, variable=self.partitioning_type, value=0)
        self.erase_all_disk = CTkOptionMenu(self, values=erase_all_disks)
        manual_partitioning = CTkRadioButton(self, text=self.lang.manual, variable=self.partitioning_type, value=1)
        back_btn = CTkButton(self, text=self.lang.back, command=self.kernel_select_stage)
        next_btn = CTkButton(self, text=self.lang.next, command=self.__partitioning_next_button_handler)

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        erase_all_partitioning.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.erase_all_disk.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        manual_partitioning.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        back_btn.grid(row=5, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=5, column=1, padx=15, pady=5, sticky="nsew")

    def __partitioning_next_button_handler(self):
        key = self.partitioning_type.get()
        match key:
            case 0:
                disk = self.erase_all_disk.get().split(" |")[0]
                self.setup_information["Partitioning"] = "Automatic"
                self.setup_information["DriveToFormat"] = disk
                self.setup_information["UseSwap"] = True
                self.setup_information["SwapSize"] = "1"
                self.encryption_key_stage(manual=False)
            case 1:
                self.setup_information["Partitioning"] = "Manual"
                self.manual_partitioning()

    def manual_partitioning(self):
        self.__delete_widgets()
        
        self.partitions = []
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    self.partitions.append(f"{partition['name']} | {partition['size']} | {partition.get('fstype', 'N/A')}")

        label = CTkLabel(self, text=self.lang.selfpart, font=(None, 16, "bold"))
        run_gparted_btn = CTkButton(self, text=self.lang.rungparted, command=lambda: os.system("/usr/bin/sudo /usr/bin/gparted"))
        update_disks = CTkButton(self, text=self.lang.refreshparts, command=self.__update_partitions)
        efi_partition_label = CTkLabel(self, text=self.lang.efipart)
        self.efi_partition_optionmenu = CTkOptionMenu(self, values=self.partitions)
        root_partition_label = CTkLabel(self, text=self.lang.rootfs)
        self.root_partition_optionmenu = CTkOptionMenu(self, values=self.partitions, command=self.__change_max_swapfile)
        self.use_swap = StringVar(value="on")
        self.swap_checkbox = CTkCheckBox(self, text=self.lang.useswap, variable=self.use_swap, onvalue="on", offvalue="off", command=self.__swapfile_handler)
        swap_label = CTkLabel(self, text=self.lang.swapsize)
        self.swap_entry = CTkEntry(self)
        self.swap_entry.insert(0, "1")
        self.swap_scrollbar = CTkSlider(self, command=self.__scroll_handler, to=16)
        back_btn = CTkButton(self, text=self.lang.back, command=self.partitioning_stage)
        next_btn = CTkButton(self, text=self.lang.next, command=lambda: self.encryption_key_stage(manual=True))

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

    ##### END PARTITIONING #####

    ##### BEGIN ENCRYPTION KEY #####
    def __validate_english_keymap(self, password) -> bool:
        """True -> can be written with english keymap. False -> can't be written with english keymap"""
        valid_characters = string.ascii_letters + string.digits + string.punctuation + " "
        return all(char in valid_characters for char in password)

    def encryption_key_stage(self, manual, first_execution = True):
        if first_execution:
            if manual:
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

        self.__delete_widgets()
        self.progressbar.set(0.75)

        label = CTkLabel(self, text=self.lang.os_encryption, font=(None, 16, "bold"))
        label1 = CTkLabel(self, text=self.lang.enckey)
        self.system_partition_encryption_key_entry = CTkEntry(self, show='*')
        label2 = CTkLabel(self, text=self.lang.enckey2)
        self.system_partition_encryption_key_entry2 = CTkEntry(self, show='*')
        back_btn = CTkButton(self, text=self.lang.back, command=self.partitioning_stage)
        next_btn = CTkButton(self, text=self.lang.next, command=self.admin_creation_stage)

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        label1.grid(row=2, column=0, padx=15, pady=5, sticky="nsew", columnspan=2)
        self.system_partition_encryption_key_entry.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        label2.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.system_partition_encryption_key_entry2.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        back_btn.grid(row=6, column=0, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=6, column=1, padx=15, pady=5, sticky="nsew")

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

    def admin_creation_stage(self, first_execution = True):
        if first_execution:
            if not compare_digest(self.system_partition_encryption_key_entry.get(), self.system_partition_encryption_key_entry2.get()):
                Notification(title=self.lang.passwordmismatch, icon="warning.png", message=self.lang.passwordmsg, message_bold=True, exit_btn_msg=self.lang.exit)
                return
            if len(self.system_partition_encryption_key_entry.get()) < MIN_PASSWORD_LENGTH:
                Notification(title=self.lang.pwd_length_title, icon="warning.png", message=self.lang.pwd_length, message_bold=True, exit_btn_msg=self.lang.exit)
                return
            if not self.__validate_english_keymap(self.system_partition_encryption_key_entry.get()):
                Notification(title=self.lang.encryption_password_title, icon="warning.png", message=self.lang.encryption_password, message_bold=False, exit_btn_msg=self.lang.exit)
                return
            self.setup_information["EncryptionKey"] = self.system_partition_encryption_key_entry.get()
        
            self.system_partition_encryption_key_entry.delete(0, 'end')
            self.system_partition_encryption_key_entry2.delete(0, 'end')
            gc_collect()

        self.__delete_widgets()
        self.progressbar.set(0.875)

        label = CTkLabel(self, text=self.lang.admin_creation, font=(None, 16, "bold"))
        your_name_label = CTkLabel(self, text=self.lang.yourname)
        self.your_name_entry = CTkEntry(self)
        hostname_label = CTkLabel(self, text=self.lang.hostname)
        self.hostname_entry = CTkEntry(self)
        username_label = CTkLabel(self, text=self.lang.username)
        self.username_entry = CTkEntry(self)
        password_label = CTkLabel(self, text=self.lang.password1)
        self.password_entry = CTkEntry(self, show='*')
        password_label2 = CTkLabel(self, text=self.lang.password2)
        self.password_entry2 = CTkEntry(self, show="*")
        back_btn = CTkButton(self, text=self.lang.back, command=lambda: self.encryption_key_stage(manual=False, first_execution=False))
        next_btn = CTkButton(self, text=self.lang.next, command=self.final_stage)

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

    ##### BEGIN FINAL STAGE #####
    def final_stage(self):
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

        self.__delete_widgets()
        self.progressbar.set(1)

        label = CTkLabel(self, text=self.lang.final, font=(None, 16, "bold"))
        timezone_label = CTkLabel(self, text=self.lang.fulltimezone)
        timezone_entry = CTkEntry(self)
        timezone_entry.insert(0, self.setup_information["Timezone"])
        timezone_entry.configure(state="disabled")

        installation_type_label = CTkLabel(self, text=self.lang.installoption)
        installation_type_entry = CTkEntry(self)
        match self.setup_information["InstallationType"]:
            case "Secure":
                installation_type_entry.insert(0, self.lang.securetype)
            case "InSecure":
                installation_type_entry.insert(0, self.lang.insecuretype)
            case "LessSecure":
                installation_type_entry.insert(0, self.lang.lessecuretype)
        installation_type_entry.configure(state="disabled")

        de_label = CTkLabel(self, text=self.lang.de)
        de_entry = CTkEntry(self)
        de_entry.insert(0, self.setup_information["DE"])
        de_entry.configure(state="disabled")

        partitioning_type_label = CTkLabel(self, text=self.lang.partitioningtype)
        partitioning_type_entry = CTkEntry(self)
        if self.setup_information["Partitioning"] == "Automatic":
            partitioning_type_entry.insert(0, self.lang.automatic)
            drive_to_format_label = CTkLabel(self, text=self.lang.systeminstallto)
            drive_to_format_entry = CTkEntry(self)
            drive_to_format_entry.insert(0, self.setup_information["DriveToFormat"])
            drive_to_format_entry.configure(state="disabled")
        else:
            partitioning_type_entry.insert(0, self.lang.manual)
            loader_label = CTkLabel(self, text=self.lang.efipart)
            loader_entry = CTkEntry(self)
            loader_entry.insert(0, self.setup_information["EfiPartition"])
            loader_entry.configure(state="disabled")

            system_label = CTkLabel(self, text=self.lang.rootfs)
            system_entry = CTkEntry(self)
            system_entry.insert(0, self.setup_information["SystemPartition"])
            system_entry.configure(state="disabled")
        partitioning_type_entry.configure(state="disabled")

        use_swap_label = CTkLabel(self, text=self.lang.useswap)
        use_swap_entry = CTkEntry(self)
        if self.setup_information["UseSwap"]:
            use_swap_entry.insert(0, self.lang.yes)
            swap_size_label = CTkLabel(self, text=self.lang.swapsize_final)
            swap_size_entry = CTkEntry(self)
            swap_size_entry.insert(0, self.setup_information["SwapSize"])
            swap_size_entry.configure(state="disabled")
        else:
            use_swap_entry.insert(0, self.lang.no)
        use_swap_entry.configure(state="disabled")

        hostname_label =CTkLabel(self, text=self.lang.hostname)
        hostname_entry = CTkEntry(self)
        hostname_entry.insert(0, self.setup_information["Hostname"])
        hostname_entry.configure(state="disabled")

        fullname_label = CTkLabel(self, text=self.lang.yourname)
        fullname_entry = CTkEntry(self)
        fullname_entry.insert(0, self.setup_information["FullName"])
        fullname_entry.configure(state="disabled")

        username_label = CTkLabel(self, text=self.lang.username)
        username_entry = CTkEntry(self)
        username_entry.insert(0, self.setup_information['Username'])
        username_entry.configure(state="disabled")

        back_button = CTkButton(self, text=self.lang.back, command=lambda: self.admin_creation_stage(first_execution=False))
        begin_installation_button = CTkButton(self, text=self.lang.begin_install, command=self.begin_installation_ui)

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
        begin_installation_button.grid(row=i, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
    
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
        if input:
            self.commands.append({"command": command, "input": input})
        else:
            self.commands.append({"command": command})

    def _execute_commands(self, commands: list):
        def run_commands():
            for cmd in commands:
                try:
                    # Run the command
                    if "input" in cmd:
                        process = subprocess.Popen(
                            # f"stdbuf -oL {cmd["command"]}",
                            cmd["command"],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            text=True,
                            bufsize=1  # Line-buffered output
                        )
                        process.stdin.write(cmd["input"])
                        process.stdin.close()
                    else:
                        process = subprocess.Popen(
                            # f"stdbuf -oL {cmd["command"]}",
                            cmd["command"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True,
                            text=True,
                            bufsize=1  # Line-buffered output
                        )

                    # Update the console in real-time
                    self.console.configure(state="normal")
                    for line in process.stdout:
                        self.console.insert(END, line)
                        self.console.see(END)
                    for line in process.stderr:
                        self.console.insert(END, line)
                        self.console.see(END)

                    process.stdout.close()
                    process.stderr.close()
                    process.wait()  # Ensure the process finishes

                    self.console.configure(state="disabled")
                except Exception as e:
                    self.console.configure(state="normal")
                    self.console.insert(END, f"Error: {str(e)}\n")
                    self.console.configure(state="disabled")
                    self.console.see(END)

        # Run the commands in a separate thread to avoid blocking the UI
        threading.Thread(target=run_commands, daemon=True).start()

    def __check_secure_boot_and_setup_mode(self):
        secure_boot_path = "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c"
        setup_mode_path = "/sys/firmware/efi/efivars/SetupMode-8be4df61-93ca-11d2-aa0d-00e098032b8c"

        def read_efi_var(path):
            try:
                with open(path, "rb") as f:
                    # EFI variable data starts after the first 4 bytes of metadata
                    return ord(f.read()[4:5])  # Convert byte to int
            except FileNotFoundError:
                return None

        secure_boot = read_efi_var(secure_boot_path)
        setup_mode = read_efi_var(setup_mode_path)

        if secure_boot is None or setup_mode is None:
            print("Secure Boot or Setup Mode variables not found. Is the system EFI-enabled?")
            return (False, 0, 0)

        return (True, secure_boot, setup_mode)
    
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

    def begin_installation_ui(self):
        try:
            answ = get("http://gstatic.com/generate_204", timeout=5)
        except ConnectionError:
            Notification(title=self.lang.network_title, icon="warning.png", message=self.lang.network, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if answ.status_code != 204:
            Notification(title=self.lang.network_title, icon="warning.png", message=self.lang.network, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        
        uefi_info = self.__check_secure_boot_and_setup_mode()
        if not uefi_info[0]:
            Notification(title=self.lang.not_uefi_title, icon="warning.png", message=self.lang.not_uefi, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        if self.setup_information["InstallationType"] != "InSecure":
            if uefi_info[1] != 0 and uefi_info[2] != 1:
                Notification(title=self.lang.not_setup_mode_title, icon="warning.png", message=self.lang.not_setup_mode, message_bold=False, exit_btn_msg=self.lang.exit)
                return
        
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
        kernels = " ".join(self.setup_information["Kernel"]) + " " + " ".join([i+'-headers' for i in self.setup_information["Kernel"]])
        pacstrap_command = f"stdbuf -oL pacstrap -K /mnt base {kernels} linux-firmware {self.__get_ucode_package()} vim nano efibootmgr sudo plymouth python-pip lvm2 networkmanager systemd-ukify sbsigntools efitools less git ntfs-3g gvfs gvfs-mtp xdg-user-dirs fwupd "
        if self.setup_information["InstallationType"] == "Secure":
            pacstrap_command += "sbctl "
        elif self.setup_information["InstallationType"] == "LessSecure":
            pacstrap_command += "shim-signed mokutil "
        
        if self.setup_information["DE"] == "GNOME":
            pacstrap_command += "xorg gnome networkmanager-openvpn gnome-tweaks gdm vlc firefox chromium tk python-pexpect python-pillow"
        elif self.setup_information["DE"] == "KDE":
            pacstrap_command += "xorg plasma networkmanager-openvpn kde-applications vlc firefox chromium tk python-pexpect python-pillow"
        self._execute(pacstrap_command)
        
        self._execute("echo lolo1")
        # Adding custom repo
        self._execute(f'echo "[kolbanidze]\nServer = {REPO_URL}\n" >> /mnt/etc/pacman.conf')
        self._execute("cp /usr/share/pacman/keyrings/kolbanidze* /mnt/usr/share/pacman/keyrings")
        self._execute("arch-chroot /mnt pacman-key --recv CE48F2CC9BE03B4EFAB02343AA0A42D146D35FCE")
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
        self._execute(f"echo \"rd.luks.name=$(blkid -s UUID -o value {rootfs_partition})=cryptlvm root=/dev/volumegroup/root rw rootfstype=ext4 rd.shell=0 rd.emergency=reboot quiet lockdown=confidentiality splash\" > /mnt/etc/cmdline.d/root.conf")

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
            for kernel in self.setup_information["Kernel"]:
                self._execute(f"arch-chroot /mnt sbsign --key /etc/secureboot/sb.key --cert /etc/secureboot/sb.crt --output /efi/EFI/Linux/arch-{kernel}.efi /efi/EFI/Linux/arch-{kernel}.efi")
                self._execute(f"arch-chroot /mnt sbsign --key /etc/secureboot/sb.key --cert /etc/secureboot/sb.crt --output /efi/EFI/Linux/arch-{kernel}-fallback.efi /efi/EFI/Linux/arch-{kernel}-fallback.efi")
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
            base, num = self.__split_device(rootfs_partition)
            self._execute(f'efibootmgr --create --disk {base} --part {num} --label "SECUX SHIM" --loader "\\EFI\\Linux\\shimx64.efi"')

        # Installing secux-apps
        self._execute("mkdir -p /usr/local/bin/secux-apps")
        self._execute("git clone https://github.com/kolbanidze/secux-apps /usr/local/bin/secux-apps --depth=1")
        self._execute("cp /usr/local/share/secux-installer/scripts/org.freedesktop.policykit.securitymanager.policy /usr/share/polkit-1/actions/")

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
        
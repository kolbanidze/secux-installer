from customtkinter import *
from PIL import Image
from language import Locale
import subprocess
import json
from gc import collect as gc_collect
import os
import threading

timezones = {'Africa': ['Abidjan', 'Accra', 'Addis_Ababa', 'Algiers', 'Asmara', 'Bamako', 'Bangui', 'Banjul', 'Bissau', 'Blantyre', 'Brazzaville', 'Bujumbura', 'Cairo', 'Casablanca', 'Ceuta', 'Conakry', 'Dakar', 'Dar_es_Salaam', 'Djibouti', 'Douala', 'El_Aaiun', 'Freetown', 'Gaborone', 'Harare', 'Johannesburg', 'Juba', 'Kampala', 'Khartoum', 'Kigali', 'Kinshasa', 'Lagos', 'Libreville', 'Lome', 'Luanda', 'Lubumbashi', 'Lusaka', 'Malabo', 'Maputo', 'Maseru', 'Mbabane', 'Mogadishu', 'Monrovia', 'Nairobi', 'Ndjamena', 'Niamey', 'Nouakchott', 'Ouagadougou', 'Porto-Novo', 'Sao_Tome', 'Tripoli', 'Tunis', 'Windhoek'], 'America': ['Adak', 'Anchorage', 'Anguilla', 'Antigua', 'Araguaina', 'Argentina/Buenos_Aires', 'Argentina/Catamarca', 'Argentina/Cordoba', 'Argentina/Jujuy', 'Argentina/La_Rioja', 'Argentina/Mendoza', 'Argentina/Rio_Gallegos', 'Argentina/Salta', 'Argentina/San_Juan', 'Argentina/San_Luis', 'Argentina/Tucuman', 'Argentina/Ushuaia', 'Aruba', 'Asuncion', 'Atikokan', 'Bahia', 'Bahia_Banderas', 'Barbados', 'Belem', 'Belize', 'Blanc-Sablon', 'Boa_Vista', 'Bogota', 'Boise', 'Cambridge_Bay', 'Campo_Grande', 'Cancun', 'Caracas', 'Cayenne', 'Cayman', 'Chicago', 'Chihuahua', 'Costa_Rica', 'Creston', 'Cuiaba', 'Curacao', 'Danmarkshavn', 'Dawson', 'Dawson_Creek', 'Denver', 'Detroit', 'Dominica', 'Edmonton', 'Eirunepe', 'El_Salvador', 'Fort_Nelson', 'Fortaleza', 'Glace_Bay', 'Godthab', 'Goose_Bay', 'Grand_Turk', 'Grenada', 'Guadeloupe', 'Guatemala', 'Guayaquil', 'Guyana', 'Halifax', 'Havana', 'Hermosillo', 'Indiana/Indianapolis', 'Indiana/Knox', 'Indiana/Marengo', 'Indiana/Petersburg', 'Indiana/Tell_City', 'Indiana/Vevay', 'Indiana/Vincennes', 'Indiana/Winamac', 'Inuvik', 'Iqaluit', 'Jamaica', 'Juneau', 'Kentucky/Louisville', 'Kentucky/Monticello', 'Kralendijk', 'La_Paz', 'Lima', 'Los_Angeles', 'Lower_Princes', 'Maceio', 'Managua', 'Manaus', 'Marigot', 'Martinique', 'Matamoros', 'Mazatlan', 'Menominee', 'Merida', 'Metlakatla', 'Mexico_City', 'Miquelon', 'Moncton', 'Monterrey', 'Montevideo', 'Montserrat', 'Nassau', 'New_York', 'Nipigon', 'Nome', 'Noronha', 'North_Dakota/Beulah', 'North_Dakota/Center', 'North_Dakota/New_Salem', 'Ojinaga', 'Panama', 'Pangnirtung', 'Paramaribo', 'Phoenix', 'Port-au-Prince', 'Port_of_Spain', 'Porto_Velho', 'Puerto_Rico', 'Rainy_River', 'Rankin_Inlet', 'Recife', 'Regina', 'Resolute', 'Rio_Branco', 'Santarem', 'Santiago', 'Santo_Domingo', 'Sao_Paulo', 'Scoresbysund', 'Sitka', 'St_Barthelemy', 'St_Johns', 'St_Kitts', 'St_Lucia', 'St_Thomas', 'St_Vincent', 'Swift_Current', 'Tegucigalpa', 'Thule', 'Thunder_Bay', 'Tijuana', 'Toronto', 'Tortola', 'Vancouver', 'Whitehorse', 'Winnipeg', 'Yakutat', 'Yellowknife'], 'Antarctica': ['Casey', 'Davis', 'DumontDUrville', 'Macquarie', 'Mawson', 'McMurdo', 'Palmer', 'Rothera', 'Syowa', 'Troll', 'Vostok'], 'Arctic': ['Longyearbyen'], 'Asia': ['Aden', 'Almaty', 'Amman', 'Anadyr', 'Aqtau', 'Aqtobe', 'Ashgabat', 'Atyrau', 'Baghdad', 'Bahrain', 'Baku', 'Bangkok', 'Barnaul', 'Beirut', 'Bishkek', 'Brunei', 'Chita', 'Choibalsan', 'Colombo', 'Damascus', 'Dhaka', 'Dili', 'Dubai', 'Dushanbe', 'Famagusta', 'Gaza', 'Hebron', 'Ho_Chi_Minh', 'Hong_Kong', 'Hovd', 'Irkutsk', 'Jakarta', 'Jayapura', 'Jerusalem', 'Kabul', 'Kamchatka', 'Karachi', 'Kathmandu', 'Khandyga', 'Kolkata', 'Krasnoyarsk', 'Kuala_Lumpur', 'Kuching', 'Kuwait', 'Macau', 'Magadan', 'Makassar', 'Manila', 'Muscat', 'Nicosia', 'Novokuznetsk', 'Novosibirsk', 'Omsk', 'Oral', 'Phnom_Penh', 'Pontianak', 'Pyongyang', 'Qatar', 'Qyzylorda', 'Riyadh', 'Sakhalin', 'Samarkand', 'Seoul', 'Shanghai', 'Singapore', 'Srednekolymsk', 'Taipei', 'Tashkent', 'Tbilisi', 'Tehran', 'Thimphu', 'Tokyo', 'Tomsk', 'Ulaanbaatar', 'Urumqi', 'Ust-Nera', 'Vientiane', 'Vladivostok', 'Yakutsk', 'Yangon', 'Yekaterinburg', 'Yerevan'], 'Atlantic': ['Azores', 'Bermuda', 'Canary', 'Cape_Verde', 'Faroe', 'Madeira', 'Reykjavik', 'South_Georgia', 'St_Helena', 'Stanley'], 'Australia': ['Adelaide', 'Brisbane', 'Broken_Hill', 'Currie', 'Darwin', 'Eucla', 'Hobart', 'Lindeman', 'Lord_Howe', 'Melbourne', 'Perth', 'Sydney'], 'Europe': ['Amsterdam', 'Andorra', 'Astrakhan', 'Athens', 'Belgrade', 'Berlin', 'Bratislava', 'Brussels', 'Bucharest', 'Budapest', 'Busingen', 'Chisinau', 'Copenhagen', 'Dublin', 'Gibraltar', 'Guernsey', 'Helsinki', 'Isle_of_Man', 'Istanbul', 'Jersey', 'Kaliningrad', 'Kiev', 'Kirov', 'Lisbon', 'Ljubljana', 'London', 'Luxembourg', 'Madrid', 'Malta', 'Mariehamn', 'Minsk', 'Monaco', 'Moscow', 'Oslo', 'Paris', 'Podgorica', 'Prague', 'Riga', 'Rome', 'Samara', 'San_Marino', 'Sarajevo', 'Saratov', 'Simferopol', 'Skopje', 'Sofia', 'Stockholm', 'Tallinn', 'Tirane', 'Ulyanovsk', 'Uzhgorod', 'Vaduz', 'Vatican', 'Vienna', 'Vilnius', 'Volgograd', 'Warsaw', 'Zagreb', 'Zaporozhye', 'Zurich'], 'Indian': ['Antananarivo', 'Chagos', 'Christmas', 'Cocos', 'Comoro', 'Kerguelen', 'Mahe', 'Maldives', 'Mauritius', 'Mayotte', 'Reunion'], 'Pacific': ['Apia', 'Auckland', 'Bougainville', 'Chatham', 'Chuuk', 'Easter', 'Efate', 'Enderbury', 'Fakaofo', 'Fiji', 'Funafuti', 'Galapagos', 'Gambier', 'Guadalcanal', 'Guam', 'Honolulu', 'Johnston', 'Kiritimati', 'Kosrae', 'Kwajalein', 'Majuro', 'Marquesas', 'Midway', 'Nauru', 'Niue', 'Norfolk', 'Noumea', 'Pago_Pago', 'Palau', 'Pitcairn', 'Pohnpei', 'Port_Moresby', 'Rarotonga', 'Saipan', 'Tahiti', 'Tarawa', 'Tongatapu', 'Wake', 'Wallis'], 'UTC': None}

VERSION = "0.1"
DEBUG = True

DISTRO_NAME="SECUX"

WORKDIR = os.path.dirname(os.path.abspath(__file__))

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
    def __init__(self):
        super().__init__()
        self.title(DISTRO_NAME)

        # Available languages: ["ru", "en"]
        self.language = "ru"
        
        self.setup_information = {}
        welcome_image = CTkImage(light_image=Image.open(f'{WORKDIR}/images/waving_hand.png'), dark_image=Image.open(f'{WORKDIR}/images/waving_hand.png'), size=(80,80))
        welcome_image_label = CTkLabel(self, text="", image=welcome_image)
        welcome_entry_label = CTkLabel(self, text=f"Добро пожаловать в установщик дистрибутива {DISTRO_NAME}\nWelcome to {DISTRO_NAME} distribution installer")
        
        select_language_label = CTkLabel(self, text="Выберите язык | Select language")
        languages_optionmenu = CTkOptionMenu(self, values=["Русский", "English"], command=self.language_callback)
        next_button = CTkButton(self, text="Далее | Next", command=self.timezone_stage)
        info = CTkLabel(self, text=f"Версия | Version : {VERSION}", font=(None, 8))

        welcome_image_label.pack(padx=15, pady=15)
        welcome_entry_label.pack(padx=15, pady=15)
        select_language_label.pack(padx=15, pady=15)
        languages_optionmenu.pack(padx=15, pady=15)
        next_button.pack(padx=15, pady=15)
        info.pack(padx=15, pady=(5, 0))
        if DEBUG: CTkLabel(self, text="WARNING: DEBUG MODE", font=(None, 8)).pack(padx=15, pady=(5,0))

    def language_callback(self, choice):
        match choice:
            case "English":
                self.language = "en"
            case "Русский":
                self.language = "ru"
    
    # 15%
    def timezone_stage(self):
        self.lang = Locale(language=self.language)
        if DEBUG: print(self.lang.test)

        for widget in self.winfo_children():
            widget.destroy()
        self.progressbar = CTkProgressBar(self, orientation='horizontal', width=500)
        
        self.progressbar.set(0.15)
        title1 = CTkLabel(self, text=self.lang.select_time_zone, font=(None, 16, 'bold'))

        region_label = CTkLabel(self, text=self.lang.region)
        zone_label = CTkLabel(self, text=self.lang.timezone)
        
        self.region_box = CTkOptionMenu(self, values=list(timezones.keys()), command=self.timezone_handler)
        self.zone_box = CTkOptionMenu(self)
        
        self.timezone_handler("Europe")
        self.region_box.set("Europe")
        self.zone_box.set("Minsk")

        next_btn = CTkButton(self, text=self.lang.next, command=self.installation_type_stage)
        self.progressbar.grid(row=0, column=0, padx=15, pady=(5,15), sticky="news", columnspan=2)
        title1.grid(row=1, column=0, padx=15, pady=5, sticky="news", columnspan=2)
        region_label.grid(row=2, column=0, padx=15, pady=(5, 0), sticky="nsew")
        zone_label.grid(row=2, column=1, padx=15, pady=(5, 0), sticky="nsew")
        self.region_box.grid(row=3, column=0, padx=15, pady=5, sticky="nsew")
        self.zone_box.grid(row=3, column=1, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
    
    def timezone_handler(self, choice):
        self.zone_box.configure(values=timezones[choice])
    
    # 26%
    def installation_type_stage(self):
        self.progressbar.set(0.26)
        region = self.region_box.get()
        zone = self.zone_box.get()
        if zone:
            timezone = f"{region}/{zone}"
        else:
            timezone = f"{region}"
        self.setup_information["Timezone"] = timezone

        if DEBUG: print(self.setup_information)

        for widget in self.winfo_children():
            if type(widget) != windows.widgets.ctk_progressbar.CTkProgressBar:
                widget.destroy()
        
        label = CTkLabel(self, text=self.lang.select_install_option, font=(None, 16, "bold"))
        self.installation_type_variable = IntVar(value=0)
        self.secure_type = CTkRadioButton(self, value=0, variable=self.installation_type_variable, text=self.lang.securetype)
        self.less_secure_type = CTkRadioButton(self, value=1, variable=self.installation_type_variable, text=self.lang.lessecuretype)
        self.insecure_type = CTkRadioButton(self, value=2, variable=self.installation_type_variable, text=self.lang.insecuretype)
        
        next_btn = CTkButton(self, text=self.lang.next, command=self.desktop_environment_stage)

        label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.secure_type.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.less_secure_type.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.insecure_type.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        next_btn.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")

    # 42%
    def desktop_environment_stage(self):
        self.progressbar.set(0.42)
        for widget in self.winfo_children():
            if type(widget) != windows.widgets.ctk_progressbar.CTkProgressBar:
                widget.destroy()
        
        key = self.installation_type_variable.get()
        match key:
            case 0:
                self.setup_information["InstallationType"] = "Secure"
            case 1:
                self.setup_information["InstallationType"] = "LessSecure"
            case 2:
                self.setup_information["InstallationType"] = "InSecure"
        if DEBUG: print(self.setup_information)
        
        label = CTkLabel(self, text=self.lang.choose_de, font=(None, 16, "bold"))
        

        self.de_variable = IntVar(value=0)
        self.gnome_button = CTkRadioButton(self, value=0, variable=self.de_variable, text="GNOME")
        self.kde_button = CTkRadioButton(self, value=1, variable=self.de_variable, text="KDE")
        self.console_button = CTkRadioButton(self, value=2, variable=self.de_variable, text=self.lang.console)

        next_btn = CTkButton(self, text=self.lang.next, command=self.partitioning_stage)
        label.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.gnome_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.kde_button.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        self.console_button.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        next_btn.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)

    # 57%
    def partitioning_stage(self):
        self.progressbar.set(0.57)
        for widget in self.winfo_children():
            if type(widget) != windows.widgets.ctk_progressbar.CTkProgressBar:
                widget.destroy()
        key = self.de_variable.get()
        match key:
            case 0:
                self.setup_information["DE"] = "GNOME"
            case 1:
                self.setup_information["DE"] = "KDE"
            case 2:
                self.setup_information["DE"] = "Console"
        if DEBUG: print(self.setup_information)
        
        label = CTkLabel(self, text=self.lang.diskpart, font=(None, 16, "bold"))
        
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        erase_all_disks = []
        for disk in disks:
            erase_all_disks.append(f"/dev/{disk['name']} | {disk['size']}")
        
        self.partitioning_type = IntVar(value=0)
        erase_all_partitioning = CTkRadioButton(self, text=self.lang.erase_all_and_install, variable=self.partitioning_type, value=0)
        self.erase_all_disk = CTkOptionMenu(self, values=erase_all_disks)
        manual_partitioning = CTkRadioButton(self, text=self.lang.manual, variable=self.partitioning_type, value=1)
        next_btn = CTkButton(self, text=self.lang.next, command=self.partitioning_next_button_handler)

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        erase_all_partitioning.grid(row=2, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.erase_all_disk.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        manual_partitioning.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")

    def partitioning_next_button_handler(self):
        key = self.partitioning_type.get()
        match key:
            case 0:
                disk = self.erase_all_disk.get().split(" |")[0]
                self.setup_information["Partitioning"] = "Automatic"
                self.setup_information["DriveToFormat"] = disk
                self.setup_information["UseSwap"] = True
                self.setup_information["SwapSize"] = "8"
                self.encryption_key_stage(manual=False)
            case 1:
                self.setup_information["Partitioning"] = "Manual"
                self.manual_partitioning()

    def manual_partitioning(self):
        for widget in self.winfo_children():
            if type(widget) != windows.widgets.ctk_progressbar.CTkProgressBar:
                widget.destroy()
        
        self.partitions = []
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    self.partitions.append(f"{partition['name']} | {partition['size']} | {partition.get('fstype', 'N/A')}")

        label = CTkLabel(self, text=self.lang.selfpart, font=(None, 16, "bold"))
        

        run_gparted_btn = CTkButton(self, text=self.lang.rungparted, command=lambda: os.system("/usr/bin/sudo /usr/bin/gparted"))
        

        update_disks = CTkButton(self, text=self.lang.refreshparts, command=self._update_partitions)
        

        efi_partition_label = CTkLabel(self, text=self.lang.efipart)
        self.efi_partition_optionmenu = CTkOptionMenu(self, values=self.partitions)

        root_partition_label = CTkLabel(self, text=self.lang.rootfs)
        self.root_partition_optionmenu = CTkOptionMenu(self, values=self.partitions, command=self.change_max_swapfile)
        self.use_swap = StringVar(value="on")
        self.swap_checkbox = CTkCheckBox(self, text=self.lang.useswap, variable=self.use_swap, onvalue="on", offvalue="off", command=self.swapfile_handler)
        

        swap_label = CTkLabel(self, text=self.lang.swapsize)
        self.swap_entry = CTkEntry(self)
        self.swap_entry.insert(0, "8")
        self.swap_scrollbar = CTkSlider(self, command=self.scroll_handler, to=16)
        

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
        next_btn.grid(row=8, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")

    def scroll_handler(self, newvalue):
        newvalue = round(newvalue, 1)
        self.swap_entry.delete(0, 'end')
        self.swap_entry.insert(0, str(newvalue))
    
    def swapfile_handler(self):
        if self.swap_checkbox.get() == "off":
            self.swap_entry.configure(state="disabled")
            self.swap_scrollbar.configure(state="disabled")
        else:
            self.swap_entry.configure(state="normal")
            self.swap_scrollbar.configure(state="normal")
            self.change_max_swapfile(None)

    def _update_partitions(self):
        self.partitions.clear()
        disks = json.loads(subprocess.run(['lsblk', '-o', 'NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE', '--json'], text=True, capture_output=True, check=True).stdout).get('blockdevices', [])
        for disk in disks:
            if 'children' in disk:
                for partition in disk['children']:
                    self.partitions.append(f"{partition['name']} | {partition['size']} | {partition.get('fstype', 'N/A')}")
        self.efi_partition_optionmenu.configure(values=self.partitions)
        self.root_partition_optionmenu.configure(values=self.partitions)

    def change_max_swapfile(self, newvalue):
        if self.swap_checkbox.get() == "off":
            return
        half_of_max_space = int(self._get_max_swap_size() / (2**30))//2
        if half_of_max_space == 0:
            print("Max swap space can't be zero!")
            self.swap_scrollbar.configure(state="disabled")
            return 
        else:
            self.swap_scrollbar.configure(state="normal")
        self.swap_scrollbar.configure(to=half_of_max_space)
        # self.swap_scrollbar.set(0)

    def _get_max_swap_size(self):
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

    def encryption_key_stage(self, manual):
        if manual:
            efi_partition = "/dev/" + self.efi_partition_optionmenu.get().split(" | ")[0]
            system_partition = "/dev/" + self.root_partition_optionmenu.get().split(" | ")[0]
            use_swapfile = ("on" == self.swap_checkbox.get())
            self.setup_information["Partitioning"] = "Manual"
            self.setup_information["EfiPartition"] = efi_partition
            self.setup_information["SystemPartition"] = system_partition
            self.setup_information["UseSwap"] = use_swapfile
            if use_swapfile:
                swapsize = self.swap_entry.get()
                self.setup_information["SwapSize"] = swapsize
        if DEBUG: print(self.setup_information)

        for widget in self.winfo_children():
            if type(widget) != windows.widgets.ctk_progressbar.CTkProgressBar:
                widget.destroy()
        self.progressbar.set(0.71)

        label = CTkLabel(self, text=self.lang.os_encryption, font=(None, 16, "bold"))
        label1 = CTkLabel(self, text=self.lang.enckey)
        self.system_partition_encryption_key_entry = CTkEntry(self, show='*')
        label2 = CTkLabel(self, text=self.lang.enckey2)
        self.system_partition_encryption_key_entry2 = CTkEntry(self, show='*')
        next_btn = CTkButton(self, text=self.lang.next, command=self.admin_creation_stage)

        label.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        label1.grid(row=2, column=0, padx=15, pady=5, sticky="nsew", columnspan=2)
        self.system_partition_encryption_key_entry.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        label2.grid(row=4, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.system_partition_encryption_key_entry2.grid(row=5, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        next_btn.grid(row=6, column=0, padx=15, pady=5, sticky="nsew", columnspan=2)
    
    def admin_creation_stage(self):
        if self.system_partition_encryption_key_entry.get() != self.system_partition_encryption_key_entry2.get():
            Notification(title=self.lang.passwordmismatch, icon="warning.png", message=self.lang.passwordmsg, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        self.setup_information["EncryptionKey"] = self.system_partition_encryption_key_entry.get()
        
        self.system_partition_encryption_key_entry.delete(0, 'end')
        self.system_partition_encryption_key_entry2.delete(0, 'end')
        gc_collect()

        for widget in self.winfo_children():
            if type(widget) != windows.widgets.ctk_progressbar.CTkProgressBar:
                widget.destroy()
        self.progressbar.set(0.86)

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
        next_btn.grid(row=7, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
    
    def final_stage(self):
        if self.password_entry.get() != self.password_entry2.get():
            Notification(title=self.lang.passwordmismatch, icon="warning.png", message=self.lang.passwordmsg, message_bold=True, exit_btn_msg=self.lang.exit)
            return
        self.setup_information["FullName"] = self.your_name_entry.get()
        self.setup_information["Hostname"] = self.hostname_entry.get()
        self.setup_information["Username"] = self.username_entry.get()
        self.setup_information["Password"] = self.password_entry.get()
        if DEBUG: print(self.setup_information)
        for widget in self.winfo_children():
            if type(widget) != windows.widgets.ctk_progressbar.CTkProgressBar:
                widget.destroy()
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

        begin_installation_button = CTkButton(self, text=self.lang.begin_install, command=self.begin_installation)

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
    
    def _list_partitions(self, drive):
        result = subprocess.run(['lsblk', '-ln', '-o', 'NAME,TYPE'], stdout=subprocess.PIPE, text=True)
        partitions = []
        for line in result.stdout.splitlines():
            name, type_ = line.split()
            if type_ == 'part' and name.startswith(drive.replace('/dev/', '')):
                partitions.append(f"/dev/{name}")
        return partitions

    def __execute_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            output = process.stdout.readline()
            if output:
                self.console_output.insert("end", output)
                self.console_output.see("end")  # Auto-scroll to the bottom
            elif process.poll() is not None:
                break
            error = process.stderr.read()
            if error:
                self.console_output.insert("end", error, "error")
                self.console_output.see("end")

    def _execute(self, command):
        self.__execute_command(command)

    def begin_installation(self):
        print(self.setup_information)
        for widget in self.winfo_children():
            widget.destroy()
        self.console_output = CTkTextbox(self)
        self.console_output.pack(padx=10, pady=10, expand=True, fill="both")
        exit()
        if self.setup_information["Partitioning"] == "Automatic":
            if not DEBUG: self._execute(f"sgdisk -Z {self.setup_information["DriveToFormat"]}")
            if not DEBUG: self._execute(f"sgdisk -n1:0:+1G -t1:ef00 -c1:EFI -N2 -t2:8304 {self.setup_information["DriveToFormat"]}")
            partitions = self._list_partitions(self.setup_information["DriveToFormat"])
            efi_partition = partitions[0]
            rootfs_partition = partitions[1]
        else:
            efi_partition = self.setup_information["EfiPartition"]
            rootfs_partition = self.setup_information["SystemPartition"]
        
        print(efi_partition, rootfs_partition)
        if not DEBUG: self._execute(f"echo -n {self.setup_information["EncryptionKey"]} | cryptsetup luksFormat {rootfs_partition}")
        if not DEBUG: self._execute(f"echo -n {self.setup_information["EncryptionKey"]} | cryptsetup luksOpen {rootfs_partition} cryptlvm")
        
        # if self.setup_information["UseSwap"] == False:
        #     if not DEBUG: self._execute("mkfs.ext4 /dev/mapper/cryptlvm")
        #     rootfs = "/dev/mapper/cryptlvm"
        # else:
        if not DEBUG: self._execute("pvcreate /dev/mapper/cryptlvm")
        if not DEBUG: self._execute("vgcreate volumegroup /dev/mapper/cryptlvm")
        
        if self.setup_information["UseSwap"] == False:
            if not DEBUG: self._execute("lvcreate -l 100%FREE volumegroup -n root")
        else:
            if not DEBUG: self._execute(f"lvcreate -L {self.setup_information["SwapSize"]}G volumegroup -n swap")
            if not DEBUG: self._execute("lvcreate -l 100%FREE volumegroup -n root")
        
        if not DEBUG: self._execute("mkfs.ext4 /dev/volumegroup/root")
        if not DEBUG: self._execute("mkswap /dev/volumegroup/root")
            # rootfs = "/dev/volumegroup/root"
        
        if self.setup_information["Partitioning"] == "Automatic":
            if not DEBUG: self._execute(f"mkfs.fat -F32 {efi_partition}")

        if not DEBUG: self._execute(f"mount /dev/volumegroup/root /mnt")
        if self.setup_information["UseSwap"]:
            if not DEBUG: 
                self._execute("swapon /dev/volumegroup/swap")
        if not DEBUG: self._execute(f"mount --mkdir -o uid=0,gid=0,fmask=0077,dmask=0077 {efi_partition} /mnt/efi")

        if not DEBUG: self._execute("pacstrap -K /mnt base linux linux-firmware linux-headers amd-ucode vim nano efibootmgr sudo lvm2 networkmanager")
        if not DEBUG: self._execute("genfstab -U /mnt >> /mnt/etc/fstab")

        if not DEBUG: self._execute(f"useradd -m {self.setup_information["Username"]} -c \"{self.setup_information["FullName"]}\"")
        
        if not DEBUG:
            process = subprocess.run(
                    ['passwd', self.setup_information["Username"]],
                    input=f"{self.setup_information["Password"]}\n{self.setup_information["Password"]}\n",  # Pass the password twice for confirmation
                    text=True,  # Enables passing string as input
                    check=True  # Raises an exception if the command fails
                )
        
                    
if __name__ == "__main__":
    App().mainloop()
        
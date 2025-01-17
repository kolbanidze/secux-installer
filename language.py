
class Locale:
    def __init__(self, language):
        if language == "en":
            self.test = "TEST | English"
            self.select_time_zone = "Select time zone"
            self.region = "Region"
            self.timezone = "Zone"
            self.next = "Next"
            self.select_install_option = "Select installation option"
            self.choose_de = "Choose desktop environment"
            self.console = "Console"
            self.diskpart = "Disk Partitioning"
            self.erase_all_and_install = "Erase all drive and install OS"
            self.manual = "Manual"
            self.selfpart = "Self-partitioning of the disk"
            self.rungparted = "Run GParted"
            self.refreshparts = "Refresh disk list"
            self.efipart = "EFI partition (loader)"
            self.rootfs = "Root partition (system and data)"
            self.useswap = "Use swap partition"
            self.swapsize = "Enter the size of the swap partition (GiB)"
            self.securetype = "Use of all security mechanisms"
            self.lessecuretype = "Using backward compatible security mechanisms (less secure)"
            self.insecuretype = "Without using security mechanisms (least secure)"
            self.os_encryption = "OS Encryption"
            self.enckey = "Enter encryption passphrase (US keymap)"
            self.enckey2 = "Enter encrpytion passphrase (repeat)"
            self.admin_creation = "Creating admin"
            self.yourname = "Full name"
            self.hostname = "Device name"
            self.username = "User name"
            self.password1 = "Password"
            self.password2 = "Password (check)"
            self.passwordmismatch = "Password mismatch!"
            self.passwordmsg = "Passwords mismatch. Please try again!"
            self.exit = "Exit"
            self.final = "Final"
            self.fulltimezone = "Time zone"
            self.installoption = "Installation option"
            self.de = "Desktop Environment"
            self.partitioningtype = "Type of disk layout"
            self.systeminstallto = "The disk on which the system will be installed"
            self.automatic = "Automatic"
            self.swapsize_final = "Size of swap partition (GiB)"
            self.begin_install = "Begin install"
            self.yes = "Yes"
            self.no = "No"
            self.pwd_length_title = "Minimum length not met"
            self.pwd_length = "Error: Password is shorter than 8 characters."
            self.efi_small_title = "Too small EFI partition"
            self.efi_small = "Error. EFI Partition must be larger than 200 MiB"
            self.network_title = "No internet connection"
            self.network = "Please connect to internet"
            self.not_uefi = "The system does not support UEFI. Installation is not possible.."
            self.not_uefi_title = "No UEFI support"
            self.not_setup_mode = "Setup Mode is not enabled in Secure Boot"
            self.not_setup_mode_title = "The system is not in Setup Mode"
            self.installing = "The system is being installed. For now, you can sit back in your chair.\nTechnical information about the installation process:"
        elif language == "ru":
            self.test = "ТЕСТ | Русский"
            self.select_time_zone = "Выберите часовой пояс"
            self.region = "Регион"
            self.timezone = "Пояс"
            self.next = "Далее"
            self.select_install_option = "Выберите вариант установки"
            self.choose_de = "Выберите окружение рабочего стола"
            self.console = "Консольный"
            self.diskpart = "Разметка диска"
            self.erase_all_and_install = "Стереть весь диск и установить ОС"
            self.manual = "Вручную"
            self.selfpart = "Самостоятельная разметка диска"
            self.rungparted = "Запустить GParted"
            self.refreshparts = "Обновить список дисков"
            self.efipart = "EFI раздел (загрузочный)"
            self.rootfs = "Корневой раздел (система и данные)"
            self.useswap = "Использовать раздел подкачки"
            self.swapsize = "Введите размер раздела подкачки (ГиБ)"
            self.securetype = "Использование всех механизмов безопасности"
            self.lessecuretype = "Использование механизмов безопасности с обратной совместимостью (менее безопасно)"
            self.insecuretype = "Без использования механизмов безопасности (наименее безопасно)"
            self.os_encryption = "Шифрование системы"
            self.enckey = "Введите парольную фразу для шифрования (ракладка: США)"
            self.enckey2 = "Введите парольную фразу для шифрования (повтор)"
            self.admin_creation = "Создание администратора"
            self.yourname = "Полное имя"
            self.hostname = "Название устройства"
            self.username = "Имя пользователя"
            self.password1 = "Пароль"
            self.password2 = "Пароль (проверка)"
            self.passwordmismatch = "Пароли отличаются"
            self.passwordmsg = "Пароли отличаются. Пожалуйста, попробуйте снова!"
            self.exit = "Выйти"
            self.final = "Итого"
            self.fulltimezone = "Часовой пояс"
            self.installoption = "Вариант установки"
            self.de = "Графическое окружение"
            self.partitioningtype = "Вид разметки диска"
            self.systeminstallto = "Диск, на который будет установлена система"
            self.automatic = "Автоматически"
            self.swapsize_final = "Размер раздела подкачки (ГиБ)"
            self.begin_install = "Начать установку"
            self.yes = "Да"
            self.no = "Нет"
            self.pwd_length_title = "Несоответствие минимальной длине"
            self.pwd_length = "Ошибка. Пароль короче 8 символов."
            self.efi_small_title = "Слишком маленький EFI раздел"
            self.efi_small = "Ошибка. EFI раздел должен быть больше 200 МиБ"
            self.network_title = "Отсутствует подключение к интернету"
            self.network = "Пожалуйста, подключитесь к интернету"
            self.not_uefi = "Система не поддерживает UEFI. Установка невозможна."
            self.not_uefi_title = "Отсутствие поддержки UEFI"
            self.not_setup_mode = "Не включен Setup Mode в Secure Boot"
            self.not_setup_mode_title = "Система не в Setup Mode"
            self.installing = "Система устанавливается. Пока можете откинуться на спинку стула.\nТехническая информация о процессе установки:"
from typing import Dict, Optional
import telebot
from .database import Database
from .menuitem import MenuItem


class Bot:
    """
    Bot for employee introductions.
    """

    def __init__(self, api_token: str) -> None:
        """
        :param api_token: API token for telegram bot.
        """

        self._bot: telebot.TeleBot = telebot.TeleBot(api_token)
        self._database: Database = Database()
        self._create_main_menu_items()
        self._register_message_handlers()

    def _create_main_menu_items(self) -> None:
        menu_items = {"company_info": "О компании",
                      "company_info_a": "О компании А",
                      "company_info_b": "О компании Б",
                      "offices": "Офисы компании",
                      "check_list": "Чек-лист",
                      "digital_transformation": "Цифровая трансформация",
                      "health": "Здоровье",
                      "general_questions": "Общие вопросы",
                      "adviсe": "Советы и рекомендации",
                      "glossary": "Глоссарий"}
        self._menu_items: Dict[str, MenuItem] = {item_name: MenuItem(item_name, item_title)
                                                 for item_name, item_title in menu_items.items()}

    @staticmethod
    def _get_employee_id(message) -> int:
        """
        :return: employee ID in Telegram.
        """

        return message.from_user.id

    @staticmethod
    def _get_employee_name(message) -> str:
        """
        :return: the name of the employee by which to greet him.
        """

        if message.from_user.first_name is not None:
            return message.from_user.first_name

        if message.from_user.username is not None:
            return message.from_user.username

        return message.from_user.id

    @staticmethod
    def _get_employee_username(message) -> int:
        """
        :return: employee username in Telegram.
        """

        return message.from_user.username

    def _get_menu_item(self, menu_title: str) -> Optional[MenuItem]:
        """
        :param menu_title: menu item name.
        :return: menu item with given name.
        """

        for menu_item in self._menu_items.values():
            if menu_item.title == menu_title:
                return menu_item

        return None

    def _greet_employee(self, message) -> None:
        user_name = self._get_employee_name(message)
        self._bot.send_message(message.chat.id, f"Привет, {user_name}!")

    def _handle_unknown_command(self, message):
        menu_item = self._get_menu_item(message.text)
        if menu_item:
            self._show_main_menu_item(message, menu_item)
            return

        self._bot.reply_to(message, "Неизвестная команда")

    def _register_employee(self, message) -> None:
        employee_id = self._get_employee_id(message)
        if not self._database.check_employee(employee_id):
            self._database.add_employee(employee_id, self._get_employee_username(message))

    def _register_message_handlers(self) -> None:
        self._bot.register_message_handler(self._start_executor, commands=["start"])
        self._bot.register_message_handler(self._show_main_menu, regexp="(Главное меню|Назад)")
        self._bot.register_message_handler(self._handle_unknown_command, func=lambda msg: True)

    def _show_main_menu(self, message):
        employee_id = self._get_employee_id(message)
        self._database.save_employee_history(employee_id, "Главное меню")

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [telebot.types.KeyboardButton(menu_item.title) for menu_item in self._menu_items.values()]
        markup.add(*buttons)
        self._bot.send_message(message.chat.id, "Главное меню", reply_markup=markup)

    def _show_main_menu_item(self, message, menu_item: MenuItem):
        """
        :param menu_item: the item from the main menu that needs to be shown.
        """

        employee_id = self._get_employee_id(message)
        self._database.save_employee_history(employee_id, menu_item.title)

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(telebot.types.KeyboardButton("Назад"))
        markup.add(telebot.types.KeyboardButton("Главное меню"))
        self._bot.send_message(message.chat.id, menu_item.text, reply_markup=markup)
        if menu_item.image is not None:
            self._bot.send_photo(message.chat.id, menu_item.image)

    def _start_executor(self, message):
        self._greet_employee(message)
        self._register_employee(message)

        employee_id = self._get_employee_id(message)
        last_menu_name = self._database.get_last_menu_item_name(employee_id)
        if last_menu_name:
            menu_item = self._get_menu_item(last_menu_name)
            if menu_item:
                self._bot.send_message(message.chat.id, f"В прошлый раз Вы остановились на '{last_menu_name}'")
                self._show_main_menu_item(message, menu_item)
                return

        self._show_main_menu(message)

    def run(self) -> None:
        self._bot.infinity_polling()

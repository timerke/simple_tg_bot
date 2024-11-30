import os
from typing import Optional


class MenuItem:
    """
    Class for main menu items.
    """

    def __init__(self, menu_item_name: str, menu_item_name_to_display: str) -> None:
        """
        :param menu_item_name: main menu item name;
        :param menu_item_name_to_display: display name of the main menu item.
        """

        self._name: str = menu_item_name
        self._name_to_display: str = menu_item_name_to_display
        self._text: Optional[str] = None

        self._read_data_for_menu_item()

    @property
    def text(self) -> str:
        """
        :return: text to be shown on the menu item page.
        """

        if self._text is None:
            return "Нет данных"

        return self._text

    @property
    def title(self) -> str:
        """
        :return: display name of the main menu item.
        """

        return self._name_to_display

    def _read_data_for_menu_item(self) -> None:
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(root_path, "data", f"{self._name}.txt")
        if os.path.exists(file_path):
            self._text = self._read_file(file_path)

    @staticmethod
    def _read_file(file_path: str) -> str:
        """
        :param file_path: path to the file to be read.
        :return: data from file.
        """

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

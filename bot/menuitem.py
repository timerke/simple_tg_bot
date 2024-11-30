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

        self._image: Optional[bytes] = None
        self._name: str = menu_item_name
        self._name_to_display: str = menu_item_name_to_display
        self._text: Optional[str] = None

        self._read_data_for_menu_item()

    @property
    def image(self) -> Optional[bytes]:
        """
        :return: image to be shown on the menu item page.
        """

        return self._image

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
        data_dir_path = "data"
        self._read_text(data_dir_path)
        self._read_image(data_dir_path)

    @staticmethod
    def _read_file(file_path: str, mode: str = "r", encoding: str = "utf-8") -> str:
        """
        :param file_path: path to the file to be read;
        :param mode: file opening mode;
        :param encoding:
        :return: data from file.
        """

        with open(file_path, mode, encoding=encoding) as file:
            return file.read()
    
    def _read_image(self, data_dir_path: str) -> None:
        """
        :param data_dir_path: path to the data folder.
        """

        for ext in ("png", "jpg", "jpeg"):
            file_path = os.path.join(data_dir_path, f"{self._name}.{ext}")
            if os.path.exists(file_path):
                self._image = self._read_file(file_path, "rb", None)
                break

    def _read_text(self, data_dir_path: str) -> None:
        """
        :param data_dir_path: path to the data folder.
        """

        file_path = os.path.join(data_dir_path, f"{self._name}.txt")
        if os.path.exists(file_path):
            self._text = self._read_file(file_path)

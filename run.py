from bot import Bot, parse_config


def run() -> None:
    """
    The function launches the bot.
    """

    data = parse_config("config.ini")
    telegram_bot = Bot(data["GENERAL"]["token"])
    telegram_bot.run()


if __name__ == "__main__":
    run()

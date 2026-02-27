from scripts.bootstrap import bootstrap


def main():
    config, logger = bootstrap()

    logger.info("Система успешно инициализирована")

    # здесь запускаешь бота / API / сервис


if __name__ == "__main__":
    main()

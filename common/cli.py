from common.commands import cli
from config.settings.settings import DATA_DIR
from config.django.files_and_storage import create_directory


def main():
    create_directory(DATA_DIR)
    cli()


if __name__ == '__main__':
    main()

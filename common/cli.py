from common.commands import cli
from common.settings import DATA_DIRECTORY
from common.utils.files_and_storage import create_directory


def main():
    create_directory(DATA_DIRECTORY)
    cli()


if __name__ == '__main__':
    main()

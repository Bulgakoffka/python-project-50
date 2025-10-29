import argparse as ap  # pragma: no cover

from gendiff.diff_core.diff_builder import generate_diff
from gendiff.parser import arg_parser, load_file  # pragma: no cover

# позже посмотреть требования проекта к названиям файлов.
#  если нет, то переименовать в main


def main():  # pragma: no cover
    args = arg_parser()
    first_file = load_file(args.first_file)
    second_file = load_file(args.second_file)
    format_name = args.format_name
    if format_name == 'stylish':
        return generate_diff(first_file, second_file, format_name)


if __name__ == "__main__":
    main()

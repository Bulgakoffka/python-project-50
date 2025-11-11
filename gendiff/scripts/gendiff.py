
from gendiff.diff_core.diff_builder import generate_diff
from gendiff.parser import arg_parser  # pragma: no cover

# позже посмотреть требования проекта к названиям файлов.
#  если нет, то переименовать в main


def main():  # pragma: no cover
    args = arg_parser()
    first_file = args.first_file
    second_file = args.second_file
    format_name = args.format_name
    if format_name:
        generated_diff = generate_diff(first_file, second_file, format_name)
        print(generated_diff)


if __name__ == "__main__":
    main()

import argparse as ap

from gendiff.modules.generate_diff import generate_diff

# позже посмотреть требования проекта к названиям файлов.
#  если нет, то переименовать в main


def parser_function():
    parser = ap.ArgumentParser(
                    prog='gendiff',
                    description='Compares two configuration' 
                    ' files and shows a difference.',
                    usage='gendiff [-h] first_file second_file'
    )
    parser.add_argument('-f', '--format', help='set format of output')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    return parser.parse_args()


def main():
    args = parser_function()
    first_file = args.first_file
    second_file = args.second_file
    return generate_diff(first_file, second_file)


if __name__ == '__main__':
    main()

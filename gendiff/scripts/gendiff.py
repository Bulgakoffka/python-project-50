import argparse as ap


def main():
    parser = ap.ArgumentParser(
                    prog='gendiff',
                    description='Compares two configuration files and shows a difference.',
                    usage='gendiff [-h] first_file second_file'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.parse_args()

if __name__ == '__main__':
    main()
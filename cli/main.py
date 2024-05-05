import argparse

import libem


def main():
    parser = argparse.ArgumentParser(description="Libem CLI tool")
    parser.add_argument('e1', type=str, help='First entity')
    parser.add_argument('e2', type=str, help='Second entity')

    args = parser.parse_args()

    entity1 = args.e1
    entity2 = args.e2

    result = libem.match(entity1, entity2)
    print("Match result:", result)


if __name__ == '__main__':
    main()

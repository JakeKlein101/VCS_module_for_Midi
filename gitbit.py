import VCS_main
import argparse
import sys

parser = argparse.ArgumentParser(description="Parser for gitbit VCS commands.")
parser.add_argument("opcode", type=str, help="Choose an opcode that suits the wanted operation."
                                             " for example: commit, push, init.")
parser.add_argument("-o", "--opcode_args", type=str, help="Optional arguments for certian functions.")

# TODO: Research about how to make only specific arguments have optional parameters with the argpare library.


def main():
    args = parser.parse_args()
    if args.opcode == "commit":
        VCS_main.handle_commit(args.opcode_args)
    elif args.opcode == "init":
        VCS_main.handle_init()
    # TODO: Add rollback command.


if __name__ == '__main__':
    main()

import VCS_main
import argparse

parser = argparse.ArgumentParser(description="Parser for gitbit VCS commands.")
parser.add_argument("opcode", type=str, help="Choose an opcode that suits the wanted operation."
                                             " for example: commit, push, init.")


def main():
    args = parser.parse_args()
    if args.opcode == "commit":
        VCS_main.handle_commit()
    elif args.opcode == "init":
        VCS_main.handle_init()
    elif args.opcode == "delete":
        VCS_main.handle_delete()
    elif args.opcode == "push":
        VCS_main.handle_push()
    elif args.opcode == "add":
        VCS_main.handle_add()
    elif args.opcode == "rollback":
        VCS_main.handle_rollback()  # TODO: Add optional arguments.
    elif args.opcode == "status":
        VCS_main.handle_status()
    else:
        print(f"{args.opcode} is not a legal command.")


if __name__ == '__main__':
    main()

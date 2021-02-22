import CliMethods


def main():
    cli_command_raw = input()
    cli_opcode, arg = CliMethods.parse_cli(cli_command_raw)
    if cli_opcode.lower() == "commit":
        CliMethods.commit_handle(arg)


if __name__ == '__main__':
    main()

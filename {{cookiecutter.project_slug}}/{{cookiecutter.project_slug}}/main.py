import sys
import platform
import logging
import argparse
import {{cookiecutter.project_slug}}


def parse_args(args_list):
    """Parse command-line arguments

    Params:
        args_list: list of strings with command-line flags (sys.argv[1:])
    """
    logger = logging.getLogger(f'{__name__}:parse_args')
    description = '{{cookiecutter.project_description}}'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--quiet', action='store_true',
                        help='Only print warning/error messages')
    parser.add_argument('--verbose', action='store_true',
                        help='Print debug messages')
    #
    # Add more command-line arguments and/or sub-commands
    #

    # Parse arguments in order to obtain results in argparse.Namespace object
    args_ns = parser.parse_args(args_list)

    # Set log level according to command-line flags
    if args_ns.verbose:
        {{cookiecutter.project_slug}}.LOGCONFIG.debug()
        logger.debug('%s:: %s\n', platform.node(), ' '.join(sys.argv))
    elif args_ns.quiet:
        {{cookiecutter.project_slug}}.LOGCONFIG.warning()

    return args_ns


def main():
    """Entry point for the command-line interface"""
    logger = logging.getLogger(f'{__name__}:main')
    args_ns = parse_args(sys.argv[1:])
    logger.info(args_ns)
    # Start application according to parsing result in args_ns


if __name__ == "__main__":
    main()
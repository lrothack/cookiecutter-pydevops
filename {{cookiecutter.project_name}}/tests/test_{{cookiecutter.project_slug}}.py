import pytest
from argparse import Namespace
import {{cookiecutter.project_slug}}.main


@pytest.fixture
def args_ns_ref():
    return Namespace()


def test_parseargs(args_ns_ref):
    arg_list = []
    args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
    # Define reference/expected result
    args_ns_ref.verbose = False
    args_ns_ref.quiet = False
    assert args_ns == args_ns_ref


def test_parseargs_verbose(args_ns_ref):
    arg_list = ['--verbose']
    args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
    args_ns_ref.verbose = True
    args_ns_ref.quiet = False
    assert args_ns == args_ns_ref


def test_parseargs_quiet(args_ns_ref):
    arg_list = ['--quiet']
    args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
    args_ns_ref.verbose = False
    args_ns_ref.quiet = True
    assert args_ns == args_ns_ref


if __name__ == "__main__":
    pytest.main()
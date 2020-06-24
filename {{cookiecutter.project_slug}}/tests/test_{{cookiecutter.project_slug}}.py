import pytest
from argparse import Namespace
import {{cookiecutter.project_slug}}.main


@pytest.fixture
def args_ns_exp():
    return Namespace()


def test_parseargs(args_ns_exp):
    arg_list = []
    args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
    # Define expected result
    args_ns_exp.verbose = False
    args_ns_exp.quiet = False
    assert args_ns == args_ns_exp


def test_parseargs_verbose(args_ns_exp):
    arg_list = ['--verbose']
    args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
    args_ns_exp.verbose = True
    args_ns_exp.quiet = False
    assert args_ns == args_ns_exp


def test_parseargs_quiet(args_ns_exp):
    arg_list = ['--quiet']
    args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
    args_ns_exp.verbose = False
    args_ns_exp.quiet = True
    assert args_ns == args_ns_exp
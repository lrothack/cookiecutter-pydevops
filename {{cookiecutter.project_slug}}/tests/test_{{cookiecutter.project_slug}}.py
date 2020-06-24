import unittest
from argparse import Namespace
import {{cookiecutter.project_slug}}.main


class TestMain(unittest.TestCase):

    def setUp(self):
        self.__args_ns_exp = Namespace()

    def test_parseargs(self):
        arg_list = []
        args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
        # Define expected result
        self.__args_ns_exp.verbose = False
        self.__args_ns_exp.quiet = False
        self.assertEqual(args_ns, self.__args_ns_exp)

    def test_parseargs_verbose(self):
        arg_list = ['--verbose']
        args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
        self.__args_ns_exp.verbose = True
        self.__args_ns_exp.quiet = False
        self.assertEqual(args_ns, self.__args_ns_exp)

    def test_parseargs_quiet(self):
        arg_list = ['--quiet']
        args_ns = {{cookiecutter.project_slug}}.main.parse_args(arg_list)
        self.__args_ns_exp.verbose = False
        self.__args_ns_exp.quiet = True
        self.assertEqual(args_ns, self.__args_ns_exp)
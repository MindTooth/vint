import unittest
from test.asserting.policy import PolicyAssertion, get_fixture_path

from vint.linting.level import Level
from vint.linting.policy.prohibit_misplaced_vim9script import ProhibitMisplacedVim9script


def fixture(name):
    return get_fixture_path('prohibit_misplaced_vim9script_{}.vim'.format(name))


def violation(line, column, path):
    return {
        'name': 'ProhibitMisplacedVim9script',
        'level': Level.ERROR,
        'position': {'line': line, 'column': column, 'path': path},
    }


class TestProhibitMisplacedVim9script(PolicyAssertion, unittest.TestCase):
    def test_valid_after_comments(self):
        self.assertFoundNoViolations(fixture('valid'), ProhibitMisplacedVim9script)

    def test_valid_vim9_mix(self):
        self.assertFoundNoViolations(fixture('valid_mix'), ProhibitMisplacedVim9script)

    def test_invalid_after_command(self):
        path = fixture('invalid_after_command')
        self.assertFoundViolationsEqual(path, ProhibitMisplacedVim9script,
                                        [violation(3, 1, path)])

    def test_invalid_in_block(self):
        path = fixture('invalid_in_block')
        self.assertFoundViolationsEqual(path, ProhibitMisplacedVim9script,
                                        [violation(2, 3, path)])

    def test_invalid_after_if_without_finish(self):
        path = fixture('invalid_if_without_finish')
        self.assertFoundViolationsEqual(path, ProhibitMisplacedVim9script,
                                        [violation(4, 1, path)])


if __name__ == '__main__':
    unittest.main()

import unittest
from test.asserting.policy import PolicyAssertion, get_fixture_path

from vint.linting.level import Level
from vint.linting.policy.prohibit_recursive_mapping import ProhibitRecursiveMapping

PATH_VALID_VIM_SCRIPT = get_fixture_path('prohibit_recursive_mapping_valid.vim')
PATH_INVALID_VIM_SCRIPT = get_fixture_path('prohibit_recursive_mapping_invalid.vim')


class TestProhibitRecursiveMapping(PolicyAssertion, unittest.TestCase):
    def test_get_violation_if_found_when_file_is_valid(self):
        self.assertFoundNoViolations(PATH_VALID_VIM_SCRIPT, ProhibitRecursiveMapping)


    def create_violation(self, line, column):
        return {
            'name': 'ProhibitRecursiveMapping',
            'level': Level.STYLE_PROBLEM,
            'position': {'line': line, 'column': column, 'path': PATH_INVALID_VIM_SCRIPT},
        }


    def test_get_violation_if_found_when_file_is_invalid(self):
        expected_violations = [
            self.create_violation(1, 1),
            self.create_violation(2, 1),
            self.create_violation(3, 1),
            self.create_violation(4, 9),
            self.create_violation(5, 1),
        ]

        self.assertFoundViolationsEqual(PATH_INVALID_VIM_SCRIPT, ProhibitRecursiveMapping,
                                        expected_violations)


if __name__ == '__main__':
    unittest.main()

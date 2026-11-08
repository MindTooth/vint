import unittest
from test.asserting.policy import PolicyAssertion, get_fixture_path

from vint.linting.level import Level
from vint.linting.policy.prohibit_missing_ftplugin_guard import ProhibitMissingFtpluginGuard
from vint.linting.policy.prohibit_missing_undo_ftplugin import ProhibitMissingUndoFtplugin
from vint.linting.policy.prohibit_global_mapping_in_ftplugin import ProhibitGlobalMappingInFtplugin

VALID = get_fixture_path('ftplugin', 'valid.vim')
INVALID = get_fixture_path('ftplugin', 'invalid.vim')
NO_LOCAL_CHANGES = get_fixture_path('ftplugin', 'no_local_changes.vim')
VIM9 = get_fixture_path('ftplugin', 'vim9.vim')
DELEGATING = get_fixture_path('ftplugin', 'delegating.vim')
AFTER_VALID = get_fixture_path('after', 'ftplugin', 'valid.vim')
NOT_FTPLUGIN = get_fixture_path('not_ftplugin.vim')

ALL_POLICIES = [
    ProhibitMissingFtpluginGuard,
    ProhibitMissingUndoFtplugin,
    ProhibitGlobalMappingInFtplugin,
]


def violation(policy, line, path):
    return {
        'name': policy.__name__,
        'level': Level.WARNING,
        'position': {'line': line, 'column': 1, 'path': path},
    }


class TestFtpluginPolicies(PolicyAssertion, unittest.TestCase):
    def test_valid_ftplugin(self):
        for policy in ALL_POLICIES:
            self.assertFoundNoViolations(VALID, policy)

    def test_valid_vim9_ftplugin(self):
        for policy in ALL_POLICIES:
            self.assertFoundNoViolations(VIM9, policy)

    def test_valid_after_ftplugin(self):
        for policy in ALL_POLICIES:
            self.assertFoundNoViolations(AFTER_VALID, policy)

    def test_ignores_files_outside_ftplugin(self):
        for policy in ALL_POLICIES:
            self.assertFoundNoViolations(NOT_FTPLUGIN, policy)

    def test_missing_guard(self):
        self.assertFoundViolationsEqual(INVALID, ProhibitMissingFtpluginGuard, [
            violation(ProhibitMissingFtpluginGuard, 1, INVALID),
        ])

    def test_guard_delegated_by_runtime(self):
        self.assertFoundNoViolations(DELEGATING, ProhibitMissingFtpluginGuard)

    def test_missing_undo(self):
        self.assertFoundViolationsEqual(INVALID, ProhibitMissingUndoFtplugin, [
            violation(ProhibitMissingUndoFtplugin, 1, INVALID),
        ])

    def test_no_undo_needed_without_local_changes(self):
        self.assertFoundNoViolations(NO_LOCAL_CHANGES, ProhibitMissingUndoFtplugin)

    def test_global_mapping_and_command(self):
        self.assertFoundViolationsEqual(INVALID, ProhibitGlobalMappingInFtplugin, [
            violation(ProhibitGlobalMappingInFtplugin, 2, INVALID),
            violation(ProhibitGlobalMappingInFtplugin, 4, INVALID),
        ])


if __name__ == '__main__':
    unittest.main()

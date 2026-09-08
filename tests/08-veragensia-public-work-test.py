#!/usr/bin/env python3
import copy
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/veragens-public-work.py'
API = runpy.run_path(str(SCRIPT))
PROFILE = json.loads((ROOT / 'config/public-work-profile.json').read_text())


class PublicWorkTests(unittest.TestCase):
    def setUp(self):
        self.packet = {
            'canonical': True, 'project_root': str(ROOT), 'continuity_id': 'public-test',
            'mission': PROFILE['mission'], 'status': 'active',
            'action_intent': {'action_type': 'implement_public_work_view'},
            'next_slice': PROFILE['actions']['implement_public_work_view']['next_action'] + '\nPRIVATE_CONTEXT',
            'updated_at': '2026-09-08T20:00:00Z', 'stale_note': None,
            'session_id': 'PRIVATE_SESSION', 'workpoint_id': 'PRIVATE_ID',
            'verification_records': [{'token': 'PRIVATE_TOKEN'}],
        }

    def test_only_public_fields_and_approved_wording_cross_boundary(self):
        result = API['public_snapshot'](self.packet, PROFILE)
        self.assertEqual(result['visibility'], 'public')
        self.assertEqual(result['state'], 'active')
        self.assertEqual(result['mission'], PROFILE['mission'])
        self.assertNotIn('PRIVATE_', json.dumps(result))
        self.assertNotIn(str(ROOT), json.dumps(result))
        self.assertEqual(len(result), 10)

    def test_changed_mission_next_stage_or_state_is_rejected(self):
        for field, value in [('mission', 'PRIVATE_MISSION'), ('next_slice', 'PRIVATE_NEXT'),
                             ('status', 'unknown'), ('updated_at', 'not-a-date'), ('next_slice', None)]:
            with self.subTest(field=field):
                packet = copy.deepcopy(self.packet); packet[field] = value
                with self.assertRaises((ValueError, TypeError)):
                    API['public_snapshot'](packet, PROFILE)
        self.packet['action_intent']['action_type'] = 'unapproved'
        with self.assertRaises(KeyError):
            API['public_snapshot'](self.packet, PROFILE)

    def test_stale_reason_is_not_published(self):
        self.packet['stale_note'] = 'PRIVATE_REASON'
        result = API['public_snapshot'](self.packet, PROFILE)
        self.assertTrue(result['stale'])
        self.assertNotIn('PRIVATE_REASON', json.dumps(result))

    def run_cli(self, packet, root=ROOT, canonical=True):
        with tempfile.TemporaryDirectory() as tmp:
            binary = Path(tmp) / 'focusa'
            envelope = {'schema_version': 'focusa.workpoint_resume_packet.v2',
                        'status': 'completed', 'canonical': canonical, 'resume_packet': packet}
            binary.write_text('#!/usr/bin/python3\nprint(' + repr(json.dumps(envelope)) + ')\n')
            binary.chmod(0o755)
            return subprocess.run([sys.executable, str(SCRIPT), '--project-root', str(root),
                                   '--continuity-id', 'public-test'], text=True, capture_output=True,
                                  env={**os.environ, 'PATH': tmp + ':' + os.environ.get('PATH', ''),
                                       'PYTHONDONTWRITEBYTECODE': '1'}, timeout=10)

    def test_cli_reuses_canonical_scope_guard_and_exports_valid_packet(self):
        result = self.run_cli(self.packet)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['project'], PROFILE['project'])
        self.assertNotIn('PRIVATE_', result.stdout + result.stderr)

    def test_cli_rejects_foreign_or_noncanonical_packet_without_echo(self):
        foreign = copy.deepcopy(self.packet); foreign['project_root'] = '/PRIVATE_FOREIGN'
        for packet, canonical in [(foreign, True), (self.packet, False)]:
            result = self.run_cli(packet, canonical=canonical)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            self.assertNotIn('PRIVATE_', result.stderr)

    def test_cli_refuses_profile_on_another_project(self):
        with tempfile.TemporaryDirectory() as root:
            result = self.run_cli(self.packet, root=Path(root))
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')

    def test_activation_wrapper_does_not_start_daemon_or_desktop(self):
        source = (ROOT / 'scripts/uiai-lab-remote-control').read_text()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp); stub = tmp / 'live'; log = tmp / 'calls'
            stub.write_text('#!/bin/bash\necho "$1" >> "$CALL_LOG"\nif [[ $1 == status ]]; then echo "container: $CONTAINER_STATE"; fi\n')
            stub.chmod(0o755)
            wrapper = tmp / 'wrapper'
            wrapper.write_text(source.replace('/usr/local/bin/uiai-lab-live', str(stub)))
            for state, expected in [('running', ['status', 'reload-chrome', 'status']), ('down', ['status'])]:
                log.write_text('')
                result = subprocess.run(['/bin/bash', str(wrapper), 'sync-activate'], capture_output=True,
                                        env={**os.environ, 'CALL_LOG': str(log), 'CONTAINER_STATE': state})
                self.assertEqual(log.read_text().splitlines(), expected)
                self.assertEqual(result.returncode, 0 if state == 'running' else 1)


if __name__ == '__main__':
    unittest.main()

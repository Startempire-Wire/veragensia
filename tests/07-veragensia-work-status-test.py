#!/usr/bin/env python3
"""Read-only Work presentation: canonical input, bounded output, no hidden actions."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/veragens'
API = runpy.run_path(str(SCRIPT))


class WorkStatusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.packet = {
            'schema_version': 'focusa.workpoint_resume_packet.v2',
            'status': 'completed', 'canonical': True,
            'resume_packet': {
                'canonical': True, 'project_root': str(self.root),
                'continuity_id': 'test-continuity', 'mission': 'Ship the Work surface',
                'status': 'active', 'next_slice': 'Review evidence',
                'updated_at': '2026-09-08T00:00:00Z', 'stale_note': None,
            },
        }

    def cli(self, output, packet=None, failure=False):
        provider = self.root / 'focusa'
        # Controlled fixture performs no execution; its argv assertion also catches
        # accidental status/run/dispatch calls instead of the existing read route.
        expected = ['workpoint', 'resume', '--project-root=' + str(self.root),
                    '--continuity-id=test-continuity', '--json']
        body = ('raise SystemExit(7)' if failure else
                'print(' + repr(json.dumps(packet or self.packet)) + ')')
        provider.write_text('#!' + sys.executable + '\nimport sys\n'
                            + 'assert sys.argv[1:] == ' + repr(expected) + '\n' + body + '\n')
        provider.chmod(0o700)
        env = dict(os.environ, PATH=str(self.root) + os.pathsep + os.environ['PATH'],
                   PYTHONDONTWRITEBYTECODE='1')
        return subprocess.run([sys.executable, str(SCRIPT), 'status', output,
                               '--project-root', str(self.root), '--continuity-id', 'test-continuity'],
                              env=env, capture_output=True, text=True, timeout=10)

    def test_daemon_read_has_bounded_headroom_without_changing_inventory(self):
        module = API['inventory_module']()
        self.assertEqual(module.TIMEOUT, 2.0)
        calls = []
        def probe(argv, *, timeout):
            calls.append(timeout)
            return {'status': 'ok'}, json.dumps(self.packet).encode()
        module.probe = probe
        with patch.dict(API['resume'].__globals__, {'inventory_module': lambda: module}):
            _, code = API['resume'](str(self.root), 'test-continuity')
        self.assertEqual(code, 0)
        self.assertEqual(calls, [5.0])

    def test_json_is_existing_canonical_envelope(self):
        result = self.cli('--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), self.packet)

    def test_waybar_shows_real_fields_as_checkpoint_not_worker_health(self):
        result = self.cli('--waybar')
        self.assertEqual(result.returncode, 0, result.stderr)
        frame = json.loads(result.stdout)
        self.assertIn('Ship the Work surface', frame['text'])
        self.assertIn('Project: ' + str(self.root), frame['tooltip'])
        self.assertIn('Workpoint state: active', frame['tooltip'])
        self.assertIn('Next: Review evidence', frame['tooltip'])
        self.assertIn('not live worker status', frame['tooltip'])
        self.assertEqual(frame['class'], 'checkpoint')

    def test_markup_controls_and_unbounded_fields_are_not_rendered(self):
        self.packet['resume_packet'].update(mission='<b>&"\x1b\n' + 'x' * 5000,
                                            next_slice='<img>' * 5000, status='<script>')
        frame = API['waybar_frame'](self.packet, 0)
        self.assertNotIn('<', frame['text'] + frame['tooltip'])
        self.assertNotIn('\x1b', frame['text'] + frame['tooltip'])
        self.assertIn('&lt;b&gt;', frame['text'])
        self.assertLess(len(json.dumps(frame)), 12000)
        self.assertEqual(frame['class'], 'checkpoint')

    def test_stale_checkpoint_is_explicit(self):
        self.packet['resume_packet']['stale_note'] = 'Scope needs reassessment'
        frame = API['waybar_frame'](self.packet, 0)
        self.assertEqual(frame['class'], 'stale')
        self.assertTrue(frame['text'].startswith('Work (stale):'))
        self.assertIn('Stale: Scope needs reassessment', frame['tooltip'])

    def test_missing_optional_display_fields_are_unknown(self):
        for name in ('mission', 'status', 'next_slice', 'updated_at'):
            self.packet['resume_packet'][name] = {'unsupported': 'shape'}
        frame = API['waybar_frame'](self.packet, 0)
        self.assertEqual(frame['text'], 'Work: unknown')
        self.assertIn('Next: unknown', frame['tooltip'])

    def test_foreign_scope_cannot_leak_into_waybar(self):
        self.packet['resume_packet']['project_root'] = '/foreign/project'
        self.packet['resume_packet']['mission'] = 'PRIVATE FOREIGN MISSION'
        result = self.cli('--waybar')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['class'], 'unavailable')
        self.assertNotIn('PRIVATE', result.stdout)
        self.assertNotIn('/foreign', result.stdout)

    def test_failure_frame_clears_previous_state_but_json_keeps_error_exit(self):
        result = self.cli('--waybar', failure=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['text'], 'Work: unavailable')
        self.assertNotIn('Ship the Work surface', result.stdout)
        self.assertNotEqual(self.cli('--json', failure=True).returncode, 0)

    def test_noncanonical_input_is_unavailable(self):
        self.packet['canonical'] = False
        self.assertEqual(json.loads(self.cli('--waybar').stdout)['class'], 'unavailable')

    def test_compatibility_requires_selected_presenter_not_legacy_metadata(self):
        data = json.loads((ROOT / 'config/v0.1-release-candidate.json').read_text())
        data['platform']['quickshell_version'] = 'legacy-observation'
        path = self.root / 'candidate.json'
        path.write_text(json.dumps(data))
        fields = {g['field'] for g in API['manifest_gaps'](path)['gaps']}
        self.assertIn('platform.waybar_version', fields)
        self.assertNotIn('platform.quickshell_version', fields)
        self.assertFalse(data['release_ready'])

    def test_example_has_no_implicit_scope_or_action(self):
        source = (ROOT / 'config/waybar-work.jsonc').read_text()
        config = json.loads('\n'.join(s for s in source.splitlines() if not s.startswith('//')))
        module = config['custom/veragensia-work']
        self.assertIn('--project-root=', module['exec'])
        self.assertIn('--continuity-id=', module['exec'])
        self.assertNotIn('on-click', module)
        self.assertFalse(module['escape'])  # Output already escapes Pango markup.


if __name__ == '__main__':
    unittest.main()

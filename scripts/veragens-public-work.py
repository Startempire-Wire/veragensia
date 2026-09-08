#!/usr/bin/env python3
"""Curate a public display artifact from the existing explicitly scoped read adapter."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import runpy
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def public_snapshot(packet, profile):
    # Only configured public wording can cross this boundary; raw context never does.
    if profile.get('schema') != 'veragensia.public_work_profile.v1':
        raise ValueError('unsupported publication profile')
    action = packet['action_intent']['action_type']
    approved = profile['actions'][action]
    if (packet['mission'] != profile['mission'] or
            not isinstance(packet['next_slice'], str) or
            not isinstance(packet['updated_at'], str) or
            packet['next_slice'].split('\n', 1)[0].strip() != approved['next_action'] or
            packet['status'] not in ('active', 'blocked', 'completed')):
        raise ValueError('checkpoint does not match approved public wording')
    checkpoint = datetime.fromisoformat(packet['updated_at'].replace('Z', '+00:00'))
    if checkpoint.tzinfo is None:
        raise ValueError('checkpoint timestamp has no timezone')
    return {
        'schema': 'focusa.public_work_snapshot.v1', 'visibility': 'public',
        'project': profile['project'], 'mission': profile['mission'],
        'state': packet['status'], 'stage': approved['stage'],
        'next_action': approved['next_action'],
        'checkpoint_at': checkpoint.isoformat(),
        'published_at': datetime.now(timezone.utc).isoformat(),
        'stale': bool(packet.get('stale_note')),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', required=True)
    parser.add_argument('--continuity-id', required=True)
    args = parser.parse_args()
    try:
        if Path(args.project_root).resolve() != ROOT:
            raise ValueError('publication profile belongs to another project')
        api = runpy.run_path(str(ROOT / 'scripts/veragens'))
        reply, code = api['resume'](args.project_root, args.continuity_id)
        if code:
            raise ValueError('scoped continuation unavailable')
        profile = json.loads((ROOT / 'config/public-work-profile.json').read_text())
        snapshot = public_snapshot(reply['resume_packet'], profile)
        print(json.dumps(snapshot, ensure_ascii=False))
        return 0
    except (KeyError, TypeError, ValueError, OSError):
        print('Public Work export rejected: unavailable or unapproved checkpoint; no context exported.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check append-only evidence against an explicit trusted Git base revision."""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def check_change(path, before, after):
    """A new file is allowed; recorded evidence cannot be edited or deleted."""
    if before is None:
        return None
    immutable = path.startswith(('artifacts/', 'sources/imports/')) and path != 'artifacts/README.md'
    # Captured README payloads are evidence too; only root directory guides are exempt.
    if path.startswith('artifacts/') and len(Path(path).parts) > 2:
        immutable = True
    if path.startswith('benchmarks/preregistrations/') and path.endswith('.json'):
        try:
            immutable = json.loads(before).get('status') == 'frozen'
        except (ValueError, AttributeError):
            return 'Cannot read base protocol; review before changing it'
    if immutable and before != after:
        return 'Immutable evidence changed; use a new snapshot/run/protocol ID'
    if path == 'state/UPDATES.md' or (path.startswith('sessions/') and path.endswith('/journal.md')):
        if after is None or not after.startswith(before):
            return 'Append-only journal/update was rewritten'
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    def git(*argv):
        return subprocess.check_output(['git', '-C', str(root), *argv])
    try:
        base = git('rev-parse', '--verify', args.base+'^{commit}').decode().strip()
        paths = git('diff', '--no-renames', '--name-only', '-z', base, 'HEAD').decode().split('\0')
        errors = []
        for path in filter(None, paths):
            def at(revision):
                exists = subprocess.run(['git','-C',str(root),'cat-file','-e',revision+':'+path],capture_output=True)
                return git('show',revision+':'+path) if exists.returncode == 0 else None
            error = check_change(path, at(base), at('HEAD'))
            if error: errors.append(path+': '+error)
        if errors:
            print('\n'.join(errors),file=sys.stderr)
            return 1
        print('PASS: append-only history against '+base)
        return 0
    except subprocess.CalledProcessError as error:
        print('Cannot verify base history: '+str(error),file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())

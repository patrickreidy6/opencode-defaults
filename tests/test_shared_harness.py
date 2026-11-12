import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import install
from tests.test_baseline import DEFAULT_SOURCE, REPO_ROOT, cli_env, make_source, snapshot

try:
    import shared_harness
except ModuleNotFoundError:
    shared_harness = None


class SharedResetTests(unittest.TestCase):
    def test_update_resets_shared_items_and_backs_up_retired_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old_config = json.loads(DEFAULT_SOURCE['global/opencode.json'])
            old_config['agents']['retired'] = {'model': 'old'}
            old_config['mcp']['servers']['retired'] = {'url': 'old'}
            old = make_source(root / 'old', {
                **DEFAULT_SOURCE,
                'global/opencode.json': json.dumps(old_config).encode(),
                'global/commands/retired.md': b'original\n',
            })
            new = make_source(root / 'new')
            dest = root / 'dest'
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(install.run_install(old, dest, dry_run=False), 0)
            edited = b'my edited retired command\n'
            (dest / 'commands/retired.md').write_bytes(edited)
            (dest / 'commands/mine.md').write_bytes(b'local only\n')
            (dest / 'skills/demo/SKILL.md').write_bytes(b'edited shared\n')
            config = install.read_config(dest / 'opencode.json')
            config['agents']['retired']['model'] = 'edited'
            config['agents']['retired']['local_note'] = 'keep unowned field'
            config['mcp']['servers']['retired']['url'] = 'edited'
            config['agents']['title']['model'] = 'my-model'
            config['providers'] = {'local': {'apiKey': 'do not print'}}
            (dest / 'opencode.json').write_text(json.dumps(config), encoding='utf-8')
            before = snapshot(dest)
            with contextlib.redirect_stdout(output):
                self.assertEqual(install.run_install(new, dest, dry_run=True, reset_shared=True), 0)
            self.assertEqual(snapshot(dest), before)
            with contextlib.redirect_stdout(output):
                self.assertEqual(install.run_install(new, dest, dry_run=False, reset_shared=True), 0)
            self.assertFalse((dest / 'commands/retired.md').exists())
            self.assertEqual((dest / 'commands/mine.md').read_bytes(), b'local only\n')
            self.assertEqual((dest / 'skills/demo/SKILL.md').read_bytes(), DEFAULT_SOURCE['.opencode/skills/demo/SKILL.md'])
            updated = install.read_config(dest / 'opencode.json')
            self.assertEqual(updated['agents']['title']['model'], 'openai/gpt-6.1-sol#medium')
            self.assertEqual(updated['agents']['retired'], {'local_note': 'keep unowned field'})
            self.assertNotIn('retired', updated['mcp']['servers'])
            self.assertEqual(updated['providers'], config['providers'])
            backups = list((dest / 'backups').glob('harness-*/commands/retired.md'))
            self.assertEqual([p.read_bytes() for p in backups], [edited])
            self.assertNotIn('do not print', output.getvalue())


class DriftTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(shared_harness, 'shared_harness driver is not implemented')
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = make_source(self.root / 'source')
        self.dest = self.root / 'dest'
        self.project = self.root / 'project'
        self.project.mkdir()
        subprocess.run(['git', 'init', '--quiet', str(self.project)], check=True, capture_output=True)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(install.run_install(self.source, self.dest, dry_run=False), 0)

    def report(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), mock.patch.object(install, 'probe_opencode_version', return_value=('ok', '2.2.7')):
            code = shared_harness.report_drift(self.source, self.dest, self.project)
        return code, output.getvalue()

    def test_drift_separates_upstream_workspace_and_project_without_writes(self):
        (self.source / 'global/commands/xm-demo.md').write_bytes(b'upstream improvement\n')
        (self.dest / 'skills/demo/SKILL.md').write_bytes(b'LOCAL SECRET CONTENT\n')
        (self.dest / 'commands/local.md').write_bytes(b'local addition\n')
        cfg = install.read_config(self.dest / 'opencode.json')
        cfg['agents']['title']['model'] = 'LOCAL_SECRET_VALUE'
        (self.dest / 'opencode.json').write_text(json.dumps(cfg), encoding='utf-8')
        (self.project / 'AGENTS.md').write_bytes(b'project instructions\n')
        (self.project / '.opencode/skills/my-skill').mkdir(parents=True)
        (self.project / '.opencode/skills/my-skill/SKILL.md').write_bytes(b'private project skill\n')
        before = snapshot(self.dest), snapshot(self.project)
        code, output = self.report()
        self.assertEqual(code, 0)
        self.assertIn('Upstream updated file commands/xm-demo.md', output)
        self.assertIn('Workspace edited file skills/demo/SKILL.md', output)
        self.assertIn('Workspace changed setting agents.title.model', output)
        self.assertIn('Local commands/local.md', output)
        self.assertIn('Project AGENTS.md', output)
        self.assertIn('Project .opencode/skills/my-skill/', output)
        self.assertNotIn('LOCAL_SECRET', output)
        self.assertEqual((snapshot(self.dest), snapshot(self.project)), before)

    def test_upstream_removed_files_and_local_deletions_are_distinct(self):
        (self.source / 'global/commands/xm-demo.md').unlink()
        (self.dest / 'AGENTS.md').unlink()
        code, output = self.report()
        self.assertEqual(code, 0)
        self.assertIn('Upstream removed file commands/xm-demo.md', output)
        self.assertIn('Workspace removed file AGENTS.md', output)

    def test_missing_or_corrupt_receipt_is_error_not_clean_drift(self):
        for content in (None, b'bad JSON'):
            with self.subTest(content=content):
                receipt = self.dest / install.RECEIPT_NAME
                if content is None:
                    receipt.unlink(missing_ok=True)
                else:
                    receipt.write_bytes(content)
                with self.assertRaises((install.ReceiptError, shared_harness.HarnessError)):
                    self.report()

    def test_update_verifies_resets_and_reloads_but_leaves_project_files(self):
        (self.dest / 'AGENTS.md').write_bytes(b'changed managed instructions\n')
        (self.project / 'AGENTS.md').write_bytes(b'project owns this\n')
        project_before = snapshot(self.project)
        output = io.StringIO()
        with contextlib.redirect_stdout(output), mock.patch.object(install, 'probe_opencode_version', return_value=('ok', '2.2.7')), mock.patch.object(shared_harness, 'run_opencode', return_value=None) as runtime:
            self.assertEqual(shared_harness.apply_update(self.source, self.dest), 0)
        self.assertEqual(runtime.call_args_list, [mock.call('reload')])
        self.assertEqual((self.dest / 'AGENTS.md').read_bytes(), DEFAULT_SOURCE['global/AGENTS.md'])
        self.assertEqual(snapshot(self.project), project_before)
        self.assertTrue(list((self.dest / 'backups').glob('harness-*/AGENTS.md')))

    def test_upgrade_failure_does_not_apply_harness_or_claim_success(self):
        before = snapshot(self.dest)
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(install, 'probe_opencode_version', return_value=('ok', '2.2.5')), mock.patch.object(shared_harness, 'run_opencode', side_effect=shared_harness.HarnessError('upgrade failed')):
            with self.assertRaises(shared_harness.HarnessError):
                shared_harness.apply_update(self.source, self.dest)
        self.assertEqual(snapshot(self.dest), before)

    def test_upgrade_uses_pin_and_reports_service_restart_without_killing_it(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), mock.patch.object(install, 'probe_opencode_version', side_effect=[('ok', '2.2.5'), ('ok', '2.2.7')]), mock.patch.object(shared_harness, 'run_opencode') as runtime:
            self.assertEqual(shared_harness.apply_update(self.source, self.dest), 0)
        self.assertEqual(runtime.call_args_list, [mock.call('upgrade', '2.2.7'), mock.call('reload')])
        self.assertIn('opencode service restart', output.getvalue())

    def test_invalid_install_stops_before_runtime_upgrade(self):
        (self.dest / install.RECEIPT_NAME).write_bytes(b'invalid')
        before = snapshot(self.dest)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()), mock.patch.object(shared_harness, 'run_opencode') as runtime:
            with self.assertRaises((install.ReceiptError, shared_harness.HarnessError)):
                shared_harness.apply_update(self.source, self.dest)
        runtime.assert_not_called()
        self.assertEqual(snapshot(self.dest), before)

    def test_reload_failure_says_defaults_were_already_installed(self):
        (self.dest / 'AGENTS.md').write_bytes(b'local edit\n')
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(install, 'probe_opencode_version', return_value=('ok', '2.2.7')), mock.patch.object(shared_harness, 'run_opencode', side_effect=shared_harness.HarnessError('reload failed')):
            with self.assertRaisesRegex(shared_harness.HarnessError, 'were installed, but reload failed'):
                shared_harness.apply_update(self.source, self.dest)
        self.assertEqual((self.dest / 'AGENTS.md').read_bytes(), DEFAULT_SOURCE['global/AGENTS.md'])


class GitSourceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(shared_harness, 'shared_harness driver is not implemented')
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.upstream = make_source(self.root / 'upstream')
        (self.upstream / '.gitignore').write_text('__pycache__/\n', encoding='utf-8')
        self.git(self.upstream, 'init', '-b', 'main')
        self.git(self.upstream, 'add', '.')
        self.git(self.upstream, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'initial')
        self.local = self.root / 'cache'
        self.git(self.root, 'clone', str(self.upstream), str(self.local))

    def git(self, cwd, *args):
        result = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def change_upstream(self, name='change.md', content=b'new version\n'):
        (self.upstream / name).write_bytes(content)
        self.git(self.upstream, 'add', '.')
        self.git(self.upstream, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'upstream change')

    def refresh(self):
        return shared_harness.refresh_source(self.local, expected_remote=str(self.upstream))

    def test_receive_fast_forwards_without_mutating_remote(self):
        self.change_upstream()
        before = self.git(self.upstream, 'rev-parse', 'HEAD')
        result = self.refresh()
        self.assertEqual(result, before)
        self.assertEqual(self.git(self.local, 'rev-parse', 'HEAD'), before)
        self.assertEqual(self.git(self.upstream, 'rev-parse', 'HEAD'), before)
        self.assertEqual((self.local / 'change.md').read_bytes(), b'new version\n')

    def test_dirty_source_is_not_overwritten(self):
        (self.local / 'global/AGENTS.md').write_bytes(b'dirty local source')
        before = snapshot(self.local / 'global')
        self.change_upstream()
        with self.assertRaisesRegex(shared_harness.HarnessError, 'local changes'):
            self.refresh()
        self.assertEqual(snapshot(self.local / 'global'), before)

    def test_local_commits_and_wrong_origin_are_rejected(self):
        self.change_upstream()
        with self.assertRaises(shared_harness.HarnessError):
            shared_harness.refresh_source(self.local, expected_remote='https://wrong.invalid/repo')
        self.git(self.local, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-m', 'local commit')
        with self.assertRaisesRegex(shared_harness.HarnessError, 'local commits'):
            self.refresh()

    def test_dispatch_runs_newly_fetched_driver_not_stale_import(self):
        self.change_upstream('shared_harness.py', b'import sys\nprint("CURRENT DRIVER", *sys.argv[1:])\n')
        with contextlib.redirect_stdout(io.StringIO()), mock.patch.object(shared_harness, 'PUBLIC_REPO', str(self.upstream)):
            result = shared_harness.dispatch('drift', self.local, self.root / 'dest', self.root)
        self.assertEqual(result.returncode, 0)
        self.assertIn('CURRENT DRIVER drift', result.stdout)


if __name__ == '__main__':
    unittest.main()

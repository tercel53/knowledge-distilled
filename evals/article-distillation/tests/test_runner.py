import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import runner


def score(value=3):
    return dict(fidelity=value, reasoning=value, language=value, structure=value,
                visual=None, usability=None, blockers=[], evidence=['plan.md: concrete observation'])


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.skill = self.base / 'skill'
        self.skill.mkdir()
        (self.skill / 'SKILL.md').write_text('Test-only synthetic skill. Produce the requested artifact.')
        self.run = self.base / 'run'
        runner.prepare(self.run, self.skill, self.skill, ['approval-workflow'], 1, 'test-only')

    def finish(self, job, text='A synthetic plan with conditions.'):
        output = Path(job['output_dir'])
        if job['kind'] == 'generate':
            (output / 'plan.md').write_text(text)
        elif job['kind'] == 'read':
            (output / 'reader.md').write_text('A and B both explain the workflow.')
        else:
            runner.write(output / 'judgment.json', dict(scores={'A':score(), 'B':score()}, winner='tie', reason='Same observed content.'))
        return runner.complete(self.run, job['id'], {'agent_id':job['id'], 'backend':'test-double'})

    def generators(self):
        for _ in range(2):
            job = runner.next_job(self.run)
            self.assertEqual(job['kind'], 'generate')
            self.finish(job)

    def test_lifecycle_and_no_source_before_blind_read(self):
        job = runner.next_job(self.run)
        self.assertNotIn('baseline', job['prompt'])
        self.assertNotIn('candidate', job['prompt'])
        self.assertFalse((Path(job['cwd']) / 'checks.json').exists())
        self.finish(job)
        self.finish(runner.next_job(self.run))
        reader = runner.next_job(self.run)
        self.assertEqual(reader['kind'], 'read')
        self.assertFalse((Path(reader['cwd']) / 'source.md').exists())
        self.assertFalse((Path(reader['cwd']) / 'checks.json').exists())
        self.finish(reader)
        judge = runner.next_job(self.run)
        self.assertEqual(judge['kind'], 'judge')
        self.assertTrue((Path(judge['cwd']) / 'source.md').is_file())
        self.assertTrue((Path(judge['cwd']) / 'checks.json').is_file())
        self.assertIn('HTML', runner.read(Path(judge['cwd']) / 'checks.json')['task'])
        self.finish(judge)
        report = runner.report(self.run)
        self.assertEqual(report['decision'], 'no_demonstrated_improvement')
        self.assertEqual(report['groups']['plan/development']['verdicts'], {'tie':1})
        self.assertTrue(runner.next_job(self.run)['done'])

    def test_missing_expected_artifact_cannot_complete(self):
        job = runner.next_job(self.run)
        with self.assertRaisesRegex(ValueError, 'expected artifact'):
            runner.complete(self.run, job['id'], {'agent_id':'fresh'})
        self.assertEqual(runner.load(self.run)['jobs'][0]['status'], 'active')
        self.assertEqual(runner.report(self.run)['decision'], 'incomplete')

    def test_active_resume_and_unique_context(self):
        first = runner.next_job(self.run)
        self.assertEqual(runner.next_job(self.run, first['id'])['id'], first['id'])
        self.finish(first)
        second = runner.next_job(self.run)
        (Path(second['output_dir']) / 'plan.md').write_text('valid')
        with self.assertRaisesRegex(ValueError, 'already used'):
            runner.complete(self.run, second['id'], {'agent_id':first['id']})

    def test_freeze_rejects_output_mutation(self):
        job = runner.next_job(self.run)
        self.finish(job)
        (Path(job['output_dir']) / 'plan.md').write_text('changed after freezing')
        with self.assertRaisesRegex(ValueError, 'frozen material changed'):
            runner.report(self.run)

    def test_freeze_rejects_rubric_mutation(self):
        path = self.run / 'control/suite/rubrics/review.md'
        path.write_text('adjust scoring to favor candidate')
        with self.assertRaisesRegex(ValueError, 'frozen material changed'):
            runner.next_job(self.run)

    def test_no_replacing_completed_artifacts(self):
        job = runner.next_job(self.run)
        self.finish(job)
        with self.assertRaisesRegex(ValueError, 'active'):
            runner.complete(self.run, job['id'], {'agent_id':'new'})

    def test_symlinks_and_escaping_paths_rejected(self):
        job = runner.next_job(self.run)
        (Path(job['output_dir']) / 'plan.md').symlink_to(self.skill / 'SKILL.md')
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            runner.complete(self.run, job['id'], {'agent_id':'new'})
        with self.assertRaisesRegex(ValueError, 'escapes'):
            runner.contained(self.run, '../../elsewhere')

    def test_scoring_failure_can_be_recovered_before_freeze(self):
        self.generators()
        self.finish(runner.next_job(self.run))
        job = runner.next_job(self.run)
        path = Path(job['output_dir']) / 'judgment.json'
        row = dict(scores={'A':score(), 'B':score()}, winner='tie', reason='Same')
        row['scores']['A']['visual'] = 3
        runner.write(path, row)
        with self.assertRaisesRegex(ValueError, 'planning'):
            runner.complete(self.run, job['id'], {'agent_id':job['id']})
        self.finish(job)
        self.assertEqual(runner.report(self.run)['coverage']['judged_pairs'], 1)

    def test_regression_is_not_hidden_by_winner(self):
        self.generators()
        self.finish(runner.next_job(self.run))
        job = runner.next_job(self.run)
        state = runner.load(self.run)
        pair = state['pairs'][0]
        candidate = next(k for k,v in pair['mapping'].items() if v == 'candidate')
        row = dict(scores={'A':score(), 'B':score()}, winner=candidate, reason='Preference despite language regression')
        row['scores'][candidate]['language'] = 1
        runner.write(Path(job['output_dir']) / 'judgment.json', row)
        runner.complete(self.run, job['id'], {'agent_id':job['id']})
        report = runner.report(self.run)
        self.assertEqual(report['decision'], 'regression_or_blocker')
        self.assertEqual(report['regressions'][0]['dimension'], 'language')

    def test_html_requires_browser_evidence(self):
        state = runner.load(self.run)
        pair = copy.deepcopy(state['pairs'][0]);pair['case']['scope']='html';pair['mapping']={'A':'baseline','B':'candidate'}
        out = self.base / 'judge'
        row = dict(scores={'A':score(), 'B':score()}, winner='tie', reason='Both rendered')
        for sheet in row['scores'].values():sheet.update(visual=3,usability=3)
        runner.write(out / 'judgment.json',row)
        with self.assertRaisesRegex(ValueError, 'rendering'):
            runner.judgment_row(self.run,state,pair,out)
        row['winner']='inconclusive'
        for sheet in row['scores'].values():sheet.update(visual=None,usability=None)
        runner.write(out / 'judgment.json',row)
        self.assertEqual(runner.judgment_row(self.run,state,pair,out)['winner'],'inconclusive')

    def test_automatic_worker_protocol(self):
        worker=self.base/'worker.py'
        worker.write_text('''import sys,json,uuid
from pathlib import Path
j=json.load(sys.stdin);p=Path(j['output_dir'])
if j['kind']=='generate':(p/'plan.md').write_text('Synthetic test plan')
elif j['kind']=='read':(p/'reader.md').write_text('Synthetic reading')
else:
 s=dict(fidelity=2,reasoning=2,language=2,structure=2,visual=None,usability=None,blockers=[],evidence=['Synthetic fixture'])
 (p/'judgment.json').write_text(json.dumps(dict(scores={'A':s,'B':s},winner='tie',reason='Fixture tie')))
print(json.dumps({'agent_id':str(uuid.uuid4()),'backend':'test-double'}))
''')
        result=runner.execute(self.run,[sys.executable,str(worker)],10)
        self.assertEqual(result['coverage']['judged_pairs'],1)
        self.assertEqual(len(result['timing']),4)

    def test_worker_failure_leaves_resumable_job(self):
        with self.assertRaisesRegex(ValueError,'remains active'):
            runner.execute(self.run,[sys.executable,'-c','raise SystemExit(7)'],10)
        active=[j for j in runner.load(self.run)['jobs'] if j['status']=='active']
        self.assertEqual(len(active),1)
        self.assertEqual(runner.next_job(self.run,active[0]['id'])['id'],active[0]['id'])

    def test_interrupted_state_commit_recovers_without_replacing_first_copy(self):
        job=runner.next_job(self.run)
        (Path(job['output_dir'])/'plan.md').write_text('frozen first version')
        with patch.object(runner, 'save', side_effect=OSError('simulated interruption')):
            with self.assertRaises(OSError):
                runner.complete(self.run,job['id'],{'agent_id':job['id']})
        frozen=self.run/'control/frozen'/job['id']/'plan.md'
        self.assertEqual(frozen.read_text(),'frozen first version')
        runner.complete(self.run,job['id'],{'agent_id':job['id']})
        self.assertEqual(frozen.read_text(),'frozen first version')

    def test_partial_copy_never_commits_destination(self):
        dest=self.base/'copy-target'
        def fail(source, target):
            target.mkdir();(target/'partial').write_text('partial');raise OSError('interrupted copy')
        with patch.object(runner.shutil,'copytree',side_effect=fail):
            with self.assertRaises(OSError):runner.copy_tree(self.skill,dest)
        self.assertFalse(dest.exists())
        runner.copy_tree(self.skill,dest)
        self.assertEqual(runner.digest(self.skill),runner.digest(dest))

    def test_changed_runner_rejected_for_old_run(self):
        elsewhere=self.base/'other-tool';elsewhere.mkdir()
        (elsewhere/'runner.py').write_text('different implementation')
        with patch.object(runner,'HERE',elsewhere):
            with self.assertRaisesRegex(ValueError,'tool changed'):runner.report(self.run)

    def test_actual_backend_and_model_mismatch_reported(self):
        for model in ('model-one','model-two'):
            job=runner.next_job(self.run)
            (Path(job['output_dir'])/'plan.md').write_text('valid')
            runner.complete(self.run,job['id'],{'agent_id':job['id'],'backend':'actual-worker','model':model})
        self.finish(runner.next_job(self.run));self.finish(runner.next_job(self.run))
        report=runner.report(self.run)
        self.assertEqual(report['decision'],'incomparable_conditions')
        self.assertIn('model',report['conditions']['mismatches'])
        self.assertEqual(report['conditions']['observed'][0]['backend'],'actual-worker')

    def test_structural_failure_is_frozen_and_reported(self):
        html_run=self.base/'html-run'
        runner.prepare(html_run,self.skill,self.skill,['approval-workflow-html'],1,'test')
        job=runner.next_job(html_run);out=Path(job['output_dir'])
        (out/'index.html').write_text('<section id="x"></section><section id="x"></section>')
        (out/'README.md').write_text('Synthetic note')
        (out/'content-plan.md').write_text('Synthetic content plan')
        runner.write(out/'metadata.json',{'outline':[]})
        runner.complete(html_run,job['id'],{'agent_id':'html-test'})
        result=runner.report(html_run)
        self.assertEqual(len(result['structural_failures']),1)
        self.assertIn('duplicate',result['structural_failures'][0]['details'])
        self.assertEqual(result['coverage']['judged_pairs'],0)

    def test_grouped_results_do_not_hide_holdout_regression(self):
        row=dict(case_id='development-case',run=1,scope='plan',split='development',
                 mapping={'A':'baseline','B':'candidate'},winner='B',reason='Observed improvement',
                 scores={'A':score(2),'B':score(3)})
        other=copy.deepcopy(row);other.update(case_id='held-out-case',split='holdout',winner='A')
        other['scores']['B']['reasoning']=1
        result=runner.summarize([row,other])
        self.assertEqual(result['groups']['plan/holdout']['verdicts'],{'baseline':1})
        self.assertEqual(result['regressions'][0]['split'],'holdout')

    def test_unknown_case_has_no_partial_run(self):
        bad=self.base/'invalid'
        with self.assertRaisesRegex(ValueError,'unknown case'):
            runner.prepare(bad,self.skill,self.skill,['unknown'],1,'test')
        self.assertFalse(bad.exists())


if __name__=='__main__':
    unittest.main()

import os
import shutil
import git

from backgitup import Backgitup, BackgitupFile, system_file_name

source_path = os.path.join(os.path.split(__file__)[0], 'test_source')
backup_path = os.path.join(os.path.split(__file__)[0], 'test_backup')


def _create_test_repository(paths:list):
    for p in paths:
        assert not os.path.exists(p)
        os.mkdir(p)
        git.Repo.init(p)


def _remove_test_repository(paths:list):
    for p in paths:
        shutil.rmtree(p)


def test_create_new_and_backup():
    test_paths = [source_path]
    _create_test_repository(test_paths)
    try:
        bgu = Backgitup.create_new_source(source_path=source_path)
        try:
            bgu = Backgitup.create_new_source(source_path=source_path)
            assert False, 'This should fail, since the there obviously is a backitup allready in place.'
        except AssertionError:
            pass  # It failed as expected.

        # Add some new files to commit:
        files = [os.path.join(source_path, 'nissefjes.txt'), os.path.join(source_path, 'trollansikt.txt')]
        for file in files:
            with open(file, 'w') as fid:
                fid.writelines(['nisse', 'fjes'])

        assert [os.path.join(bgu.source.repo.working_dir, utf) for utf in bgu.source.repo.untracked_files] == files
        bgu.commit_all()
        assert not bgu.source.repo.untracked_files
    finally:
        _remove_test_repository(test_paths)
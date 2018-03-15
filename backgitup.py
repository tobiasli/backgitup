from typing import List
from codecs import open
import uuid
import pytz
import datetime

import git
import os

from tzlocal import get_localzone
from socket import gethostname

system_file_name = '.backgitup'

class BackgitupGenericClass(object):
    timezone = get_localzone()
    hostname = gethostname()
    system_file = '.backgitup'


class Backgitup(BackgitupGenericClass):
    def __init__(self, *, source_path: str) -> None:
        self.source = Source(path=source_path)

    def find_backups(self) -> List[str]:
        # Search for backup identities. Start with top level drives (as we assume USB-based backups).
        pass

    @staticmethod
    def create_new_source(*, source_path: str):
        source = Source.create_new_source(path=source_path)
        return Backgitup(source_path=source.path)

    def create_new_backup(self, backup_path: str):
        pass

    def commit_all(self):
        self.source.commit_all()


class BackgitupFile(BackgitupGenericClass):
    def __init__(self, path, create=False) -> None:
        """The backgitup file is a textfile called .backgitup that contains the key for this unique backup relationship
        and also the log for all transactions in the backup system."""

        self.path = os.path.join(path, self.system_file)

        if create:
            self.key = uuid.uuid4().hex
            assert not os.path.exists(self.path), '.backgitup allready exists'
            self.add_message(self.key, timestamp=False)
            self.add_message('', timestamp=False)

        else:
            assert os.path.exists(self.path), '.backgitup file does not exists.'
            with open(self.path, 'r', encoding='utf-8') as file:
                self.key = file.readline()

    def __eq__(self, other: 'BackgitupFile') -> bool:
        return self.key == other.key

    def add_message(self, message:str, timestamp:bool=True) -> None:
        with open(self.path, 'w+', encoding='utf-8') as file:
            if timestamp:
                time = str(datetime.datetime.now(tz=self.timezone)) + '\t'
            else:
                time = ''
            file.write(f'{time}{message}')


class BackupRepositoryObject(BackgitupGenericClass):
    def __init__(self, *,  path):
        try:
            self.repo = git.Repo(path)
        except git.exc.InvalidGitRepositoryError:
            print(f'Invalid git repository at {path}')
        self.path = path
        self.backgitup_file = BackgitupFile(path)


class Source(BackupRepositoryObject):

    @staticmethod
    def create_new_source(*, path):
        file = BackgitupFile(path, create=True)
        try:
            repo = git.Repo(path)
        except git.exc.InvalidGitRepositoryError:
            repo = git.Repo.init(path)
        file.add_message('Created source at {self.hostname}\\{path}')
        repo.index.add([file.path])
        repo.index.commit('backgitup: Added .backgitup to repository.')
        return Source(path=path)

    def commit_all(self):
        message = 'Commiting all changes'
        self.backgitup_file.add_message(message)
        self.repo.git.add('--all')
        self.repo.index.commit(message)


class Backup(BackupRepositoryObject):
    pass
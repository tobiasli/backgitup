Backgitup
=====

Simple python framework on top of GitPython that enables systematic backups of any amount of files with full history.

Backgitup designates a folder as a source, and can set any number of backup locations reached by cloning and pushing the
source repository. 

Sources and backups are identified with a unique key. Most of my non-cloud backups are on external drives that are 
connected intermittently. Backgitup will therefore have a discovery function that looks at all connected drives and 
identifies backups with matching keys to the source. It may then proceed to push any changes in source to the backups.

In this way, if backgitup is setup as a service on your machine of choice, it may backup anything as soon as you connect
the drive, without any manual interference.

The git repositories contain a .backgitup-file, which contains the backgitup key and any information on successful or
failed backups and when they were performed. It is part of the tracked by the repository, so any push to a backup is
follows by an commit append that contains a "successfull" entry into the .backgitup-file.
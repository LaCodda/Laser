import click

from lib.backup import *
from lib.host import *
from lib.tools.bitrix import *

Host = Host ()


# Backup = Backup ()
# Restore = Restore ()


@click.group ()
@click.version_option (version=Config.progVersion, prog_name=Config.progName, message='%(prog)s %(version)s')
def cli ():
	"""Laser
	LaCodda Server Tools
	"""


@cli.group ('host')
def host ():
	"""Manages hosts."""


@host.command ('new')
@click.argument ('name')
@click.option ('--alias', default='default', help='Server Alias')
@click.option ('--tech', default='none', help='Tech')
@click.option ('--db', default='none', help='Data Base')
@click.option ('--dbname', default='default', help='Data Base Name')
@click.option ('--backup', default='none', help='Backup')
@click.option ('--load', default='none', help='Load')
@click.option ('--adminer', default='none', help='Load Adminer')
def host_new (name, alias, tech, db, dbname, backup, load, adminer):
	"""Creates a new host."""
	Host.new (serverName=name, serverAlias=alias, tech=tech, db=db, dbname=dbname, backup=backup, load=load, adminer=adminer)


@host.command ('up')
def host_up ():
	"""Host up."""
	Host.up ()


@host.command ('start')
def host_start ():
	"""Host start."""
	Host.start ()


@host.command ('restart')
def host_restart ():
	"""Host restart."""
	Host.restart ()


@host.command ('stop')
def host_stop ():
	"""Host stop."""
	Host.stop ()


@host.command ('del')
@click.argument ('name')
def host_del (name):
	"""Host delete."""
	Host.delete (name)


@host.command ('list')
def host_list ():
	"""Host list."""
	Host.list ()


@cli.group ('backup')
def backup ():
	"""Manages backups."""


@backup.command ('host')
@click.argument ('name', default='all')
@click.option ('--type', default='all', type=click.Choice (['db', 'files', 'all']))
def backup_host (name, type):
	backup = Backup (name, type)
	backup.host ()


@backup.command ('project')
@click.argument ('name', default='all')
@click.option ('--type', default='all', type=click.Choice (['db', 'files', 'all']))
def backup_project (name, type):
	backup = Backup (name, type)
	backup.project ()


@cli.group ('restore')
def restore ():
	"""Manages restores."""


@restore.command ('host')
@click.argument ('name', default='all')
@click.option ('--type', default='all', type=click.Choice (['db', 'files', 'all']))
def restore_host (name, type):
	restore = Restore (hostName=name, type=type)
	restore.host ()


@restore.command ('project')
@click.argument ('name', default='all')
@click.option ('--type', default='all', type=click.Choice (['db', 'files', 'all']))
def restore_project (name, type):
	restore = Restore (hostName=name, type=type)
	restore.project ()


@cli.group ('tools')
def tools ():
	"""Manages tools."""


@tools.command ('prolong-bitrix-demo')
@click.argument ('destination')
@click.option ('--source', default='none', help='Source')
def bitrixLong (destination, source):
	bitrix = Bitrix (destinationHost=destination, sourceHost=source)
	# bitrix.snichPass ()
	bitrix.install ()


if __name__ == '__main__':
	cli ()

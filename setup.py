from cx_Freeze import setup, Executable


base = None    
# Activate for stand alone, no prompt (with gui)
#base = "Win32GUI"

executables = [Executable("dawkside.py", base=base)]

packages = ["idna"]
options = {
	'build_exe': {    
		'packages':packages,
		'include_files': [
			('setup', 'setup'),
			('media', 'media'),
			('plugins', 'plugins'),
			('devices', 'devices'),
			('devices', 'lib\devices'),
		],
	},    
}

setup(
	name = "Dawkside",
	options = options,
	version = "1.0",
	description = 'Multi daw, multi devices control surface manager for the visually impaired.',
	executables = executables
)
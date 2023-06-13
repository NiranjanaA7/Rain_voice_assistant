from cx_Freeze import setup, Executable

# Specify the main script file
main_script = 'mainp.py'

# Create an executable
executables = [Executable(main_script)]

# Additional files or directories to be included
additional_files = []

# Create the setup configuration
setup(
    name='Your Voice Assistant',
    version='1.0',
    description='Voice assistant with GUI',
    executables=executables,
    options={
        'build_exe': {
            'include_files': additional_files,
        },
    },
)
from pathlib import Path

def get_files_info(working_directory, directory=None):
    try:
        working_directory = Path(working_directory).resolve()
        directory = Path(directory).resolve() if directory else working_directory
    except Exception as e:
        return f'Error: Could not resolve path: {e}'

    # SECURITY FIRST: Block access if outside working_directory
    try:
        directory.relative_to(working_directory)
    except ValueError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Now that it's within the sandbox, check existence and type
    if not directory.exists():
        return f'Error: "{directory}" does not exist'

    if not directory.is_dir():
        return f'Error: "{directory}" is not a directory'

    try:
        entries = []
        for entry in sorted(directory.iterdir()):
            try:
                size = entry.stat().st_size
                is_dir = entry.is_dir()
                entries.append(f'- {entry.name}: file_size={size} bytes, is_dir={is_dir}')
            except Exception as e:
                entries.append(f'- {entry.name}: Error retrieving metadata: {e}')
        return '\n'.join(entries)
    except Exception as e:
        return f'Error: Could not list contents of "{directory}": {e}'

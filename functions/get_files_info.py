from pathlib import Path

def get_files_info(working_directory, directory=None):
    try:
        working_directory = Path(working_directory).resolve()
        # 👇 JOIN BEFORE RESOLVE — this is the key fix
        directory_path = (working_directory / (directory or ".")).resolve()
    except Exception as e:
        return f'Error: Could not resolve path: {e}'

    # SECURITY FIRST: Check if inside sandbox
    try:
        directory_path.relative_to(working_directory)
    except ValueError:
        return f'Error: Cannot list "{directory_path}" as it is outside the permitted working directory'

    if not directory_path.exists():
        return f'Error: "{directory_path}" does not exist'

    if not directory_path.is_dir():
        return f'Error: "{directory_path}" is not a directory'

    try:
        entries = []
        for entry in sorted(directory_path.iterdir()):
            try:
                size = entry.stat().st_size
                is_dir = entry.is_dir()
                entries.append(f'- {entry.name}: file_size={size} bytes, is_dir={is_dir}')
            except Exception as e:
                entries.append(f'- {entry.name}: Error retrieving metadata: {e}')
        return '\n'.join(entries)
    except Exception as e:
        return f'Error: Could not list contents of "{directory_path}": {e}'

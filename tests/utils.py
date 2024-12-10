import difflib

def are_files_identical(file1_path, file2_path, print_diff=False):
    """
    Compare two files and return True if they are identical (ignoring trailing line breaks).
    
    Args:
        file1_path: Path to the first file
        file2_path: Path to the second file
        print_diff: Whether to print differences when files don't match
    
    Returns:
        True if files are identical, False otherwise
    """
    with open(file1_path, 'r', encoding='latin-1') as file1,\
            open(file2_path, 'r', encoding='latin-1') as file2:
        file1_lines = [line.strip() for line in file1.read().strip().splitlines()]
        file2_lines = [line.strip() for line in file2.read().strip().splitlines()]

    if file1_lines == file2_lines:
        return True
    
    if print_diff:
        diff = difflib.unified_diff(file1_lines, file2_lines, lineterm='',
                                  fromfile=file1_path, tofile=file2_path)
        diff_lines = list(diff)
        differing_lines_count = sum(1 for line in diff_lines if line.startswith('+'))
        print(f"Files are different. Number of differing lines: {differing_lines_count // 2}")
        print("Differences:")
        for line in diff_lines:
            print(line)
    
    return False

if __name__ == '__main__':
    # Example usage:
    file1 = 'path/to/first/file.txt'
    file2 = 'path/to/second/file.txt'

    if are_files_identical(file1, file2):
        print("The files are identical.")
    else:
        print("The files are different.")


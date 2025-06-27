from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

# Test Cases for 'get_files_info'
# test_1 = get_files_info("calculator")  # lists 'calculator'
# test_2 = get_files_info("calculator", "calculator/pkg")  # lists 'calculator/pkg'
# test_3 = get_files_info("calculator", "/bin")  # stays the same for out-of-bounds test
# test_4 = get_files_info("calculator", "calculator/../")  # should still trigger the security check!

# Test Cases for 'get_file_content'
# test_1 = get_file_content("calculator", "lorem.txt")  # Lorem text file test
# test_2 = get_file_content("calculator", "main.py")  # lists 'calculator/pkg'
# test_3 = get_file_content("calculator", "pkg/calculator.py")  # stays the same for out-of-bounds test
# test_4 = get_file_content("calculator", "/bin/cat")  # should still trigger the security check!

# Test Cases for 'write_file'
# test_1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# test_2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# test_3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

# Test Cases for 'run_python_file'
test_1 = run_python_file("calculator", "main.py")
test_2 = run_python_file("calculator", "tests.py")
test_3 = run_python_file("calculator", "../main.py")
test_4 = run_python_file("calculator", "nonexistent.py")

print(test_1)
print(test_2)
print(test_3)
print(test_4)

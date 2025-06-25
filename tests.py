from functions.get_files_info import get_files_info

test_1 = get_files_info("calculator")  # lists 'calculator'
test_2 = get_files_info("calculator", "calculator/pkg")  # lists 'calculator/pkg'
test_3 = get_files_info("calculator", "/bin")  # stays the same for out-of-bounds test
test_4 = get_files_info("calculator", "calculator/../")  # should still trigger the security check!

print(test_1)
print(test_2)
print(test_3)
print(test_4)

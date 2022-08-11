from test_bash_script_OK.test_ import test as bash_script_test
from test_auto_tiger_launch_OK.test_ import test as auto_tiger_launch_test
from test_csv_writer_reader_OK.test_ import test as csv_reader_writer_test

# Tests to run
BASH_SCRIPT_TEST = True
AUTO_TIGER_LAUNCH_TEST = True
CSV_READER_WRITER_TEST = True


def run_tests():
    print('Running the tests, see the tests folder under the root directory to learn more')
    if BASH_SCRIPT_TEST:
        if bash_script_test("test_bash_script_OK/sample.i"):
            print("--> Bash script test: OK" )
        else:
            print("--> Bash script test: NOT WORKING")
    if AUTO_TIGER_LAUNCH_TEST:
        if auto_tiger_launch_test():
            print("--> Auto tiger launch test: OK")
        else:
            print("--> Auto tiger launch test: NOT WORKING")
    if CSV_READER_WRITER_TEST:
        if csv_reader_writer_test("test_csv_writer_reader_OK/sample.csv"):
            print("--> CSV reader / writer test: OK")
        else:
            print("--> CSV reader / writer test: NOT WORKING")


if __name__ == '__main__':
    run_tests()

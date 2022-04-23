import main
import test_batch_config as test_cases


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    TESTPASS = OKGREEN + "PASS" + ENDC
    TESTFAIL = FAIL + "FAIL" + ENDC


def single_resp_test(func, test_assert, func_name):
    test_log = []
    print(f"{'*' * 5} Testing {func_name} {'*' * 5}")
    for case in test_assert:
        try:
            result = func(case["Input"])
            if repr(result) == repr(case["Output"]):
                test_log.append(f"{bcolors.TESTPASS} [{case['Input']} => {result}]")
            else:
                test_log.append(f"{bcolors.TESTFAIL} [{case['Input']}: {repr(case['Output'])} != {repr(result)}]")
        except Exception as error:
            error_type = type(error)
            if repr(type(error)) == repr(case["Output"]):
                test_log.append(f"{bcolors.TESTPASS} [{case['Input']} => {error_type}]")
            else:
                test_log.append(f"{bcolors.TESTFAIL} [{case['Input']}: {repr(case['Output'])} != {repr(error_type)}]")
    return test_log


def test_eval_blocksize():
    func_name = "Class: Hashfile => eval_blocksize [Static Method]"
    test_assert = test_cases.eval_block_size_list
    test_log = single_resp_test(main.HashFile.eval_blocksize, test_assert, func_name)
    for log in test_log:
        print(log)


if __name__ == "__main__":
    test_eval_blocksize()

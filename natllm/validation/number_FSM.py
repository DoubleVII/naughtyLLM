import unittest
class number_FSM:
    def __init__(self):
        # 定义状态
        self.start_state = 'START'
        self.accept_state = 'ACCEPT'
        self.reject_state = 'REJECT'
        
        # 当前状态初始化为开始状态
        self.current_state = self.start_state
        
        # 定义状态转移表
        self.transitions = {
            'START': {'-': 'SIGNED', '0': 'LEADING_ZERO', 'digit': 'INTEGER_PART'},
            'SIGNED': {'0': 'LEADING_ZERO', 'digit': 'INTEGER_PART'},
            'LEADING_ZERO': {'0': 'REJECT', 'digit': 'REJECT', '.': 'DOT', 'e': 'REJECT', 'E': 'REJECT'},
            'INTEGER_PART': {'0': 'INTEGER_PART', 'digit': 'INTEGER_PART', '.': 'DOT', 'e': 'EXP', 'E': 'EXP'},
            'DOT': {'0': 'FRACTION_PART', 'digit': 'FRACTION_PART'},
            'FRACTION_PART': {'0': 'FRACTION_PART', 'digit': 'FRACTION_PART', 'e': 'EXP', 'E': 'EXP'},
            'EXP': {'+': 'EXP_SIGN', '-': 'EXP_SIGN', 'digit': 'EXP_NUMBER'},
            'EXP_SIGN': {'0': 'EXP_NUMBER', 'digit': 'EXP_NUMBER'},
            'EXP_NUMBER': {'0': 'EXP_NUMBER', 'digit': 'EXP_NUMBER'}
        }
    
    def is_digit(self, char):
        return char.isdigit()
    
    def get_char_type(self, char):
        if char == '0':
            return char
        elif self.is_digit(char):
            return 'digit'
        elif char in '-+.eE':
            return char
        else:
            return None
    
    def transition(self, char):
        char_type = self.get_char_type(char)
        if char_type in self.transitions[self.current_state]:
            self.current_state = self.transitions[self.current_state][char_type]
        else:
            self.current_state = self.reject_state
        return self.current_state
    
    def is_accepting(self):
        return self.current_state in ['INTEGER_PART', 'FRACTION_PART', 'EXP_NUMBER']
    
    def reset(self):
        self.current_state = self.start_state
    
    def match(self, string):
        # 调试用函数
        self.reset()
        for char in string:
            self.transition(char)
            if self.current_state == self.reject_state:
                return False
        return self.is_accepting()


class TestNumberFSM(unittest.TestCase):
    def setUp(self):
        self.fsm = number_FSM()

    def test_valid_numbers(self):
        test_cases = ["123",
                      "-123",
                      "123.45",
                      "-123.45",
                      "0.123",
                      "1e10",
                      "12.3e4",
                      "-1.23e4",
                      "-1.23e-4"]
        for test in test_cases:
            with self.subTest(test=test):
                self.assertTrue(self.fsm.match(test), f"Failed for {test}")

    def test_invalid_numbers(self):
        test_cases = ["abc",  #not digit
                      "123e",  #no digit after e
                      ".123"  #no digit before dot
                      "1.2.3",  #mutiple dots
                      "1e10e10",  #multiple es
                      "123e4.5",  #dot after e
                      "0123",  #leading zero
                      "00.123",  #leading zeros
                      "0e10"]  #leading zero with e
        for test in test_cases:
            with self.subTest(test=test):
                self.assertFalse(self.fsm.match(test), f"Failed for {test}")

if __name__ == '__main__':
    # test cases
    unittest.main()
    # fsm = number_FSM()
    # test_cases = ["123", "-123", "123.45", "-123.45", "1e10",
    # "-1.23e-4", "abc", "123e", "1.2.3", "1e10e10"]

    # for test in test_cases:
    #     result = fsm.match(test)
    #     print(f"'{test}': {result}")

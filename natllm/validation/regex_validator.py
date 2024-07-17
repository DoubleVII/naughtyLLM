import interegular


class Validator:
    def __init__(self) -> None:
        pass

    def init_state(self) -> None:
        raise NotImplementedError

    def validate(self, input_str: str) -> bool:
        raise NotImplementedError

    def finish(self) -> bool:  # <eos>
        raise NotImplementedError


class RegexValidator(Validator):
    #  regex 参数是一个正则表达式字符串。
    def __init__(self, regex: str) -> None:
        super().__init__()
        # 解析正则表达式模式并将其转换为FSM（有限状态自动机）对象
        self.fsm = interegular.parse_pattern(regex).to_fsm()
        #  初始化当前状态为 None，表示还未开始验证过程
        self.current_state = None

    # 初始化状态为 FSM 的初始状态
    def init_state(self) -> None:
        self.current_state = self.fsm.start_state

    # 验证输入字符串是否使 FSM 转移到一个有效状态
    def validate(self, input_str: str) -> bool:
        # 遍历输入字符串 input_str 中的每个字符char，检查它是否在当前状态self.current_state的转移字典中
        for char in input_str:
            # 如果是，则更新self.current_state到下一个状态，即self.fsm.transitions[self.current_state][char]
            if char in self.fsm.transitions[self.current_state]:
                self.current_state = self.fsm.transitions[self.current_state][char]
            # 如果不是，则表示当前字符在当前状态下无法继续转移，返回False表示验证失败
            else:
                return False

        # 检查当前状态是否为最终状态
        if self.current_state in self.fsm.final_states:
            return True
        else:
            return False

    # 确认整个验证过程结束时，当前状态是否是最终状态
    def finish(self) -> bool:  # <eos>
        return self.current_state in self.fsm.final_states

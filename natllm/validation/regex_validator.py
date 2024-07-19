
import interegular

class Validator:
    def __init__(self) -> None:
        pass

    def init_state(self) -> None:
        raise NotImplementedError

    def validate(self, input_str: str) -> bool:
        raise NotImplementedError

    def finish(self) -> bool:
        raise NotImplementedError


class RegexValidator(Validator):
    def __init__(self, regex: str) -> None:
        super().__init__()
        self.fsm = interegular.parse_pattern(regex).to_fsm()
        print(self.fsm)

        # 显示了fsm的状态转移字典
        # map: Dict[State, Dict[TransitionKey, State]]
        # 这是一个嵌套字典，其中外层字典的键是状态，值是另一个字典。内层字典的键是过渡符号或条件，值是目标状态
        print(self.fsm.map)

        # 显示了每个符号对应的 TransitionKey,
        # 每个符号会映射到一个特定的 TransitionKey， 此TransitionKey 可用于在状态转移字典map中查找对应的目标状态
        print(self.fsm.alphabet)

        # print(self.fsm.initial)
        # print(self.fsm.states)
        # print(self.fsm.finals)
        self.current_state = None

    def init_state(self) -> None:
        if hasattr(self.fsm, 'initial'):
            self.current_state = self.fsm.initial
        else:
            raise AttributeError("FSM 对象没有 initial 属性作为起始状态")

    def validate(self, input_str: str) -> bool:
        print(f"Validating input: {input_str}")
        self.current_state = self.fsm.initial
        for char in input_str:
            # 获取当前字符的 TransitionKey
            # 如果 char 在 self.fsm.alphabet 中，获取其转移键
            if char in self.fsm.alphabet:
                transition_key = self.fsm.alphabet[char]
            # 如果 char 不在字母表中，则使用 anything_else 的转移键
            else:
                # 处理 anything_else 的情况
                transition_key = self.fsm.alphabet.get("anything_else", None)

            # print(transition_key)

            if self.current_state in self.fsm.map and transition_key in self.fsm.map[self.current_state]:
                self.current_state = self.fsm.map[self.current_state][transition_key]
            else:
                print(f"Character '{char}' not in FSM transitions for state {self.current_state}")
                return False
        return self.current_state in self.fsm.finals

    def finish(self) -> bool:
        return self.current_state in self.fsm.finals

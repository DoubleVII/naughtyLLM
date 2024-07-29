
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

        self.current_state = None
        self.last_state = None
        # print(self.fsm.initial)
        # print(self.fsm.finals)
        # print(self.fsm.states)

    def init_state(self) -> None:
        if hasattr(self.fsm, 'initial'):
            self.last_state = self.fsm.initial
        else:
            raise AttributeError("FSM 对象没有 initial 属性作为起始状态")

    def validate(self, input_str: str) -> bool:
        print(f"Validating input: {input_str}")
        # 若上一个test_token 验证不通过，则 self.last_state未更新，即仍为上一个test_token的初始状态
        # 若上一个test_token 验证通过，则 self.last_state更新，即为上一个test_token的最终状态
        self.current_state = self.last_state

        for char in input_str:
            # 获取当前字符的 TransitionKey
            # 如果 char 在 self.fsm.alphabet 中，获取其转移键
            if char in self.fsm.alphabet:
                transition_key = self.fsm.alphabet[char]
            # 如果 char 不在字母表中，则使用 anything_else 的转移键
            else:
                # 处理 anything_else 的情况
                transition_key = self.fsm.alphabet.get("anything_else", None)

            print(f"Current state: {self.current_state}, Character: {char}, Transition key: {transition_key}")

            # 若当前状态是状态转移表中的一个状态；
            # 并且在当前状态下，当前字符在状态转移字典中有定义相应的状态转移，则更新当前状态为转移后的状态
            if self.current_state in self.fsm.map and transition_key in self.fsm.map[self.current_state]:
                self.current_state = self.fsm.map[self.current_state][transition_key]
            # 否则当前状态不接收此字符，本次test_token验证不通过，不更新self.last_state，使之仍为本次test_token的初始状态
            else:
                print(f"Character '{char}' not in FSM transitions for state {self.current_state}")
                return False

        # 本次test_token验证通过，更新self.last_state为本次test_token的最终状态
        self.last_state = self.current_state
        print(f"Final state: {self.current_state}")
        return True

    def finish(self) -> bool:
        return self.current_state in self.fsm.finals



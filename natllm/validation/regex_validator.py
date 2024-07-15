

class Validator:
    def __init__(self) -> None:
        pass

    def init_state(self) -> None:
        raise NotImplementedError

    def validate(self, input_str:str) -> bool:
        raise NotImplementedError

    def finish(self) -> bool: # <eos>
        raise NotImplementedError



class RegexValidator(Validator):
    def __init__(self, regex: str) -> None:
        super().__init__()
        pass

    def init_state(self) -> None:
        pass

    def validate(self, input_str:str) -> bool:
        pass

    def finish(self) -> bool: # <eos>
        pass
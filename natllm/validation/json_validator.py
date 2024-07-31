from number_FSM import number_FSM
from regex_validator import Validator

EOS = '<EOS>' # 指代模型输出的结尾
PlaceHolder = 'General Exception' # 异常占位符

class JsonValidator(Validator):
    ignore_list = [' ', '\t', '\n']

    def __init__(self):
        self.current_str = ""
        self.next_char = None

    def init_state(self):
        self.current_str = ""
        self.next_char = None

    def validate(self, input_str: str) -> bool:
        tmp = self.current_str
        self.current_str = self.current_str + input_str
        if self.__validate_string_either_json(self.current_str):
            return True
        else:
            self.current_str = tmp
            return False
    
    def finish(self) -> bool:
        tmp = self.current_str
        self.current_str = self.current_str + EOS
        if self.__validate_string_either_json(self.current_str):
            return True
        else:
            self.current_str = tmp
            return False
        
    def __set_generator(self, generator_func):
        self.generator = generator_func()

    def __validate_string_either_json(self, str) -> bool:
        self.next_char = None
        self.generator = None

        def inner_generator():
            for char in str:
                yield char
        self.__set_generator(inner_generator)

        try:
            self.__scan()
            self.__read_value()

            if self.next_char != EOS:
                raise Exception("Expecting the End")
        except StopIteration:
            return True
        except Exception as e:
            return False
        
    

    def __scan(self):
        scan_char = next(self.generator)
        if scan_char in JsonValidator.ignore_list:
            self.next_char = self.__scan()
        else:
            self.next_char = scan_char
        return self.next_char
    
    def __read_string(self):
        #读到"之后才开始(此时next_char 为 ")
        while(self.__scan()!='\"'):
            pass
        self.__scan()

    def __read_number(self):
        #读到数字开头(此时next_char 为 任意非0数字或负号)
        fsm = number_FSM()
        last_char_can_accept = False
        while(True):
            new_state = fsm.transition(self.next_char)
            if (new_state == fsm.reject_state):
                if (last_char_can_accept):
                    break
                else:
                    raise Exception(PlaceHolder)
            elif (fsm.is_accepting()):
                last_char_can_accept = True
            self.__scan()

        ##json中数字的正则表达式：-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?


    def __read_object(self):
        self.__scan()
        if self.next_char == '}':
            self.__scan()
            return
        else:
            while True:
                if self.next_char != '\"':
                    raise Exception(PlaceHolder)
                self.__read_string()
                if self.next_char != ':':
                    raise Exception(PlaceHolder)
                self.__scan()
                self.__read_value()
                if self.next_char == ',':
                    self.__scan()
                    continue
                elif self.next_char == '}':
                    break
                else:
                    raise Exception(PlaceHolder)
            self.__scan()
            return

    def __read_array(self):
        self.__scan()
        if self.next_char == ']':
            self.__scan()
            return
        else:
            while True:
                self.__read_value()
                if self.next_char == ',':
                    self.__scan()
                    continue
                elif self.next_char == ']':
                    break
                else:
                    raise Exception(PlaceHolder)
            self.__scan()
            return


    def __read_value(self):
        if self.next_char == 't':
            try:
                assert(self.__scan()=='r')
                assert(self.__scan()=='u')
                assert(self.__scan()=='e')
            except:
                raise Exception(PlaceHolder)
            self.__scan()
        elif self.next_char == 'f':
            try:
                assert(self.__scan()=='a')
                assert(self.__scan()=='l')
                assert(self.__scan()=='s')
                assert(self.__scan()=='e')
            except:
                raise Exception(PlaceHolder)
            self.__scan()
        elif self.next_char == 'n':
            try:
                assert(self.__scan()=='u')
                assert(self.__scan()=='l')
                assert(self.__scan()=='l')
            except:
                raise Exception(PlaceHolder)
            self.__scan()
        elif self.next_char == '\"':
            self.__read_string()
        elif self.next_char.isdigit() or (self.next_char in '-+.eE'):
            self.__read_number()
        elif self.next_char == '{':
            self.__read_object()
        elif self.next_char == '[':
            self.__read_array()
        else:
            raise Exception(PlaceHolder)

    def __read_json(self):
        try:
            assert(self.char_list == [])
            assert(self.next_char == None)
        except:
            raise Exception(PlaceHolder)
        
        self.__scan()
        self.__read_value()

        if self.next_char != EOS:
            raise Exception(PlaceHolder)


        

if __name__ == '__main__':
    j=JsonValidator()
    j.init_state()
    print(j.validate("{}"))
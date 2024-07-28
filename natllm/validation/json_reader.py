import re 
from number_FSM import number_FSM

EOS = '<EOS>' # 指代模型输出的结尾
PlaceHolder = 'General Exception' # 异常占位符，后续异常会替换自定义异常

class JsonReader:
    ignore_list = [' ', '\t', '\n']

    def __init__(self, a_model_that_can_yield_char):
        self.current_char = None
        self.next_char = None
        self.generator = a_model_that_can_yield_char()

    def set_next_char(self, char):
        self.next_char = char

    def clear(self):
        self.current_char = None
        self.next_char = None

    def __scan(self):
        scan_char = next(self.generator)
        if scan_char in JsonReader.ignore_list:
            self.next_char = self.__scan()
        else:
            self.next_char = scan_char
        return self.next_char
    
    def read_string(self):
        #读到"之后才开始(此时next_char 为 ")
        while(self.__scan()!='\"'):
            pass
        self.__scan()

    def read_number(self):
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

        ##json中数字的正则表达式：-?\d+(\.\d+)?([eE][+-]?\d+)?


    def read_object(self):
        self.__scan()
        if self.next_char == '}':
            self.__scan()
            return
        else:
            while True:
                if self.next_char != '\"':
                    raise Exception(PlaceHolder)
                self.read_string()
                if self.next_char != ':':
                    raise Exception(PlaceHolder)
                self.__scan()
                self.read_value()
                if self.next_char == ',':
                    self.__scan()
                    continue
                elif self.next_char == '}':
                    break
                else:
                    raise Exception(PlaceHolder)
            self.__scan()
            return

    def read_array(self):
        self.__scan()
        if self.next_char == ']':
            self.__scan()
            return
        else:
            while True:
                self.read_value()
                if self.next_char == ',':
                    self.__scan()
                    continue
                elif self.next_char == ']':
                    break
                else:
                    raise Exception(PlaceHolder)
            self.__scan()
            return


    def read_value(self):
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
            self.read_string()
        elif self.next_char.isdigit() or (self.next_char in '-+.eE'):
            self.read_number()
        elif self.next_char == '{':
            self.read_object()
        elif self.next_char == '[':
            self.read_array()
        else:
            raise Exception(PlaceHolder)

    def read_json(self):
        try:
            assert(self.char_list == [])
            assert(self.next_char == None)
        except:
            raise Exception(PlaceHolder)
        
        self.__scan()
        self.read_value()

        if self.next_char != EOS:
            raise Exception(PlaceHolder)


        

if __name__ == '__main__':
    from tester import generater
    j = JsonReader(generater)
    j.read_json()
    print('Pass')
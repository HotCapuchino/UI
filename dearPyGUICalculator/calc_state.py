class CalcState:
    def __init__(self) -> None:
        self.__current_expression: str = ''
        self.__error: str = ''
        self.__results: list = []
        self.__buttons = [
            ['7', '8', '9', '/'], 
            ['4', '5', '6', '*'], 
            ['1', '2', '3', '+'], 
            ['0', 'C', '=', '-']
        ]

    def get_current_expression(self):
        return self.__current_expression

    def get_error(self):
        return self.__error

    def get_results(self):
        return self.__results

    def get_buttons(self):
        return self.__buttons

    def update_state(self, current_expression='', error='', result=''):
        self.__current_expression = current_expression
        self.__error = error
        
        if result:
            self.__results.append(result)

            if len(self.__results) == 4:
                self.__results = self.__results[1:]
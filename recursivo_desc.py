from Consts import Consts


class RecDescendente:
    def __init__(self, tokens):
        self.tokens = tokens
        self.id = -1
        self.current = None
        self.txt = ""

    def start(self):
        self.nextToken()
        acertos, erro = self.input_list()
        if self.currentToken().type != Consts.EOF:
            return None, f"Erro: EOF esperado, mas '{self.currentToken().value}' encontrado"
        return acertos, erro

    def nextToken(self):
        self.id += 1
        if self.id < len(self.tokens):
            self.current = self.tokens[self.id]
        return self.current

    def input_list(self):
        if self.currentToken().type in [Consts.KEY, Consts.INT, Consts.FLOAT]:
            acertos, erros = self.comando()
            if erros:
                return None, erros
            return self.input_list()
        return self.txt, None

    def comando(self):
        if self.currentToken().type == Consts.KEY:
            if self.currentToken().value == Consts.LET:
                return self.let_comando()
        elif self.currentToken().type == Consts.INT:
            return self.E()
        elif self.currentToken().type == Consts.FLOAT:
            return self.E()
        
        return None, f"Erro de sintaxe em comando: token inesperado '{self.currentToken().value}'"

    def let_comando(self):    
        regra = "let_comando -> "
        self.nextToken()
        if self.currentToken().type == Consts.ID:
            regra += "ID "
            self.nextToken()
            if self.currentToken().type == Consts.EQ:
                regra += "= expr"
                self.nextToken()
                acertos, erros = self.E()    
                self.txt += f"\n{regra} -> {acertos}"
                return acertos, erros
        return None, "Erro em let_comando: esperado 'ID = expressão'"

    def E(self):
        if self.currentToken().type == Consts.INT or self.currentToken().type == Consts.FLOAT:
            self.txt += "i"
            self.nextToken()
            acertos, erros = self.K()
            return acertos, erros
        return None, "falha E(), precisa iniciar com inteiro"
    
    def K(self):
        if self.currentToken().type == Consts.PLUS:
            self.nextToken()
            
            if self.currentToken().type == Consts.INT or self.currentToken().type == Consts.FLOAT:
                self.nextToken()
                self.txt += "+i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após + não é numérico"
            
        if self.currentToken().type == Consts.MINUS:
            self.nextToken()
            
            if self.currentToken().type == Consts.INT or self.currentToken().type == Consts.FLOAT:
                self.nextToken()
                self.txt += "-i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após - não é numérico"
            
        if self.currentToken().type == Consts.DIV:
            self.nextToken()
            
            if self.currentToken().type == Consts.INT or self.currentToken().type == Consts.FLOAT:
                self.nextToken()
                self.txt += "/i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após / não é numérico"
            
        if self.currentToken().type == Consts.MUL:
            self.nextToken()
            
            if self.currentToken().type == Consts.INT or self.currentToken().type == Consts.FLOAT:
                self.nextToken()
                self.txt += "*i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após * não é numérico"
            
        if self.currentToken().type == Consts.POW:
            self.nextToken()
            
            if self.currentToken().type == Consts.INT or self.currentToken().type == Consts.FLOAT:
                self.nextToken()
                self.txt += "^i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após ^ não é numérico"
            
        self.txt += "e"
        return self.txt, None

    def currentToken(self):
        return self.current

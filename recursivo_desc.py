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
        if self.currentTok().type != Consts.EOF:
            return None, f"Erro: EOF esperado, mas '{self.currentTok().value}' encontrado"
        return acertos, erro

    def nextToken(self):
        self.id += 1
        if self.id < len(self.tokens):
            self.current = self.tokens[self.id]
        return self.current

    def input_list(self):
        if self.currentTok().type in [Consts.KEY, Consts.INT]:
            acertos, erros = self.comando()
            if erros:
                return None, erros
            return self.input_list()
        return self.txt, None

    def comando(self):
        if self.currentTok().type == Consts.KEY:
            if self.currentTok().value == Consts.LET:
                return self.let_comando()
        elif self.currentTok().type == Consts.INT:
            return self.E()
        return None, f"Erro de sintaxe em comando: token inesperado '{self.currentTok().value}'"

    def let_comando(self):    
        regra = "let_comando -> "
        self.nextToken()
        if self.currentTok().type == Consts.ID:
            regra += "ID "
            self.nextToken()
            if self.currentTok().type == Consts.EQ:
                regra += "= expr"
                self.nextToken()
                acertos, erros = self.E()    
                self.txt += f"\n{regra} -> {acertos}"
                return acertos, erros
        return None, "Erro em let_comando: esperado 'ID = expressão'"

    def E(self):
        if self.currentTok().type == Consts.INT:
            self.txt += "i"
            self.nextToken()
            acertos, erros = self.K()
            return acertos, erros
        return None, "falha E(), precisa iniciar com inteiro"
    
    def K(self):
        if self.currentTok().type == Consts.PLUS:
            self.nextToken()
            
            if self.currentTok().type == Consts.INT:
                self.nextToken()
                self.txt += "+i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após + não é numérico"
            
        if self.currentTok().type == Consts.MINUS:
            self.nextToken()
            
            if self.currentTok().type == Consts.INT or self.currentTok().type == Consts.FLOAT:
                self.nextToken()
                self.txt += "-i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após - não é numérico"
            
        if self.currentTok().type == Consts.DIV:
            self.nextToken()
            
            if self.currentTok().type == Consts.INT or self.currentTok().type == Consts.FLOAT:
                self.nextToken()
                self.txt += "/i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após / não é numérico"
            
        if self.currentTok().type == Consts.MUL:
            self.nextToken()
            
            if self.currentTok().type == Consts.INT or self.currentTok().type == Consts.FLOAT:
                self.nextToken()
                self.txt += "*i"
                acertos, erros = self.K()
                return self.txt, erros
            
            else:
                return self.txt, "caractere após * não é numérico"
            
        self.txt += "e"
        return self.txt, None

    def currentTok(self):
        return self.current

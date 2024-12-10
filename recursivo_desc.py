from Consts import Consts


class RecDescendente:
    def __init__(self, tokens):
        self.tokens = tokens
        self.id = -1
        self.current = None
        self.txt = ""

    def start(self):
        self.nextToken()
        acertos, erro = self.comando_list()
        if self.currentTok().type != Consts.EOF:
            return None, f"Erro: EOF esperado, mas '{self.currentTok().value}' encontrado"
        return acertos, erro

    def nextToken(self):
        self.id += 1
        if self.id < len(self.tokens):
            self.current = self.tokens[self.id]
        return self.current

    def comando_list(self):
        if self.currentTok().type in [Consts.KEY, Consts.INT]:
            acertos, erros = self.comando()
            if erros:
                return None, erros
            return self.comando_list()
        return self.txt, None

    def comando(self):
        if self.currentTok().type == Consts.KEY:
            if self.currentTok().value == Consts.LET:
                return self.let_comando()
            elif self.currentTok().value == Consts.IF:
                return self.if_comando()
            elif self.currentTok().value == Consts.WHILE:
                return self.while_comando()
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

    def if_comando(self):
        regra = "if_comando -> "
        self.nextToken()
        if self.currentTok().type == Consts.LPAR:
            regra += "( expr ) comando"
            self.nextToken()
            acertos, erros = self.E()
            if erros:
                return None, erros
            if self.currentTok().type == Consts.RPAR:
                self.nextToken()
                self.txt += f"\n{regra} -> ({acertos}) "
                return self.comando()
        return None, "Erro em if_comando: esperado '(condição) comando'"

    def while_comando(self):
        regra = "while_comando -> "
        self.nextToken()
        if self.currentTok().type == Consts.LPAR:
            regra += "( expr ) comando"
            self.nextToken()
            acertos, erros = self.E()
            if erros:
                return None, erros
            if self.currentTok().type == Consts.RPAR:
                self.nextToken()
                self.txt += f"\n{regra} -> ({acertos})"
                return self.comando()
        return None, "Erro em while_comando: esperado '(condição) comando'"

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
            
        self.txt += "e"
        return self.txt, None

    def currentTok(self):
        return self.current

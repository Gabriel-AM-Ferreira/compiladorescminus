from sys import exit
from constants import *
from node import *
from bnfType import *


SEQUENCIA_DECLARACAO = [Constants.PONTO_VIRGULA, Constants.ID, Constants.PARENTESE_ABRE, Constants.NUM]
SEQUENCIA_STATEMENT = [Constants.PONTO_VIRGULA, Constants.ID, Constants.PARENTESE_ABRE, Constants.NUM, 
  Constants.RETURN, Constants.CHAVE_ABRE, Constants.IF, Constants.WHILE]

class Parser:
  def __init__(self, tokens):
    self.tokens = [token for token in tokens if token.token_type != Constants.COMENTARIO]
    self.token_index = 0
    self.token_atual = self.tokens[self.token_index]
    self.ids_declarados = []
    self.houve_erro = False
    self.len_tokens = len(self.tokens)

    
  def avancaToken(self):
    print(f"{self.token_atual} avancaToken")
    novo_index = self.token_index + 1
    self.token_index = novo_index
    if self.token_index < self.len_tokens:
      self.token_atual = self.tokens[novo_index]

  def validaToken(self, *token_tipo_esperado):
    print(f"{self.token_atual} validaToken")
    print("Token Atual", self.token_atual)
    if self.token_atual.token_type in token_tipo_esperado:
      if self.token_atual.token_type == Constants.ID:
        self.ids_declarados.append(self.token_atual.value)
      token = self.token_atual
      self.avancaToken()

      return token
    else:
      self.erroValidacao(token_tipo_esperado, self.token_atual)


  def erroValidacao(self, tipo_esperado, token_atual):
    print("Houve um problema na linha {} na posicao {}: Deveria ter um {} no lugar de {}.".format(token_atual.line, token_atual.pos, tipo_esperado, token_atual.token_type))
    self.houve_erro = True
    exit(1)

  def erroDuplicado(self, token_atual):
    print("Houve um problema na linha {} na posicao {}: {} não pode ser declarado novamente.".format(token_atual.line, token_atual.pos, token_atual.value))
    self.houve_erro = True
    exit(1)
  
  def verificaDeclaracao(self, token):
    return token.value in self.ids_declarados
  
  def programa(self):
    print()
    no = Node(None, BNFType.PROGRAMA)
    no.add(self.declaracaoLista())
    
    return no

  def declaracaoLista(self):
    no = Node(None, BNFType.DECLARACAO_LISTA)
    no.add(self.declaracao())
    
    while self.token_atual.token_type == Constants.INT or self.token_atual.token_type == Constants.VOID:
      no.add(self.declaracao())
      
    if not self.houve_erro:
      print("Compilado com sucesso!")

    return no

  def declaracao(self):
    no = Node(self.tokens[self.token_index+1], self.token_atual.token_type)
    self.validaToken(Constants.INT, Constants.VOID)
    no_id = Node(self.tokens[self.token_index+1], Constants.ID)
    self.validaToken(Constants.ID)
    no.add(no_id)

    if self.token_atual.token_type == Constants.PARENTESE_ABRE: 
      no.token_type = BNFType.FUN_DECLARACAO
      self.funDeclaracao(no)
    else: 
      no.token_type = BNFType.VAR_DECLARACAO
      self.varDeclaracao(no_id)
      
    return no

  def varDeclaracao(self, no):
    if self.token_atual.token_type == Constants.COLCHETE_ABRE:
      self.validaToken(Constants.COLCHETE_ABRE)
      self.validaToken(Constants.NUM)
      self.validaToken(Constants.COLCHETE_FECHA)
    self.validaToken(Constants.PONTO_VIRGULA)
    
    if self.verificaDeclaracao(no.token):
      self.erroDuplicado(no.token)
    return no

  def tipoEspecificador(self):
    no = Node(self.token_atual, BNFType.TIPO_ESPECIFICADOR)
    self.validaToken(self.token_atual.token_type)
    return no

  def funDeclaracao(self, no):
    self.validaToken(Constants.PARENTESE_ABRE)
    no_aux = self.params()

    params = []
    for param in no_aux.filhos:
      params.append(param.filhos[1].token)

    self.validaToken(Constants.PARENTESE_FECHA)
    no.add(no_aux)
    no.add(self.compostoDecl())
    return no

  def params(self):
    no = Node(None, BNFType.PARAMS)
    
    if self.token_atual.token_type == Constants.VOID:
      self.validaToken(Constants.VOID)
    else:
      no.filhos += self.paramLista()
    
    return no

  def paramLista(self):
    no = self.param()
    params = []
    params.append(no)
    
    while self.token_atual.token_type == Constants.VIRGULA:
      self.validaToken(Constants.VIRGULA)
      no_temp = self.param()
      params.append(no_temp)

    return params

  def param(self):
    no = Node()
    no.add(self.tipoEspecificador())

    no_id = Node(self.tokens[self.token_index+1], Constants.ID)
    self.validaToken(Constants.ID)
    no.add(no_id)
    no.token = self.tokens[self.token_index+1]
    
    if self.token_atual.token_type == Constants.COLCHETE_ABRE:
      self.validaToken(Constants.COLCHETE_ABRE)
      self.validaToken(Constants.COLCHETE_FECHA)
    no.token_type = BNFType.PARAM
    
    return no

  def compostoDecl(self):
    no = Node(None, BNFType.COMPOSTO_DECL)
    self.validaToken(Constants.CHAVE_ABRE)
    no.filhos += self.localDeclaracoes()
    no.filhos += self.statementLista()
    self.validaToken(Constants.CHAVE_FECHA)
    
    return no

  def localDeclaracoes(self):
    delclaracoes = []

    while self.token_atual.token_type == Constants.INT or self.token_atual.token_type == Constants.VOID:
      no = Node(None, BNFType.VAR_DECLARACAO)
      no.add(self.tipoEspecificador())

      no_id = Node(self.tokens[self.token_index+1], Constants.ID)
      self.validaToken(Constants.ID)
      no.add(no_id)
      
      if self.verificaDeclaracao(no_id.token):
        self.erroDuplicado(no_id.token)
      
      if self.token_atual.token_type == Constants.COLCHETE_ABRE:
        self.validaToken(Constants.COLCHETE_ABRE)
        self.validaToken(Constants.NUM)
        self.validaToken(Constants.COLCHETE_FECHA)

      self.validaToken(Constants.PONTO_VIRGULA)
      delclaracoes.append(no)

    return delclaracoes

  def statementLista(self):
    statements = []
    while (self.token_atual.token_type in SEQUENCIA_STATEMENT):
      statements.append(self.statement())
    
    return statements

  def statement(self):
    if self.token_atual.token_type == Constants.RETURN:
      return self.retornoDecl()
    elif self.token_atual.token_type == Constants.CHAVE_ABRE:
      return self.compostoDecl()
    elif self.token_atual.token_type == Constants.IF:
      return self.selecaoDecl()
    elif self.token_atual.token_type == Constants.WHILE:
      return self.iteracaoDecl()
    else:
      return self.expressaoDecl()

  def expressaoDecl(self):
    no = Node(None, BNFType.EXPRESSAO_DECL)
    
    if (self.token_atual.token_type in SEQUENCIA_DECLARACAO):
      no.add(self.expressao())
    self.validaToken(Constants.PONTO_VIRGULA)
    
    return no

  def selecaoDecl(self):
    no = Node(None, BNFType.SELECAO_DECL)
    self.validaToken(Constants.IF)
    self.validaToken(Constants.PARENTESE_ABRE)
    no.add(self.expressao())
    self.validaToken(Constants.PARENTESE_FECHA)
    no.add(self.statement())
    
    if self.token_atual.token_type == Constants.ELSE:
      self.validaToken(Constants.ELSE)
      no.add(self.statement())
    
    return no

  def iteracaoDecl(self):
    no = Node(None, BNFType.ITERACAO_DECL)
    self.validaToken(Constants.WHILE)
    self.validaToken(Constants.PARENTESE_ABRE)
    no.add(self.expressao())
    self.validaToken(Constants.PARENTESE_FECHA)
    no.add(self.statement())
    
    return no

  def retornoDecl(self):
    no = Node(None, BNFType.RETORNO_DECL)
    self.validaToken(Constants.RETURN)
    
    if (self.token_atual.token_type in SEQUENCIA_DECLARACAO):
      no.add(self.expressao())
    self.validaToken(Constants.PONTO_VIRGULA)
    
    return no

  def expressao(self):
    no = Node(None, BNFType.EXPRESSAO)
    no_aux = no

    while self.token_atual.token_type == Constants.ID:
      no_temp = Node(self.tokens[self.token_index+1])
      self.validaToken(Constants.ID)
      
      if self.token_atual.token_type == Constants.COLCHETE_ABRE:
        self.validaToken(Constants.COLCHETE_ABRE)
        no_temp.add(self.expressao())
        self.validaToken(Constants.COLCHETE_FECHA)

        if self.token_atual.token_type == Constants.ATRIBUI:
          self.validaToken(Constants.ATRIBUI)
      else:
        if self.token_atual.token_type == Constants.ATRIBUI:
          self.validaToken(Constants.ATRIBUI)
        else:
          break

      no_temp.token_type = Constants.ATRIBUI
      no_aux.add(no_temp)
      no_aux = no_temp
    
    no_aux.add(self.simplesExpressao())
    return no

  def var(self, no):
    if self.token_atual.token_type == Constants.COLCHETE_ABRE:
      self.validaToken(Constants.COLCHETE_ABRE)
      no.add(self.expressao())
      self.validaToken(Constants.COLCHETE_FECHA)

  def simplesExpressao(self):
    no = Node(None, BNFType.SIMPLES_EXPRESSAO)
    no.add(self.somaExpressao())

    if (self.token_atual.token_type in list(OPERADORES.values())):
      no.add(self.relacional())
      no.add(self.somaExpressao())

    return no

  def relacional(self):
    no = Node(self.token_atual, BNFType.RELACIONAL)
    self.validaToken(self.token_atual.token_type)

    return no

  def somaExpressao(self):
    no = Node(None, BNFType.SOMA_EXPRESSAO)
    no.add(self.termo())
    
    if self.token_atual.token_type == Constants.MAIS or self.token_atual.token_type == Constants.MENOS:
      no.add(self.soma())
      no.add(self.termo())

    return no

  def soma(self):
    no = Node(self.token_atual, BNFType.SOMA)
    self.validaToken(self.token_atual.token_type)

    return no

  def termo(self):
    no = Node(None, BNFType.TERMO)
    no.add(self.fator())

    while self.token_atual.token_type == Constants.MULT or self.token_atual.token_type == Constants.DIV:
      no.add(self.mult())
      no.add(self.fator())

    return no 

  def mult(self):
    no = Node(self.token_atual, BNFType.MULT)
    self.validaToken(self.token_atual.token_type)

    return no

  def fator(self):
    no = Node(None, BNFType.FATOR)
    
    if self.token_atual.token_type == Constants.ID:
      no_aux = Node(self.tokens[self.token_index+1])
      self.validaToken(Constants.ID)
      
      if self.token_atual.token_type == Constants.PARENTESE_ABRE:
        no_aux.token_type = BNFType.ATIVACAO
        self.ativacao(no_aux)
      else:
        no_aux.token_type = BNFType.VAR
        self.var(no_aux)
      no.add(no_aux)
    elif self.token_atual.token_type == Constants.PARENTESE_ABRE:
      self.validaToken(Constants.PARENTESE_ABRE)
      no.add(self.expressao())
      self.validaToken(Constants.PARENTESE_FECHA)
    elif self.token_atual.token_type == Constants.NUM:
      no.add(Node(self.tokens[self.token_index+1], Constants.NUM))
      self.validaToken(Constants.NUM)

    return no

  def ativacao(self, no):
    self.validaToken(Constants.PARENTESE_ABRE)
    no.add(self.args())
    self.validaToken(Constants.PARENTESE_FECHA)

  def args(self):
    no = Node(None, BNFType.ARGS)
    no.add(self.expressao())
    
    if self.token_atual.token_type == Constants.VIRGULA:
      self.validaToken(Constants.VIRGULA)
      no.add(self.args())

    return no
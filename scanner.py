from string import ascii_letters as letters
from constants import *

class Scanner:
  def __init__(self, scanned_file):
    self.scanned_file = scanned_file
    self.lines_in_file = sum(1 for line in scanned_file)
    self.tokens = []
    #Linha a ser Scaneada
    self.current_line = scanned_file[0].strip()
    # Ponteiro que indica o que esta sendo analisado 
    self.scanner_pointer = -1
    # Posicao de linha do Scanner
    self.scanned_line = 0


  def nextLine(self):
    try:
      self.scanned_line = self.scanned_line+1
      self.current_line = self.scanned_file[self.scanned_line].strip()
      #print(repr(self.current_line))
      # Reseta o ponteiro do Scanner para primeira pos da Linha
      self.scanner_pointer = 0

      return self.current_line[self.scanner_pointer]
     # Except é usado para burlar o problema que teremos ao tentar acessar o arquivo fora de seu tamanho em linha
    except:
      return "EOF"

  def nextColumn(self):
    try:
      self.scanner_pointer = self.scanner_pointer+1
      return self.current_line[self.scanner_pointer]
    except:
      return self.nextLine()

  def goBack(self):
     self.scanner_pointer = self.scanner_pointer -1

  def scanInt(self,value):
    pointer = self.nextColumn()
    while pointer.isnumeric():
      value = value + str(pointer)
      pointer = self.nextColumn()

    self.goBack()
    return value

  def scanId(self,value):
    pointer = self.nextColumn()
    while pointer in letters:
      value = value + str(pointer)
      pointer = self.nextColumn()
      if pointer.isnumeric():
        ErrorMessage.erroDeNumericoNoID(self.scanned_line+1,self.scanner_pointer+1)
        exit(1)

    self.goBack()
    return value 

  def scanComment(self,value):
    pointer = self.nextColumn()
    while value[-2:] != '*/':
      value = value + pointer
      pointer = self.nextColumn()
    self.goBack()
    return value

  def judgeToken(self):
    pointer = self.nextColumn()
    #print(f"pointer: {repr(pointer)}")
    if pointer in {' ','\n', '\t',None,'EOF'}:
      #print(f"pointer: {repr(pointer)}")
      return None
    token_type = None
    token_value = pointer

    if pointer == '>':
      pointer = self.nextColumn()
      if pointer == '=':
        token_value += pointer
        token_type = Constants.MAIOR_IGUAL
      else:
        self.goBack()
        token_type = Constants.MAIOR
    elif pointer == '<':
      pointer = self.nextColumn()
      if pointer == '=' :
        token_value += pointer
        token_type = Constants.MENOR_IGUAL
      else:
        self.goBack()
        token_type = Constants.MENOR
    elif pointer == '=':
      pointer = self.nextColumn()
      if pointer == '=' :
        token_value += pointer
        token_type = Constants.IGUAL
      else:
        self.goBack()
        token_type = Constants.ATRIBUI
    elif pointer == '!':
      if pointer == '=' :
        token_value += pointer
        token_type = Constants.DIF
      else:
        self.goBack()
        token_type = Constants.ERROR
        ErrorMessage.erroDeTokenInvalidoPosExclamacao()
    elif pointer == '/':
      token_type = Constants.DIV
      pointer = self.nextColumn()
      if pointer == '*':
        token_type = Constants.COMENTARIO
        token_value = self.scanComment(token_value+pointer)
      else:
        self.goBack()
    # elif pointer == 'EOF':
    #   token_type = Constants.EOF
    elif pointer == '*':
      token_type = Constants.MULT
    elif pointer == '(':
      token_type = Constants.PARENTESE_ABRE
    elif pointer == ')':
      token_type = Constants.PARENTESE_FECHA
    elif pointer == '{':
      token_type = Constants.CHAVE_ABRE
    elif pointer == '}' :
      token_type = Constants.CHAVE_FECHA
    elif pointer == '[':
      token_type = Constants.COLCHETE_ABRE
    elif pointer == ']':
      token_type = Constants.COLCHETE_FECHA
    elif pointer == '+':
      token_type = Constants.MAIS
    elif pointer == '-':
      token_type = Constants.MENOS
    elif pointer == ';':
      token_type = Constants.PONTO_VIRGULA
    elif pointer == ',':
      token_type = Constants.VIRGULA
    elif pointer.isnumeric():
      token_type = Constants.NUM
      token_value = self.scanInt(pointer)
    elif pointer in letters:
        token_type = Constants.ID
        token_value = self.scanId(pointer)
        if token_value in list(PALAVRAS_RESERVADAS.keys()):
            token_type = PALAVRAS_RESERVADAS[token_value]

    return Token(token_value, token_type, self.scanned_line, self.scanner_pointer)

  def scanAllTokens(self):
    while self.scanned_line < self.lines_in_file:
        token = self.judgeToken()
        # print(token)
        
        if token is not None:
            self.tokens.append(token)
    return self.tokens
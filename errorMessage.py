class ErrorMessage:
  
  def erroDeNumericoNoID(line,column):
    print(f"Na linha {line} e coluna {column} foi detectado um numérico no meio de um ID")
    
  def erroDeTokenInvalidoPosExclamacao():
    print("Token invalido recebido depois de uma exclamacao!")
class Token:
  def __init__(self,value,token_type,line,pos):
    self.value = value
    self.token_type = token_type
    self.line = line+1
    self.pos = pos

  def __str__(self):
    return f"{self.value}: {self.token_type} \n"
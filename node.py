class Node:
  def __init__(self, token = None, token_type = None, filhos = None):
    if filhos is None:
        filhos = []
    self.token = token
    self.token_type = token_type
    self.filhos = filhos
  
  def __repr__(self): 
    return "{}: {} - Filhos {} \n".format(self.token, self.token_type, len(self.filhos))

  def __str__(self):
    return "{}: {} - Filhos {} \n".format(self.token, self.token_type, len(self.filhos))

  def add(self, value):
    self.filhos.append(value)
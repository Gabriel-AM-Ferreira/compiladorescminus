from scanner import Scanner
from parser_1 import Parser
import sys

def leArquivo(nome):
  try:
    with open(nome, 'r') as arquivo:
      resultado = arquivo.readlines()
      # for linha in resultado:
      #   print(repr(linha))
    return resultado
  except FileNotFoundError:
    raise FileNotFoundError('Arquivo não encontrado.')

nome_arquivo = '/content/sort.txt'

programa = leArquivo(nome_arquivo)
tokens = Scanner(programa).scanAllTokens()
#print("Tokens", tokens)
print("Numero de tokens: {}".format(len(tokens)))
parser = Parser(tokens)
parser.programa()
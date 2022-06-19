#Funciones auxiliares

def ListToInt(lista):
  '''
  Dada una lista A de str, retorna el numero representado por la lista \n 
  A = ['1','.','4','5','6'] \n
  number = 1.456
  '''  
  number = 0
  temp = ""

  for i in lista:
    if i == ',' or i == ' ':
      continue
    temp += i

  number = float(temp)
  return number

def txtToList(text):
    '''
    Dada un texto A, crea una lista con cada elemento separado por una coma.\n 
    text = Hola mundo, este es un test, saludos. \n
    list = [Hola mundo, este es un test, saludos.]
    '''
    list = []
    with open(text) as text:
      for line in text:
        current = []
        temp = ""
        for char in line:

          if char == ',':
            temp = ListToInt(current)
            current_x = temp
            temp = ""
            current = []

          if char == line[-1]:

            current += [char]
            temp = ListToInt(current)
            current_y = temp

          else:
            current += [char]
     
        list += [current_x,current_y]

    return list
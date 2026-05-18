import json

#Nomalize to have no accent
def normalize(text):
  text=text.strip().lower() #remove space at biginnig and end + minuscule 
  accents={
    'à':'a','â':'a','á':'a',
    'é':'e','è':'e','ê':'e','ë':'e',
    'î':'i','ï':'i','ì':'i','í':'i',
    'ô': 'o', 'ö': 'o', 'ó': 'o',
    'ù': 'u', 'û': 'u', 'ú': 'u', 'ü': 'u',
    'ç': 'c', 'ñ': 'n'
  }
  return "".join(accents.get(c,c) for c in text #parcours the text and replace it with the version without accent
  #without join, we would have a listé

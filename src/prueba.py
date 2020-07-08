import json
data = {'hello':None}
# Save
print('Guardando Archivo General')
with open('./data/data_prueba.json', 'w') as fp:
    json.dump(data, fp)
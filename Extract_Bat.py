# %%
import json
import os

# %%
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--nb_path", type=str, default='')
arg = parser.parse_args()
root = arg.nb_path
# root = ''



def walk_to_depth(dir_path, max_depth):
    dir_path = os.path.realpath(dir_path)
    level = dir_path.count(os.sep)

    for root, dirs, files in os.walk(dir_path):
        yield root, dirs, files
        current_depth = root.count(os.sep) - level
        if current_depth >= max_depth:
            del dirs[:]


path = os.path.join('.',root)

ipynb_list = []


for root, dirs, files in walk_to_depth(path, 0):

    for file in files:

        if file.endswith('.ipynb') and 'empty' not in file:
            ipynb_list.append(os.path.join(root, file))
            print(os.path.join(root, file))
# %%
for notebook in ipynb_list:
    notebook = notebook.split('.ipynb')[0]
    # print(notebook)
    if not os.path.exists(notebook):
        os.mkdir(notebook)
    nbname = os.path.split(notebook)[-1]

    path = os.path.join(notebook, 'Extracted_{}.ipynb'.format(nbname))
    # print(path)

    with open(notebook + '.ipynb') as f:
        data = json.load(f)

    with open('empty.ipynb') as f:
        empty = json.load(f)

# mdcell = empty['cells'][0]
# codecell = empty['cells'][1]

    newnb = data.copy()
    newnb['cells'] = []


    for i in range(len(data['cells'])):
        if data['cells'][i]['cell_type'] == 'markdown':
            md_list = []
            py_list = []
            count = 0
            while count < len(data['cells'][i]['source']): 
                if '```python' not in data['cells'][i]['source'][count] and '```' not in data['cells'][i]['source'][count]:
                    md_list.append(data['cells'][i]['source'][count])
                else:
                    mdcell = empty['cells'][0].copy()
                    mdcell['source'] = md_list

                    newnb['cells'].append(mdcell)
                
                    md_list = []
                    count+=1
                    while '```' not in data['cells'][i]['source'][count]:
                        py_list.append(data['cells'][i]['source'][count])
                        count+=1
                    codecell = empty['cells'][1].copy()
                    codecell['source'] = py_list
                    newnb['cells'].append(codecell)
                    py_list = []

                count+=1
            if len(md_list) > 0:
                mdcell = empty['cells'][0].copy()
                mdcell['source'] = md_list
                newnb['cells'].append(mdcell)
                # print(newnb['cells'][-1]['source'])

        elif data['cells'][i]['cell_type'] == 'code':
            newnb['cells'].append(data['cells'][i])
        else:
            print('error')

    with open(path, 'w') as new_file:
        json.dump(newnb, new_file)




# %%

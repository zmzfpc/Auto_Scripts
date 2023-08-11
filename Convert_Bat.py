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
    if not os.path.exists(notebook):
        os.mkdir(notebook)

    nbname = os.path.split(notebook)[-1]
    path_md = os.path.join(notebook,'Description_{}.md'.format(nbname))
    path_sh = os.path.join(notebook,'Html_{}.ipynb'.format(nbname))
    path_srs = os.path.join(notebook,'Run_Solution_{}.ipynb'.format(nbname))

    with open(notebook + '.ipynb') as f:
        data = json.load(f)




    with open(path_md, 'w') as md_file:

        for i in range(len(data['cells'])):
            strings = ''
            for string in data['cells'][i]['source']:
                strings+=string.lower() 
            if 'load data' not in strings:       
                markdown = ''.join(data['cells'][i]['source'])
                md_file.write(markdown + '\n')
            else:
                break



    SH_Cell = []
    SRS_Cell = []
    d = {}
    i = 0
    while i < len(data['cells']):
    

        if data['cells'][i]['cell_type'] == 'markdown':
            strings = ''
            for string in data['cells'][i]['source']:
                strings+=string.lower() 

            if 'solution:' not in strings and 'question' not in strings:
                SRS_Cell.append(data['cells'][i])
                if 'load data' in strings:
                    SH_Cell.append(data['cells'][i])
                # SRS_Cell.append(data['cells'][i])
                    while i+1 < len(data['cells']) and data['cells'][i+1]['cell_type'] == 'code':
                        SH_Cell.append(data['cells'][i+1])
                        SRS_Cell.append(data['cells'][i+1])
                        i+=1
            elif 'solution' in strings:
                title = data['cells'][i]['source'][0].lower()
                title = title.split('q')[1].split('.')[0]
                if title not in d:
                    SH_Cell.append(data['cells'][i])
                    if i+1 < len(data['cells']):
                    
                        strings = ''
                        for string in data['cells'][i+1]['source']:
                            strings+=string.lower() 
                    # print(strings)
                    while i+1 < len(data['cells']) and (data['cells'][i+1]['cell_type'] == 'code' or 'solution' not in strings):
                        SH_Cell.append(data['cells'][i+1])
                        # print(data['cells'][i+1]['source'])
                        i+=1
                        if i+1 < len(data['cells']):
                            strings = ''
                            for string in data['cells'][i+1]['source']:
                                strings+=string.lower() 
                    d[title] = True
                else:
                    SRS_Cell.append(data['cells'][i])
                    if i+1 < len(data['cells']):
                        strings = ''
                        for string in data['cells'][i+1]['source']:
                            strings+=string.lower() 
                    while i+1 < len(data['cells']) and (data['cells'][i+1]['cell_type'] == 'code' or 'solution' in strings):
                        SRS_Cell.append(data['cells'][i+1])
                        i+=1 
                        if i+1 < len(data['cells']):
                            strings = ''
                            for string in data['cells'][i+1]['source']:
                                strings+=string.lower() 
        i+=1
    

    with open(path_sh, 'w') as code_file, open(path_srs, 'w') as md_file:
        sh = data.copy()
        srs = data.copy()
        sh['cells'] = SH_Cell
        srs['cells'] = SRS_Cell
        json.dump(sh, code_file)
        json.dump(srs, md_file)

# %%


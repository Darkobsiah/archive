import os
import re
import natsort

path = './countries/ir/2308/'

output_file = f'{path}/integrated.txt'
output_file_final = f'{path}/final.txt'

def get_all_paths(path):
    all_files = []
    all_dirs = []

    for dir_name, dir_names, file_names in os.walk(path, topdown=False):
        for file_name in file_names:
            all_files.append(os.path.join(dir_name, file_name))
        all_dirs.append(dir_name)

    return all_files, all_dirs

def merge_files(all_files, output_file):
    with open(output_file, 'a') as fout:
        for file in all_files:
            if file.endswith(".txt"):
                with open(file) as fin:
                    fout.write(fin.read())

all_files, all_dirs = get_all_paths(path)
merge_files(all_files, output_file)

with open(output_file) as f:
    lines = f.readlines()

keys = []
for line in lines:
    match = re.search(r'@([^:]+):\s*(\S+)', line)
    if match:
        key = match.group(1)
    else:
        key = ''
    keys.append(key)

sorted_lines = [lines[keys.index(key)] for key in natsort.natsorted(keys)]

duplicates = []
seen = set()
regex = r'[@][^?]*[?]'

for line in sorted_lines:
    match = re.search(regex, line)
    if match:
        val = match.group()
        if val in seen:
            duplicates.append(line)
        else:
            seen.add(val)

deduped_lines = []
for line in sorted_lines:
    if line not in deduped_lines:
        deduped_lines.append(line)


final_lines = []
for line in deduped_lines:
    protocols = ['vless://', 'trojan://', 'vmess://', 'ss://', 'ssr://']
    for protocol in protocols:
        regex = re.compile(f"^{protocol}(.*)")
        match = regex.match(line)
        if match:
            link = match.group(1)
            final_lines.append(protocol + link)


with open(output_file_final, 'w') as outfile:
    for line in final_lines:
        outfile.write(line + '\n')
    print("Server cleanup completed... !"+"\n")

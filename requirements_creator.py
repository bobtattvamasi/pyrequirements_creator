import glob
import os
import sys

project_folder = sys.argv[1]
print(project_folder)

listdir = [dI for dI in os.listdir(project_folder) if os.path.isdir(os.path.join(project_folder,dI))]

listdir = [os.path.join(project_folder, dI) for dI in listdir]
listdir.append(project_folder)

pyfiles = []


def findPyFiles(folder_name):
	for file in glob.glob(f"{folder_name}/*.py"):
		pyfiles.append(file)

for dl in listdir:
	fl = findPyFiles(dl)
	if fl is not None:
		for pyFile in fl:
			pyfiles.append()


imports = []

for pyfile in pyfiles:
	with open(pyfile, 'r') as f:
		lines = f.read().split("\n")

	for i,line in enumerate(lines):
		if 'import' in line:
			imports.append(line.split(' ')[1])

#for _import_ in imports:
imports = set(imports)

copy_imports = imports.copy()
for _import_ in imports:
	if _import_ == 'cv2':
		copy_imports.remove('cv2')
		copy_imports.add('opencv-python')
	# if _import_ == 'cv2,':
	# 	copy_imports.remove('cv2,')
	if _import_ == 'from':
		copy_imports.remove('from')
	if ',' in _import_:
		word = _import_.split(',')[0]
		copy_imports.remove(_import_)
		copy_imports.add(word)

imports = copy_imports.copy()

for im in copy_imports:
	if '.' in im:
		words = im.split('.')
		if words[0] in listdir or words[1] in listdir:
			imports.remove(im)
			continue
		imports.remove(im)
		imports.add(words[0])


print(imports)
print(pyfiles)
print(listdir)


with open(f"{project_folder}/requirements.txt", 'w') as f:
	for im in imports:
		f.write(im+'\n')


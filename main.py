import zipfile
import xml.etree.ElementTree as ET   

file_path = '/home/anp/lhc/examples/resources/pg8438-images-3.epub'
file_name = file_path.split('/')[-1]
temp_path = './.' + file_name 
container_path = temp_path + '/META-INF/container.xml'

with zipfile.ZipFile(file_path, 'r') as archive:
    archive.extractall(temp_path)

tree = ET.parse(container_path)
root = tree.getroot()

if not (len(root) == 1 and len(root[0]) == 1):
    raise NotImplementedError('Unable to parse EPUB file, multiple roofiles present')

opf_rel_path = root[0][0].attrib['full-path']

opf_path = temp_path + '/' + opf_rel_path

tree = ET.parse(opf_path)
root = tree.getroot()

# root must have atleast 3 children: metadata, manifest, spine 
# metadata is not relevant to us 
# mainfest is a listing of all the files used in the publication 
# spine is going to be used to build the table of contents 

xmlns = 'package'.join(root.tag.split('package')[:-1]) 

data = {} 
idref_to_file = {} 

for child in root:
    if xmlns + 'manifest' == child.tag:
        data['manifest'] = child 
    if xmlns + 'metadata' == child.tag:
        data['metadata'] = child   
    if xmlns + 'spine' == child.tag:
        data['spine'] = child 

for item in data['manifest']: 
    idref_to_file[item.attrib['id']] = item.attrib['href']

pages_idref = []
for page in data['spine']:
    pages_idref.append(page.attrib['idref'])
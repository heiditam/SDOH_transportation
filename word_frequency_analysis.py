import xml.etree.ElementTree as ET
tree = ET.parse('sources.xml')
root = tree.getroot()

print(root)
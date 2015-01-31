from pprint import pprint

import os
import xml.etree.ElementTree as ET


config_dir = "Config"


def mergify(to, frum):
    for key, value in frum.items():
        if key not in to:
            to[key] = set()
        to[key].update(value)
    return to


def get_attribs(root, parent_path=""):
    attributes = {}
    for element in root:
        full_tag = "/".join([parent_path, element.tag])
        if full_tag not in attributes:
            attributes[full_tag] = set()
        attributes[full_tag].update(element.attrib.keys())

        child_attribs = get_attribs(element, full_tag)
        if child_attribs:
            mergify(attributes, child_attribs)

    return attributes

def main():
    configs = os.listdir(config_dir)
    configs = map(lambda c: os.path.join(config_dir, c), configs)
    
    for config in configs:
        tag_map = {}
        tree = ET.parse(config)
        root = tree.getroot()
        print config
        for child in root:
            mergify(tag_map, get_attribs(child, child.tag))
        pprint(tag_map)
        


main() if __name__ == "__main__" else None
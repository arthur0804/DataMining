import xml.etree.ElementTree as ET
import re
import pandas as pd

columns = ['content', 'tone']
df = pd.DataFrame(columns=columns)

tree = ET.parse('novelist_project.xml')
root = tree.getroot()


def CleanText(raw_text):
    # clean html charsets
    new_text = re.sub(r'&[\w;#\w]*;', ' ', raw_text)
    return new_text


i = 0

# each record
for record in root:
    tone = []
    content = []
    # each field
    for field in record:
        if field.tag.endswith('datafield'):
            if 'tag' in field.attrib:
                # find the tag of tone(694)
                if field.attrib['tag'] == "598":
                    # iterate through subfileds
                    for subfield in field:
                        if subfield.tag.endswith('subfield'):
                            if 'code' in subfield.attrib:
                                if subfield.attrib['code'] == 'a':
                                    new_text = CleanText(subfield.text)
                                    content.append(new_text)

                elif field.attrib['tag'] == "694":
                    # iterate through subfileds
                    for subfield in field:
                        if subfield.tag.endswith('subfield'):
                            if 'code' in subfield.attrib:
                                if subfield.attrib['code'] == 'a':
                                    tone.append(subfield.text)

    if len(tone) > 0 and len(content) > 0:
        contents = "-----".join(content)
        tones = ",".join(tone)
        df.loc[len(df)] = [contents, tones]

    i += 1

    if i % 100 == 0:
        print("{} results have been done".format(i))

df.to_csv("tone_and_not_empty_content.tsv", encoding="utf-8", index=False)

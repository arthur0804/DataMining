import sys
import xml.etree.ElementTree as ET
from random import random

if len(sys.argv) != 2:
	exit('Params: xml_file_path')

file_path = sys.argv[1]

ET.register_namespace("", "http://www.loc.gov/MARC21/slim")
tree = ET.parse(file_path)
root = tree.getroot()

FIELD_CODE = {
	'Title': '245',
	'Author': '100',
	'Annotation': '520',
	'Reviews': '598',
	'Subject (personal name)': '600',
	'Subject (general)': '650',
	'Genre': '655',
	'Tone': '694'
}

# get a list of textual contents for a given XML record and a data-field tag
# params:
#     record: an XML element pointer
#     tag: a string of numbers representing the tag of a data-field, e.g. '694'
# return:
#     a Python list. A record can have multiple data-fields with the same tag,
#     each having a string content. For instance, if tag is '694', then 
#     the function returns the list of assigned tones to the record.
def get_datafield_content_array(record, tag):
	content_array = []
	for field in record:
		if field.tag.endswith('datafield'):
			if 'tag' in field.attrib:
				if field.attrib['tag'] == tag: # find the tag
					for subfield in field:
						if subfield.tag.endswith('subfield'):
							if 'code' in subfield.attrib:
								if subfield.attrib['code'] == 'a':
									content_array.append( subfield.text )
	return content_array

# get the textual content for a given XML record and a control-field tag
# params:
#     record: an XML element pointer
#     tag: a string of numbers representing the tag of a control-field, e.g. '001' for control number
# returns:
#     the string of control field
def get_control_field(record, tag):
	for field in record:
		if field.tag.endswith('controlfield'):
			if 'tag' in field.attrib:
				if field.attrib['tag'] == tag:
					return field.text
	return 'NULL'

num_record = 0
num_record_with_title = 0
num_record_with_author = 0
num_record_with_annotation = 0
num_record_with_review = 0
num_record_with_subject_general = 0
num_record_with_genre = 0
num_record_with_tone = 0
num_record_with_review_and_tone = 0

tone_freq = {}
control_numbers = {}

for record in root:

	record_id  		= get_control_field(record, '001')
	title           = get_datafield_content_array(record, FIELD_CODE['Title'])
	author          = get_datafield_content_array(record, FIELD_CODE['Author'])
	annotation      = get_datafield_content_array(record, FIELD_CODE['Annotation'])
	reviews         = get_datafield_content_array(record, FIELD_CODE['Reviews'])
	subject_general = get_datafield_content_array(record, FIELD_CODE['Subject (general)'])
	genre           = get_datafield_content_array(record, FIELD_CODE['Genre'])
	tone            = get_datafield_content_array(record, FIELD_CODE['Tone'])

	# collecting statistics
	num_record += 1

	if len(title) >=1:
		num_record_with_title += 1
	if len(author) >= 1:
		num_record_with_author += 1
	if len(annotation) >= 1:
		num_record_with_annotation += 1
	if len(reviews) >= 1:
		num_record_with_review += 1
	if len(subject_general) >= 1:
		num_record_with_subject_general += 1
	if len(genre) >= 1:
		num_record_with_genre += 1
	if len(tone) >= 1:
		num_record_with_tone += 1

	if len(reviews) >= 1 and len(tone) >= 1:
		num_record_with_review_and_tone += 1

	# update the tone frequency dictionary 
	for t in tone:
		if t in tone_freq:
			tone_freq[t] += 1
		else:
			tone_freq[t] = 1

	# update the control number dictionary (to check if there's any duplicated control numbers)
	if record_id in control_numbers:
		control_numbers[record_id] += 1
	else:
		control_numbers[record_id] = 1

	
print ('number of records:', num_record)
print ('number of records with title:', num_record_with_title) 						# 28737
print ('number of records with author:', num_record_with_author) 					# 28059
print ('number of records with annotation:', num_record_with_annotation) 			# 25769
print ('number of records with review:', num_record_with_review)					# 14044
print ('number of records with subject_general:', num_record_with_subject_general) 	# 28406
print ('number of records with genre:', num_record_with_genre)						# 28633
print ('number of records with tone:', num_record_with_tone) 						# 12787
print ('number of records with review_tone:', num_record_with_review_and_tone) 		# 7005

print ('number of unique control_numbers:', len(control_numbers)) 					# 28737
print ('number of unique tones:', len(tone_freq)) 									# 59
print ('tones by frequency:')
print (sorted(tone_freq.items(), key = lambda x: x[1], reverse = True))


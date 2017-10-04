import os

def text_clean(inp_txt):

    opt_txt = str(inp_txt).replace("\t", "").replace(" ", "").replace("\r", "").replace("\n", "")

    return opt_txt

def extract_digits(inpt_str):

	digitstr = ""
	
	for char in inpt_str:
		if char.isdigit() == True:
			digitstr = digitstr + char
			
	return digitstr

def extract_alpha(inpt_str):

	alphastr = ""
	
	for char in inpt_str:
		if char.isalpha() == True or char == "_" or char == "'":
			alphastr = alphastr + char
			
	return alphastr

def extract_alnum(inpt_str):

	alnumstr = ""
	
	for char in inpt_str:
		if char.isalnum() == True or char == "_" or char == "'":
			alnumstr = alnumstr + char
			
	return alnumstr

def list_to_str(input_list):
	output_str = ""
	
	first_comma_flag = 0
	
	for entry in input_list:
	
		if first_comma_flag == 1:
			output_str = output_str + "," +  str(entry)
	
		if first_comma_flag == 0:
			first_comma_flag = 1
			output_str = output_str +  str(entry)

	return output_str

def first_four_chars(input_str):
	output_str = ""
	char_number_flag = 0

	for char in input_str:
		
		if char_number_flag <= 3:
			char_number_flag = char_number_flag + 1
			output_str = output_str + char
	
	return output_str

def tuple_to_list(input_tuple):

	output_list = list()
	
	for element in input_tuple:
		output_list.append(element)
	
	return output_list
	
def most_common_element(input_list):
	
	input_dict = dict()
	
	for element in input_list:

		if element in input_dict:
			element_count = input_dict[element]
		
			input_dict.update({element:element_count + 1})
			
		if element not in input_dict:
			input_dict.update({element:1})

	most_common_list = ["",0]
	
	for element in input_dict:
		if input_dict[element] >= most_common_list[1]:
			most_common_list = [element, input_dict[element]]
		else:
			continue
	
	return most_common_list[0]
	
def print_dict(input_dict):
	for key in input_dict:
		print str(key) + "\t" + str(input_dict[key])
		
def print_list(input_list):
	for entry in input_list:
		print str(entry)
		
def dict_with_list_writer(input_dict, output_file_str):

	output_file = open(output_file_str, 'w')
	line_str = ""
	
	for key in input_dict:
		line_str = line_str + key
		
		for entry in input_dict[key]:
			
			entry_str = ""
			
			for i in entry:
				if entry_str == "":
					entry_str = i
					continue

				if len(i) > 1:
					entry_str = entry_str + "," + i
					continue
			
				if len(i) == 1:
					entry_str = entry_str + i
					continue
			
			line_str = line_str + "\t" + entry_str

		line_str = line_str + "\n"

	output_file.write(line_str)

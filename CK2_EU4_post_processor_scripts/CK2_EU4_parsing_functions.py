import os
import sys

#----------------------------------------------------------------

CK2_EU4_main_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(CK2_EU4_main_dir + "/CK2_EU4_post_processor_scripts/"))

from CK2_EU4_utility_functions import *

#----------------------------------------------------------------

def history_countries_extractor(input_dir, output_dir):

	input_source = "MSC"
	
	if "from_CK2" in input_dir:
		input_source = "CK2"
	if "from_EU4" in input_dir:
		input_source = "EU4"
		
	output_info_file = open(output_dir + input_source + "_country_info_file.txt", 'w')

	for tag_file_name in os.listdir(input_dir):
		
		tag = tag_file_name[0] + tag_file_name[1] + tag_file_name[2]
		
		tag_file = open(input_dir + tag_file_name, 'r')
    
		try:
			country_name = extract_alpha(tag_file_name.split("-")[1].strip(".txt")).lower()
		except:
			country_name = extract_alpha(tag_file.readline()).lower()
    
		for line in tag_file:
			
			if first_four_chars(line).isdigit() == True:
				break
				
			if line[0] == "#":
				continue
			
			if "government" in line and "=" in line and not "government_rank" in line:
				country_government = extract_alpha(line.split("=")[1].split("#")[0])
				
			if "government_rank" in line and "=" in line:
				country_rank = extract_digits(line)
				
			if "technology_group" in line and "=" in line:
				country_tech_group = extract_alpha(line.split("=")[1].split("#")[0])
				
			if "primary_culture" in line and "=" in line:
				country_culture = extract_alpha(line.split("=")[1].split("#")[0])
				
			if "religion" in line and "=" in line:
				country_religion = extract_alpha(line.split("=")[1].split("#")[0])
			
			if "capital" in line and "=" in line:
				country_capital = extract_digits(line)
		
		tag_file.close()
		
		output_info_file.write(tag + "\t" + country_name + "\t" + country_government + "\t" + country_rank  + "\t" + country_tech_group + "\t" + country_culture + "\t" + country_religion + "\t" + country_capital + "\n")

	output_info_file.close()

def history_provinces_extractor(input_dir, output_dir):

	input_source = "MSC"
	
	if "from_CK2" in input_dir:
		input_source = "CK2"
	if "from_EU4" in input_dir:
		input_source = "EU4"
	
	output_info_file = open(output_dir + input_source + "_province_info_file.txt", 'w')
	
	for province_file_name in os.listdir(input_dir):
		try:
			province_name = extract_alnum(province_file_name.split("_conv")[0].split(".txt")[0].split("-")[1]).lower()
		except:
			province_name = extract_alpha(province_file_name.split("_conv")[0].split(".txt")[0])
		
		province_id = extract_digits(province_file_name.split("-")[0])

		province_file = open(input_dir + province_file_name, 'r')
		
		#For removing files with blank entries
		province_owner = "@"; province_controller = "@"; province_core = "@"; province_culture = "@"; province_religion="@"; province_claim="@"
		
		province_core_list = list()
		province_claim_list = list()
    
		for line in province_file:
			
			if first_four_chars(line).isdigit() == True:
				break
				
			if line[0] == "#":
				continue
			
			#if "discovered_by" in line:
				#break

			if "owner" in line and "=" in line:
				province_owner = extract_alnum(line.split("=")[1].split("#")[0])
			
			if "controller" in line and "=" in line:
				province_controller = extract_alnum(line.split("=")[1].split("#")[0])
			
			if "add_core" in line and "=" in line:
				province_core = extract_alnum(line.split("=")[1].split("#")[0])
				province_core_list.append(province_core)
			
			if "culture" in line and "=" in line:
				province_culture = extract_alpha(line.split("=")[1].split("#")[0])
            
			if "religion" in line and "=" in line:
				province_religion = extract_alpha(line.split("=")[1].split("#")[0])
				
			if "claim" in line and "=" in line:
				province_claim = extract_alnum(line.split("=")[1].split("#")[0])
				province_claim_list.append(province_claim)
			
		if province_core_list == []:
			province_core_list = "@"
		if province_claim_list == []:
			province_claim_list = "@"
		
		province_file.close()

		if province_owner == "@" and province_controller == "@" and province_core_list == "@" and province_culture == "@" and province_religion == "@" and province_claim_list == "@":
        
			print str(province_id) + "\t" + province_name 
			continue
    
		else:
			if province_owner == "@":
				province_owner = ""
			if province_controller == "@":
				province_controller = ""
			if province_core_list == "@":
				province_core_list = ""
			if province_culture == "@":
				province_culture = ""
			if province_religion == "@":
				province_religion = ""
			if province_claim_list == "@":
				province_claim_list = ""
			
			output_info_file.write(province_id + "\t" + province_name + "\t" + province_owner + "\t" + province_controller + "\t" + list_to_str(province_core_list) + "\t" + province_culture + "\t" + province_religion + "\t" + list_to_str(province_claim_list) + "\n")

	output_info_file.close()
	
def common_cultures_extractor(input_dir, output_dir):

	input_source = "MSC"
	
	if "from_CK2" in input_dir:
		input_source = "CK2"
	if "from_EU4" in input_dir:
		input_source = "EU4"
	
	output_info_file = open(output_dir + input_source + "_culture_info_file.txt", 'w')
	
	for culture_file_name in os.listdir(input_dir):
		
		culture_file = open(input_dir + culture_file_name, 'r')
		
		level_counter = 0
		
		for line in culture_file:

			if "=" not in line and "{" not in line and "}" not in line:
				continue

			else:
				read_line_flag = True
				
				if level_counter == 1 or level_counter == 2:
					if "names" in line or "graphical_culture" in line:
						read_line_flag = False
						
				if read_line_flag == True:
					if "=" in line:
						if len(line.split("#")[0]) == 0:
							continue

						if level_counter == 0:
						
							culture_group_string = ""
						
							super_group = extract_alpha(line.split("#")[0])
							culture_group_string = culture_group_string + super_group

						if level_counter == 1:
							sub_culture = extract_alpha(line.split("#")[0])
							culture_group_string = culture_group_string + "\t" + sub_culture

						if level_counter == 2:
							primary_tag = extract_alpha(line.split("#")[0].split("=")[1])
							culture_group_string = culture_group_string + "," + primary_tag

				if "{" in line:
					level_counter = level_counter + 1
				if "}" in line:
					level_counter = level_counter - 1

				if level_counter == 0:
				
					culture_group_list = culture_group_string.split("\t")
					super_group = culture_group_list.pop(0)
					
					culture_group_string = ""
					
					for culture_inf in culture_group_list:
					
						sub_culture = culture_inf.split(",")[0]
						try:
							primary_tag = culture_inf.split(",")[1]
						except:
							primary_tag = ""
					
						output_info_file.write(super_group + "\t" + sub_culture + "\t" + primary_tag + "\n")
						
					culture_group_list = list()
						
		culture_file.close()
	output_info_file.close()

#----------------------------------------------------------------

def country_info_dict_maker(input_file_str):
	
	input_file = open(input_file_str, 'r')

	country_info_dict = dict()
	
	for line in input_file:
	
		tag_data_list = line.strip("\n").split("\t")
		tag = tag_data_list.pop(0)
		
		tag_data_tuple = tuple(tag_data_list)
		
		country_info_dict.update({tag:tag_data_tuple})

	return country_info_dict

def province_info_dict_maker(input_file_str):
	
	input_file = open(input_file_str, 'r')
	
	province_info_dict = dict()
	
	for line in input_file:
	
		province_data_list = line.strip("\n").split("\t")
		province_id = province_data_list.pop(0)
		
		core_tuple = tuple(province_data_list[3].split(","))
		province_data_list[3] = core_tuple
		
		claim_tuple = tuple(province_data_list[6].split(","))
		province_data_list[6] = claim_tuple
		
		province_data_tuple = tuple(province_data_list)
	
		province_info_dict.update({province_id:province_data_tuple})
		
	return province_info_dict
	
def sub_super_culture_dict_maker(input_file_str):

	input_file = open(input_file_str, 'r')
	
	sub_super_culture_dict = dict()
	
	for line in input_file:
		sub_culture = line.replace(" ", "").strip("\n").split("\t")[1]
		super_culture = line.replace(" ", "").strip("\n").split("\t")[0]
		
		sub_super_culture_dict.update({sub_culture:super_culture})
	
	input_file.close()
	
	return sub_super_culture_dict

def sub_culture_tag_dict_maker(input_file_str):

	input_file = open(input_file_str, 'r')

	sub_culture_tag_dict = dict()
	
	for line in input_file:
		sub_culture = line.replace(" ", "").strip("\n").split("\t")[1]
		tag = line.replace(" ", "").strip("\n").split("\t")[2]
		
		sub_culture_tag_dict.update({sub_culture:tag})
	
	return sub_culture_tag_dict

def tag_sub_culture_dict_maker(input_file_str):

	input_file = open(input_file_str, 'r')

	tag_sub_culture_dict = dict()
	
	for line in input_file:
		sub_culture = line.replace(" ", "").strip("\n").split("\t")[1]
		tag = line.replace(" ", "").strip("\n").split("\t")[2]
		
		if tag == "":
			continue
		
		else:
			tag_sub_culture_dict.update({tag:sub_culture})
	
	return tag_sub_culture_dict

def tag_majority_culture_dict_maker(input_province_info_dict):

	tag_province_culture_list = list()
	tag_province_culture_dict = dict()

	for province_id in input_province_info_dict:
	
		province_info_tuple = tuple(input_province_info_dict[province_id])
		province_core_tuple = province_info_tuple[3]
		province_sub_culture = province_info_tuple[4]
		
		for core in province_core_tuple:
			if core == "":
				continue
			else:
				tag_province_culture_list.append([core,province_sub_culture])
		
	for core_info in tag_province_culture_list:
		tag = core_info[0]
		culture = core_info[1]
		
		try:
			tag_culture_list = tag_province_culture_dict[tag]
			tag_culture_list.append(culture) 
			tag_province_culture_dict.update({tag:tag_culture_list})
		except:
			tag_province_culture_dict.update({tag:[culture]})

	tag_culture_count_dict = dict()

	for tag in tag_province_culture_dict:
	
		province_culture_list = tag_province_culture_dict[tag]
		culture_count_dict = dict()
			
		for culture in province_culture_list:
			try:
				culture_count = culture_count_dict[culture]
				culture_count = culture_count + 1
				culture_count_dict.update({culture:culture_count})
			except:
				culture_count_dict.update({culture:1})

		tag_culture_count_dict.update({tag:culture_count_dict}) 

	#Figure out which are the majority cultures:

	majority_culture_dict = dict()
	
	for tag in tag_culture_count_dict:
	
		count = 0
		
		for culture in tag_culture_count_dict[tag]:
			if len(tag_culture_count_dict[tag]) == 1:
				majority_culture_dict.update({tag:culture})
				continue
			
			culture_count = tag_culture_count_dict[tag][culture]
			
			if culture_count >= count:
				majority_culture_dict.update({tag:culture})
				continue

	return majority_culture_dict

#----------------------------------------------------------------

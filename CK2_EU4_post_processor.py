import os
import sys
import shutil

USE_CULTURE_EXCLUSIONS = True

CULTURE_EXCLUSIONS_set = ("german","italian","russian_culture","mongol","turkish","mali","cosmopolitan_french","kurdish")

USE_TAG_NAME_FIX = True

TAG_NAME_FIX_EU4_to_CK2_dict = ({"chanda":"canda","ottomanempire":"ottoman","kachar":"kachari","denmark":"danmark","eretna":"eretnid","sami":"spmi","delhi":"tughluq","brittany":"bretagne","mongolkhanate":"mongolia","mameluks":"bahri"})

IGNORE_CK2_TO_EU4_TAG_MAPPING = True

IGNORE_CK2_name_set = ("ilkhanate")

#----------------------------------------------------------------

#Listing directories used by the script:

CK2_EU4_main_dir = os.path.dirname(__file__)

post_processor_dir = CK2_EU4_main_dir + "/post_processor_files/"

from_EU4_file_dir = CK2_EU4_main_dir + "/from_EU4/"
from_CK2_file_dir = CK2_EU4_main_dir + "/from_CK2/"

for dir in os.listdir(from_CK2_file_dir):
    if "Converted" in dir:
        if ".mod" not in dir:
            CK2_converted_dir = from_CK2_file_dir + dir + "/"

#----------------------------------------------------------------

#Import function scripts:

sys.path.append(os.path.abspath(CK2_EU4_main_dir + "/CK2_EU4_post_processor_scripts/"))

from CK2_EU4_utility_functions import *
from CK2_EU4_parsing_functions import *

CK2_EU4_main_dir = os.path.dirname(__file__)
	
#----------------------------------------------------------------

#Extract country history data

CK2_country_history_dir = CK2_converted_dir + "history/countries/"
history_countries_extractor(CK2_country_history_dir, post_processor_dir)

EU4_country_history_dir = from_EU4_file_dir + "history/countries/"
history_countries_extractor(EU4_country_history_dir, post_processor_dir)

#----------------------------------------------------------------

#Extract province history data

CK2_province_history_dir = CK2_converted_dir + "history/provinces/"
history_provinces_extractor(CK2_province_history_dir, post_processor_dir)

EU4_province_history_dir = from_EU4_file_dir + "history/provinces/"
history_provinces_extractor(EU4_province_history_dir, post_processor_dir)

#----------------------------------------------------------------

#Extract culture information

CK2_common_cultures_dir = CK2_converted_dir + "common/cultures/"
common_cultures_extractor(CK2_common_cultures_dir, post_processor_dir)

EU4_common_cultures_dir = from_EU4_file_dir + "common/cultures/"
common_cultures_extractor(EU4_common_cultures_dir, post_processor_dir)

#----------------------------------------------------------------

#Create country information dictionaries with the following format:
#tag : "name", government, rank, tech_group, sub_culture, religion, capital_id 

CK2_country_history_file_str = post_processor_dir + "CK2_country_info_file.txt"
CK2_country_info_dict = country_info_dict_maker(CK2_country_history_file_str)

EU4_country_history_file_str = post_processor_dir + "EU4_country_info_file.txt"
EU4_country_info_dict = country_info_dict_maker(EU4_country_history_file_str)

print ;
print "CK2_country_info_dict\t" + str(len(CK2_country_info_dict))
print "EU4_country_info_dict\t" + str(len(EU4_country_info_dict))

#----------------------------------------------------------------

#Create province information dictionaries with the following format:
#province_id : "name", owner, controller, cores, sub_culture, religion, claim

CK2_province_history_file_str = post_processor_dir + "CK2_province_info_file.txt"
CK2_province_info_dict = province_info_dict_maker(CK2_province_history_file_str)

EU4_province_history_file_str = post_processor_dir + "EU4_province_info_file.txt"
EU4_province_info_dict = province_info_dict_maker(EU4_province_history_file_str)

print ;
print "CK2_province_info_dict\t" + str(len(CK2_province_info_dict))
print "EU4_province_info_dict\t" + str(len(EU4_province_info_dict))

#----------------------------------------------------------------

#Create culture dictionaries and joint CK2-EU4 dictionaries

CK2_common_cultures_file_str = post_processor_dir + "CK2_culture_info_file.txt"
CK2_sub_super_culture_dict = sub_super_culture_dict_maker(CK2_common_cultures_file_str)
CK2_sub_culture_primary_tag_dict = sub_culture_tag_dict_maker(CK2_common_cultures_file_str)

print ;
print "CK2_sub_super_culture_dict\t" + str(len(CK2_sub_super_culture_dict))
print "CK2_sub_culture_primary_tag_dict\t" + str(len(CK2_sub_culture_primary_tag_dict))

EU4_common_cultures_file_str = post_processor_dir + "EU4_culture_info_file.txt"
EU4_sub_super_culture_dict = sub_super_culture_dict_maker(EU4_common_cultures_file_str)

print ;
print "EU4_common_cultures_file_str\t" + str(len(EU4_common_cultures_file_str))
print "EU4_sub_super_culture_dict\t" + str(len(EU4_sub_super_culture_dict))

EU4_sub_culture_primary_tag_dict = sub_culture_tag_dict_maker(EU4_common_cultures_file_str)
EU4_primary_tag_sub_culture_dict = tag_sub_culture_dict_maker(EU4_common_cultures_file_str)

print ;
print "EU4_sub_culture_primary_tag_dict\t" + str(len(EU4_sub_culture_primary_tag_dict))
print "EU4_primary_tag_sub_culture_dict\t" + str(len(EU4_primary_tag_sub_culture_dict))

EU4_CK2_sub_super_culture_dict = EU4_sub_super_culture_dict.copy()
for sub_super_entry in CK2_sub_super_culture_dict:
	EU4_CK2_sub_super_culture_dict.update({sub_super_entry:CK2_sub_super_culture_dict[sub_super_entry]})

EU4_CK2_sub_primary_culture_dict = EU4_sub_culture_primary_tag_dict.copy()
for sub_primary_entry in CK2_sub_culture_primary_tag_dict:
	EU4_CK2_sub_primary_culture_dict.update({sub_primary_entry:CK2_sub_culture_primary_tag_dict[sub_primary_entry]})
	
print ;
print "EU4_CK2_sub_super_culture_dict\t" + str(len(EU4_CK2_sub_super_culture_dict))
print "EU4_CK2_sub_primary_culture_dict\t" + str(len(EU4_CK2_sub_primary_culture_dict))

#----------------------------------------------------------------

#Remove the EU4 provinces not in the CK2 dict:

wip_EU4_province_info_dict = dict()

for CK2_province_id in CK2_province_info_dict:
	wip_EU4_province_info_dict.update({CK2_province_id:EU4_province_info_dict[CK2_province_id]})

print ;
print "CK2_province_info_dict\t" + str(len(CK2_province_info_dict))
print "wip_EU4_province_info_dict\t" + str(len(wip_EU4_province_info_dict))

#Create a new dictionary of active EU4 tags: 
#province_id : "name", owner, controller, cores, sub_culture, religion, claim

active_EU4_cores_set = set()

for EU4_province_id in wip_EU4_province_info_dict:

	EU4_province_info = list(wip_EU4_province_info_dict[EU4_province_id])
	EU4_province_cores = EU4_province_info[3]
	EU4_province_sub_culture = EU4_province_info[4]
	
	for EU4_core in EU4_province_cores:
		if EU4_core != "":
			active_EU4_cores_set.add(EU4_core)

wip_EU4_country_info_dict = dict()
for EU4_tag in active_EU4_cores_set:
	wip_EU4_country_info_dict.update({EU4_tag:EU4_country_info_dict[EU4_tag]}) 

print ;
print "active_EU4_cores_set\t" + str(len(active_EU4_cores_set))
print "wip_EU4_country_info_dict\t" + str(len(wip_EU4_country_info_dict))

#----------------------------------------------------------------

#Create a new dictionary of active CK2 tags: 
#province_id : "name", owner, controller, cores, sub_culture, religion, claim

active_CK2_cores_set = set()

for CK2_province_id in CK2_province_info_dict:

	CK2_province_info = list(CK2_province_info_dict[CK2_province_id])
	CK2_province_cores = CK2_province_info[3]

	for CK2_core in CK2_province_cores:
		if CK2_core != "":
			active_CK2_cores_set.add(CK2_core)

wip_CK2_country_info_dict = dict()
for CK2_tag in active_CK2_cores_set:
	wip_CK2_country_info_dict.update({CK2_tag:CK2_country_info_dict[CK2_tag]}) 

CK2_country_info_dict = dict() #Delete CK2_country_info_dict

print ;
print "active_CK2_cores_set\t" + str(len(active_CK2_cores_set))
print "wip_CK2_country_info_dict\t" + str(len(wip_CK2_country_info_dict))

#Remove the inactive CK2 tags from claims:
			
wip_CK2_province_info_dict = dict()

for CK2_province_id in CK2_province_info_dict:

	CK2_province_info_list = list(CK2_province_info_dict[CK2_province_id])
	CK2_province_claims_list = CK2_province_info_list[6]
	
	wip_CK2_province_claims_list = list()
	
	for CK2_claim in CK2_province_claims_list:
		if CK2_claim == "":
			continue
			
		if CK2_claim in active_CK2_cores_set:
			wip_CK2_province_claims_list.append(CK2_claim)
	
	CK2_province_info_list[6] = tuple(wip_CK2_province_claims_list)
	CK2_province_info_tuple = tuple(CK2_province_info_list)
	
	wip_CK2_province_info_dict.update({CK2_province_id:CK2_province_info_tuple})
			
#----------------------------------------------------------------

#If a CK2 province id and CK2 tag share the same name then replace the tag capital
#with the CK2 province id, this will make it easier to identify matching EU4 tags.
	
for CK2_province_id in CK2_province_info_dict:
	
	CK2_province_info_list = list(CK2_province_info_dict[CK2_province_id])
	CK2_province_name = CK2_province_info_list[0]
	
	for CK2_tag in wip_CK2_country_info_dict:
		CK2_country_info_list = list(wip_CK2_country_info_dict[CK2_tag])
		CK2_name = CK2_country_info_list[0]
		CK2_capital = CK2_country_info_list[6]
		
		if CK2_name == CK2_province_name and CK2_capital != CK2_province_id:
			CK2_country_info_list[6] = CK2_province_id
			CK2_country_info_tuple = tuple(CK2_country_info_list)
			
			wip_CK2_country_info_dict.update({CK2_tag:CK2_country_info_tuple})

#Try and identify the active CK2 tags with the EU4 tags and create a map:
#tag : "name", government, rank, tech_group, sub_culture, religion, capital_id 

active_CK2_tags_to_EU4_dict = dict()
assigned_EU4_tag_set = set()

for CK2_tag in wip_CK2_country_info_dict:

	#Match the CK2 and EU4 if they are identical:
	
	if CK2_tag in EU4_country_info_dict:
		active_CK2_tags_to_EU4_dict.update({CK2_tag:CK2_tag})
		assigned_EU4_tag_set.add(CK2_tag)
		continue
		
	CK2_country_info_list = list(wip_CK2_country_info_dict[CK2_tag])
	CK2_name = CK2_country_info_list[0]
	
	if IGNORE_CK2_TO_EU4_TAG_MAPPING == True and CK2_name in IGNORE_CK2_name_set:
		active_CK2_tags_to_EU4_dict.update({CK2_tag:""})
		continue

	CK2_sub_culture = CK2_country_info_list[4]
	CK2_super_culture = EU4_CK2_sub_super_culture_dict[CK2_sub_culture]
	CK2_capital = CK2_country_info_list[6]

	CK2_capital_sub_culture = wip_CK2_province_info_dict[CK2_country_info_list[6]][4]
	CK2_capital_super_culture = EU4_CK2_sub_super_culture_dict[CK2_capital_sub_culture]

	#If the CK2 tags assign them if they have the same name, sometimes they are outside europe:
	
	for EU4_tag in EU4_country_info_dict:
	
		EU4_country_info_list = list(EU4_country_info_dict[EU4_tag])
		EU4_name = EU4_country_info_list[0]

		if USE_TAG_NAME_FIX == True and EU4_name in TAG_NAME_FIX_EU4_to_CK2_dict:
			EU4_name = TAG_NAME_FIX_EU4_to_CK2_dict[EU4_name]

		if CK2_name == EU4_name:
			active_CK2_tags_to_EU4_dict.update({CK2_tag:EU4_tag})
			assigned_EU4_tag_set.add(EU4_tag)
			break

	if CK2_tag in active_CK2_tags_to_EU4_dict:
		continue
	
	#Assign active EU4 tags if they share capital ids and culture:
	
	for EU4_tag in wip_EU4_country_info_dict:
	
		if EU4_tag in assigned_EU4_tag_set:
			continue
	
		EU4_country_info_list = list(wip_EU4_country_info_dict[EU4_tag])
		EU4_sub_culture = EU4_country_info_list[4]
		EU4_super_culture = EU4_CK2_sub_super_culture_dict[EU4_sub_culture]
		EU4_capital = EU4_country_info_list[6]
		EU4_capital_sub_culture = EU4_province_info_dict[EU4_country_info_list[6]][4]
		EU4_capital_super_culture = EU4_CK2_sub_super_culture_dict[EU4_capital_sub_culture]
		
		if CK2_capital == EU4_capital and CK2_super_culture == EU4_super_culture:
			active_CK2_tags_to_EU4_dict.update({CK2_tag:EU4_tag})
			assigned_EU4_tag_set.add(EU4_tag)
			break

		if CK2_capital == EU4_capital and CK2_capital_super_culture == EU4_super_culture:
			active_CK2_tags_to_EU4_dict.update({CK2_tag:EU4_tag})
			assigned_EU4_tag_set.add(EU4_tag)
			break
		
		if CK2_capital == EU4_capital and CK2_super_culture == EU4_capital_super_culture:
			active_CK2_tags_to_EU4_dict.update({CK2_tag:EU4_tag})
			assigned_EU4_tag_set.add(EU4_tag)
			break

		if CK2_capital == EU4_capital and CK2_capital_super_culture == EU4_capital_super_culture:
			active_CK2_tags_to_EU4_dict.update({CK2_tag:EU4_tag})
			assigned_EU4_tag_set.add(EU4_tag)
			break
			
	if CK2_tag not in active_CK2_tags_to_EU4_dict:
		active_CK2_tags_to_EU4_dict.update({CK2_tag:""})

CK2_province_info_dict = dict() #Delete CK2_province_info_dict		
EU4_province_info_dict = dict() #Delete EU4_province_info_dict	

#Make sure all the EU4 tags assigned in the previous are also in the new EU4 country dict:

for EU4_tag in assigned_EU4_tag_set:
	if EU4_tag not in wip_EU4_country_info_dict:
		wip_EU4_country_info_dict.update({EU4_tag:EU4_country_info_dict[EU4_tag]})

EU4_country_info_dict = dict() #Delete EU4_country_info_dict

print ;
#----------------------------------------------------------------
#What are the majority cultures of the CK2 and EU4 tags?

CK2_majority_culture_dict = tag_majority_culture_dict_maker(wip_CK2_province_info_dict)
EU4_majority_culture_dict = tag_majority_culture_dict_maker(wip_EU4_province_info_dict)

for CK2_tag in wip_CK2_country_info_dict:
	try:
		CK2_majority_culture_dict[CK2_tag]
	except:
		print EU4_tag + " has no majority"
		CK2_majority_culture_dict.update({CK2_tag:wip_CK2_country_info_dict[CK2_tag][4]})
		
for EU4_tag in wip_EU4_country_info_dict:
	try:
		EU4_majority_culture_dict[EU4_tag]
	except:
		print EU4_tag + " has no majority"
		EU4_majority_culture_dict.update({EU4_tag:wip_EU4_country_info_dict[EU4_tag][4]})

print ;
print "CK2_majority_culture_dict\t" + str(len(CK2_majority_culture_dict))
print "EU4_majority_culture_dict\t" + str(len(EU4_majority_culture_dict))
		
#----------------------------------------------------------------

#Try and transform the CK2 country cultures with the EU4 cultures. If the EU4 and CK2 tags
#match and they share the same super cultures, then use the EU4 sub culture. If they dont
#try the CK2 and EU4 majority cultures.

#tag : "name", government, rank, tech_group, sub_culture, religion, capital_id 

modded_CK2_country_info_dict = dict()

for CK2_tag in wip_CK2_country_info_dict:

	CK2_country_info_list = list(wip_CK2_country_info_dict[CK2_tag])
	CK2_name = CK2_country_info_list[0]
	CK2_sub_culture = CK2_country_info_list[4]
	CK2_super_culture = EU4_CK2_sub_super_culture_dict[CK2_sub_culture]
	
	CK2_majority_culture = CK2_majority_culture_dict[CK2_tag]
	CK2_majority_super_culture = EU4_CK2_sub_super_culture_dict[CK2_majority_culture]

	if active_CK2_tags_to_EU4_dict[CK2_tag] != "":
		CK2_tag = active_CK2_tags_to_EU4_dict[CK2_tag]

	if CK2_tag in wip_EU4_country_info_dict:
	
		EU4_tag = CK2_tag
		EU4_country_info_list = wip_EU4_country_info_dict[EU4_tag]
		EU4_sub_culture = EU4_country_info_list[4]
		EU4_super_culture = EU4_CK2_sub_super_culture_dict[EU4_sub_culture]
		
		EU4_majority_culture = EU4_majority_culture_dict[EU4_tag]
		EU4_majority_super_culture = EU4_CK2_sub_super_culture_dict[EU4_majority_culture]

		if CK2_super_culture == EU4_super_culture:
			CK2_sub_culture = EU4_sub_culture

		elif CK2_majority_super_culture == EU4_super_culture:
			CK2_sub_culture = EU4_sub_culture

		elif CK2_super_culture == EU4_majority_super_culture:
			CK2_sub_culture = EU4_majority_culture
			
		elif CK2_majority_super_culture == EU4_majority_super_culture:
			CK2_sub_culture = EU4_majority_culture

	if CK2_tag not in wip_EU4_country_info_dict:

		CK2_capital = CK2_country_info_list[6]
		CK2_capital_sub_culture = wip_CK2_province_info_dict[CK2_country_info_list[6]][4]
		CK2_capital_super_culture = EU4_CK2_sub_super_culture_dict[CK2_capital_sub_culture]
		
		EU4_CK2_capital_sub_culture = wip_EU4_province_info_dict[CK2_capital][4]
		EU4_CK2_capital_super_culture = EU4_CK2_sub_super_culture_dict[EU4_CK2_capital_sub_culture]
	
		if EU4_super_culture == EU4_CK2_capital_super_culture:
			CK2_sub_culture = EU4_CK2_capital_sub_culture
		
		elif EU4_majority_super_culture == EU4_CK2_capital_super_culture:
			CK2_sub_culture = EU4_CK2_capital_sub_culture

		elif CK2_capital_super_culture == EU4_CK2_capital_super_culture:
			CK2_sub_culture = EU4_CK2_capital_sub_culture
	
	if USE_CULTURE_EXCLUSIONS == False:
		CULTURE_EXCLUSIONS_set = set()

	if CK2_sub_culture in CK2_sub_super_culture_dict or CK2_sub_culture in CULTURE_EXCLUSIONS_set:

		if CK2_tag in wip_EU4_country_info_dict:
			CK2_sub_culture = EU4_sub_culture
		else:
			CK2_sub_culture = EU4_CK2_capital_sub_culture
			
	CK2_country_info_list[4] = CK2_sub_culture
	CK2_country_info_tuple = tuple(CK2_country_info_list)
	modded_CK2_country_info_dict.update({CK2_tag:CK2_country_info_tuple})

print ;
print "wip_CK2_country_info_dict\t" + str(len(wip_CK2_country_info_dict))
print "modded_CK2_country_info_dict\t" + str(len(modded_CK2_country_info_dict))

wip_CK2_country_info_dict = dict() #Delete wip_CK2_country_info_dict

#----------------------------------------------------------------

#Transform the CK2 province ids replacing the province cultures with those in
#EU4 if their superculture matchs that of EU4. Consider the modded CK2 tag
#sub culture and change accordingly. Also transform all CK2 tags with those
#with the EU4 mappings.

#province_id : "name", owner, controller, cores, sub_culture, religion, claim

modded_CK2_province_info_dict = dict()

for CK2_province_id in wip_CK2_province_info_dict:
	
	CK2_province_info_list = list(wip_CK2_province_info_dict[CK2_province_id])
	CK2_province_name = CK2_province_info_list[0]
	
	CK2_province_owner = CK2_province_info_list[1]
	CK2_province_controller = CK2_province_info_list[2]
	CK2_province_cores_list = list(CK2_province_info_list[3])
	CK2_province_claims_list = list(CK2_province_info_list[6])
	
	CK2_province_sub_culture = CK2_province_info_list[4]
	CK2_province_super_culture = EU4_CK2_sub_super_culture_dict[CK2_province_sub_culture]
	
	#Update all tags with the ones using the EU4 mappings:
	
	if CK2_province_owner != "" and CK2_province_owner in active_CK2_tags_to_EU4_dict:
	
		if active_CK2_tags_to_EU4_dict[CK2_province_owner] != "":
			CK2_province_owner = active_CK2_tags_to_EU4_dict[CK2_province_owner]
			CK2_province_controller = active_CK2_tags_to_EU4_dict[CK2_province_controller]

		updated_cores_set = set()
		for core in CK2_province_cores_list:
			if active_CK2_tags_to_EU4_dict[core] == "":
				updated_cores_set.add(core)
			elif active_CK2_tags_to_EU4_dict[core] != "":
				updated_cores_set.add(active_CK2_tags_to_EU4_dict[core])
		if CK2_province_owner not in updated_cores_set:
			updated_cores_set.add(CK2_province_owner)
		CK2_province_cores_list = list(updated_cores_set)
		
		updated_claims_set = set()
		for claim in CK2_province_claims_list:
			if active_CK2_tags_to_EU4_dict[core] == "":
				updated_claims_set.add(claim)
			elif active_CK2_tags_to_EU4_dict[core] != "":
				updated_claims_set.add(active_CK2_tags_to_EU4_dict[claim])
		CK2_province_claims_list = list(updated_claims_set)
	
	#Update the province cultures using the EU4 province cultures and tag cultures:
	
	EU4_province_info_list = list(wip_EU4_province_info_dict[CK2_province_id])
	EU4_province_sub_culture = EU4_province_info_list[4]
	EU4_province_super_culture = EU4_CK2_sub_super_culture_dict[EU4_province_sub_culture]
	
	if CK2_province_owner != "":
		CK2_owner_sub_culture = modded_CK2_country_info_dict[CK2_province_owner][4]
	else:
		CK2_owner_sub_culture = CK2_province_sub_culture
	CK2_owner_super_culture = EU4_CK2_sub_super_culture_dict[CK2_owner_sub_culture]

	if CK2_province_super_culture == EU4_province_super_culture:
		CK2_province_sub_culture = EU4_province_sub_culture
	elif CK2_owner_super_culture == EU4_province_super_culture:
		CK2_province_sub_culture = EU4_province_sub_culture
	elif CK2_province_super_culture == CK2_owner_super_culture:
		CK2_province_sub_culture = CK2_owner_sub_culture
	elif USE_CULTURE_EXCLUSIONS == True and CK2_province_sub_culture in CULTURE_EXCLUSIONS_set:
		CK2_province_sub_culture = EU4_province_sub_culture

	#print  CK2_province_name + "\t" + CK2_province_owner+ "\t" + CK2_province_sub_culture + "\t" + CK2_owner_sub_culture + "\t" + EU4_province_sub_culture

	#Add EU4 cores to the map if the core owner isnt in the CK2 dict and it shares the province
	#superculture. Reorder the cores list to ensure that tags sharing the province culture come first.

	EU4_province_cores_list = 	list(EU4_province_info_list[3])
	province_culture_primary_tag = EU4_CK2_sub_primary_culture_dict[CK2_province_sub_culture]
	
	if CK2_province_owner != "":
		for core in EU4_province_cores_list:
			if core not in CK2_province_cores_list and core not in modded_CK2_country_info_dict:
				CK2_province_cores_list.append(core)
		
	CK2_province_info_list[1] = CK2_province_owner
	CK2_province_info_list[2] = CK2_province_controller
	CK2_province_info_list[3] = tuple(CK2_province_cores_list)
	CK2_province_info_list[4] = CK2_province_sub_culture
	CK2_province_info_list[6] = tuple(CK2_province_claims_list)

	modded_CK2_province_info_dict.update({CK2_province_id:tuple(CK2_province_info_list)})
		
print ;
print "wip_CK2_province_info_dict\t" + str(len(wip_CK2_province_info_dict))
print "modded_CK2_province_info_dict\t" + str(len(modded_CK2_province_info_dict))

wip_CK2_province_info_dict = dict() #Delete wip_CK2_province_info_dict

#----------------------------------------------------------------

#Create modded output files from modded CK2 dictionaries:

modded_CK2_country_history_file_str = post_processor_dir + "modded_CK2_country_info_file.txt"
modded_CK2_province_history_file_str = post_processor_dir + "modded_CK2_province_info_file.txt"

dict_with_list_writer(modded_CK2_country_info_dict,modded_CK2_country_history_file_str)
dict_with_list_writer(modded_CK2_province_info_dict,modded_CK2_province_history_file_str)

#----------------------------------------------------------------

modded_history_countries_dir = CK2_EU4_main_dir + "/mod_files/"

try:
	shutil.rmtree(modded_history_countries_dir)
	print; print modded_history_countries_dir + "\tdeleted"
	
	os.makedirs(modded_history_countries_dir + "history/countries/")
	os.makedirs(modded_history_countries_dir + "history/provinces/")
	os.makedirs(modded_history_countries_dir + "common/ideas/")
except:
	os.makedirs(modded_history_countries_dir + "history/countries/")
	os.makedirs(modded_history_countries_dir + "history/provinces/")
	os.makedirs(modded_history_countries_dir + "common/ideas/")

#----------------------------------------------------------------
	
#Create modded country files:

#tag : "name", government, rank, tech_group, sub_culture, religion, capital_id

CK2_country_history_dir = CK2_converted_dir + "history/countries/"
modded_CK2_country_history_dir = modded_history_countries_dir + "history/countries/"

in_modded_dir_set = set()

for CK2_country_file_name in os.listdir(CK2_country_history_dir):

	file_CK2_tag = CK2_country_file_name[0] + CK2_country_file_name[1] + CK2_country_file_name[2]

	if file_CK2_tag in active_CK2_tags_to_EU4_dict:
		
		CK2_country_history_file = open(CK2_country_history_dir + CK2_country_file_name, 'r')
		
		#Transform tags using the EU4 mapping
		if active_CK2_tags_to_EU4_dict[file_CK2_tag] != "":
			CK2_tag = active_CK2_tags_to_EU4_dict[file_CK2_tag]
		else:
			CK2_tag = file_CK2_tag
		
		#Make sure the countries with EU4 tags take priority over those mapped to EU4 tags
		if file_CK2_tag in wip_EU4_country_info_dict:
			in_modded_dir_set.add(CK2_tag)
		elif file_CK2_tag not in wip_EU4_country_info_dict and CK2_tag in in_modded_dir_set:
			continue
		else:
			in_modded_dir_set.add(CK2_tag)

		
		CK2_country_info_list = modded_CK2_country_info_dict[CK2_tag]
		CK2_country_name = CK2_country_info_list[0]
				
		new_CK2_country_file_name = CK2_tag + " - " + CK2_country_name + ".txt"

		modded_CK2_country_history_file = open(modded_CK2_country_history_dir + new_CK2_country_file_name, 'w')

		for line in CK2_country_history_file:
			modded_CK2_country_history_file.write(line)

		CK2_country_history_file.close()
		#modded_CK2_country_history_file.flush()
		modded_CK2_country_history_file.close()
		
print ;
print "in_modded_CK2_country_dir_set\t" + str(len(in_modded_dir_set))

#----------------------------------------------------------------

#Create modded province files:

#province_id : "name", owner, controller, cores, sub_culture, religion, claim

CK2_province_history_dir = CK2_converted_dir + "history/provinces/"
modded_CK2_province_history_dir = modded_history_countries_dir + "history/provinces/"

for CK2_province_file_name in os.listdir(CK2_province_history_dir):

	CK2_province_history_file = open(CK2_province_history_dir + CK2_province_file_name, 'r')
	modded_CK2_province_history_file = open(modded_CK2_province_history_dir + CK2_province_file_name, 'w')
	
	#Get rid of rebel files:
	if "Rebels" in CK2_province_file_name:
		for line in CK2_province_history_file:
			modded_CK2_province_history_file.write(line)
		
		modded_CK2_province_history_file.close()
		continue
	
	#Open CK2 province data:
	
	province_id = extract_digits(CK2_province_file_name.split("-")[0])

	modded_CK2_province_tuple = modded_CK2_province_info_dict[province_id]
	
	modded_CK2_province_name = modded_CK2_province_tuple[0]
	modded_CK2_province_owner = modded_CK2_province_tuple[1]
	modded_CK2_province_controller = modded_CK2_province_tuple[2]
	modded_CK2_province_cores_tuple = modded_CK2_province_tuple[3]
	modded_CK2_province_sub_culture = modded_CK2_province_tuple[4]
	#modded_CK2_province_religion = modded_CK2_province_tuple[5]
	modded_CK2_province_claims_tuple = modded_CK2_province_tuple[6]
	
	#modded_CK2_province_history_file.write("# " + modded_CK2_province_name)
	
	indentation = ""
	level = 0
	first_add_core_line = True
	first_add_claim_line = True
	
	for line in CK2_province_history_file:
		
		if level == 0:
			indentation = ""
		elif level == 1:
			indentation = "\t"
		
		if "{" in line:
			level = level + 1
		if "}" in line:
			level = level - 1

		if "owner = " in line.split("#")[0]:
			line = indentation + "owner = " + modded_CK2_province_owner + "\n"
			
		if "controller = " in line.split("#")[0]:
			line = indentation + "controller = " + modded_CK2_province_controller + "\n"
			
		if "add_core = " in line.split("#")[0]:
			if first_add_core_line == True:
				line = ""
				for core in modded_CK2_province_cores_tuple:
					line = line + indentation + "add_core = " + str(core) + "\n"
				first_add_core_line = False
			else:
				continue
		
		if "culture = " in line.split("#")[0]:
			line = indentation + "culture = " + modded_CK2_province_sub_culture + "\n"
		
		if "add_permanent_claim = " in line.split("#")[0]:
			if first_add_claim_line == True:
				line = ""
				for claim in modded_CK2_province_claims_tuple:
					line = line + indentation + "add_permanent_claim = " + str(claim) + "\n"
				first_add_claim_line = False
			else:
				continue
				
		if "remove_core" in line and "=" in line:
			remove_core_tag = extract_alpha(line.split("=")[1].split("#")[0])
			if remove_core_tag in modded_CK2_province_cores_tuple:
				continue
				
		modded_CK2_province_history_file.write(line) 

	CK2_province_history_file.close()
	modded_CK2_province_history_file.close()

#modded_CK2_province_info_dict

#----------------------------------------------------------------

#Create modded tech files:



print ;print "fin"
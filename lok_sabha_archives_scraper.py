from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

lsno = 17 # 1
tab = 0 # 15

base_url = 'http://loksabhaph.nic.in/Members/lokaralpha.aspx?lsno={lsno}&tab={tab}'

lim = 17

browser = webdriver.Chrome('/Users/lbhattacharjee/documents/chromedriver')

while lsno <= lim:
	lok_sabha_members_url = base_url.format(lsno = lsno, tab = tab)
	if lsno == 17:
		lok_sabha_members_url = 'http://loksabhaph.nic.in/Members/AlphabeticalList.aspx'

	browser.get(lok_sabha_members_url)

	# get all rows in members table
	members_table = browser.find_elements(By.XPATH, '//table[@class="member_list_table"]/tbody/tr')

	member_names = []
	party_names = []
	constituencies = []
	
	for i in range(len(members_table)):
		_, member_name, party_name, constituency = members_table[i].find_elements(By.TAG_NAME, 'td')
		member_name = member_name.text.strip().replace('"', '')
		party_name = party_name.text.strip().replace('"', '')
		constituency = constituency.text.strip().replace('"', '')

		# append to list for curr url
		member_names.append(member_name)
		party_names.append(party_name)
		constituencies.append(constituency)

	# create df from lists
	curr_lok_sabha = pd.DataFrame({
			'Member': member_names,
			'Party Name': party_names,
			'Constituency': constituencies,
		})

	# save df to csv file
	curr_lok_sabha.to_csv('lok_sabha_member_data/lok_sabha_{lsno}.csv'.format(lsno = lsno))

	print(lok_sabha_members_url)

	lsno += 1
	tab -= 1

browser.quit()

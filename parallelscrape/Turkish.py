from datetime import datetime
from scrapersettings import scraper
# get todays date and time
todaydate = datetime.now().strftime("%d_%m_%Y__%H%M")
# name of the file and the directory it has to be in
# intconvert for interpreters, translator_convert for translators and converterd data for deaf interpreter
datadirectory = "intconvert"
dataname = "Turkish"
language_index = 207
# 1 for translater, 2 for interpreter and 3 for deaf interpreter
practitioner = 2
data = open(datadirectory + "/" + dataname + "{}.csv".format(todaydate), "w", newline='', encoding='utf-8')
scraper(data, language_index, practitioner)
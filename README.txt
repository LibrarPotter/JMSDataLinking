This is the readme file for the programs and general procedure used in the Journal of Molecular Spectroscopy article "Are your spectroscopic data being used?", by Iouli E. Gordon, Megan R. Potterbusch, Daina Bouquin, Christopher C. Erdmann,  Jonas S. Wilzewski and Laurence S. Rothman.
The clean data created by these programs are shown in Figures 3 and 4 of this article. Papers published in the Journal of Molecular Spectroscopy in Year1-Year2 were analysed for: 1. Amount of working and broken web links provided in the articles., 2. How many of these links point to curated archives, and 3. How many times each article was cited based on the statistics in the Astrophysical Data System (ADS).
Below we describe the steps of the procedure and the programs provided in this repository.

Before starting any data cleaning or processing, we received full-text, raw-XML copies of the Journal of Molecular Spectroscopy.

Using extract.py we removed the XML tags from the full-text and then used regular expressions to extract the links and the pre link text from the full-text articles.  The format expected by the extract.py program is MainFolder->SubFoldersByVolume->Articles.xml

Steps taken to clean up the URLs in order to run link_checker.ipynb:
- Added a duplicate column for "clean_link_text_not_article", which includes only the non-self-referential links on which all following actions were taken to preserve the original information in "link_text"
- Split URLs on "[" and "]"
- Removed the trailing symbols: ".", ",", "<", ">", "(", ")", ";", and "/"
- Removed trailing words "appendix" and "supplement" (pattern indicated these words were not part of actual links, but should have been the next word after the link)

HTTP status (from all levels):
All 200 codes returned are considered good
for 301, 302, and 303:
	Redirect locations have been checked.
	For these redirects:
		301 are generally good
		302 are generally good		
		303 are bad

403, 404, 502, and 503 are considered bad in general
	2 of the 503 links go to actual science direct articles and may be OK.

check_new_location_for_300.ipynb
- Eventually, this should be combined with the original link checker, because there is a great deal of duplication between the two, but for now this should be run after link_checker.pynb


Workflow:
- clean the data as mentioned above
- run link_checker
-- this adds columns for status and headers for URLs provided in the article (returned using the requests library)
- run check_location_for_300
-- this adds columns for the new/temporary/perminant "location" for all URLs that returned 300-304 statuses (these are refered to as status2, header2, and url2)
-- the locations are provided in the header fields
-- new columns are added to the dataframe
-- the new columns are: HTTPstatus2, HTTPheaders2, and URL2 (these are based on the reference location given in the header from the first status call.  AKA These columns have the same info as the original Status, Header, and URL information but the URL used to populate them was given in the header of the first URL) The 2 at the end signifies that this is the second URL that I tried use to get to the correct page.
- run check_locations_for_300 again but change input "status" and "header" from column: "HTTPstatus" and "HTTPheaders" to "HTTPstatus2" and "HTTPheaders2" (so that the status and the header used by the script are from the second URL).
-- this adds 3 more columns: HTTPstatus3, HTTPheaders3, and URL3.  The three indicates that this is the third URL that I tried programatically.
-- Use AddTheStatusListAndStatusOverviewColumn.ipynb to add "TheStatusList" column for the final status code and a "StatusOverview" column for if we are classifying the links as Active or Broken. 
-- Essentially what that code does:
	Psudo code for next step:
	if HTTPstatus3 is not null:
		if value does not equal "error getting status2"
			add value of status3 to new column X
		else
			add value of status2 to column X 
			(I found that over 133 of the 139 instences of an "error getting status2" were elsevier links that used 	"http://linkinghub.elsevier.com/retrieve", which is probably what created the unusual error)

	ifelse HTTPstatus2 is not null:
		add value to column X
	else
		add value from HTTPstatus to column X

	if HTTPheaders3 == "error getting status2" and status2 == 302:
		URL is broken
	if HTTPheaders3 == "error getting status2" and status2 == 301:
		URL is active

	Add "statusOverview" column for:
		if 200, 301, 302:
			ACTIVE
		else:
			BROKEN


Run get_citation_count_data_ADS_API.ipynb on data:
Open csv (hardcoded location) with a column of DOIs |
takes DOIs from dataframe |
Uses ADS API to search by DOI and return citation_count and pubdate  (publication date) |
Makes each into a list |
Adds lists to dataframe as new columns |
Outputs to csv (hardcoded location)

Add a column for year based on the date in the new csv


Group by DOI
For each DOI: # of links, year published
	# of links per article per year

Citations overtime by article
	DOI of paper, # of citation

Exclude duplicates based on DOI!


Used the GREL filter:  
	isNotNull(value.match(/.*jmsa_hp.*|.*dx\.doi.*/))
	to create column "trustedRepo", which contains true or false info.  True == Ohio State or if it is a link to a doi.  If it's a doi that means that it is in a trusted repo, because it has to be compliant with DOI requirements. (Most of the DOIs point to Elsevier.) 
	To use regular expresions to find strings in a column, follow the example above. All GREL REs start and end with a backslash, /.  The pipe, |, works as the boolean AND. the dot, ., and the astrix, *, are vital to the RE.  

Questions? Contact me at mpotterbusch@gmail.com
from bs4 import BeautifulSoup
from urllib import request,error
import csv

# Function to extract the desired information
# given a page source
def get_info(html):
    """
       Take a page's source and return the information
       Returns tuple
       (picture,item_number,UPC)
    """
    # Create soup from page's source
    soup = BeautifulSoup(html,'html.parser')

    # Pick out information of picture
    picture = soup.main.img['data-image']

    # Picking another location in html to get remaining info
    info = soup.find_all("div", class_="product-info")[0]

    # Loop through section in search of information
    for entry in info.find_all("li"):

        # When come upon line with information and pick it out
        if "Item" in entry.text:
            item_num = entry.text[5:]
        elif "UPC" in entry.text:
            upc = entry.text[4:]
    return (picture,item_num,upc)

# Create log file and information file
log_file = open("log_file.txt",'w')
csvfile = open("bulb_info.csv",'w')

# Create instance of csvwriter to write data
csvwriter = csv.writer(csvfile,dialect='unix')

# Write header row
csvwriter.writerow(("PICTURE","ITEM_NUM","UPC"))

# Take urls and grab info from each page 
for url in open("bulbrite_url.txt","r"):
    try:
        response  = request.urlopen(url[:-1])
    except error.URLError as e:
        if hasattr(e,'reson'):
            print("Failed to reach server",file=log_file)
            print("Reason:", e.reason,file=log_file)
            print("URL:",url,file=log_file)
        elif hasattr(e,'code'):
            print("The server couldn\'t fulfill the request",file=log_file)
            print("Error code:", e.code,file=log_file)
            print("URL:",url,file=log_file)            
        continue

    # Create variable to hold the extracted information
    information = get_info(response)
    # Write information to the created csv file
    csvwriter.writerow(information)

# Close log and csv file
log_file.close()
csvfile.close()

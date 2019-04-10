import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from bs4 import SoupStrainer as strainer

"""
Description: This function creates the intial web environment. This part will let the user decide which category
the user thinks they fit the most in and grabs the appropriate link in amazon.

Arguements:
    - choose: variable containing integer number 1,2, or 3 corresponding to user choice.

returns:
    -links: an array containing the potential laptops.

"""
def web_environment(choose):

    # This part contains the links preset for each category. 
    if (choose == 1): # Gaming laptops
        main_url = 'https://www.amazon.com/Gaming-Laptops/b?ie=UTF8&node=8588812011'
    elif(choose == 2): # Artist laptops
        main_url = 'https://www.amazon.ca/s/ref=nb_sb_noss_1?url=search-alias%3Delectronics&field-keywords=laptop+2+in+1&rh=n%3A667823011%2Ck%3Alaptop+2+in+1'
    elif (choose == 3): # Business laptops
        main_url = 'https://www.amazon.ca/s/gp/search/ref=sr_nr_p_n_feature_fourteen_1?fst=as%3Aoff&rh=n%3A667823011%2Cn%3A%21677211011%2Cn%3A2404990011%2Cn%3A677252011%2Cp_n_feature_two_browse-bin%3A7322166011%2Cp_n_feature_fourteen_browse-bin%3A7322419011&bbn=677252011&hidden-keywords=windows&ie=UTF8&qid=1543443506&rnid=7322417011'

    try:

        uClient = uReq(main_url) # Requests a connection to the page and downloads the page
        html_file = uClient.read() # Reads the html file
        uClient.close()
        products = strainer("div", {"class":"s-item-container"}) # This part gets rid of all irrelevant tags and classes for effeciency.
        page = soup(html_file,"lxml",parse_only=products) # Parses the html_file using the rule specificed in products.
        links = link_grab(page)

        return(links)
    except:
        # Takes care of the case where the request to link fails.
        print("unable to open link, please check internet connection and try again")


"""
Description: This function grabs the links for each laptop page from the main search result page in amazon. Then returns the links 
for each laptop page.

Arguements:
    page: contains the main page result page html file.

returns: 
    links: an array containing the potential laptops

"""
def link_grab(page):

    # main container containing all the items/laptops.
    m_container = page.find_all("div", {"class":"s-item-container"}) # main container for the products. It contains the html parts of each laptop

    links = []
    print("Grabbing relevant laptops")

    # finds the links from each computer in the main search page.
    for container in m_container:
        line = container.find("a", {"class": "a-link-normal a-text-normal"}) # Jumps to the tag "a" from a certain class
        if (line is not None):
            links.append(line['href']) # this 'href' is the key in the dictionary, and the dictionary returns the link
    return(links)
"""
Description: This function recieves the laptops links and traverses each link grabbing the specs for each laptop
This function then puts each laptop in a dictionary and appends each laptop dictionary in a list.

Arguements:
    links: an array containing the laptop links

returns:
    laptops: an array containing dictionaries for each laptop.
"""
def sort_and_pack(links):
    laptops = []
    count = 0

    print("Grabbing laptops...")

    # This for-loop iterates through each link found. Then it traverses each item link and grabs the item specifications.
    for link in links:
        try: 
            t_Client = uReq(link)
            prod_file = t_Client.read()
            
            # This does the same straining as discussed above. It strains each file, this was done for effeciency.
            label = strainer("td", {"class" : "label"})
            value = strainer("td", {"class" : "value"})  
            price = strainer("td", {"class" : "a-span12"})
            name = strainer("h1", {"class": "a-size-large a-spacing-none"}) 
            
            # Repeatedly parses the main html file for the rules set by the strainers
            l_Page = soup(prod_file,"lxml", parse_only=label)
            v_Page = soup(prod_file,"lxml", parse_only=value)
            price_page = soup(prod_file, "lxml", parse_only=price)
            name_page = soup(prod_file, "lxml", parse_only=name)
            
            # The function .find_all converts the list elements into lists.
            labels = l_Page.find_all("td", {"class" : "label"})
            values = v_Page.find_all("td", {"class": "value"})
            
            details = {}
            count = 0
            # This indicates which parts of the tables in each amazon page will be grabbed by the scrapper.
            grab = ["Hard Disk Size", "Graphics Coprocessor", "Processor Type", "Item Weight", "Maximum Display Resolution", "Memory Size", "Brand Name", "Series"]
            
            price = price_page.find("span", {"class" : "a-size-medium a-color-price"})
            name = name_page.find("span", {"class":"a-size-large"})
            
            # This grabs the prices, name, and link of the computer and puts them in a dictionary.
            details["price"] = price.text
            details["title"] = name.text.strip()
            details["link"] = link
            
            # This grabs in general all the tables and compares each table label to the grab list if it is a match append the label
            # as a key value and the text of table as a value in the dictionary.
            # This loop runs m amount of times. So over all this nested loop runs at m*n order.
            for l,v in zip(labels, values):
                if (l.text in grab):
                    count += 1
                    details[l.text] = v.text
            # if the amount of items that are added in the dictionary does not equal the length of the grab list 
            # Then the laptop requirements have not been met and the laptop is discarded.
            if (count >= 8):
                print("Laptop found")
                laptops.append(details)
            t_Client.close()

        except:
            pass

    return(laptops)

if __name__ == "__main__":
    links = web_environment(1)
    laptops = sort_and_pack(links)










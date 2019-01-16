import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from bs4 import SoupStrainer as strainer
import pickle
from time import sleep

def web_environment(choose):

    # main_url = 'https://www.amazon.ca/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=gaming+laptops&rh=i%3Aaps%2Ck%3Agaming+laptops'

    # main_url = 'https://www.amazon.ca/s/ref=nb_sb_noss?url=node%3D677252011&field-keywords=touchscreen+laptops&rh=n%3A667823011%2Cn%3A2404990011%2Cn%3A677252011%2Ck%3Atouchscreen+laptops'
    # main_url = 'https://www.amazon.ca/gp/search/ref=sr_pg_1?rh=n%3A667823011%2Cn%3A2404990011%2Cn%3A677252011%2Ck%3Athin+laptops&keywords=thin+laptops&ie=UTF8&qid=1543442369'
    
    if (choose == 1): # Gaming laptops
        main_url = 'https://www.amazon.ca/s/ref=s9_acss_bw_cg_Laptops_1c1_w?rh=i:electronics,n:677252011,k:Gaming&ie=UTF8&pf_rd_m=A1IM4EOPHS76S7&pf_rd_s=merchandised-search-4&pf_rd_r=1KX9XWS7BAZNDB21J1W3&pf_rd_t=101&pf_rd_p=485b441d-08ae-4633-8faa-39d773fa6f6c&pf_rd_i=677252011'
    elif(choose == 2): # Artist laptops
        main_url ='https://www.amazon.ca/s/s/ref=sr_nr_p_n_size_browse-bin_5?fst=as%3Aoff&rh=n%3A667823011%2Cn%3A2404990011%2Cn%3A677252011%2Ck%3Aconvertible%2Cp_n_size_browse-bin%3A7326921011&keywords=convertible&ie=UTF8&qid=1544062930&rnid=7326915011'
        #'https://www.amazon.ca/s/ref=nb_sb_noss_1?url=search-alias%3Delectronics&field-keywords=laptop+2+in+1&rh=n%3A6678#23011%2Ck%3Alaptop+2+in+1'
    elif (choose == 3): # Business laptops
        main_url = 'https://www.amazon.ca/s/gp/search/ref=sr_nr_p_n_feature_fourteen_1?fst=as%3Aoff&rh=n%3A667823011%2Cn%3A%21677211011%2Cn%3A2404990011%2Cn%3A677252011%2Cp_n_feature_two_browse-bin%3A7322166011%2Cp_n_feature_fourteen_browse-bin%3A7322419011&bbn=677252011&hidden-keywords=windows&ie=UTF8&qid=1543443506&rnid=7322417011'

    page_count = 0;
    try:
        header = {'User-Agent': 'Mozilla/61.0'}
        uClient = uReq(main_url) # Creates a client environment.
        html_file = uClient.read() # downloads the html file/ webpage
        uClient.close()
        products = strainer("div", {"class":"s-item-container"})
        page = soup(html_file,"lxml",parse_only=products) # parses and creates the soup
        links = []
        links = link_grab(page)
        page_count += 1; # need to use a page iterator if len not equal 10 in the laptop elements.

        return(links)
    except:
        print("unable to open link, please check internet connection and try again")

def link_grab(page):

    m_container = page.find_all("div", {"class":"s-item-container"}) # main container for the products. It contains the html parts of each laptop

    links = []
    print("Grabbing relevant laptops")
    for container in m_container:
        line = container.find("a", {"class": "a-link-normal a-text-normal"}) # This jumps
        if (line is not None):
            links.append(line['href']) # this 'href' is the key in the dictionary, and the dictionary returns the link
    # print(links)
    return(links)

def sort_and_pack(links):
    laptops = []
    count = 0
    # This for-loop is what causes it to be slow. I have a fix in mind, can be implemented.
    print("Packing laptops...")
    for link in links:
        try: # it was put in a try-statement because it can fail to open
            header = {'User-Agent': 'Mozilla/61.0'}
            t_Client = uReq(link) # this opens each link file and creates an instantaneous environement for one loop cycle
            prod_file = t_Client.read()
            
            label = strainer("td", {"class" : "label"})
            value = strainer("td", {"class" : "value"})  
            price = strainer("td", {"class" : "a-span12"})
            name = strainer("h1", {"class": "a-size-large a-spacing-none"}) 
            
            l_Page = soup(prod_file,"lxml", parse_only=label)
            v_Page = soup(prod_file,"lxml", parse_only=value)
            price_page = soup(prod_file, "lxml", parse_only=price)
            name_page = soup(prod_file, "lxml", parse_only=name)
            
            labels = l_Page.find_all("td", {"class" : "label"})
            values = v_Page.find_all("td", {"class": "value"})
            
            details = {}
            count = 0
            grab = ["Hard Disk Size", "Graphics Coprocessor", "Processor Type", "Item Weight", "Maximum Display Resolution", "Memory Size", "Brand Name", "Series"]
            
            price = price_page.find("span", {"class" : "a-size-medium a-color-price"})
            name = name_page.find("span", {"class":"a-size-large"})
            
            details["price"] = price.text
            details["title"] = name.text.strip()
            details["link"] = link
            
            for l,v in zip(labels, values):
                if (l.text in grab):
                    count += 1
                    details[l.text] = v.text
            if (count >= 8):
                count += 1
                laptops.append(details)
            t_Client.close()
            print("Laptop Found")

        except:
            #print("Failed link")
            pass

    return(laptops)
    # with open("laptops.scrape", "wb") as scraped:
    #     pickle.dump(laptops, scraped)


if __name__ == "__main__":
    links = web_environment(2)
    laptops = sort_and_pack(links)
    print(laptops)
    #with open("Artist2.laptops", "wb") as saved:
    #    pickle.dump(laptops, saved)

    # print(len(laptops))
    # print(laptops)
    # print(laptops[0])
    # print(len(laptops))









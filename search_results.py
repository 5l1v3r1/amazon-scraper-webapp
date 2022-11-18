import streamlit as st
from bs4 import BeautifulSoup
import requests

def scrape_search_page(url):
    #saves all the links in a list
    link = url 
    
    links_in_page , temp = [] , []

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

    page = requests.get(link, headers = header)

    soup = BeautifulSoup(page.content , "html.parser")

    soup1 = BeautifulSoup(soup.prettify(), "lxml")

    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})    

    for link in links:
        temp.append(link.get('href'))

    #cleaning an filtering links and crap links
    for i in temp:
        i = i.strip()
        if('sspa' not in i):
            links_in_page.append(i)

    return links_in_page
    

st.markdown(
'''
# Amazon Search Results Scraper

 Below are the funtionalities of this app:

* Get keyword from user
* Get the page number upto which user wants to scrape the results
* Display scraped links
* Save the product links in txt file

'''
)

#code to hide the hamburger menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


keyword = st.text_input("Enter the keyword :")

npages = st.text_input("Enter the number of pages to scrape :")
column1, column2 = st.columns(2)

display_links = column2.checkbox("Display Links")

save_links = column2.checkbox("Save Links")


if column1.button("Submit"):

    if display_links == 0 and save_links == 0:
        st.warning("Please select atleast one checkbox")
    
    else:
    
        if keyword and npages:
            
            st.text_area("STATUS","You have entered keyword : {} \nYou have entered the number of pages to scrape : {} \nESTIMATED TIME REMAINING : {} seconds".format(keyword, npages, int(npages)*3))
            
            search_term = keyword

            n_page = npages

            search_term = search_term.replace(" ", "+")

            base_page = "https://www.amazon.in/s?k=" + search_term


            input_links = []

            for i in range(1, int(npages) + 1):
                query = base_page + "&page=" + str(i)
                input_links.append(query)

            final = []

            for i in input_links:
                temp = scrape_search_page(i)
                final.extend(temp)

            links = []
            for raw in final:
                link = "https://www.amazon.in" + raw + "\n"
                links.append(link)
            
            s = ''.join(links)
            
            st.success(f'Successfully Scraped {len(links)} Product Links.')
            
            if display_links and save_links:
                st.write("Product Links :")
                st.write(s)
                st.download_button("Download Text File", s.encode('utf-8'), 'productlinks.txt', 'text/plain')            
            
            elif display_links:
                st.write("Product Links :")
                st.write(s)
            
            elif save_links:
                st.download_button("Download Text File", s.encode('utf-8'), 'productlinks.txt', 'text/plain')


        
        else:
            st.warning("Please enter valid Input")
                                        ################## LIBRARIES ###############
import requests
from bs4 import BeautifulSoup
import time
import datetime
                                        ################## CODE ###############


                    ## FUNCTION ##

def gtimg(x,tags):#x = page number // tags == specific tag.
    
    url = f'yoururlhere?page={x}&tags={tags}' # adjust page and tags(if any) for your needs.
    r = requests.get(url) # sends a GET request to your url. 
    sp = BeautifulSoup(r.content, 'html.parser')  
    images = sp.find_all('a',class_='directlink largeimg') #Select div/class
    for image in images:
        print(image['href'])#ITINERATE INSIDE THE CLASS SEARCHING FOR THE LINK.
    
    return
                    ## SESSION ##

def gtimg_session(x,tags):#Makes it work faster by using the same request for page you are in, instead of sending a new request for every image downloaded

    url = f'yoururlhere?page={x}&tags={tags}' 
    r = s.get(url)#STARTS THE SESSION
    sp = BeautifulSoup(r.content, 'html.parser')
    images = sp.find_all('a',class_='directlink largeimg')
    for image in images:
            zx = image['href'] 
            response = requests.get(zx) 
            print(f'Still Downloading... Page:',x,'Statuscode:',response.status_code) 
            filename = r'urfolderhere' + zx[zx.rfind('/'):]  #create the folder//name it
            with open(filename, 'wb') as f: 
                for chunk in response.iter_content(chunk_size=128): #builds the img
                    f.write(chunk) 
                    
if __name__ == '__main__': # execute the first function
    s = requests.session()
    start = datetime.datetime.now()
    tags = input('Tag: ') # LEAVE BLANK IF NONE
    page1 = int(input('First page: '))
    page2 = int(input('Second page: '))
    for x in range(page1,page2):
        gtimg_session(x,tags)
    finish = datetime.datetime.now() - start
    print(finish)
    total =(page2-page1)




#### ADJUST THE CODE ACCORDING TO THE WEBSITE YOU WANT TO SCRAPE IMAGES FROM ####

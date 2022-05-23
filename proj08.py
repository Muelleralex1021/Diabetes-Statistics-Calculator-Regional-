import csv
#Project 8 is a program that takes a file with a region's country population and number of diabetics and
#takes this data and sorts it into a dictionary of lists with the keys being the regions and the values
#being the lists of countries population and diabetics. it includes 4 functions. 1 that finds the diabetics
#per capita of the country, another two that finds the max and min per capita of a region and one that
#displays this information. the main function opens and reads the files then adds the per capita to each
#countries list and displays the information and a goodbye statement



from operator import itemgetter

def open_file():
    filename = input("Input a file: ") #prompts for file name
    done = False
    while not done:
        try:
            fp =  open(filename, encoding='utf-8') #tries to open file
            done = True
        except:
            print("Error: file does not exist. Please try again.") #if file cannot be opened error statement
            filename = input("Input a file: ") #reprompt
            
    return fp
        

def max_in_region(master_dictionary,region):
    max_list = [] #empty list
    for key,value in master_dictionary.items(): #iterate  through dictionary regions and lists
        if key == region: #seperates regions so that only specific countries are added to list
            for i in value: #iterate through lists
                max_list.append(i[3]) #append only the per capita value
                
    m_in_r = max((max_list)) #find the highest per capita
    c_ind = max_list.index(max(max_list)) #find index of per capita
    country = master_dictionary[region][c_ind][0] #using index of max per capita find the specific region and country
    tup = (country,m_in_r) #create tuple with max percapita and its country
    
    return tup
    
            
    

def min_in_region(master_dictionary,region):
    min_list = [] #empty list
    for key,value in master_dictionary.items(): #iterate  through dictionary regions and lists
        if key == region: #seperates regions so that only specific countries are added to list
            for i in value:#iterate through lists
                if i[3]>0: # if per capita is not zero
                    min_list.append(i[3]) #append only the per capita value
                
    m_in_r = min((min_list)) #find the highest per capita that is not zero
    for key,value in master_dictionary.items(): #iterate  through dictionary regions and lists
        if key == region:#seperates regions so that only specific countries are added to list
            for i in value:#iterate through lists
                if i[3] == m_in_r: #if this countries per capita is equal to the lowest per capita
                    country = i[0] #this is country with lowest per capita
    
    tup = (country,m_in_r) #create tuple with max percapita and its country
    
    
    return tup

def read_file(fp):
    country_info = []#empty list
    master_dictionary = {} #create dictionary
    reader = csv.reader(fp) #open file and give variable name
    next(reader,None) #skip header
    for L in reader: # for line in file
        region = L[1] #name regions
        country = L[2] #name country
        population = L[5] #name population
        diabetes = L[9] #name diabetes
        
        try:
            population = str(population) #turn population into string so that i can remove comma and turn it into a float
            population = population.replace(',','')
            population = float(population)
        except:
            continue
        
        try:
            diabetes = str(diabetes) #turn diabetes into string so that i can remove comma and turn it into a float
            diabetes = diabetes.replace(',','')
            diabetes = float(diabetes)
        except:
            continue
        
        
        tup_list = [country,diabetes,population] #make list of countries name diabetes and population
        if region in master_dictionary: #for each region in master dictionary
            master_dictionary[region].append(tup_list) #append that regions countries to list in dictionary
        if region not in master_dictionary: # if region not yet in master dictionary
            master_dictionary[region] = country_info #add region as key
            master_dictionary[region].append(tup_list) #append country list to region
        country_info = [] #empty list for each new country
        
        master_dictionary[region].sort() #sort alphabetically

        
    return master_dictionary    
    



def add_per_capita(master_dictionary):
    for region, c_info in master_dictionary.items(): #for each key and value in master dictionary
        for value in c_info: #for each value in country's list
            per_c = value[1]/value[2] #find per capita number
            value.append(per_c) #append the per capita value to each country

    return master_dictionary
              

    

def display_region(master_dictionary,region): #this function gave me a lot of trouble as I would create two tables but they included all regions and all countries
    print("{:<37s} {:>9s} {:>12s} {:>11s}".format("Region","Cases","Population","Per Capita")) #print header
    for key,value in master_dictionary.items(): #iterate through master dictionary
        if key == region: #if country name is actually the whole region this is also to solve my trouble with printing all regions and countries
            for i in value: #iterate through the whole regions list
                if i[0] == key: #if country is actually the whole regions data
                    print("{:<37s} {:>9.0f} {:>12,.0f} {:>11.5f}".format(key,i[1],i[2],i[3])) #print whole regions data
                
    print()
    print("{:<37s} {:>9s} {:>12s} {:>11s}".format("Country","Cases","Population","Per Capita")) #print header
    for key,value in master_dictionary.items(): #iterate through master dictionary
        if key == region: #if country name is actually the whole region this is also to solve my trouble with printing all regions and countries
            master_dictionary[region].sort(key = itemgetter(3),reverse = True) #sort lists from greatest per capita to lowest
            for i in value: #iterate through each country's lists
                if i[0] != key: #skip whole regions data
                    print("{:<37s} {:>9.1f} {:>12,.0f} {:>11.5f}".format(i[0],i[1],i[2],i[3])) #print countries name, cases, population, and per capita
            
    print("\nMaximum per-capita in the {} region".format(region)) # max per capita header with specific region
    print("{:<37s} {:>11s}".format("Country","Per Capita")) #print header
    
    max_country, max_perc = (max_in_region(master_dictionary,region)) #use pervious function to find the max per capita country and per capita number
    print("{:<37s} {:>11.5f}".format(max_country, max_perc)) #print country name and per capita
    
    print("\nMinimum per-capita in the {} region".format(region)) # min per capita header with specific region
    print("{:<37s} {:>11s}".format("Country","Per Capita")) #print header
    min_country, min_perc = (min_in_region(master_dictionary,region)) #use pervious function to find the min per capita country and per capita number
    print("{:<37s} {:>11.5f}".format(min_country, min_perc)) #print country name and per capita
    print()
 
    
    
def main():
    fp = open_file() #call open file function and name file
    master_dictionary = read_file(fp) #call read file function and name master dictionary
    master_dictionary = add_per_capita(master_dictionary) #update master dictionary with per capita values
    for region in master_dictionary.keys(): #iterate through each region in master dictionary
        print("Type1 Diabetes Data (in thousands)") #print header
        display_region(master_dictionary,region) #call display function
        print('-'*72) #print seperator for each region
    print('\n Thanks for using this program!\nHave a good day!') #print goodbye statement
    

# These two lines allow this program to be imported into other code
# such as our function_test code allowing other functions to be run
# and tested without 'main' running.  However, when this program is
# run alone, 'main' will execute.  
if __name__ == "__main__": 
    main()
                    
                    
                    
                
                
                
                
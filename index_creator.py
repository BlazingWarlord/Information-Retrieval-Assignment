#Index_Creator

#Modules Needed
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import os
from PyPDF2 import PdfReader

#Read The PDF and Extract Text

def ExtractPDF(filename):
    global pages
    pages = []
    
    #Reads the PDF in given path
    reader = PdfReader(f'Assignment-1 (1)/SamplePolicyDocs/Auto/{filename}') 

    for i in range(0,len(reader.pages)):
        # getting pages from the pdf file one by one
        page = reader.pages[i]
        
        # extracting text from page
        text = page.extract_text()

        #storing page by page text in a list
        pages.append(text)
    

#Generating the Index
def IndexGenerator():

    #Iterating through the folder to get all pdfs from given path
    for file in os.listdir("Assignment-1 (1)/SamplePolicyDocs/Auto/"):

        #Generate page by page data from ExtractPage function defined above
        ExtractPDF(file)

        #Creating the index for current document
        index = {}

        new_page_data = []


        #Taking page by page data and removing unnecessary words and punctuation

        for page_data in pages:
            stop_words = set(stopwords.words('english'))
            stop_words = []
            filtered_page_data = ''
            for word in page_data.split(' '):
                word = word.replace(',','')
                word = word.replace('.','')
                word = word.replace('(','')
                word = word.replace(')','')
                word = word.replace('-','')
                word = word.replace(';','')
                word = word.replace('\'','')
                word = word.replace('"','')
                word = word.replace('_','')
                word = word.replace('\n','')
                if word.casefold() not in stop_words:
                    filtered_page_data += word
                    filtered_page_data += ' '

            ind = pages.index(page_data)
            pages[ind] = filtered_page_data

        #Adding word to index if not yet added or adding page number to word
        for page in pages:
            for word in page.split(' '):
                if word.casefold() in index:
                    index[word.casefold()].add(pages.index(page))
                else:
                    index[word.casefold()] = set([pages.index(page)])
        index_list[file] = index


#Dictionary to contain document by document indices
index_list = {}

#Creating Index Document by Document
IndexGenerator()


#Get Query
query = input("Enter Query: ")

result = {}


#Iterate through the overall index to find all documents with query word. If yes, returns all pages with the query, else returns nothing
for word in query.split(' '):
    for file_name in index_list:
        if(file_name in result):
            if word.casefold() in index_list[file_name]:
                result_set = result[file_name].union(set(index_list[file_name][word.casefold()]))
                result[file_name] = result_set
        else:
            result[file_name] = set()
            if word.casefold() in index_list[file_name]:
                result_set = result[file_name].union(set(index_list[file_name][word.casefold()]))
                result[file_name] = result_set   
            
        
#Result will be a dictionary with keys as document names and values as a set of all pages where any query word was found
print(result)


    
    

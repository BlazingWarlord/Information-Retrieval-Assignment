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
    reader = PdfReader(f'C:/Users/11110/Downloads/Assignment-1 (1)/SamplePolicyDocs/Auto/{filename}') 

    for i in range(0,len(reader.pages)):
        # getting pages from the pdf file one by one
        page = reader.pages[i]
        
        # extracting text from page
        text = page.extract_text()

        #storing page by page text in a list
        pages.append(text)

    #print(text,repr(text)[1:-1])
    

#Generating the Index
def IndexGenerator():

    #Iterating through the folder to get all pdfs from given path
    for file in os.listdir("C:/Users/11110/Downloads/Assignment-1 (1)/SamplePolicyDocs/Auto/"):

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


#Function to normalize query
def Normalize(query):

    #Import required functions from nltk
    #nltk.download("stopwords")
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer

    stemmer = PorterStemmer()

    #nltk.download('punkt')
    #nltk.download('averaged_perceptron_tagger')

    
    #Find all tokens (words) from the query
    tokens = nltk.word_tokenize(query)

    filtered_query = []

    #Get stop words list and add only non stopwords to filtered_query
    stop_words = set(stopwords.words('english'))
    for word in tokens:
        if word.casefold() not in stop_words:
            filtered_query.append(word)

    #Return a final filtered_query
    return filtered_query

#Retrieve Data chunk by chunk
def ParagraphRetriever(filename,page_number,query):
    
    #Read PDF and extract data by page. Both PDF name and page number given as parameters for the function 
    reader = PdfReader(f"C:/Users/11110/Downloads/Assignment-1 (1)/SamplePolicyDocs/Auto/{filename}")
    page = reader.pages[page_number]
    text = page.extract_text()

    #Split entire data by breaks
    paragraphs = text.split('\n')

    #Check which paragraph(s) has the query in it and return 2 lines before and after if existing else returns that line alone
    for i in range(0,len(paragraphs)):
        if query in paragraphs[i]:
            try:
                return paragraphs[i-2] + paragraphs[i-1]+paragraphs[i]+paragraphs[i+1]+paragraphs[i+2]
            except:
                return paragraphs[i]

            

#Dictionary to contain document by document indices
index_list = {}

#Creating Index Document by Document
IndexGenerator()


#Get Query
query = input("Enter Query: ")

normalized_query = Normalize(query)

result = {}


#Iterate through the overall index to find all documents with query word. If yes, returns all pages with the query, else returns nothing
for word in normalized_query:
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
                
#print(result)


#Iterate through result, each word in normalized_query, and page_number from result set and execute ParagraphRetriever with the above as parameters                
for file_name in result:
    result_paras = set()
    for word in normalized_query:
        for page_number in result[file_name]:
            #Adding result paragraph to final set
            result_paras.add(ParagraphRetriever(file_name,page_number,word))

    #Take each paragraph in final_set and print it. Try except here is to handle null
    for para in result_paras:
        try:
            print(file_name+":  "+para+'\n')
        except:
            print()



    
    
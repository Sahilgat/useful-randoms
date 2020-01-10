from bs4 import BeautifulSoup
import requests

def get_book_names():
    bookNames = []
    userInput = None
    
    # Loop to get book names
    while userInput != 'done':
        userInput = input("Enter the book name or 'done' if done!\n")
        if (userInput == 'done'):
            return bookNames
        else:
            bookNames.append(userInput)
    # Check that at least one value provided
    if (len(bookNames) == 0):
        raise ValueError("No book names provided!")
    return bookNames

def create_urls_from_book_names(bookNames = [], *args):
    startURL = "http://gen.lib.rus.ec/search.php?req="
    endURL = "&open=0&res=25&view=simple&phrase=1&column=def"
    finalURLs = []
    for bookName in bookNames:
        arguements = bookName.replace(" ", "+")
        finalURLs.append(startURL + arguements + endURL)
    return finalURLs


def main():
    # Gets user book names
    bookNames = get_book_names()
    finalURls = create_urls_from_book_names(bookNames)
    # print (finalURls)

    # Connects to Libgen
    for URL in finalURls:
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'lxml')
        tables = soup.findChildren('table')
        searchResults = tables[2]
        resultRows = searchResults.findChildren('tr')

        # Using dictionary so only one link of each file type
        formatLinkDictionary = {}

        # Skip header row
        for row in resultRows[1:]:
            cells = row.findChildren('td')
            formatLinkDictionary[cells[8].string] = cells[9].find('a').get('href')

        # Try different file types in order of priority
        if "epub" in formatLinkDictionary:
            URLPre = formatLinkDictionary["epub"][:20]
            finalsource = requests.get(formatLinkDictionary["epub"]).text
            soup = BeautifulSoup(finalsource, 'lxml')
            tables = soup.findChildren('table')
            table = tables[0]
            resultRows = table.findChildren('tr')
            cells = resultRows[0].findChildren('td')
            URLPost = cells[1].find('a').get('href')
            downloadLink = URLPre + URLPost
            book = requests.get(downloadLink)
            name = input("What would you like to name this book?\n") # Name to file conventions
            open("C:\\Users\\nisga\\OneDrive\\Desktop\\Books\\" + name + ".epub", 'wb').write(book.content)
            
        else:
            print("No epub file format found!")
main()
# Check if same if not using adblocker webpage
# Add exception if no results found
# Archive links so can try others if more than one available
# Parallelize this?
# Modularize into methods
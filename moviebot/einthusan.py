import requests
from bs4 import BeautifulSoup
import wget


def downloadLink(einthusan_url: str) -> str:
    """ Gets the download link for the einthusan player url """
    url = 'https://qdownloader.io/download?download={}'.format(einthusan_url)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    download_url = soup.find('a', {'class': 'downloadBtn'})['href']
    return download_url


def einthusanDetails(query: str) -> str:
    """ Gets the einthusan player url for the query given """
    url = 'https://einthusan.tv/movie/results/?lang=tamil&query={}'.format(
        query)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    elem = soup.find('li')
    playerlink = 'https://einthusan.tv' + elem.find('a')['href']
    moviename = elem.find('h3').text
    downloadlink = downloadLink(playerlink)
    # posterlink = 'https://' + elem.find('img')['src'].replace('//','')
    # moviesynopsis = elem.find('p',{'class' : 'synopsis'}).text
    # trailerlink = elem.find_all('a')[-1]['href']
    return moviename, downloadlink


def downloadMovie(movie_name: str, download_link: str):
    download_directory = 'Movies'
    output_file = download_directory + '/' + movie_name + '.mp4'
    wget.download(download_link, output_file)


if __name__ == "__main__":
    query = input("Which movie would you like to download? ")
    movie_name, einthusan_link = einthusanDetails(query)
    downloadMovie(movie_name, einthusan_link)

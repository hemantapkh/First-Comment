import requests
import re, json
from time import sleep
from bs4 import BeautifulSoup

def url2Id(url):
    try:
        return re.search(r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)", url).group(0)
    except AttributeError:
        raise Exception('Invalid URL')

class firstComment():
    def __init__(self, rawURL, wait=False):
        self.videoId = url2Id(rawURL)
        self.reqObject = requests.get(f'https://first-comment.com/v/{self.videoId}')
        self.soup =  BeautifulSoup(self.reqObject.content, 'html.parser')
        
        while True:
            if wait and not self.inDatabase:
                sleep(3)
                self.reqObject = requests.get(f'https://first-comment.com/v/{self.videoId}')
                self.soup =  BeautifulSoup(self.reqObject.content, 'html.parser')
            else:
                break
                 
    @property
    def title(self):
        try:
            return  self.soup.find("meta",  property="og:title").get('content')
        except AttributeError:
            raise Exception('Invalid URL')
    
    @property
    def inDatabase(self):
        if self.soup.find("h2", {"class": "text-center"}).contents[0].strip() == 'You are lucky, we already read all of its comments !':
            return True
        else:
            return False
    
    @property
    def luckMsg(self):
        return self.soup.find("h2", {"class": "text-center"}).contents[0].strip()
    
    @property
    def comment(self):
        return self.soup.find("div", {"class": "font-weight-normal"}).contents[0].strip()
    
    @property
    def author(self):
        return self.soup.find("span", {"class": "font-weight-bold"}).contents[1].contents[0].strip()
    
    @property
    def authorChannelUrl(self):
        return self.soup.find("span", {"class": "font-weight-bold"}).contents[1]['href']
    
    @property
    def publishedDate(self):
        return self.soup.find("span", {"class": "font-weight-light"}).contents[1].contents[0].strip()
    
class ytApi():
    def __init__(self,apiKey):
        self.apiKey = apiKey
        
    
    def start(self,rawURL ,nextPageToken=None):
        videoId = url2Id(rawURL)
        firstTime = True
        while True:
            if firstTime and not nextPageToken:
                response = requests.get(f"https://www.googleapis.com/youtube/v3/commentThreads?key={self.apiKey}&textFormat=plainText&part=snippet&videoId={videoId}&maxResults=100")
                self.jsn = json.loads(response.text)
                
                firstTime = False
                try:
                    nextPageToken = self.jsn['nextPageToken']
                except KeyError:
                    break
            
            else:
                response = requests.get(f"https://www.googleapis.com/youtube/v3/commentThreads?key={self.apiKey}&textFormat=plainText&part=snippet&videoId={videoId}&maxResults=100&pageToken={nextPageToken}")
                self.jsn = json.loads(response.text)
                
                try:
                    nextPageToken = self.jsn['nextPageToken']
                except KeyError:
                    break
    @property
    def comment(self):
        return self.jsn['items'][-1]['snippet']['topLevelComment']['snippet']['textOriginal']
    
    @property
    def author(self):
        return self.jsn['items'][-1]['snippet']['topLevelComment']['snippet']['authorDisplayName']
    
    @property
    def authorChannelUrl(self):
        return self.jsn['items'][-1]['snippet']['topLevelComment']['snippet']['authorChannelUrl']
    
    @property
    def publishedDate(self):
        return self.jsn['items'][-1]['snippet']['topLevelComment']['snippet']['publishedAt']
    
    @property
    def likeCount(self):
        return self.jsn['items'][-1]['snippet']['topLevelComment']['snippet']['likeCount']
    
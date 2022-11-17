# CSIRTbot by Michele Barp
# this bot read the news from a RSS feed and post them to a Mastodon profile

from mastodon import Mastodon
import feedparser

# RSS URL
csirt_url = 'https://www.csirt.gov.it/data/indexer/rss'

# Set up Mastodon connection
mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://mastodon.uno/'
)

# Feed Parser
d=feedparser.parse(csirt_url)
last_guid=-1

# Open file for read where the last posted entry GUID is saved
try:
    f=open('lastpostguid.txt','r')
    lastpostguid=f.readline()
    f.close()
except:
    print("file inesistente")
    lastpostguid='inesistente'
    last_guid=(len(d['entries']))-1

# Search for last posted entry
for n in range((len(d['entries'])-1),-1,-1):
    if d.entries[n].guid == lastpostguid:
        print(n)
        last_guid=n-1

# Post to mastodon all entry after the last posted one
if (last_guid>=0):
    for y in range(last_guid, -1, -1):
        post=(d.entries[y].title+"\n"+d.entries[y].description+"\n"+d.entries[y].link)
        print(post)
        mastodon.status_post(post)
        # save last post guid
        f=open('lastpostguid.txt','w')
        f.write(d.entries[y].guid)
        f.close()

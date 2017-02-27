from webutils import *
import re,sys,urllib
from addon.common.addon import Addon
addon = Addon('plugin.video.nbafullgames', sys.argv)
from log_utils import log

base_url='http://www.nbahd.net'


from modules.log_utils import log

def get_games(site):
    html=read_url(site)
    soup=get_soup(site)
    items=soup.findAll('div',{'class':'thumb'})
    out=[]
    for item in items:
        url=item.find('a')['href']
        title=item.find('a')['title']
        thumb=item.find('img')['src']
        out+=[[title,url,thumb]]
    try:
        next_page=re.findall('<a.+?rel="next".+?href="(.+?)"',html)[0]
        if 'nbahd' not in next_page:
            next_page = base_url + next_page
    except:
        next_page='0'
    return out,next_page


def get_teams():
    team_list = [[u'http://nbahd.net/?s=76ers', u'Philadelphia 76Ers', u'http://i.imgur.com/KtSDfDX.png'], 
        [u'http://nbahd.net/?s=blazers', u'Portland Trail Blazers', u'http://i.imgur.com/fLa6krI.png'], 
        [u'http://nbahd.net/?s=bucks', u'Milwaukee Bucks', u'http://i.imgur.com/4rMpMsV.png'], 
        [u'http://nbahd.net/?s=bulls', u'Chicago Bulls', u'http://i.imgur.com/RpF3amJ.png'], 
        [u'http://nbahd.net/?s=cavaliers', u'Cleveland Cavaliers', u'http://i.imgur.com/1B2LieQ.png'], 
        [u'http://nbahd.net/?s=celtics', u'Boston Celtics', u'http://i.imgur.com/9poCmBL.png'], 
        [u'http://nbahd.net/?s=clippers', u'Los Angeles Clippers', u'http://i.imgur.com/SEwO6KA.png'], 
        [u'http://nbahd.net/?s=grizzlies', u'Memphis Grizzlies', u'http://i.imgur.com/651AtvO.png'], 
        [u'http://nbahd.net/?s=hawks', u'Atlanta Hawks', u'http://i.imgur.com/PKXfzFb.png'], 
        [u'http://nbahd.net/?s=heat', u'Miami Heat', u'http://i.imgur.com/uiT6LZV.png'], 
        [u'http://nbahd.net/?s=hornets', u'Charlotte Hornets', u'http://i.imgur.com/ZaTTvAt.png'], 
        [u'http://nbahd.net/?s=jazz', u'Utah Jazz', u'http://i.imgur.com/5pw1NIR.png'], 
        [u'http://nbahd.net/?s=kings', u'Sacramento Kings', u'http://i.imgur.com/NfvLz4g.png'],
        [u'http://nbahd.net/?s=knicks', u'New York Knicks', u'http://i.imgur.com/VDv8ntK.png'], 
        [u'http://nbahd.net/?s=lakers', u'Los Angeles Lakers', u'http://i.imgur.com/1p3nEZu.png'], 
        [u'http://nbahd.net/?s=magic', u'Orlando Magic', u'http://i.imgur.com/0dqVPuU.png'], 
        [u'http://nbahd.net/?s=mavericks', u'Dallas Mavericks', u'http://i.imgur.com/P1tPEpC.png'], 
        [u'http://nbahd.net/?s=nets', u'Brooklyn Nets', u'http://i.imgur.com/EVVastT.png'], 
        [u'http://nbahd.net/?s=nuggets', u'Denver Nuggets', u'http://i.imgur.com/B6Gyq3Z.png'], 
        [u'http://nbahd.net/?s=pacers-/', u'Indiana Pacers', u'http://i.imgur.com/glh7tDS.png'], 
        [u'http://nbahd.net/?s=pelicans', u'New Orleans Pelicans', u'http://i.imgur.com/XvqBSFK.png'], 
        [u'http://nbahd.net/?s=pistons', u'Detroit Pistons', u'http://i.imgur.com/Ze2GGX0.png'], 
        [u'http://nbahd.net/?s=raptors', u'Toronto Raptors', u'http://i.imgur.com/4ZFUqRD.png'], 
        [u'http://nbahd.net/?s=rockets', u'Houston Rockets', u'http://i.imgur.com/BuXlW6e.png'], 
        [u'http://nbahd.net/?s=spurs', u'San Antonio Spurs', u'http://i.imgur.com/9M775dI.png'], 
        [u'http://nbahd.net/?s=suns', u'Phoenix Suns', u'http://i.imgur.com/001dpsM.png'], 
        [u'http://nbahd.net/?s=thunder', u'Oklahoma City Thunder', u'http://i.imgur.com/M1vLzwN.png'], 
        [u'http://nbahd.net/?s=timberwolves', u'Minnesota Timberwolves', u'http://i.imgur.com/VgjbiWm.png'], 
        [u'http://nbahd.net/?s=warriors', u'Golden State Warriors', u'http://i.imgur.com/Frs8DtL.png'], 
        [u'http://nbahd.net/?s=wizards', u'Washington Wizards', u'http://i.imgur.com/X4UagVO.png']]

    lista = sorted(team_list,key=lambda x: x[1])
    team_links = [[x[1],x[0],x[2]] for x in lista]
    return team_links



def get_title(url):
    soup=get_soup(url)
    return soup.find('div',{'class':'entry-content rich-content'}).findAll('p')[0].getText().replace('Watch ','')
def get_urls(url,option):
    soup=get_soup(url)
    tags=soup.find('div',{'class':'entry-content rich-content'}).findAll('p')
    tags.pop(0)
    tags.pop(-1)
    tag=tags[option]
    
    tmp=tag.findAll('a')
    urls=[]

    for t in tmp:
        urls+=[t['href']]

    return urls

def get_link_hd(url):

    if 'nbahd' in url:
        return url,False
    html=read_url(url)
    ref = url
    base = 'wefights.com'
    if 'wtutor' in url:
        base = 'play.wtutor.net'
    urls = re.findall('data-link=[\"\']([^\"\']+)[\"\']',html)
    url = 'http://%s/wp-admin/admin-ajax.php?action=ts-ajax&p=%s&n=1'%(base,urllib.quote(urls[0]))
    html = read_url(url)
    
    videos = re.findall('file\s*:\s*[\"\']([^\"\']+).+?label\s*:\s*[\"\'](\d+)p[^\}]',html)
    videos.sort(key=lambda x: x[1],reverse=True)

    HD = addon.get_setting('enable_hd')=='true'
    if HD:
        return videos[0][0],True
    else:
        for v in videos:
            if v[1]!='720' and v[1]!='1080':
                return v[0],True


    
        

def get_parts(url):
    log(url)
    if 'nbahd' not in url:
        url = base_url + url

    html = read_url(url)
    soup = get_soup(url)
    out=[]
    urls = []
    subs = ['GVIDEO','ALTERNATIVE']
    gvideos = []
    for i in range(1,5):
        gvideos += re.findall('(http://play.wtutor.net/cgi-bin/ProtectFile.File[^\"\']+)[\"\'] target="_blank"><img src=[\"\'](http://nbahd.(?:net|com)/wp-content/uploads/2015/04/p(%s).png)[\"\']'%i,html)



    
    for i in range(1,5):
        gvideos += re.findall('href=[\"\'](http://wefights.com[^\"\']+)[\"\'] target="_blank"><img src=[\"\'](http://nbahd.(?:net|com)/wp-content/uploads/2015/04/p(%s).png)[\"\']'%i,html)

    for i in range(1,5):
        gvideos += re.findall('href=[\"\'](http://nbahd.(?:net|com)/[^\"\']+)[\"\'] target="_blank"><img src=[\"\'](http://nbahd.(?:net|com)/wp-content/uploads/2015/04/p(%s).png)[\"\']'%i,html)

    for v in gvideos:
        url = v[0]
        sub = subs[0]
        if 'nbahd' in url:
            sub = subs[1]


        title = 'Part %s %s'%(v[2],sub)
        img = v[1]
        if url not in urls:
            out.append((title,url,img))
            urls.append(url)
    return out

def get_game_options(url):
    soup=get_soup(url)
    tags=soup.find('div',{'class':'entry-content rich-content'}).findAll('p')
    tags.pop(0)
    tags.pop(-1)
    options=[]
    for tag in tags:
        try:
            title=''
            title=re.compile('src="http://(?:nba|NBA|nfl|NFL)hd.(?:com|net)/wp-content/uploads/(.+?).png"').findall(str(tag))[0].title()

            if 'p1' in title.lower() or 'p2' in title.lower() or 'p3' in title.lower() or 'p4' in title.lower():
                return
            tmp=tag.findAll('a')
            urls,titles=[],[]
            for t in tmp:
                url=t['href']
                title2=t.getText()
                titl=title+' '+title2
                options+=[[titl,url]]
        except:
            pass
    return options

def resolve_nbahd(url):
    try:
        html=read_url(url)
        urls = re.findall('iframe.+?src=[\"\']([^\"\']+)[\"\']',html)
        import urlresolver
        for url in urls:
            try:
                resolved = urlresolver.resolve(url)
            except:
                resolved = False
            if resolved:
                break
        return resolved
    except:
        return ''

def getlink_nbahd(link):
    link=link.replace('temporarylink.net','moevideo.net')
    if 'nbahd.net' not in link:
        return link,True
    resolved=resolve_nbahd(link)
    if resolved:
        return resolved,False
    soup=get_soup(link)
    link=soup.find('iframe',{'frameborder':'0'})['src']
    return link,True
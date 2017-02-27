from modules import client
import re,sys
from addon.common.addon import Addon
addon = Addon('plugin.video.nbafullgames', sys.argv)

class zunox():
    def __init__(self):
        self.base = 'http://zunox.hk'
        self.html = client.request('http://sportsnation.xyz/scheduleframe.php')

    def get_basketball_events(self):
        reg = re.compile('<li\s*(?:id="hd")?><a\s*href="([^"]+)"\s*target="\s*(?:slipframe|_*blank|_self)"\s*id="NBA"><span\s*id="title">\s*([^<]+)\s*</span>\s*<span\s*id="time">\s*[^<]*?(\d{1,2}:\d\d\s*\w\w)\/(?:bst|gmt)[^<]*?\s*</span>')
        events = re.findall(reg,self.html)
        events = self.__prepare_events(events)
        return events

    @staticmethod
    def convert_time(time):
        pm = False
        if 'PM' in time:

            pm = True
        li = time.replace(' PM','').replace(' AM','').replace('PM','').replace('AM','').split(':')
        hour,minute=li[0],li[1]
        if int(hour) == 12 and not pm:
            hour = 0
        if pm and hour !='12':
            hour = int(hour) + 12


        import datetime
        from resources.lib.modules import pytzimp
        d = pytzimp.timezone(str(pytzimp.timezone('Europe/London'))).localize(datetime.datetime(2000 , 1, 1, hour=int(hour), minute=int(minute)))
        timezona= addon.get_setting('timezone_new')
        my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
        convertido=d.astimezone(my_location)
        fmt = "%H:%M"
        time=convertido.strftime(fmt)
        return time

    def __prepare_events(self,events):
        new = []
        for event in events:
            url = self.base + event[0]

            title = event[1]
            time = self.convert_time(event[2])
            title = '[COLOR orange](%s)[/COLOR] %s'%(time,title)
            new.append((url,title))

        return new
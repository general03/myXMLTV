# -*- coding: utf-8 -*-
import sys

from dateutil.parser import parse
from lxml import etree


def b_decorate(func):
    def func_wrapper(self, sentence):
        sentenceFormatted = ''
        for word in self.keyword:
            sentenceFormatted += sentence.lower().replace(word, "<b>"+word+"</b>")
        return sentenceFormatted
    return func_wrapper


class myXMLTV:

    SEPARATOR = ','

    FORMAT_DATE_OUT = '%A %d %b %H:%M'

    result = []

    channelXML = {}
    channelXMLReverse = {}

    founded = False

    def __init__(self):
        # To display day in FR
        # locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
        # Keyword to search, first argument separated by special character
        self.keyword = None
        if(len(sys.argv) == 2):
            self.keyword = sys.argv[1].lower().split(self.SEPARATOR)

        # Channel to search, second argument separated by special character 
        self.channel = None
        if(len(sys.argv) == 3):
            self.channel = sys.argv[2].lower().split(self.SEPARATOR)

    def scan(self):
        print('Scanning tv guide ...')
        tree = etree.parse("http://www.xmltv.fr/guide/tvguide.xml")
        print('Analyzing tv guide ...')

        for channel in tree.xpath("/tv/channel"):
            self.channelXML.update({channel.get('id'): channel.find('display-name').text.lower() });

        self.channelXMLReverse = {v: k for k, v in self.channelXML.items()}

        for programme in tree.xpath("/tv/programme"):
            movie = {}
            self.founded = False

            matchChannel = self.channelXML.get(programme.get("channel"))
            if (self.channel is None or matchChannel in self.channel):
                    movie.update({'channel': matchChannel})
            else:
                continue

            movie.update({'start': programme.get("start")})
            movie.update({'end': programme.get("stop")})

            for child in programme.getchildren():
                if(child.tag in ('title', 'sub-title', 'desc', 'date')):
                    if (self.keyword is None or any(x in child.text.lower() for x in self.keyword)):
                        movie.update({child.tag: child.text})
                        self.founded = True

                if child.tag == 'icon':
                    movie.update({child.tag: child.get('src')})

                if child.tag == 'length':
                    movie.update({child.tag: child.text + ' ' + child.get('units')})

            if(self.founded):
                self.result.append(movie)

        return sorted(self.result, key=lambda k: k['start'])

    @b_decorate
    def get_text(self, text):
        return text

    def get_img_channel(self, channel):
        id_channel = filter(str.isdigit, self.channelXMLReverse.get(channel))
        if(channel is None or not id_channel):
            return channel.capitalize()
        else:
            return '<img src="http://television.telerama.fr/sites/tr_master/files/sheet_media/tv/500x500/'+ id_channel +'.png" width="50px" alt="'+ channel.capitalize() +'" style="vertical-align:middle;">'

    def display ( self, data ):
        htmlContent = '<table>'
        for programme in data:         
            htmlContent += '<tr><td> <img src="' + programme.get('icon', 'http://via.placeholder.com/250x150?text=Pas+d+image') + '" width="250px" > </td>'
            htmlContent += '<td>' + self.get_img_channel(programme.get('channel', None))
            htmlContent += '<span>' + parse(programme.get('start', '')).strftime(self.FORMAT_DATE_OUT) + ' (' + programme.get('length', '') + ')</span> <br />'
            htmlContent += self.get_text(programme.get('title', '')) + '<br />'
            htmlContent += self.get_text(programme.get('sub-title', '')) + '<br />'
            htmlContent += self.get_text(programme.get('desc', '')) + '<br />'
            htmlContent += '</td></tr>'

        htmlContent += '</table>'

        file = open("index.html", "w")
        file.write(htmlContent.encode('utf-8'))
        file.close()

        return htmlContent


custom = myXMLTV()
custom.display(custom.scan())

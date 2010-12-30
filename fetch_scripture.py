from BeautifulSoup import BeautifulSoup, NavigableString
from esv import *

def strip_tags(html, invalid_tags):
    """
    Modified and used from:
    http://stackoverflow.com/questions/1765848/remove-a-tag-using-beautifulsoup-but-keep-its-contents
    """
    soup = BeautifulSoup(html)
    for tag in soup.findAll(True):
        if tag.name not in invalid_tags:
            s = ""
            for c in tag.contents:
                if type(c) != NavigableString:
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)
            tag.replaceWith(s)
        else:
            tag.extract()
    return soup.renderContents()

class ESV:

    def __init__(self, key='IP'):
        self.api = ESVWebServiceAPI(key=key)

    def get_verses(self, passage=''):
        """
        Takes a passage and returns a list of the verse, it's chapter, and it's contents
        """
        verse_xml = self.api.passage_query(format='xml', passage=passage).read()
        soup = BeautifulSoup(verse_xml)
        verses = soup('verse-unit')
        
        current_chapter = 0
        verse_list = []

        for verse in verses:
            # Get current chapter
            chapter = soup('current')[0].contents[0]
            if len(chapter) > 0:
                current_chapter = chapter

            current_verse = verse('verse-num')[0].contents[0]
            
            # Verse contents are stored in <marker> tags
            marker_contents = str(verse('marker')[0].renderContents())
            
            # Strip out all of the unnecessary tags
            verse_contents = strip_tags(marker_contents, ['verse-num', 'footnote', 'heading'])

            verse_list.append({
                'chapter': current_chapter,
                'verse': current_verse,
                'contents': verse_contents.rstrip("\r\n").strip('\n')
            })
        
        return verse_list
        
if __name__ == '__main__':
    e = ESV(key='TEST')
    print e.get_verses('John 3:16')
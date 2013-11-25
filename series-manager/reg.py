__author__ = 'ronnie'
class PageProcessList():

    def __init__(self):
        self.page = urllib.request.urlopen(
            "http://www.animetake.com/anime-downloads/")
        self.page_string = self.page.read().decode('utf-8')

    def load_items(self):
        anime_links_names = re.findall(
            r'<li\b[^>]*>(.*?)</li>', self.page_string)
        anime_names = []
        anime_database = {}
        for string in anime_links_names:
            link = None
            name = None
            link = re.findall(r'href="(.*?)"', string)
            name = re.findall(r'<a\b[^>]*>(.*?)</a>', string)[
                0]  # findall returns a list
            anime_names.append(name)
            if link != [] and link is not None:
                anime_database[name] = link[0]
        delist = ['Home', 'Anime Downloads', 'Manga',
                  'Anime Genres', 'Recently Updated Posts', 'FAQ', 'Forums']
        for item in delist:
            del anime_database[item]

        return anime_database, anime_names

class PageProcessList2():

    def __init__(self, link):
        self.page = urllib.request.urlopen(link)
        self.page_string = self.page.read().decode('utf-8')
        pass

    def load_items(self):
        full_list = re.findall(r'<ul\b[]>(.*?)</ul>', self.page_string) #get list of elpisode names (not working)
        print(full_list)
        for string in full_list:
            li_tag_content = re.findall(r'<li\b[^>]*>(.*?)</li>', string)
            #print(li_tag_content)
            for content in li_tag_content:
                link = re.findall(r'href="(.*?)"', content)
                anime_episode_name = re.findall(r'<span\b[^>]*>(.*?)</span>', content)
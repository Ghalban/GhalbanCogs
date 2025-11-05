import discord
from discord.embeds import Embed
import requests
from bs4 import BeautifulSoup
from redbot.core import commands

class Search(commands.Cog):
    """Webscraping off the MSU Website, delivering results straight to your local MSU Discord server"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, *, keyWords):
        """Returns 3 search results scraped from MSU HawkEye search"""
        keywords = str(keyWords)
        searchFilters = ['academic', 'department', 'page', 'people']
        word_list = keyWords.lower().split()
        last = word_list[-1]

        if last not in searchFilters: last = 'all'

        else:
            last = word_list[-1]
            word_list.pop()

        keyWords = ' '.join(word_list)
        query_marker = '%20'.join(word_list)
        # Create url
        url = 'https://www.montclair.edu/search.php?q=' + query_marker + '&filter=' + last + '&Submit=Search'
        # Get page
        page = requests.get(url)
        # Soup the page
        soup = BeautifulSoup(page.text, 'html.parser')
        hits = soup.find('div', {'class': 'result-count'}).text.split()[0]
        #hits = hits.split()[0]

        #Defaults
        links = []
        titles = []
        summaries = []
        listCap = 0
        count = 0
        listing = ""
        plurality = " results"
        resColor = 0x2ecc71 #Green
        thumbnail = "https://hotemoji.com/images/dl/m/left-pointing-magnifying-glass-emoji-by-twitter.png"
        footerText = "To narrow search add one filter word from below after search terms:\npeople | page | department | academic"

        if int(hits) >= 0:
            if int(hits) == 0:
                resColor = 0xf1c40f #Warning Yellow
                thumbnail = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/281/warning_26a0-fe0f.png"
                footerText = "Consider Trying:\n➤ changing your keywords\n➤ checking Google under Results linked above"
            if int(hits) == 1:
                listCap = 1
                plurality = " result"
            if int(hits) > 1:
                if hits == 2:
                    listCap = 2
                else:
                    listCap = 3

            for result in soup.find_all('p', {'class': 'title'}, limit = listCap):
                a_tag = result.find('a')
                links.append(a_tag.attrs['href'])
                titles.append(result.find('a').get_text())
                
                try:
                    summary_item = result.find_next_sibling('p')
                    summaries.append(summary_item.get_text())
                except:
                    summaries.append('')

        # Repair links and build listings to ensure proper display  of results
        while (int(count) < int(listCap)):

            if ('www.montclair.edu' not in links[count]):
                links[count] = 'www.montclair.edu'+links[count]
            if ('https://' not in links[count]):
                links[count] = 'https://' + links[count]

            listing = listing + (f"\n\n[**{titles[count]}**]({links[count]})\n{summaries[count]}")
            count = count + 1

        found = discord.Embed(
            title=(f"There are {hits}{plurality} for `{keyWords}`!"),
            description=
            (f"***`Filter: {last}`***\n\n[***Click Here for More Results***]({url})\n{listing}"),
            color=resColor)
        found.set_thumbnail(
            url = thumbnail
        )
        found.set_footer(
            text = footerText,
            icon_url=
            "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/twitter/53/electric-light-bulb_1f4a1.png"
        )
        await ctx.send(embed=found)
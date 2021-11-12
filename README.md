# mutiebot!!!!

this doesnt run yet.

This is another discord bot. 

Function: backing up a server to a set of text files.

These text files are meant to be human readable, like a pesterlog. Little or no additional formatting so that they can be reviewed after the fact, or posted to a fic hosting website. Less content also means faster searching and indexing, so you can use the folder search function of your computer to find things.

Options to download images or not. If you do not plan to delete the messages that are being backed up, it is possible to do exclusively the text version which includes URLs to the images hosted by discord.


### old format

channel.txt
year-month-day hh:mm [username] display name: message message message [ attachments ]

### new format

year-month-day hh:mm [username] display name: message message message ![emoji](custom_emoji_image) ![image_filename](attachment_url)




message.id
message.attachments
    attachment.id
    attachment.url
message.clean_content
message.created_at

after = datetime.datetime(2019, 10, 16)
async for message in channel.history(limit=None, after=after, oldest_first=True):
    message.whatever.....
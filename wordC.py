# coding=utf-8
import os
import sys
sys.path.append('./wordcloud')
from wordcloud import WordCloud as wc
import gspread
from oauth2client.service_account import ServiceAccountCredentials
spreadsheet_key=os.environ['SPREAD']
def cloud(which,background_color='MidnightBlue',colormap='Wistia'):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet(which)
    content=worksheet.get_all_values()
    text=''.join(k for i in content for k in i)
    wcloud=wc(font_path='NotoSerifCJKtc-Regular.otf',
        width=1920,height=1080,
        relative_scaling=0.7,
        background_color=background_color,colormap=colormap
    )
    image=wcloud.generate(text).to_image()
    image.save('wc.jpg')
    return image
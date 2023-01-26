import pandas as pd
import requests
import smtplib
from bs4 import BeautifulSoup
import datetime

TODAY = datetime.date.today().strftime("%m/%d")
my_email = 'pent1162cgu@yahoo.com.tw'
password = 'duzfodyhbckqddgr'


def send_mail(new_notification):
    with smtplib.SMTP('smtp.mail.yahoo.com') as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=['wentai1984@gmail.com', 'pent1162@gmail.com'],
            msg=f'Subject:new_notification \n\n {new_notification}'.encode('utf-8')
        )


url = 'https://www.hsps.tp.edu.tw/ann/ezindex.php'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
td_tag_list = soup.find_all('td')

a_link_list = [i.find('a') for i in td_tag_list]
href_list = []
for i in a_link_list:
    if i == None:
        continue
    else:
        href_list.append(i.get('href'))

pd.set_option('display.max_colwidth', 250)
data_table = pd.read_html(url)
df = data_table[0]
df.loc[:, 'address'] = href_list
df.rename(columns={df.columns[0]:'title'}, inplace=True)
new_notification = df[df['日期'] == TODAY]
print(new_notification)

send_mail(new_notification)
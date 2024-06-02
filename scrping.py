            
from bs4 import BeautifulSoup
import sqlite3
import requests
from datetime import datetime
import os
from winotify import Notification, audio
import time
time_get_last_articles=7200
current_directory = os.getcwd()
icon_for_new_message=os.path.join(current_directory,'iconn.png')
import os
print(icon_for_new_message)
def send_Notification(web_sit_name,msg,path_text_file):
    
    # if not(os.path.exists(icon_for_new_message)):
    #     ico=r"icon.png"
    toast = Notification(app_id="Website checker",
                        title=web_sit_name,
                        msg=msg,
                        icon=icon_for_new_message
                        )
    
    toast.set_audio(audio.Mail, loop=False)
    toast.add_actions(label="اضغط لفتح الرسالة", 
                    launch=path_text_file)
    toast.show()
def delet_every_old_item_from_data_base():

    from datetime import datetime, timedelta


    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Calculate the timestamp representing 5 days ago
    days_ago = datetime.now() - timedelta(days=20)

    # Execute the SQL DELETE statement to remove rows older than 5 days
    delete_sql = '''
    DELETE FROM articles
    WHERE created_at < ?
    '''
    cur.execute(delete_sql, (days_ago,))
    conn.commit()
    conn.close()

   
def send_to_database(articles=[]):
    
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                (id INTEGER PRIMARY KEY, website TEXT, title TEXT, chapter TEXT,link TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,is_send INTEGER DEFAULT 0 )''')

    for item in articles:
        
    # Execute a SELECT query to check if the item exists
        cursor.execute("SELECT * FROM articles WHERE website=? AND  title=? AND  chapter=? AND  link=? ", item)
        existing_item = cursor.fetchone()

        if existing_item:
            pass
            # # Item exists, so delete it
            # cursor.execute("DELETE FROM articles WHERE website=? AND  title=? AND  chapter=? AND  link=? ", item)
            # print(f"Item '{item}' deleted.")
        else:
            # Item doesn't exist, so add it
            cursor.execute("INSERT INTO articles (website ,title, chapter,  link) VALUES (?,?,?, ?)", item)
            print(f"Item '{item}' added.")
    
    # Commit the changes to the database
    conn.commit()
    # Close the cursor and connection
    cursor.close()
    conn.close()
def download_page(url):
    import requests
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        with open("webpage1.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        print("HTML content saved to webpage.html.")
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)   
def convert_time_to_rizzcomic(chapterTimestamp):
    

    currentTime = int(datetime.now().timestamp())

    timeDifference = currentTime - int(chapterTimestamp)

    return timeDifference
def convert_time_interval(interval):
        if 'd' in interval or 'day' in interval:
            try:
                 days = int(interval.split('d')[0])
            except:
                 days = int(interval.split('d')[0])
            return days * 24 * 60 * 60  # Convert days to seconds
        elif 'h' in interval or 'hour' in interval:
            hours = int(interval.split('h')[0])
            return hours * 60 *60 # Convert minutes to seconds
        elif 'm' in interval:
            minutes = int(interval.split('m')[0])
            return minutes * 60  # Convert minutes to seconds
        else:
            return None  # Unsupported format or missing units
def convert_time_to_seconds_long_word(time_str):
    # Split the string into numerical value and unit
    value, unit = time_str.split()
    value = int(value)
    
    # Convert to seconds based on the unit
    if unit == 'seconds' or unit == 'second':
        return value
    elif unit == 'minutes' or unit == 'minute' or unit == 'mins' :
        return value * 60
    elif unit == 'hours' or  unit == 'hour':
        return value * 60 * 60
    elif unit == 'days' or unit == 'day':
        return value * 24 * 60 * 60
    elif unit == 'weeks' or unit == 'week':
        return value * 7 * 24 * 60 * 60    
    elif unit =='month' or unit =='months':
        return value * 7 * 24 * 60 * 60 * 30
    else:
        raise ValueError("Invalid unit provided")
def manhuaplus_website():
    All_articles=[] 
    web_sit_name='manhuaplus'
    url = 'https://manhuaplus.org'
    #get page and save
    response = requests.get(url)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')
        

        main_tag= soup.find('div', id='home-tab-update').find_all('div')
          
        for x in main_tag:
            
            tag_time_publish=x.find('span',class_='absolute c-fff s2 timeline')
            _linke_of_article=x.find('a',class_='clamp toe oh')
            

            if _linke_of_article and tag_time_publish:
                link_of_article=x.find('a',class_='clamp toe oh').get('href')
                Name_of_chapter=x.find('a',class_='clamp toe oh').text.strip()
                time_of_publish=tag_time_publish.text.strip().replace(" ago", "")
                integare_time_of_publish=convert_time_interval(time_of_publish)
                if integare_time_of_publish  < time_get_last_articles :
                    Title=x.find('a',class_='clamp toe oh block fs-15 lh-20 yt8m ck fw-600').text.strip()
                    
                    article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                    All_articles.append(article)
            send_to_database(All_articles)
            All_articles.clear() 



    else:
        print("Failed to retrieve HTML content from the website")
def flamecomics_website():

        url = 'https://flamecomics.com'
        All_articles=[] 
        web_sit_name='flamecomics'  
       
        response = requests.get(url)


        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_tag= soup.find('div', class_='latest-updates').find_all('div',class_='bigor')
            for x in main_tag:
                Title=x.find('div',class_='tt').text.strip()
                list_of_chapter=x.find('div',class_='chapter-list')
                last_item=list_of_chapter.find_next('a')
                time_publish=last_item.find('div',class_='epxdate').text.strip()
                if convert_time_to_seconds_long_word(time_publish) < time_get_last_articles:
                    Name_of_chapter=last_item.find('div',class_='epxs').text.strip()
                    link_of_article=last_item.get('href')
                    article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                    All_articles.append(article)
            send_to_database(All_articles)
            All_articles.clear()    
        else:
             print("Failed to retrieve the webpage.")
def asuratoon_website():
    
    All_articles=[] 
    web_sit_name='asuratoon'  
    url = 'https://asuratoon.com'
    response = requests.get(url)


    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser' ) 
        main_tag= soup.find_all('div', class_='bixbox')[1].find_all('div', class_='utao styletwo')

        for x in main_tag:
                the_content=x.find('div', class_='luf')
                last_item=the_content.find('ul').find_next('li')
                time_publish=last_item.find('span').text.strip().replace('ago','')
                
                
                if  convert_time_to_seconds_long_word(time_publish) < time_get_last_articles :
                    Title=the_content.find('h4').text.strip()
                    Name_of_chapter=last_item.find('a').text.strip()
                    link_of_article=last_item.find('a').get('href')
                    article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                    All_articles.append(article)
        send_to_database(All_articles)
        All_articles.clear()    
    else:
        print("Failed to retrieve the webpage.")       
def rizzcomic_website():
    
    All_articles=[] 
    web_sit_name='rizzcomic'  
    url = 'https://rizzcomic.com'


    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_tag= soup.find('div', class_='postbody').find_all('div', class_='utao styletwo')
        for x in main_tag:
                the_content=x.find('div', class_='luf')
                last_item=the_content.find('ul').find_next('li')
                time_publish=last_item.find_all('span')[1].get('id').replace('relativeTime_', '')

                if convert_time_to_rizzcomic(time_publish) < time_get_last_articles:
                    Title=the_content.find('h4').text.strip()
                    Name_of_chapter=last_item.find('a').text.strip()
                    link_of_article=last_item.find('a').get('href')
                    article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                    All_articles.append(article)
        send_to_database(All_articles)
        All_articles.clear()       
def drakescans_website():
    All_articles=[] 
    web_sit_name='drakescans'  
    url = 'https://drakescans.com/series/i-the-demon-lord-am-being-targeted-by-my-female-disciples/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_tag= soup.find('div', class_='page-content-listing item-big_thumbnail').find_all('div', class_='col-6 col-md-3 badge-pos-1')
        for x in main_tag:
               time_tag=x.find('div',class_='list-chapter').find('div', class_='chapter-item').find('span',class_='post-on font-meta').find('a')
               
               if time_tag:
                    time_publish=time_tag.get('title').replace('ago', '')
                    if (convert_time_to_seconds_long_word(time_publish)) < time_get_last_articles:
                        
                        
                        content=x.find('div', class_='item-summary')
                        Title=content.find('a').text.strip()
                        last_item=x.find('div',class_='list-chapter').find('div', class_='chapter-item').find('span',class_='chapter font-meta')
                        
                        Name_of_chapter=last_item.find('a').text.strip()
                        link_of_article=last_item.find('a').get('href')
                        
                        article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                        All_articles.append(article)
        send_to_database(All_articles)
        All_articles.clear()     
    else:
        print(f"Failed to retrieve the webpage.{response.status_code}")    
def night_scans_website():
        All_articles=[] 
        web_sit_name='night-scans'    
        url = 'https://night-scans.com'       
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_tag= soup.find_all('div', class_='listupd')[1].find_all('div',class_='bigor')
            for x in main_tag:
               
                list_of_chapter=x.find('ul',class_='chfiv')
                last_item=list_of_chapter.find('li')
                time_publish=last_item.find_all('span',class_='newchtimeluffy')[0].text.strip().replace('ago', '')
                if convert_time_to_seconds_long_word(time_publish) < time_get_last_articles:
                    Title=x.find('div',class_='tt').text.strip()
                    Name_of_chapter=last_item.find('span').text.strip()
                    link_of_article=last_item.find('a').get('href')
                    article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                    All_articles.append(article)
            send_to_database(All_articles)
            All_articles.clear()                    
        else:
             print("Failed to retrieve the webpage.")  
def freakcomic_website():
        All_articles=[] 
        web_sit_name='freakcomic' 
        url = 'https://freakcomic.com'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_tag= soup.find_all('div', class_='lastest-li')[1].find_all('div',class_='lastest-serie')
            for x in main_tag:
                content=x.find('div', class_='info')
                Title=content.find('div',class_='lastest-title').find('a').text.strip()
                list_of_chapter=x.find('ul',class_='lastest-chap')
                items=list_of_chapter.find_all('a')
                item_one=items[0]
                item_two=items[1]
                if str(item_one.find('span').text.strip())=='NEW':
                      Name_of_chapter_temp=item_one.find('li')
                      if Name_of_chapter_temp.find('svg'):
                         del_svg=Name_of_chapter_temp.find('svg').extract()
                      del_span=Name_of_chapter_temp.find('span').extract()
                      Name_of_chapter=Name_of_chapter_temp.text.strip()
                      link_of_article=item_one.get('href')
                      article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                      All_articles.append(article)
                if str(item_two.find('span').text.strip())=='NEW':
                      Name_of_chapter_temp=item_two.find('li')
                      if Name_of_chapter_temp.find('svg'):
                         del_svg=Name_of_chapter_temp.find('svg').extract()
                      del_span=Name_of_chapter_temp.find('span').extract()
                      Name_of_chapter=Name_of_chapter_temp.text.strip()
                      link_of_article=item_one.get('href')
                      article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                      All_articles.append(article)
            send_to_database(All_articles)
            All_articles.clear()                               
           
        else:
             print("Failed to retrieve the webpage.")
def suryatoon_website():
    
        url = 'https://suryatoon.com/'
        All_articles=[] 
        web_sit_name='suryatoon'      
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            main_tag= soup.find('body',class_='darkmode' ).find_all('div',class_='listupd')[1].find_all('div',class_='luf')
            for x in main_tag:
                last_item=x.find('ul').find('li')
                time_publish=last_item.find('span',).text.strip().replace('ago', '')
                if convert_time_to_seconds_long_word(time_publish) < time_get_last_articles: 
                    Title=x.find('a',class_='series').text.strip()
                    Name_of_chapter=last_item.find('a').text.strip()
                    link_of_article=last_item.find('a').get('href')
                    article=(web_sit_name,Title,Name_of_chapter,link_of_article)
                    All_articles.append(article)
            send_to_database(All_articles)
            All_articles.clear()
        else:
             print("Failed to retrieve the webpage.") 
def hidden_file():
    import subprocess
    
    subprocess.check_call(["attrib","+H",os.path.join(current_directory,'database.db')])
    subprocess.check_call(["attrib","+H",os.path.join(current_directory,'texts')])
def new_text_file(website,content,couter_to_item):
            path = os.path.join(current_directory,'texts')

            if not os.path.exists(path):
                os.makedirs(path)
            else:
               
                path_text=os.path.join(path,f'{website}.txt')   
                path_text_file='file:///'+path_text
                global icon_for_new_message
                
                message=f'add {couter_to_item} message'
                with open(path_text, 'w') as file:
                    file.write(f"{content}\n")
                   
                send_Notification(web_sit_name=website,path_text_file=path_text_file,msg=message)   
def filter_articles_in_database_and_send():

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    
    select_sql = """
SELECT website,
       GROUP_CONCAT(id) AS all_id,
       GROUP_CONCAT(title) AS all_title,
       GROUP_CONCAT(chapter) AS all_chapter,
       GROUP_CONCAT(link) AS all_link
FROM articles
WHERE is_send = 1
GROUP BY website;

   """

    cur.execute(select_sql,)
    rows = cur.fetchall()
    conn.close()
    print(rows)
    all_data=[]
    for  website,id, Titles,chapters,links in rows:
        _time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_content=f'---------Laste Update To:-{website}----------\n'+f'--------Update at:-{_time}---------\n'
        content=''
        index=1
        if (website and id and Titles and chapters and links)==None:
         print('empty query')
        else: 
            for _id,tit,ch,lin in zip( id.split(','),Titles.split(','), chapters.split(','),links.split(',')):
                    print('---------------------------')
                    print(_id)
                    print(tit)
                    print(ch)
                    print(lin)
                    print('---------------------------')
                    header=f'-------------------------------------({index})------------------------------------------------\n'
                    body= f'{tit} \n{ch}\n{lin} \n'
                    footer_content='----------------------------------------------------------------------------------------\n'
                    content=content+header+body+footer_content
                    index=index+1
            final_content=start_content+content
            art=(website,final_content,index-1,id)
            all_data.append(art)   
            
        connt = sqlite3.connect('database.db')
        cursor = connt.cursor()
        print(all_data)
    for website , content , couter_to_item,id in all_data:
        print(id)
        print('-------------')
        for c in id.split(','):
                print(int(c))
                cursor.execute('UPDATE articles SET is_send = ? WHERE id =?; ',(0,c,))
                connt.commit()
        new_text_file(website=website ,content=content,couter_to_item=couter_to_item)
    
    connt.close()
    
if __name__ == "__main__":

    while True:
        import time

        try:
            # suryatoon_website()
            # hidden_file()
            # freakcomic_website()
            # night_scans_website()
            # rizzcomic_website()
            # asuratoon_website()
            # flamecomics_website()
            # manhuaplus_website()
            # delet_every_old_item_from_data_base()
            filter_articles_in_database_and_send()
            time.sleep(60*15)  
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")
            break  # Exit the loop if KeyboardInterrupt is detected

    print("Script has exited.")
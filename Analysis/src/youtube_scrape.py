from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from googleapiclient.discovery import build
from datetime import datetime
import csv

API_KEY = 'YOUR_API_KEY_HERE'

def ScrollToBottom(driver):
    # Scroll to the bottom of the page
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    time.sleep(2)

def ScrapeChannelVideoLinks(channel_name):
    print("Starting url scrape for", channel_name)
    driver = webdriver.Chrome()
    try:
        # Load the channel
        driver.get("https://www.youtube.com/" + channel_name + "/videos")
        driver.implicitly_wait(15)

        prev_scroll_height = 0
        while True:
            ScrollToBottom(driver)
            current_scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
            
            if current_scroll_height == prev_scroll_height:
                break  # No more content to load
            prev_scroll_height = current_scroll_height

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        video_blocks = soup.find_all('a', id='thumbnail', class_='yt-simple-endpoint inline-block style-scope ytd-thumbnail')

        video_links = []
        # Extract the video link from each video block
        for video_block in video_blocks:
            video_link = video_block.get('href')
            if video_link: video_links.append("https://www.youtube.com" + video_link)
        print("Completed", channel_name, "url scrape. Total:", len(video_links))
        return video_links

    finally:
        driver.quit()

def RoundDecimal(value, decimals):
    factor = 10 ** decimals
    rounded_value = (value * factor) + 0.5
    rounded_value = int(rounded_value) / factor
    return rounded_value

def FormatVideoDuration(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    total_minutes = hours * 60 + minutes + seconds / 60
    return RoundDecimal(total_minutes, 2)

def FormatUploadDate(upload_date):
    date_time = datetime.strptime(upload_date, '%Y-%m-%dT%H:%M:%SZ')
    formatted_date = date_time.strftime('%B %d, %Y')
    formatted_time = date_time.strftime('%H:%M')
    return formatted_date, formatted_time

def FormatCategoryId(category_id):
    category_mapping = {
        '1': 'Film & Animation',
        '2': 'Autos & Vehicles',
        '10': 'Music',
        '15': 'Pets & Animals',
        '17': 'Sports',
        '18': 'Short Movies',
        '19': 'Travel & Events',
        '20': 'Gaming',
        '21': 'Videoblogging',
        '22': 'People & Blogs',
        '23': 'Comedy',
        '24': 'Entertainment',
        '25': 'News & Politics',
        '26': 'Howto & Style',
        '27': 'Education',
        '28': 'Science & Technology',
        '29': 'Nonprofits & Activism',
        '30': 'Movies',
        '31': 'Anime/Animation',
        '32': 'Action/Adventure',
        '33': 'Classics',
        '34': 'Comedy',
        '35': 'Documentary',
        '36': 'Drama',
        '37': 'Family',
        '38': 'Foreign',
        '39': 'Horror',
        '40': 'Sci-Fi/Fantasy',
        '41': 'Thriller',
        '42': 'Shorts',
        '43': 'Shows',
        '44': 'Trailers'
    }
    return category_mapping.get(category_id, 'None')

def ScrapeVideoDetails(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    response = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    ).execute()
    if 'items' in response and len(response['items']) > 0:
        item = response['items'][0]
        title = item['snippet']['title']
        duration_iso = item['contentDetails']['duration']
        duration = duration_iso[2:]
        duration_seconds = 0
        if 'T' in duration:
            parts = duration.split('T')
            if len(parts) == 2:
                time_part = parts[1]
                if 'H' in time_part:
                    duration_seconds += int(time_part.split('H')[0]) * 3600
                    time_part = time_part.split('H')[1]
                if 'M' in time_part:
                    duration_seconds += int(time_part.split('M')[0]) * 60
                    time_part = time_part.split('M')[1]
                if 'S' in time_part:
                    duration_seconds += int(time_part.split('S')[0])
        else:
            if 'H' in duration:
                duration_seconds += int(duration.split('H')[0]) * 3600
                duration = duration.split('H')[1]
            if 'M' in duration:
                duration_seconds += int(duration.split('M')[0]) * 60
                duration = duration.split('M')[1]
            if 'S' in duration:
                duration_seconds += int(duration.split('S')[0])
        formatted_duration = FormatVideoDuration(duration_seconds)
        upload_date = item['snippet']['publishedAt']
        formatted_date, formatted_time = FormatUploadDate(upload_date)
        if 'statistics' in item:
            if 'likeCount' in item['statistics']: likes = item['statistics']['likeCount']
            else: likes = 0
        else: likes = 0

        if 'statistics' in item: comments = item['statistics'].get('commentCount', 0)
        else: comments = 0

        category_id = FormatCategoryId(item['snippet'].get('categoryId', ''))
        
        if 'statistics' in item:
            if 'viewCount' in item['statistics']: views = item['statistics']['viewCount']
            else: views = 0
        else: views = 0

        tags = item['snippet'].get('tags', [])
        tags_str = ', '.join(tags) if tags else 'None'

        return {
            'Title': title,
            'Duration': formatted_duration,
            'Upload Date': formatted_date,
            'Upload Time': formatted_time,
            'Likes': likes,
            'Comments': comments,
            'Views': views,
            'Tags': tags_str,
            'Category ID': category_id
        }
    else:
        return None

def GetVideoId(video_url):
    params = video_url.split('?')[1].split('&')
    video_id = None
    for param in params:
        if param.startswith('v='):
            video_id = param[2:]
            break
    return video_id

def ScrapeEveryVideo(channel_name, channel_urls):
    print("Starting video scrape for", channel_name)
    every_video_details = []
    total_urls = len(channel_urls)
    for index, url in enumerate(channel_urls, start=1):
        print(f"Processing URL {index}/{total_urls}")
        video_details = ScrapeVideoDetails(GetVideoId(url))
        if video_details:
            every_video_details.append({
                'Channel': channel_name,
                'Title': video_details['Title'],
                'Duration': video_details['Duration'],
                'Upload Date': video_details['Upload Date'],
                'Upload Time': video_details['Upload Time'],
                'Likes': video_details['Likes'],
                'Comments': video_details['Comments'],
                'Views': video_details['Views'],
                'Tags': video_details['Tags'],
                'Category ID': video_details['Category ID'],
                'URL': url
            })
        else: print("Video details not found for", channel_name, url)
    print("Completed", channel_name, "video scrape. Total:", len(every_video_details))
    return every_video_details

def SaveChannelDetails(file_name, details, channel_name):
    print("Saving video details for", channel_name)
    with open(file_name, mode='a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Channel', 'Title', 'Duration', 'Upload Date', 'Upload Time', 'Likes','Comments','Views','Tags','Category ID','URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if csv_file.tell() == 0:
            writer.writeheader()
        for video_detail in details:
            writer.writerow(video_detail)
    print(channel_name, "save complete!")

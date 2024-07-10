import requests
from bs4 import BeautifulSoup
import json

def get_new_activities():
    url = "https://linkareer.com/list/activity"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    activities = []
    for item in soup.select('.activity-item'):
        name = item.select_one('.activity-title').text.strip()
        organizer = item.select_one('.activity-organizer').text.strip()
        link = item.select_one('a')['href']
        activities.append({
            'name': name,
            'organizer': organizer,
            'link': link
        })

    return activities

def send_to_discord(activities, webhook_url):
    for activity in activities:
        data = {
            "content": f"**이름**: {activity['name']}\n**주최 단체**: {activity['organizer']}\n**바로가기 링크**: {activity['link']}"
        }
        response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response.status_code != 204:
            print(f"Failed to send message to Discord: {response.status_code}, {response.text}")

if __name__ == "__main__":
    webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
    activities = get_new_activities()
    send_to_discord(activities, webhook_url)

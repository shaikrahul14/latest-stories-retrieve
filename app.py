from flask import Flask, jsonify, request
import requests
import re

app = Flask(__name__)

def get_latest_stories(num_stories):
    base_url = "https://time.com"
    response = requests.get(base_url)
    html_content = response.text
    
    # Extract content within the specified div tag
    div_pattern = r'<div class="partial latest-stories" data-module_name="Latest Stories">(.*?)</div>'
    div_match = re.search(div_pattern, html_content, re.DOTALL)
    
    if div_match:
        div_content = div_match.group(1)
        
        # Regular expression to find the latest stories within the extracted div content
        story_pattern = r'<li class="latest-stories__item">\s*<a href="([^"]+)">\s*<h3 class="latest-stories__item-headline">(.*?)</h3>\s*</a>'
        stories = re.findall(story_pattern, div_content)[:num_stories]
        
        # Construct JSON object array
        stories_json = [{"title": title.strip(), "link": link} for link, title in stories]
        
        return stories_json
    else:
        return []

@app.route('/get_time_stories')
def get_time_stories():
    num_stories = request.args.get('num_stories', default=6, type=int)
    latest_stories = get_latest_stories(num_stories)
    return jsonify({'latest_stories': latest_stories})

if __name__ == '__main__':
    app.run(debug=True)

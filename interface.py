import streamlit as st
import pandas as pd
import calendar
import os
import json
# import create_mockdata as mock
# Custom CSS for rounded buttons

st.set_page_config(page_title="Social Media Manager 5000", page_icon="🚀", layout="wide")

st.markdown(
    """
    <style>
        .stButton>button {
            width: 100%;
            border-radius: 50px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

days_of_week = list(calendar.day_name)

icons = {
    "Pinterest": "📌",
    "LinkedIn": "🔗",
    "Facebook": "📘",
    "Twitter": "🐦",
    "Blogger": "🅱️",
    "Tumblr": "🌀",
    "Reddit": "🔺"
}


# Create a sidebar
st.sidebar.title('Social Media Manager 5000')

pages = {
    "Create an Entry": "home",
    "Empty Canvas":'empty'
}

selected_page = st.sidebar.select_slider("", list(pages.keys()))


def create_entry():
    with st.form(key='my_form'):
        # Input fields
        title = st.text_input("Title")
        text = st.text_area("Text")
        hashtags = st.text_input("Hashtags (comma-separated)")
        link = st.text_input("Link")
        image_file = st.file_uploader("Image (optional)", type=["png", "jpg", "jpeg"])
        time = st.time_input("Time")
        day = st.date_input("Day")
        social_media_platforms = list(icons.keys())
        checks = st.multiselect(
            "Select Social Media Platforms", social_media_platforms)

        image_bytes = None
        if image_file is not None:
            image = Image.open(image_file)
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='PNG')
            image_bytes = byte_arr.getvalue()

        print(title)
        post_info = {
            "title": title,
            "text": text,
            "hashtags": [hashtag.strip() for hashtag in hashtags.split(",")],
            "link": link,
            "image": image_bytes,
            "time": str(time),
            "day": str(day),
            "platforms": checks
        }

        # Process form submission outside the form context
        if st.form_submit_button(label='Submit') and len(title)>=10 and len(text)>=10:
            # Create JSON
            print(post_info)

            try:
                with open('output.jsonl', 'a+') as file:
                    file.write(json.dumps(post_info) )
                    file.write('\n')  # Add a newline for separation
            except Exception as e:
                print(e)



# Define content for each page
if selected_page == "Create an Entry":
        # Display JSON and write to file if form is submitted
    create_entry()
    
button_states = {}
Schedule = st.sidebar.button('Schedule', key='Schedule')
# Add social media icons as buttons
for platform, icon in icons.items():
    button_states[platform] = st.sidebar.button(
        f'{icon} {platform}', key=platform)


def create_week_calendar():
    # Define the HTML and CSS for the calendar
    calendar_html = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            text-align: center;
            padding: 8px;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        .day {
            color: transparent;
            cursor: pointer;
        }
        .day:hover {
            color: black;
        }
    </style>
    <table>
        <tr>
            <th>Mon</th>
            <th>Tue</th>
            <th>Wed</th>
            <th>Thu</th>
            <th>Fri</th>
        </tr>
        <tr>
            <td><a class="day" href="#">1</a></td>
            <td><a class="day" href="#">2</a></td>
            <td><a class="day" href="#">3</a></td>
            <td><a class="day" href="#">4</a></td>
            <td><a class="day" href="#">5</a></td>
        </tr>
    </table>
    """

    # Render the calendar in Streamlit
    st.markdown(calendar_html, unsafe_allow_html=True)


def display_entries(post_info_jsonl):
    # Check if the file exists
    if not os.path.exists(post_info_jsonl):
        # Use mock data
        post_info = [
            {
                "platforms": ["Pinterest", "LinkedIn"],
                "title": "Mock Title",
                "text": "Mock Text",
                "link": "https://mock.link",
                "image": None,
                "time": "12:00",
                "day": "2024-01-01",
                "hashtags": ["#mock", "#data"]
            },
            # Add more mock posts as needed
        ]
    else:
        # Load the post info from the JSONL
        with open(post_info_jsonl, "r") as f:
            post_info = [json.loads(line) for line in f]

    # Display each post
    for post in post_info:
        icons_str = ' '.join([icons[platform]
                             for platform in post["platforms"]])
        st.markdown(
            f"<table style='border-collapse: collapse; border: none;'><tr><td style='border: none; width: 30%'>{icons_str}</td><td style='border: none; width: 60%;'>{' '.join(post['title'].split()[:10])}</td><td style='border: none;'>{post['time']}</td><td style='border: none;'>{post['day']}</td></tr></table>", unsafe_allow_html=True)


if Schedule:    
    display_entries('output.jsonl')


if button_states["Pinterest"]:
    st.title('Pinterest Chart')
    chart_data = pd.DataFrame(
        {'Likes': [15, 30, 45, 20, 35, 10, 15]},
        index=days_of_week
    )
    st.bar_chart(chart_data)
    create_week_calendar()


elif button_states["LinkedIn"]:
    st.title('LinkedIn Chart')
    chart_data = pd.DataFrame(
        {'Users': [1000, 2000, 3000, 1500, 2500, 1200, 1800]},
        index=days_of_week
    )
    st.bar_chart(chart_data)
    create_week_calendar()

elif button_states["Facebook"]:
    st.title('Facebook Chart')
    chart_data = pd.DataFrame(
        {'Likes': [500, 800, 1200, 600, 1000, 700, 900]},
        index=days_of_week
    )
    st.bar_chart(chart_data)
    create_week_calendar()

elif button_states["Twitter"]:
    st.title('Twitter Chart')
    chart_data = pd.DataFrame(
        {'Tweets': [50, 100, 150, 70, 120, 80, 110]},
        index=days_of_week
    )
    st.bar_chart(chart_data)
    create_week_calendar()

elif button_states["Blogger"]:
    st.title('Blogger Chart')
    blogger_data = pd.DataFrame(
        {'Data': [10, 20, 15, 25, 30, 20, 25]},
        index=days_of_week
    )
    st.bar_chart(blogger_data)
    create_week_calendar()

elif button_states["Tumblr"]:
    st.title('Tumblr Chart')
    tumblr_data = pd.DataFrame(
        {'Data': [5, 15, 10, 20, 25, 15, 20]},
        index=days_of_week
    )
    st.bar_chart(tumblr_data)
    create_week_calendar()

elif button_states["Reddit"]:
    st.title('Reddit Chart')
    reddit_data = pd.DataFrame(
        {'Data': [8, 18, 12, 22, 28, 15, 20]},
        index=days_of_week
    )
    st.bar_chart(reddit_data)
    create_week_calendar()

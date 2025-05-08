import pandas as pd
import seaborn as sns
#from IPython.display import display, HTML
import numpy as np
import webbrowser

# # Set the number of colors you want to use
num_colors = 5  # Adjust this as needed

# Function to generate HTML with colored messages
def colorize_messages(df,topic_colors):

    color = topic_colors.get(df['topic'], 'black')
    rgb_color = tuple(np.array(color) * 255)
    return f'<div style="color: rgb{rgb_color};"><strong>Topic \"{df["Name"]}\": </strong>{df["message_content"]}</div>'

def display_messages(df):
    """
    dataframe has the following:
    phone_number - Some identifier for the sender
    message_topic - Topic of the message
    """
    df_cloned = df.copy()
    num_colors = len(df['topic'].unique())
    palette = sns.color_palette('Set2', num_colors)
    topic_colors = dict(zip(sorted(df['topic'].unique()), palette))

    # Apply the colorize_messages function to create a new column with colored messages
    df_cloned['colored_message'] = df_cloned.apply(colorize_messages, axis=1, topic_colors=topic_colors)

    html_output = df_cloned[['phone_number', 'colored_message']].to_html(index=False, escape=False)
    with open('chat_display.html', 'w') as f:
        f.write(html_output)

    # Open the HTML file in the default web browser
    webbrowser.open('chat_display.html')
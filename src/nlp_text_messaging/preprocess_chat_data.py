import csv
from datetime import datetime
import sys
import os
import re



def convert_to_unix_timestamp(date_string):
    date_format = "%m/%d/%Y %I:%M %p"
    datetime_obj = datetime.strptime(date_string, date_format)
    timestamp = datetime_obj.timestamp()
    return int(timestamp)
    # date_formats = ["%m/%d/%Y %I:%M %p", "%m/%d/%y, %I:%M:%S%p"]
    # for date_format in date_formats:
    #     try:
    #         datetime_obj = datetime.strptime(date_string, date_format)
    #         timestamp = int(datetime_obj.timestamp())
    #         return timestamp
    #     except ValueError:
    #         pass
    # raise ValueError("Invalid date format")

def remove_non_alphanumeric(string):
    # Define the regular expression pattern to match alphanumeric and punctuation characters
    pattern = r'[^a-zA-Z0-9\s\.,!?\[\]()+-~]'
    
    # Use re.sub to replace non-matching characters with an empty string
    cleaned_string = string
    cleaned_string = re.sub(pattern, '', string) 
    cleaned_string = cleaned_string.replace('\u202f', '')
    cleaned_string = cleaned_string.replace('\u200e', '')
    cleaned_string = cleaned_string.replace('\u2011', '-')   
    #cleaned_string = cleaned_string.replace(' ', str(b'\xa0'))
    return cleaned_string

def remove_emojis(text):
    # Regular expression to remove emojis
    text = text.replace("’", "'")
    new_text = remove_non_alphanumeric(text)
    return new_text

def process_chat_data(chat_file, output_csv):
    with open(chat_file, 'r', encoding='utf-8') as file:
        chat_lines = file.readlines()

    for i, line in enumerate(chat_lines):
        chat_lines[i] = remove_emojis(line)

    rows = []
    for line in chat_lines:
        parts = line.split('] ')
        if len(parts) < 2:
            continue
        time_str = parts[0].strip('[')
        message = '] '.join(parts[1:])  # Join remaining parts to reconstruct the message

        # print(line)
        # print(time_str)
        time = convert_to_unix_timestamp(time_str)
        phone_number, message_content = message.split(': ', 1)
        # Remove emojis from message content
        message_content = remove_emojis(message_content.strip())
        rows.append([time, phone_number, message_content])

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'phone_number', 'message_content'])
        writer.writerows(rows)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_filename.txt> [<output_filename.csv>]")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_filename = sys.argv[2]
    else:
        output_filename = os.path.splitext(input_filename)[0] + ".csv"
    
    process_chat_data(input_filename, output_filename)

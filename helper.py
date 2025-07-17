from wordcloud import WordCloud
import pandas as pd
from collections import Counter

import emoji
# For sentiment analysis
from textblob import TextBlob
# from urlextract import URLExtract
# extract = URLExtract()

# def fetch_stats(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
    
#     num_messages = df.shape[0]
    
#     words = []
#     for message in df['message']:
#         words.extend(message.split())
    
#     # More comprehensive media check
#     media_indicators = [
#         'image omitted',
#         '<media omitted>',
#         '<media omitted>',
#         'video omitted',
#         'document omitted',
#         'audio omitted'
#     ]
    
#     # Case insensitive check for any media type
#     num_media_messages = df[
#         df['message'].str.lower().str.contains('omitted|media', regex=True)
#     ].shape[0]
    
#     # fetch number of links shared
#     links = []
#     for message in df['message']:
#         links.extend(extract.find_urls(message))

#     return num_messages,len(words),num_media_messages,len(links)
    

# helper.py
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    stats = {
        'total_messages': df.shape[0],
        'total_words': sum(df['message'].str.split().str.len()),
        'media_messages': df['message'].str.contains(
            'omitted|media', 
            case=False, 
            regex=True
        ).sum(),
        'links': df['message'].str.contains(
            'http|www|.com|.in', 
            case=False, 
            regex=True
        ).sum()
    }
    return stats


#fetch most busy user
def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x,df

def create_wordcloud(selected_user, df):
    
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    # print(stop_words)    
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification' ]
    temp = temp[temp['message'] != 'image omitted']
    
    def remove_stop_words(message):
        y =[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    
    wc = WordCloud(width=1000, height=1000, min_font_size=5, background_color='white')
    
    temp['message'] = temp['message'].apply(remove_stop_words)
    
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    # print(stop_words)
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification' ]
    temp = temp[temp['message'] != 'image omitted']
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_fxn(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message'].astype(str):  # Ensure message is string
        # New way to check for emojis (works with emoji>=2.0.0)
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    # Create DataFrame with proper column names
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emoji', 'Count'])
    
    return emoji_df


def  monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]) )
    timeline['time']=time
        
    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

# Sentiment analysis function
def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    sentiments = df['message'].dropna().apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    # Classify as positive, negative, or neutral
    sentiment_category = sentiments.apply(lambda x: 'Positive' if x > 0.1 else ('Negative' if x < -0.1 else 'Neutral'))
    summary = sentiment_category.value_counts().to_dict()
    # Also return average polarity
    avg_polarity = sentiments.mean()
    return {
        'positive': summary.get('Positive', 0),
        'negative': summary.get('Negative', 0),
        'neutral': summary.get('Neutral', 0),
        'average_polarity': avg_polarity
    }
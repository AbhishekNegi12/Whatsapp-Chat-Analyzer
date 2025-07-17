import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import preprocessor
import helper 
import seaborn as sns

# Set up the sidebar
st.sidebar.title("WhatsApp Chat Analyzer")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat export file", type=['txt'])
if uploaded_file is not None:
    # try:
        # Read and decode the file
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        
        # Preprocess the data
        df = preprocessor.preprocess(data)
        
        # Display the processed dataframe (optional)
        if st.checkbox("Show Raw Data"):
            st.dataframe(df)
        # st.dataframe(df)
        
        # Fetch unique users
        user_list = df['user'].unique().tolist()
        
        # Remove group notifications if needed
        # if 'group_notification' in user_list:
        #     user_list.remove('group_notification')
        
        user_list.sort()
        user_list.insert(0, "Overall")
        
        selected_user = st.sidebar.selectbox("Show Analysis with respect to:", user_list)
        
        if st.sidebar.button("Show Analysis"):
            
            # Get statistics using the helper function
            stats = helper.fetch_stats(selected_user, df)
            # num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
                        
            st.title('Top Statistics')
            
            # Create columns for metrics
            col1, col2, col3, col4 = st.columns(4)           
            
            
            with col1:
                st.subheader("Total Messages")
                st.title(stats['total_messages'])
                # st.title(num_messages)
                
            with col2:
                st.subheader("Total Words")
                st.title(stats['total_words'])
                # st.title(words)
                
            with col3:
                st.subheader("Media Shared")
                st.title(stats['media_messages'])
                # st.title(num_media_messages)
                
            with col4:
                st.subheader("Links Shared")
                st.title(stats['links'])
                # st.title(num_links)
            
            # Add more visualizations here
            # st.header("Activity Timeline")
            # Add your timeline visualization code

            # Sentiment Analysis Section
            st.header("Sentiment Analysis")
            sentiment = helper.sentiment_analysis(selected_user, df)
            col_pos, col_neu, col_neg = st.columns(3)
            with col_pos:
                st.metric("Positive Messages", sentiment['positive'])
            with col_neu:
                st.metric("Neutral Messages", sentiment['neutral'])
            with col_neg:
                st.metric("Negative Messages", sentiment['negative'])
            st.caption(f"Average Sentiment Polarity: {sentiment['average_polarity']:.2f}")
            
    # except Exception as e:
    #     st.error(f"An error occurred: {str(e)}")
    

        # timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        figure,axis = plt.subplots()
        axis.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        # plt.show()
        st.pyplot(figure)
        
        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        
        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
        #GROUP LEVEL 
        #finding the busiest users in the group 
        if  selected_user == 'Overall':
            st.title('Most Busy User')
            x, new_df = helper.most_busy_user(df)
            fig, axis = plt.subplots()
            
            col1, col2 = st.columns(2)
            
            with col1:
                axis.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
        
        
        #WordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, axis = plt.subplots()
        axis.imshow(df_wc)
        st.pyplot(fig)
        
        # most common words
        st.title('Most Used Words')
        most_common_df = helper.most_common_words(selected_user,df)
        st.dataframe(most_common_df)
        
        figure,axis = plt.subplots()
        axis.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(figure)
        
        
        # emoji analysis
        st.title('Emojis Analysis')
        emoji_df = helper.emoji_fxn(selected_user, df)

        # Filter to show only top 10 emojis to reduce clutter
        top_emojis = emoji_df.head(10)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots(figsize=(8, 8))
            
            # Create pie chart with better parameters
            wedges, texts, autotexts = ax.pie(
                top_emojis['Count'],
                labels=top_emojis['Emoji'],
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 14},
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                pctdistance=0.85
            )
            
            st.pyplot(fig)
        


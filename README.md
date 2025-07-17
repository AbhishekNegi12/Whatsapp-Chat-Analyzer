# WhatsApp Chat Analyzer

A Streamlit web application to analyze WhatsApp chat exports. Gain insights into your group or personal chats with statistics, word clouds, activity timelines, and more.

## Features
- Upload WhatsApp chat `.txt` files for instant analysis
- View total messages, words, media, and links shared
- User-wise and overall statistics
- Word cloud and most common words
- Emoji analysis
- Sentiment analysis (positive, negative, neutral message counts and average polarity)
- Activity timelines (monthly, daily)
- Visualizations for active days, months, and heatmaps


## Advanced Ideas (Make it a True ML Project)

- Integrate transformer-based sentiment/emotion models (BERT, DistilBERT)
- Topic modeling to extract main discussion themes
- User behavior clustering (KMeans, DBSCAN)
- Toxicity/abuse detection using ML models
- Chatbot/response prediction
- Network analysis of user interactions
- Time series forecasting of chat activity
- Interactive visualizations with Plotly/Altair

## Live Demo

https://whatsapp-chat-analyzer-12.streamlit.app/

## Screenshots

> Screenshots will be uploaded here to showcase the app interface and features.

## Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/AbhishekNegi12/Whatsapp-Chat-Analyzer.git
   cd whatsapp-chat-analyzer
   ```
2. Install dependencies:
   pip install -r requirements.txt


### Running Locally
Start the Streamlit app:
```bash
streamlit run app.py
```
Open the provided local URL in your browser.

## Deployment

### Deploy on Streamlit Community Cloud
1. Push your code to a public GitHub repository.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with GitHub.
3. Click "New app", select your repo and `app.py` as the entry point.
4. Click "Deploy". Your app will be live at a public URL.

### Other Deployment Options
- Heroku, AWS, GCP, Azure (using Docker or custom setup)

## Usage
1. Export your WhatsApp chat as a `.txt` file (without media).
2. Upload the file using the sidebar in the app.
3. Explore the statistics, visualizations, and insights.

## Project Structure
```
├── app.py                  # Main Streamlit app
├── helper.py               # Helper functions for analysis
├── preprocessor.py         # Chat preprocessing logic
├── requirements.txt        # Python dependencies
├── stop_hinglish.txt       # Stop words for word cloud
├── A2_chat.txt             # Sample chat file
├── Friends_chat.txt        # Sample chat file
├── whatsapp-chat-analysis.ipynb # Jupyter notebook for EDA
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.

---

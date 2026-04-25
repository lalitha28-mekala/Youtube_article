import requests
import os
import time
from google import genai

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


#  Extract video ID
def extract_video_id(url):
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    else:
        return url


# 📄 Get transcript (RapidAPI)
def get_transcript(video_id):
    url = "https://youtube-transcriptor.p.rapidapi.com/transcript"

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "youtube-transcriptor.p.rapidapi.com"
    }

    querystring = {"video_id": video_id}

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        data = response.json()

        #  Correct extraction
        if isinstance(data, list) and len(data) > 0:
            return data[0].get("transcriptionAsText", "Transcript not found.")

        return "Transcript not available."

    except Exception as e:
        return f"Transcript not available. Error: {str(e)}"


#  Summarize
def summarize_text(text):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=f"""
                You are an expert summarizer.

                IMPORTANT: Always respond in English.

                Summarize this transcript clearly and concisely.
                Highlight key ideas and remove repetition.

                Transcript:
                {text[:3000]}
                """
            )
            return response.text

        except Exception as e:
            if "503" in str(e):
                time.sleep(2)
            else:
                return f"Summarization failed: {str(e)}"

    return "⚠️ Server busy. Please try again."


#  Generate article (Markdown)
def generate_article(summary):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=f"""
                You are a professional content writer.

                IMPORTANT: Write in English.

                Convert the summary into a structured MARKDOWN article.

                Include:
                - # Title
                - ## Introduction
                - ## Key Takeaways (bullet points)
                - ## Detailed Explanation
                - ## Conclusion

                Make it clean, engaging, and easy to read.

                Summary:
                {summary}
                """
            )
            return response.text

        except Exception as e:
            if "503" in str(e):
                time.sleep(2)
            else:
                return f"Article generation failed: {str(e)}"

    return "⚠️ Server busy. Please try again."

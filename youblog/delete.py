from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
from textblob import TextBlob
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YouTubeBlogTools:
    @tool
    def extract_video_info(self, video_url):
        """Extract information from a YouTube video including title and description"""
        try:
            # Extract video ID from URL
            video_id = video_url.split('v=')[1]
            
            # Initialize YouTube API client
            youtube = googleapiclient.discovery.build(
                'youtube', 'v3', 
                developerKey=os.getenv('YOUTUBE_API_KEY')
            )
            
            # Get video details
            request = youtube.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                return "Error: Video not found"
                
            video_data = response['items'][0]['snippet']
            return {
                'title': video_data['title'],
                'description': video_data['description'],
                'video_id': video_id
            }
        except Exception as e:
            return f"Error extracting video info: {str(e)}"

    @tool
    def get_transcript(self, video_id):
        """Get the transcript of a YouTube video"""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_transcript = ' '.join([entry['text'] for entry in transcript_list])
            return full_transcript
        except Exception as e:
            return f"Error getting transcript: {str(e)}"

    @tool
    def analyze_sentiment(self, text):
        """Analyze the sentiment of the text"""
        analysis = TextBlob(text)
        return {
            'polarity': analysis.sentiment.polarity,
            'subjectivity': analysis.sentiment.subjectivity
        }

    @tool
    def extract_key_topics(self, text):
        """Extract key topics from the text"""
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        
        # Tokenize and clean text
        sentences = sent_tokenize(text)
        stop_words = set(stopwords.words('english'))
        
        # Simple topic extraction based on sentence importance
        important_sentences = []
        for sentence in sentences:
            words = nltk.word_tokenize(sentence.lower())
            words = [w for w in words if w not in stop_words and w.isalnum()]
            if len(words) > 5:  # Only consider substantial sentences
                important_sentences.append(sentence)
        
        return important_sentences[:5]  # Return top 5 important sentences

class BlogGenerationCrew:
    def __init__(self):
        self.tools = YouTubeBlogTools()
        
    def create_agents(self):
        # Research Agent
        researcher = Agent(
            role='Research Analyst',
            goal='Extract and analyze YouTube video content',
            backstory="""You are an expert at analyzing video content and extracting
                        meaningful insights from transcripts and metadata.""",
            tools=[
                self.tools.extract_video_info,
                self.tools.get_transcript,
                self.tools.analyze_sentiment
            ],
            verbose=True
        )
        
        # Content Writer
        writer = Agent(
            role='Content Writer',
            goal='Transform video content into engaging blog posts',
            backstory="""You are a skilled content writer who excels at creating
                        engaging blog posts from video content while maintaining
                        the original message and adding value.""",
            tools=[self.tools.extract_key_topics],
            verbose=True
        )
        
        # Editor
        editor = Agent(
            role='Content Editor',
            goal='Polish and optimize blog content',
            backstory="""You are a meticulous editor who ensures blog posts are
                        well-structured, engaging, and optimized for readability.""",
            verbose=True
        )
        
        return researcher, writer, editor

    def create_tasks(self, video_url, researcher, writer, editor):
        # Task 1: Research and Analysis
        research_task = Task(
            description=f"""Analyze the YouTube video at {video_url}.
                          Extract video information, transcript, and perform
                          sentiment analysis. Compile all findings.""",
            agent=researcher
        )

        # Task 2: Content Writing
        writing_task = Task(
            description="""Using the research findings, create a well-structured
                          blog post. Include an engaging introduction, main points
                          from the video, and a conclusion.""",
            agent=writer
        )

        # Task 3: Editing and Optimization
        editing_task = Task(
            description="""Review and polish the blog post. Ensure proper formatting,
                          add headers and subheaders, and optimize for readability.
                          Return the final version.""",
            agent=editor
        )

        return [research_task, writing_task, editing_task]

    def generate_blog(self, video_url):
        # Create agents
        researcher, writer, editor = self.create_agents()
        
        # Create tasks
        tasks = self.create_tasks(video_url, researcher, writer, editor)
        
        # Create and run the crew
        crew = Crew(
            agents=[researcher, writer, editor],
            tasks=tasks,
            verbose=True
        )
        
        result = crew.kickoff()
        return result

# Usage example
def main():
    # Initialize the blog generation crew
    blog_crew = BlogGenerationCrew()
    
    # Example video URL
    video_url = "https://www.youtube.com/watch?v=example"
    
    # Generate blog
    result = blog_crew.generate_blog(video_url)
    print("\nFinal Blog Post:")
    print(result)

if __name__ == "__main__":
    main()
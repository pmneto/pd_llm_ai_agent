import re
from typing import Optional
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain.agents import Tool

def extract_video_id(url_or_query: str) -> Optional[str]:
    """Extracts ID from a term, or queries a term"""
    if 'youtube.com' in url_or_query or 'youtu.be' in url_or_query:
        match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url_or_query)
        if match:
            return match.group(1)
    else:
        try:
            with YoutubeDL({'quiet': True}) as ydl:
                result = ydl.extract_info(f"ytsearch1:{url_or_query}", download=False)
                return result['entries'][0]['id']
        except Exception:
            return None
    return None

def extract_subtitles(video_id: str) -> Optional[str]:
    """Extracts subtitles from videos"""
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        for lang in ['pt-BR', 'pt', 'en']:
            if transcripts.find_transcript([lang]):
                trans = transcripts.find_transcript([lang]).fetch()
                return " ".join([t['text'] for t in trans])
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception:
        return None

def query_youtube_video(prompt: str) -> str:
    """Searches a video and extracts a small piece of subtitles"""
    video_id = extract_video_id(prompt)
    if not video_id:
        return "❌ Não consegui encontrar um vídeo correspondente."

    legenda = extract_subtitles(video_id)
    url = f"https://www.youtube.com/watch?v={video_id}"

    if legenda:
        return f"🎥 Vídeo encontrado: {url}\n\n📜 Trecho da legenda:\n{legenda[:1000]}..."
    return f"🎥 Vídeo encontrado: {url}\n\n⚠️ Não foi possível extrair as legendas desse vídeo."

## Cria Tool para o agente
#youtube_tool = Tool(
#    name="YouTubeVideoInfo",
#    func=query_youtube_video,
#    description="Use this tool to search YouTube videos and extract subtitles as context when relevant."
#)
#
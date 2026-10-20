from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Chord Line Formatter")

class SongInput(BaseModel):
    text: str

def process_chords(input_text: str) -> str:
    lines = input_text.split("\n")
    chords = {"A", "B", "C", "D", "E", "F", "G", "Am", "Em", "A7", "G7", "D7", "F#", "Bm", "Cmaj7", "Dm", "F#m", "E7", "C#m", "G#m", "B7"}
    formatted_lines = []
    
    for line in lines:
        is_chord_line = False
        trimmed_line = line.strip()
        
        if trimmed_line:
            words = trimmed_line.split()
            for word in words:
                if word in chords:
                    is_chord_line = True
                    break
        
        if is_chord_line:
            formatted_lines.append("$" + line)
        else:
            formatted_lines.append(line)
            
    return "\n".join(formatted_lines)

# This handles the main webpage view to clear the "Not Found" error
@app.get("/", response_class=HTMLResponse)
async def home_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chord Line Formatter</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background-color: #f4f7f6; color: #333; }
            h2 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
            textarea { width: 100%; height: 220px; padding: 12px; font-family: 'Courier New', monospace; font-size: 15px; border: 2px solid #bdc3c7; border-radius: 6px; box-sizing: border-box; resize: vertical; background: white; }
            textarea:focus { border-color: #3498db; outline: none; }
            button { background-color: #3498db; color: white; border: none; padding: 14px 20px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 15px; width: 100%; transition: background 0.2s; }
            button:hover { background-color: #2980b9; }
            .box { margin-bottom: 25px; }
            label { font-weight: 600; margin-bottom: 8px; display: inline-block; color: #34495e; }
        </style>
    </head>
    <body>
        <h2>Music Chord Line Formatter</h2>
        <div class="box">
            <label>Paste your raw text (chords and lyrics) below:</label>
            <textarea id="inputText" placeholder="C        G&#10;Lyrics go here..."></textarea>
        </div>
        <button onclick="formatText()">Format & Add $ Signs</button>
        <div class="box" style="margin-top: 30px;">
            <label>Your Formatted Output:</label>
            <textarea id="outputText" readonly placeholder="The updated text with $ lines will appear here..."></textarea>
        </div>

        <script>
            async function formatText() {
                const inputText = document.getElementById('inputText').value;
                if(!inputText.trim()) { alert('Please enter some text first!'); return; }
                
                try {
                    const response = await fetch('/format', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: inputText })
                    });
                    const data = await response.json();
                    document.getElementById('outputText').value = data.formatted_text;
                } catch (err) {
                    alert('Error communicating with server.');
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/format")
async def format_chords(song: SongInput):
    if not song.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    output_text = process_chords(song.text)
    return {"formatted_text": output_text}

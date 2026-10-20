from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Chord Line Formatter API")

# Define what the incoming data should look like
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

@app.post("/format")
async def format_chords(song: SongInput):
    if not song.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    output_text = process_chords(song.text)
    return {"formatted_text": output_text}

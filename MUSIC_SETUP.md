# Background Music Setup

The site includes a music player that can play "Define Myself" by Marcus Maison & Mandi Fisher.

## Option 1: Link to Apple Music (Current)

The music player currently links to the Apple Music page. Users can click the link to listen on Apple Music.

## Option 2: Host Your Own Music File

To enable automatic playback:

1. Download "Define Myself" from Apple Music (if you have the rights)
2. Save it as `define-myself.mp3` in `entries/static/entries/audio/`
3. Update `base.html` to uncomment the audio source line:
   ```html
   <source src="{% static 'entries/audio/define-myself.mp3' %}" type="audio/mpeg">
   ```

## Option 3: Use a Different Music Service

You can also:
- Use Spotify embed
- Use YouTube embed
- Host music on a CDN
- Use royalty-free music

## Current Implementation

- Music player appears in bottom-right corner
- Users can toggle music on/off
- Music preference is saved in browser localStorage
- Links to Apple Music for easy access


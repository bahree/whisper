# Use Whisper to create Speech-to-text for a podcast

I wanted to see how good (or not) Whisper is both in terms of AIQ, and easy of use. Whisper is OpenAI's newly released ASR implementation which is open-sourced. :v:	

I decided to use Sam's [TiwML Podcast](https://twimlai.com/podcast/twimlai/) as the test bed. :ok_hand:

There are a few steps to get this going:

1. You need to install all the dependencies
2. If using a GPU make sure it is properly configured for your OS implementation
3. You need to install whisper
4. We download and save (as mp3) all the episodes from YouTube where the podcasts are [published](https://www.youtube.com/playlist?list=PLILZm3MRkvH83C46bZ4rPmB-jKWBltWkP)
5. We use whisper to run through each of these episodes and transcribe them - saving three files for each episode:
    - Text file - this contains the STT (speech to text) transcription
    - VTT file - This is a WebVTT (Web Video Text Tracks), also known as a WebSRT, and is a time-indexed file format used for synchronized video caption playback
    - SRT file - This a SubRip Subtitle file - essentially it is subtitle information including start and end time-stamps and associated sequential number of subtitles.

## Transcribed output files

If you just want the transcribed files, at the time of writing this there were 525 published episodes that I have all transcribed. These were done using the base model form Whisper and can be found in the :file_folder:	twiml-episodes-whisper-transcribed.

- You can download all of the files as one zip file too -- :card_file_box: twiml-episodes-transcribed.zip

## Dependencies

There are a few things that are needed to get whisper deployed and running locally. The first is that you have a local GPU that can support CUDA. At a high level, the OS doesn't matter as long as the CUDA support is there. In my case I ran this on WSL2 with Ubuntu.
:writing_hand: TODO: Code already checked-in; need to outline details here.

## How to run this

:writing_hand: TODO: Code already checked-in; need to outline details here.

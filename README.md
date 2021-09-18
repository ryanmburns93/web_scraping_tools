# Recording and Transcription Webscraping Toolkit

This repository is designed to provide automated scripts which have been helpful for accessing videos and transcripts from various platforms. 

## Introduction
This repository houses tools developed for automating the progression through the video recording to transcription text pipeline. I have used Cisco WebEx Meetings, Microsoft Stream, and Otter.ai for audio recording and/or transcription. 

## Technologies
* Python 3.8.5
* Selenium 3.141.0
* Webvtt 0.4.6

## Code Files
The relevant scripts included are listed below with a brief description.

* **download_otter.ai_transcripts.py**
	* Download transcripts (.txt) from [Otter.ai](https://otter.ai/ "Otter.ai") for each video uploaded to the website with the account.
* **download_webex_videos.py**
	* Download videos (.mp4) and transcripts/captions (.vtt) from [Cisco Webex Meetings](https://www.webex.com "Cisco Webex") for each video personally recorded with the platform. Transcript files are downloaded when available but may not be accessible depending on profile access level.
* **download_ms_stream_transcripts.py**
	* Download transcripts (.vtt) from [Microsoft Stream](https://www.microsoft.com/en-us/microsoft-365/microsoft-stream "MS Stream") for each video uploaded to the platform.
* **scraping_utilities.py**
	* Centralized platform-agnostic scripts and utility functions leveraged across multiple modules.
	* Utility functions include:
		* launch_webdriver() - Instantiate the webdriver application.
		* scroll() - Scroll down webpage with infinite scroll.
		* go_to_downloads() - Navigate to downloads folder regardless of OS.
* **vtt_caption_parsing.py**
	* Read all .vtt caption files from a specified directory. The [WebVTT file format](https://fileinfo.com/extension/vtt "VTT File Info") can contain a variety of video metadata, but the .vtt files corresponding to the videos hosted on these platforms typically include audio segment transcriptions. Each segment info contains the transcribed text, the timestamps for the beginning and end of the segment, and occasionally the speaker when multiple participants are in the audio and their ID is associated with their person (dialing into a conference call while signed in to the platform, for example). The transcripts from the MS Stream platform also include the confidence value between zero and one of the accuracy of the segment transcription.
		* Future work: I am currently working on an automatic speech recognition model finetuned to my voice, and these shorter segments are critical to the outcome of the project. The training audio clips must be short (less than 30 seconds) to avoid extreme computing costs, and even an exciting project like ASR cannot justify manual data labeling through hours of audio - although recent advances from the [wav2vec2.0 model (Baevski et al. 2020)](https://arxiv.org/abs/2006.11477v3 "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations") and its recent descendants suggest notable improvement from finetuning on as little as 10 minutes of labeled audio. More to come - follow my profile to see the final product!


""""
 AlbumCutter is a program that uses `youtube-dl` and `pydub` to download albums
 off of youtube and break them into individual files under a specified directory

 This class provides the functions to
  * Obtain the file
  * Parse track listing
  * From the track listing, splice the audio file into individual tracks and
    export them into the filesystem

 AlbumCutter is intialized with the URL of the youtube vdieo, followed by a
 string containing the tracklist (delimited by newlines), along with the output
 directory.

 Copyright (c) Paul Longtine <paul@nanner.co>
"""
import re, os
from subprocess import call, Popen, PIPE
from pydub import AudioSegment

class AlbumCutter:
	def __init__( self, url, tracklist, output ):
		self.tracklist = tracklist
		self.url       = url
		self.output    = output
		self.fname     = None
		self.audio     = None
		self.tracks    = None
		
		# Make the directory
		if os.path.exists(output):
			print("ERROR: Directory exists, aborting")
			return

		try:
			os.mkdir(output)
		except:
			print("ERROR: Could not make directory ({})".format(output))
			return

		assert self.get_audio(self.url)
		self.process_tracklist(self.tracklist)
		self.export(self.output)

	# fetches audio from URL.
	def get_audio( self, url ):
		print("Downloading audio...")
		# youtube-dl -q -x -o$(output)/$(VIDEO ID).$(EXTENSION)
		if not call(['youtube-dl', '-q', '-x',
		             '-o{}/%(id)s.%(ext)s'.format(self.output), url]):
			return False

		# This second call here finds the filename for the audio just downloaded
		# It's not elegant at all, and it was the best solution I could find.
		# The name of the file ends up in `output` with a newline at the end.
		p = Popen(['youtube-dl', '--get-filename', '--skip-download',
		           '-x', '-o{}/%(id)s.%(ext)s'.format(self.output), url],
		           stdin=PIPE, stdout=PIPE, stderr=PIPE)
		output, err = p.communicate()
		#removes pesky newline, if it exists
		output = output[:-1] if output[-1] == "\n" else output

		if err != '':
			print(err)
			return False

		# Loads file into the fancy manipulator thingmajig I found on the web
		print("Trying to load file ({})".format(output))
		try:
			#TODO actually figure out proper encoding memnonic for this function
			#     Currently, it just assumes the extension IS the memnonic...
			#                ...which is bad. We don't want that.
			self.audio = AudioSegment.from_file(output, output.split(".")[1])
		except Exception, e:
			print("ERROR: Could not load audio\n{}".format(e))

		print("Loaded audio")

		self.fname = output

	# gives meaning to tracklist using format:
	# [ { 'start': <starting time>, 'end': <ending time>, 'title': <title> }, ]
	def process_tracklist( self, tracklist):
		tracks = []
		# Regex for finding hour, minute, and second. I am proud of this.
		rt = re.compile(r'((?P<hr>\d+):)?((?P<min>\d+):)(?P<sec>\d+)')
		for track in tracklist.split("\n"):
			# Finds hour, minute and second and converts it into miliseconds
			times = rt.search(track)
			ms = self.to_ms(times.group('hr'),
			                times.group('min'),
			                times.group('sec'))
			# If time is not a thing, continue. This is not a track listing
			if ms == None:
				continue
			# Remove timestamp and prettify the title
			title = rt.sub('', track)
			title = re.sub('[^-a-zA-Z0-9_.() ]+', '', title)
			title = title.strip()
			# Get prevous track and set the end to this start time
			if len(tracks) > 0:
				if type(tracks[-1]) == dict:
					tracks[-1]["end"] = ms
			tracks.append({"start":ms,
			               "end":-1,
			               "title":title})
		self.tracks = tracks

	# Converts hours, minutes, and seconds into ms and adds them into one number
	def to_ms( self, hour, minute, second ):
		hour   = 0 if hour == None else int(hour)
		minute = 0 if minute == None else int(minute)
		try:
			second = int(second)
		except:
			return None
		#             ms in hour        ms in minute        ms in second
		return (hour * 3600000) + (minute * 60000) + (second * 1000)

	# Exports tracks into specified directory
	def export( self, directory ):
		assert self.tracks != None
		# Loop through tracks and process them
		for track in self.tracks:
			print("Processing track: '{}'".format(track['title']))
			t = self.audio[track['start']:track['end']]
			path = os.path.join(directory, "{}.mp3".format(track['title']))
			try:
				t.export(path, format="mp3")
			except:
				print("ERROR: Could not export ({})".format(path))

	def __del__( self ):
		del self.audio

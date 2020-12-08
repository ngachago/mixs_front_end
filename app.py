import streamlit as st
import os
import json
import soundfile
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from mixs.youtube import YouTubeTools
from mixs.split import splitter
import streamlit.components.v1 as components
from streamlit.media_file_manager import _calculate_file_id, STATIC_MEDIA_ENDPOINT

stem_urls = []

# def display_waveform(song, instrument):
#     colours = {
#     'vocals': '#069692',
#     'piano': '#4a9683',
#     'drums': '#014209',
#     'bass': '#4e5251',
#     'other': '#000000'
#     }

#     fig = plt.figure(figsize=(12,0.75))
#     ax = plt.subplot()
#     plt.plot(song, c='#e8e2e1');
#     ax.spines['left'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.xaxis.set_visible(False)
#     ax.yaxis.set_visible(False)
#     ax.set_facecolor(colours[instrument])
#     fig.patch.set_facecolor(colours[instrument])

#     return fig

# Change background image
# def app():

st.set_page_config(page_title='MixS', page_icon=None, layout='wide', initial_sidebar_state='auto')

stylesheet = '<link rel="stylesheet" href="styles/app.css">'
st.markdown(stylesheet, unsafe_allow_html=True)

# Markdown texts for heading
col1, col2 = st.beta_columns(2)
col1.image("logo_transparent.png", width=260)
col2.markdown("## Practice like a Pro!")

# st.markdown("<h2 style='text-align: center; color: white; font-family: Verdana'>Get high quality backing tracks!</h2>",unsafe_allow_html=True)
# Fetching YouTube link from the end-user
col3, col4 = st.beta_columns([10,1])

youtube_link = st.text_input("Enter the YouTube link of the track to be separated")


# Fetching the song from YouTube
def youtube_display(url):
    return st.video(url)

def np_audio(np_array, stem_name, samplerate=44100):
    soundfile.write('temp.wav', np_array, samplerate, 'PCM_24')
    st.audio('temp.wav', format='audio/wav')
    with open("temp.wav", "rb") as f:
        file_id = _calculate_file_id(f.read(), "audio/wav")
        wav_url = f'{STATIC_MEDIA_ENDPOINT}/{file_id}.wav'
        stem_urls.append({
            'src': wav_url,
            'name': stem_name
            })




if youtube_link != "":
    link = YouTubeTools(youtube_link)
    button = st.button("Separate")

    if button:
        link.clear_wavs()
        filename = link.get_audio_and_directory()
        stems, rate = splitter(filename)
        rate = int(rate)

        for stem, audio in stems.items():
            np_audio(audio, stem, rate)

        # if stems != None:
        #     st.markdown("<h3 style='text-align: left; color: white; font-family: Monaco'>Vocals</h3>",unsafe_allow_html=True)
        #     np_audio(stems['vocals'], rate)

        #     st.markdown("<h3 style='text-align: left; color: white; font-family: Monaco'>Piano</h3>",unsafe_allow_html=True)
        #     np_audio(stems['piano'], rate)


        #     st.markdown("<h3 style='text-align: left; color: white; font-family: Monaco'>Drums</h3>",unsafe_allow_html=True)
        #     # write('./media/drums.wav', rate, stems['drums'])


        #     st.markdown("<h3 style='text-align: left; color: white; font-family: Monaco'>Bass</h3>",unsafe_allow_html=True)
        #     # write('./media/bass.wav', rate, stems['bass'])


        #     st.markdown("<h3 style='text-align: left; color: white; font-family: Monaco'>Other</h3>",unsafe_allow_html=True)
            # write('./media/other.wav', rate, stems['other'])

        components.html(f'''
                <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" />
<link rel="stylesheet" href="http://naomiaro.github.io/waveform-playlist/css/main.css">
  <div id="top-bar" class="playlist-top-bar">
<div class="playlist-toolbar">
    <div class="btn-group">
      <span class="btn-pause btn btn-warning"><i class="fa fa-pause"></i></span>
      <span class="btn-play btn btn-success"><i class="fa fa-play"></i></span>
      <span class="btn-stop btn btn-danger"><i class="fa fa-stop"></i></span>
      <span class="btn-rewind btn btn-success"><i class="fa fa-fast-backward"></i></span>
      <span class="btn-fast-forward btn btn-success"><i class="fa fa-fast-forward"></i></span>
    </div>
    <span class="audio-pos">00:00:00.0</span>
  </div>
</div>
<div id='playlist' data-urls='{json.dumps(stem_urls)}'> </div>

<script src="//code.jquery.com/jquery-2.1.4.min.js"></script>
<script type="text/javascript" src="http://naomiaro.github.io/waveform-playlist/js/waveform-playlist.var.js"></script>
<script type="text/javascript">
  var playlist = WaveformPlaylist.init({{
  samplesPerPixel: 10000,
  mono: true,
  waveHeight: 120,
  timescale: true,
  container: document.getElementById("playlist"),
  state: "cursor",
  colors: {{
    waveOutlineColor: "#E0EFF1",
    timeColor: "grey",
    fadeColor: "black"
  }},
  controls: {{
    show: true,
    width: 150
  }},
  zoomLevels: [500, 1000, 3000, 5000, 10000]
}});

playlist
  .load(JSON.parse(document.getElementById("playlist").dataset.urls))
  .then(function() {{
    // can do stuff with the playlist.
  }});


</script>
<script type="text/javascript" src="http://naomiaro.github.io/waveform-playlist/js/emitter.js"></script>

</script>

    ''', height=1000)

    else:
        youtube_display(youtube_link)
else:
  st.image("guitar.jpg", width=1000)



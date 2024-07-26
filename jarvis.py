from RealtimeSTT import AudioToTextRecorder
import agent
import utils


if __name__ == '__main__':
    recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en", post_speech_silence_duration =0.1, silero_sensitivity = 0.4)
    hot_words = ["jarvis"]
    skip_hot_word_check = False
    print("Say Jarvis to begin...")
    while True:
        current_text = recorder.text()
        print(current_text)
        if any(hot_word in current_text.lower() for hot_word in hot_words) or skip_hot_word_check:
                    #make sure there is text
                    if current_text:
                        print("User: " + current_text)
                        recorder.stop()
                        response = agent.query_agent(current_text)
                        print(response)
                        done = utils.TTS(response)
                        recorder.start()
                        skip_hot_word_check = True if "?" in response else False

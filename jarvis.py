from RealtimeSTT import AudioToTextRecorder
import agent
import utils


if __name__ == '__main__':
    recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en", post_speech_silence_duration =0.1, silero_sensitivity = 0.4)
    hot_words = ["jarvis"]
    clear_context = "clear context"
    skip_hot_word_check = False
    print("Say Jarvis to begin...")
    while True:
        current_text = recorder.text()
        print(current_text)
        if clear_context in current_text.lower():
            done = utils.TTS("Context cleared")
            agent.clear_context()
            print("Context cleared")
        if any(hot_word in current_text.lower() for hot_word in hot_words) or skip_hot_word_check:
                    #make sure there is text
                    if current_text:
                        print("User: " + current_text)
                        recorder.stop()
                        response = agent.query_agent(current_text)
                        #logic for determing which aspect of the response to TTS
#
#
                        if response: 
                            done = utils.TTS(response)
                            skip_hot_word_check = "?" in response
                        else:
                            skip_hot_word_check = False                
                        recorder.start()

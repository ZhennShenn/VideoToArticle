import re
import os
import datetime
import spacy


def combine_sentence():
    # set the path to the folder with screenshots
    screenshots_path = "Vozvrat_tovarov_neplatel'schikom_NDS_v_1S_8.3_Buhgalt"

    # set the path to the text file with timecode
    try:
        text_path = "test.srt"
        # replace the file extension with ".txt"
        new_text_path = os.path.splitext(text_path)[0] + '.txt'

        # rename the file
        os.rename(text_path, new_text_path)
    except:
        new_text_path = "test.txt"

    # create a list to store the sentences
    sentences = []


    # read the text file and extract the sentences and their timecodes
    with open(new_text_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            try:
                timecode = lines[i].strip()
                start_time, end_time = re.findall(r'\d{2}:\d{2}:\d{2}', timecode)
                text = lines[i + 1].strip()
                sentences.append({'start_time': start_time, 'end_time': end_time, 'text': text})
            except:
                pass

    text = " ".join([sentence['text'] for sentence in sentences])
    # with open('text.txt', 'w') as f:
    #     f.write(text)
    print(text)
    get_annotation(text)
    # iterate through the screenshots and match the corresponding sentences
    for filename in os.listdir(screenshots_path):
        try:
            screen_start_time = int(filename.split("_")[-1].replace(".jpg", "").split("-")[0])
            screen_end_time = int(filename.split("_")[-1].replace(".jpg", "").split("-")[1])
            screen_start_time, screen_end_time = sec_to_hhmmss(screen_start_time), sec_to_hhmmss(screen_end_time)
            matching_sentences = [sentence for sentence in sentences
                                  if screen_start_time <= sentence['start_time'] < screen_end_time]
            combined_text = " ".join([sentence['text'] for sentence in matching_sentences])
            start_time_sec, end_time_sec = hhmmss_to_sec(screen_start_time), hhmmss_to_sec(screen_end_time)
            # print(start_time_sec, end_time_sec)
            # print(combined_text)
        except:
            pass


def sec_to_hhmmss(seconds):
    # function to convert seconds to HH:MM:SS format
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def hhmmss_to_sec(time):
    time_delta = datetime.timedelta(hours=int(time[:2]), minutes=int(time[3:5]), seconds=int(time[6:]))
    return time_delta.total_seconds()


def get_annotation(text):
    # Load the Russian language model for spaCy
    nlp = spacy.load("ru_core_news_sm")

    # Define the article variable containing the text of the article (limited by the user)
    article = text  # Insert your text here

    # Define the maximum length of the annotation in characters
    max_length = 300

    # Process the article with spaCy
    doc = nlp(article)

    # Extract the top 3 nouns and their frequencies from the article
    nouns = {}
    for token in doc:
        if token.pos_ == "NOUN":
            if token.lemma_ in nouns:
                nouns[token.lemma_] += 1
            else:
                nouns[token.lemma_] = 1
    top_nouns = sorted(nouns.items(), key=lambda item: item[1], reverse=True)[:3]
    print(top_nouns)

    # Generate a summary of the article based on the top nouns
    summary = "В статье рассказывается о " + ", ".join([noun[0] for noun in top_nouns]) + ". "

    # Extract the most-repeated verb from the article
    verbs = {}
    for token in doc:
        if token.pos_ == "VERB":
            if token.lemma_ in verbs:
                verbs[token.lemma_] += 1
            else:
                verbs[token.lemma_] = 1
    most_repeated_verb = max(verbs.items(), key=lambda item: item[1])[0]

    # # Append a sentence to the summary based on the most-repeated verb
    # summary += "В статье " + most_repeated_verb + " " + " ".join(article.split()[:10]) + "..."

    # Trim the summary to the maximum length
    summary = summary[:max_length]

    # Print the summary
    print(summary)


if __name__ == '__main__':
    combine_sentence()

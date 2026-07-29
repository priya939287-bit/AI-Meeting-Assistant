def extract_action_items(transcript):

    action_items = []

    sentences = transcript.split(".")

    keywords = ["will", "should", "must", "need to", "schedule"]

    for sentence in sentences:

        sentence = sentence.strip()

        for keyword in keywords:

            if keyword in sentence.lower():

                action_items.append(sentence)

                break

    return action_items
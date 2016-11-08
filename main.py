import nltk
from dataset import DataSet


def main():

    ds = DataSet()
    #ds.create()
    ds.load()
    print(ds.df.describe())

    ds.save()

    print('Finished')

def main2():
    from afinn import Afinn
    import pandas as pd


    #2
    df = pd.read_pickle('data.pickle')

    afinn = Afinn()

    afinn_scores = [afinn.score(text) for text in df.Utterance]

    print(len(afinn_scores))

    df['afinn'] = afinn_scores


    #3
    #play = df[df['Play'] == 'hamlet']
    from_character = {}
    speaker = ''
    previous_speaker = ''

    dfp = df[df.Play=='hamlet']

    for i, r in dfp.iterrows():

        print('row: ', r)
        speaker = r['Speaker']

        if len(previous_speaker) > 0:
            print('Speaking from {} to {}'.format(speaker, previous_speaker))
            # Get the list of speakers that this speaker has spoken to
            if speaker in from_character:
                to_character = from_character[speaker]
            else:
                to_character = {}
                from_character[speaker] = to_character

            if previous_speaker in to_character:
                to_character[previous_speaker] += r['afinn']
            else:
                to_character[previous_speaker] = r['afinn']

        previous_speaker = speaker


if __name__ == '__main__':
    main2()

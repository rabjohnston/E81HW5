import nltk
from processing import Processing

from dataset import DataSet


def main():

    ds = DataSet()
    ds.create()
    ds.save()

    ds.load()
    #print(ds.df.describe())

    # tokens = Processing.get_tokens(ds.df['Utterance'], [Processing.remove_punctuation], [Processing.remove_stopwords])
    #
    # allWordDist = nltk.FreqDist(tokens)
    #
    # print(allWordDist.most_common())

    df = ds.get_by_speaker();

    for item in df:
        print(item)
        print(df[item])


    print('Finished')


if __name__ == '__main__':
    main()

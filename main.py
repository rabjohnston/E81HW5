import nltk
from dataset import DataSet


def main():

    ds = DataSet()
    #ds.create()
    ds.load()
    print(ds.df.describe())

    ds.save()

    print('Finished')


if __name__ == '__main__':
    main()

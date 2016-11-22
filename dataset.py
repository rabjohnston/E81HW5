from xml.etree.ElementTree import ElementTree
from os import listdir
import pandas as pd


class DataSet:
    """
    Holds all the plays in a dataframe by Play/Act/Scene/Speaker.

    create(): Loads data from XML files and stores in pandas dataframe. Will run this once and then call the save()
      method to store as pickle.
    save(): Stores dataframe to disk
    load() Loads dataframe from disk
    """
    def __init__(self):
        self.raw_files = {}
        self.df = pd.DataFrame(columns=['Play', 'Act', 'Scene', 'Speaker', 'Utterance'])
        self.chars = pd.DataFrame()

        self._plays_utterances = {}


    def get_by(self, group_name, df):
        """
        Generic method for us to split the data by a specific grouping
        :param group_name: the name of the group to split by
        :param df: the whole of the data in a pandas dataframe
        :return: a dict with keys = group names and values are the utterances.
        """
        awv = {}

        for item in df[group_name].unique():
            dfp = df[df[group_name] == item]

            # Generate one big string for the full group
            alltext = ''
            for text in dfp['Utterance']:
                alltext += text + ' '

            awv[item] = alltext

        return awv


    def get_by_play(self):
        """
        Get the uttereances for each play
        :return: a dict, keyed on play
        """
        return self.get_by('Play', self.df)


    def get_by_speaker(self):
        """
        Get the utterances for each speaker
        :return: a dict, keyed on speaker
        """
        return self.get_by('Speaker', self.df)


    def get_by_play_by_speaker(self):
        """
        Get all the utterences for a speaker, grouped by play
        :return: a dict of plays, with every entry a dict of speakers.
        """
        all_plays = {}
        for item in self.df['Play'].unique():
            dfp = self.df[self.df['Play'] == item]
            this_play = self.get_by('Speaker', dfp)
            all_plays[item] = this_play

        return all_plays


    def parse(self, play, xml):
        """
        Parse an individual XML file.
        :param play:
        :param xml:
        :return:
        """
        for i, act in enumerate(xml.findall('ACT')):
            for j, scene in enumerate(act.findall('SCENE')):
                for k, speech in enumerate(scene.findall('SPEECH')):
                    speaker = speech.findall('SPEAKER')[0].text

                    lines = ''
                    for line in speech.findall('LINE'):
                        stage_dirs = line.findall('STAGEDIR')
                        if( (stage_dirs is not None )
                                and (len(stage_dirs) > 0)
                                and (stage_dirs[0] is not None)
                                and (stage_dirs[0].tail is not None)):
                            try:
                                lines = lines + stage_dirs[0].tail + ' '
                            except:
                                print('Exception')
                        elif( line.text is None):
                            print('None')
                        else:
                            lines = lines + line.text + ' '

                    # Store this utterance.
                    self.df = self.df.append({'Play': play, 'Act': i, 'Scene': j, 'Speaker':speaker, 'Utterance' : lines},
                                             ignore_index=True)



    def readXMLFromFile(self, file):
        # print(file)
        xml = ElementTree().parse('./texts/{}'.format(file))
        play = file[:-4]

        return play, xml


    def create(self):
        """
        Loads raw data from xml and parses it into Act/Scene/Speaker/Utterance.
        An utterance is multiple continuous lines by the same speaker.
        :return: Nothing
        """


        for file in listdir("./texts"):
            if file.endswith(".xml"):
                play, xml = self.readXMLFromFile(file)
                self.raw_files[play] = xml
                self.parse(play, xml)


    def loadCharacters(self):
        self.chars = pd.read_csv('Shakespeare_characters.txt',sep='\t',encoding = 'ISO-8859-1')

        print('Play ', self.chars.Play.unique())

    def save(self):
        """
        Save internal data to a pickle
        :return:
        """
        self.df.to_pickle('data.pickle')

    def load(self):
        """
        Load play data from pickle anc characters data from CSV
        :return:
        """
        self.df = pd.read_pickle('data.pickle')

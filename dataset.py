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

                    self.df = self.df.append({'Play': play, 'Act': act, 'Scene': scene, 'Speaker':speaker, 'Utterance' : lines},
                                             ignore_index=True)
                    #print('{},{},{},{}: {}'.format(play, act.text, scene.text, speaker, lines))


    def readXMLFromFile(self, file):
        print(file)
        xml = ElementTree().parse('../texts/{}'.format(file))
        play = file[:-4]

        return play, xml


    def create(self):
        """
        Loads raw data from xml and parses it into Act/Scene/Speaker/Utterance.
        An utterance is multiple continuous lines by the same speaker.
        :return: Nothing
        """

        for file in listdir("../texts"):
            if file.endswith(".xml"):
                play, xml = self.readXMLFromFile(file)
                self.raw_files[play] = xml
                self.parse(play, xml)


    def save(self):
        """
        Save internal data to a pickle
        :return:
        """
        self.df.to_pickle('data.pickle')

    def load(self):
        """
        Load data from pickle
        :return:
        """
        self.df = pd.read_pickle('data.pickle')
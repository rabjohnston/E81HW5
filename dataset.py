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

        # self._names = {'hamlet':'Hamlet', 'othello':'Othello', 'hen_v':'Henry V',
        #                'timon':'Timon of Athens', 'm_for_m':'Measure for Measure',
        #                'a_and_c':'Antony and Cleopatra', 'lear':'King Lear', '??????':'King Edward III', 'j_caesar':'Julius Caesar',
        #                'macbeth':'Macbeth', 'titus':'Titus Andronicus', 'win_tale':"The Winter's Tale", 'rich_iii.xml':'Richard III',
        #                'as_you':'As You Like It', 'coriolan':'Coriolanus', 'tempest':'The Tempest', 'hen_iv_2':'Henry IV Part 2',
        #                'r_and_j':'Romeo and Juliet', 'pericles':'Pericles', 'hen_iv_1':'Henry IV Part 1', 'cymbelin':'Cymbeline',
        #                '??????':'The Two Noble Kinsmen', 'lll':"Love's Labour's Lost", 'taming':'The Taming of the Shrew',
        #                'merchant':'The Merchant of Venice', 'troilus':'Troilus and Cressida', 'john':'King John',
        #                "All's Well That Ends Well":'all_well', 'rich_ii':'Richard II', 'hen_viii':'Henry VIII',
        #                'two_gent':'The Two Gentlemen of Verona', 'm_wives':'The Merry Wives of Windsor',
        #                'hen_vi_3':'Henry VI Part 3', 'much_ado':'Much Ado About Nothing', 'hen_vi_1':'Henry VI Part 1',
        #                'hen_vi_2':'Henry VI Part 2', 't_night':'Twelfth Night', 'com_err':'The Comedy of Errors',
        #                'dream':"A Midsummer Night's Dream"}

    def get_by(self, group_name):

        awv = {}

        for item in self.df[group_name].unique():
            dfp = self.df[self.df[group_name] == item]

            # Generate one big string for the full group
            alltext = ''
            for text in dfp['Utterance']:
                alltext += text + ' '

            awv[item] = alltext

        return awv


    def get_by_play(self):
        return self.get_by('Play')


    def get_by_speaker(self):
        return self.get_by('Speaker')



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

                    # Store this utterance. NB, the utterance is converted to lowercase to make it easier to parse later
                    self.df = self.df.append({'Play': play, 'Act': i, 'Scene': j, 'Speaker':speaker, 'Utterance' : lines},
                                             ignore_index=True)
                    #print('{},{},{},{}: {}'.format(play, i, j, speaker, lines))


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

        #self.loadCharacters()
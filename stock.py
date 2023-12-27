import abc
import pandas as pd


class Stock(abc.ABC):
    """Abstract base class"""
    def __init__(self):
        """Initialize pandas dataframe with the given file."""
        self.data: str
        self.dataframe = pd.read_csv(self.data, parse_dates=True, index_col=0)

    def all_columns(self):
        """Return list of all columns in DataFrame.

        :return: list
        """
        return list(self.dataframe.columns)

    def get_date(self, date_from, date_to):
        """Return dataframe with specific date.

        :param date_from: str
        :param date_to: str
        :return: DataFrame
        """
        self.date = self.dataframe.loc[date_from: date_to]
        return self.date


class Microsoft(Stock):
    def __init__(self):
        self.data = 'data/MSFT.csv'
        # alternative way, can get file from url
        # self.data = 'https://cloudbox.ku.ac.th/index.php/s/Df8PBnNTF63w63r/download'
        super().__init__()


class Google(Stock):
    def __init__(self):
        self.data = 'data/GOOGL.csv'
        # alternative way, can get file from url
        # self.data = 'https://cloudbox.ku.ac.th/index.php/s/2AFfqg4PztggNwo/download'
        super().__init__()


class Tesla(Stock):
    def __init__(self):
        self.data = 'data/TSLA.csv'
        # alternative way, can get file from url
        # self.data = 'https://cloudbox.ku.ac.th/index.php/s/j2yMLN3tZMW7qMQ/download'
        super().__init__()


class Intel(Stock):
    def __init__(self):
        self.data = 'data/INTC.csv'
        # alternative way, can get file from url
        # self.data = 'https://cloudbox.ku.ac.th/index.php/s/brcjfiGewwgQBiT/download'
        super().__init__()


class Meta(Stock):
    def __init__(self):
        self.data = 'data/FB.csv'
        # alternative way, can get file from url
        # self.data = 'https://cloudbox.ku.ac.th/index.php/s/iKXTcdDeoJdJPBd/download'
        super().__init__()


class Amazon(Stock):
    def __init__(self):
        self.data = 'data/AMZN.csv'
        # alternative way, can get file from url
        # self.data = 'https://cloudbox.ku.ac.th/index.php/s/FZE2Cj5LFd8kwoy/download'
        super().__init__()


class Apple(Stock):
    def __init__(self):
        self.data = 'data/AAPL.csv'
        # alternative way, can get file from url
        # self.data = 'https://cloudbox.ku.ac.th/index.php/s/qWWzW3kJ3zJneZa/download'
        super().__init__()

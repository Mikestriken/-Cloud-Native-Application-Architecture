import os, typing, collections, string
from enum import Enum, auto


class WordOccurrences:
    """
    A class that represents the number of times words occurred in a textfile
    
    Attributes:
        wordOccurrenceDict (typing.Dict[str, int]): Dictionary in the format of {'word': numberOfOccurrences}
        occurrenceWordDict (typing.Dict[int, str]): Dictionary in the format of {numberOfOccurrences: 'word1, word2'}
        largestOccurrenceIndex (int): largest valid index for occurrenceWordDict
        
    Methods:
        printTopKOccurrences(k: int): Prints k words that occurred the most in the file this class was initialized with
    """
    
    class Options(Enum):
        SKIP_NO_OCCURRENCES = auto()
        INCLUDE_NO_OCCURRENCES = auto()
    
    def __init__(self, pathToTxtFile: os.PathLike):
        """
        Args:
            pathToTxtFile (os.PathLike): path to textfile that should have its contents read to get word occurrences.
        """
        
        self.wordOccurrenceDict:typing.Dict[str, int] = self._getUniqueWordOccurrences(pathToTxtFile)
        self.largestOccurrenceIndex:int = self.wordOccurrenceDict.pop("MAX", -1)
        assert self.largestOccurrenceIndex != -1, "ERR: No words found"
        self.occurrenceWordDict:typing.Dict[int, str] = self._swapStrIntDictKeyValue(self.wordOccurrenceDict)
    
    def _getUniqueWordOccurrences(self, pathToTxtFile: os.PathLike) -> typing.Dict[str, int]:
        """
        Returns a dictionary containing all the unique words found in the text file found at path.
        The value for each word item in the dictionary is the number of times the word was found in the file.
        Note: Punctuation is excluded from the key values

        Args:
            pathToTxtFile (os.PathLike): the path/to/the/file

        Returns:
            typing.Dict[str, int]: {'word': numOccurrences}
        """
        
        assert os.path.exists(pathToTxtFile), f"ERR: Could not find file at: {pathToTxtFile}"
        
        wordOccurrenceDict:typing.Dict[str, int] = collections.defaultdict(int)
        mostOccurringWordOccurrences:int = 0
        with open(pathToTxtFile, 'r') as txtFile:
            
            fileContent = txtFile.read()
            fileContent = fileContent.translate(str.maketrans('', '', string.punctuation)) # Remove all punctuation from fileContent
            
            words = fileContent.split()
            
            for word in words:
                
                # if word in wordOccurrenceDict:
                wordOccurrenceDict[word] += 1
                mostOccurringWordOccurrences = wordOccurrenceDict[word] if wordOccurrenceDict[word] > mostOccurringWordOccurrences else mostOccurringWordOccurrences
                
        wordOccurrenceDict["MAX"] = mostOccurringWordOccurrences
        
        return wordOccurrenceDict
    
    def _swapStrIntDictKeyValue(self, dictToSwap: typing.Dict[str, int]) -> typing.Dict[int, str]:
        """
        Swaps keys and values in passed in dictionary arg.
        Note: Expects type typing.Dict[str, int]. Matching keys merge their string values with ", ".

        Args:
            dictToSwap (typing.Dict[str, int]): Dictionary with string keys and int value; to have its keys and values swapped.

        Returns:
            typing.Dict[int, str]: Inverted dictionary argument (keys and values swapped). Matching int keys are merged with ", " for value to delimit matches.
        """
        swappedDict:typing.Dict[int, str] = {}
        
        for key, value in dictToSwap.items():
            if value in swappedDict:
                swappedDict[value] += f", {key}"
                
            else:
                swappedDict[value] = key
                
        return swappedDict
    
    def printTopKOccurrences(self, k:int, options:Options = Options.INCLUDE_NO_OCCURRENCES):
        """
        Prints a list of the top k words that occurred the most to the console.

        Args:
            - k (int): Number of occurrences to print
            - options (Options, optional): Specifies if cases were no words had x number of occurrences count.
                - Defaults To: Options.INCLUDE_NO_OCCURRENCES
                - Valid Values include:
                    - Options.SKIP_NO_OCCURRENCES
                    - Options.INCLUDE_NO_OCCURRENCES
        
        Sample Output:
            printTopKOccurrences(5)
            ```txt
            ======================================================================
            77 Occurrences:
            we
            ----------------------------------------------------------------------
            76 Occurrences:
            about
            ----------------------------------------------------------------------
            No words with: 75 Occurrences
            ----------------------------------------------------------------------
            No words with: 74 Occurrences
            ----------------------------------------------------------------------
            No words with: 73 Occurrences
            ======================================================================
            ```
            
            printTopKOccurrences(5, Options.SKIP_NO_OCCURRENCES)
            ```txt
            ======================================================================
            77 Occurrences:
            we
            ----------------------------------------------------------------------
            76 Occurrences:
            about
            ----------------------------------------------------------------------
            70 Occurrences:
            this
            ----------------------------------------------------------------------
            68 Occurrences:
            my
            ----------------------------------------------------------------------
            65 Occurrences:
            could
            ======================================================================
            ```
        """
        
        assert len(self.occurrenceWordDict) > 0, "self.occurrenceWordDict not initialized!"
        
        retrievedAllKOccurrences:bool = False
        numberOfOccurrencesIterator:int = self.largestOccurrenceIndex
        numberOfOccurrencesFound:int = 0
        
        topKOccurrence =                                                                                        f"======================================================================\n"
        while not retrievedAllKOccurrences:
            occurrenceFound:bool = False
            
            if numberOfOccurrencesIterator in self.occurrenceWordDict:
                occurrenceFound = True ; numberOfOccurrencesFound += 1
                topKOccurrence +=                                                                               f"{numberOfOccurrencesIterator} Occurrences:\n"
                topKOccurrence +=                                                                               f"{self.occurrenceWordDict[numberOfOccurrencesIterator]}\n"
                
            elif options == self.Options.INCLUDE_NO_OCCURRENCES:
                occurrenceFound = True ; numberOfOccurrencesFound += 1
                topKOccurrence +=                                                                               f"No words with: {numberOfOccurrencesIterator} Occurrences\n"
            
            numberOfOccurrencesIterator -= 1
            
            if numberOfOccurrencesFound == k: retrievedAllKOccurrences = True
                
            if (not retrievedAllKOccurrences and occurrenceFound):
                topKOccurrence +=                                                                               f"----------------------------------------------------------------------\n"
                
            
        topKOccurrence +=                                                                                       f"======================================================================\n"
        
        print(topKOccurrence)


# For development testing purposes
if __name__ == "__main__":
    textfilePath = os.path.join(__file__, "..\\..\\tests\\sample_data\\Sample1.txt")
    wordOccurrences = WordOccurrences(textfilePath)
    
    wordOccurrences.printTopKOccurrences(5, wordOccurrences.Options.INCLUDE_NO_OCCURRENCES)
    
    print(f"Largest: {wordOccurrences.occurrenceWordDict[wordOccurrences.largestOccurrenceIndex]}")
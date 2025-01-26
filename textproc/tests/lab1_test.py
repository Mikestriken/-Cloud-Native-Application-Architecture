import pytest

from textproc.lab1 import *

@pytest.fixture
def wordOccurrences_Sample1():
    textfilePath = os.path.join(__file__, "..\\sample_data\\Sample1.txt")
    wordOccurrences = WordOccurrences(textfilePath)
    
    return wordOccurrences

def test_Sample1(wordOccurrences_Sample1, capsys):
    
    # Print 1
    wordOccurrences_Sample1.printTopKOccurrences(5, wordOccurrences_Sample1.Options.SKIP_NO_OCCURRENCES)
    
    captured = capsys.readouterr()
    assert not "No words with:" in captured.out, "printTopKOccurrences(5, wordOccurrences_Sample1.Options.SKIP_NO_OCCURRENCES) did not output as expected. Expected Missing Word occurrences to be skipped."
    
    # Print 2
    wordOccurrences_Sample1.printTopKOccurrences(5, wordOccurrences_Sample1.Options.INCLUDE_NO_OCCURRENCES)
    
    captured = capsys.readouterr()
    assert "No words with:" in captured.out, "printTopKOccurrences(5, wordOccurrences_Sample1.Options.INCLUDE_NO_OCCURRENCES) did not output as expected. Expected Missing Word occurrences to be included."
    
    # Print 3
    wordOccurrences_Sample1.printTopKOccurrences(5)
    
    captured = capsys.readouterr()
    assert "No words with:" in captured.out, "printTopKOccurrences(5) did not output as expected. Expected Missing Word occurrences to be included."
    
    mostOccurringWords:string = wordOccurrences_Sample1.occurrenceWordDict[wordOccurrences_Sample1.largestOccurrenceIndex]
    assert mostOccurringWords == "we"
    
    with pytest.raises(Exception):
        wordOccurrences_Sample1.occurrenceWordDict[wordOccurrences_Sample1.largestOccurrenceIndex + 1] # largestOccurrenceIndex should be the most occurring word index
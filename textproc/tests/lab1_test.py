import pytest

from textproc.lab1 import *

@pytest.fixture
def wordOccurrences_Sample1():
    textfilePath = os.path.join(__file__, "..\\sample_data\\Sample1.txt")
    wordOccurrences = WordOccurrences(textfilePath)
    
    return wordOccurrences

@pytest.fixture
def wordOccurrences_Sample2():
    textfilePath = os.path.join(__file__, "..\\sample_data\\Sample2.txt")
    wordOccurrences = WordOccurrences(textfilePath)
    
    return wordOccurrences

def test_printTopKOccurrences(wordOccurrences_Sample1, wordOccurrences_Sample2, capsys):
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
    
    # Print 4
    wordOccurrences_Sample2.printTopKOccurrences(100)
    
    captured = capsys.readouterr()
    assert not "0" in captured.out, "printTopKOccurrences(1000) did not output as expected. Output is printing occurrences less than 1."
    assert not "-1" in captured.out, "printTopKOccurrences(1000) did not output as expected. Output is printing occurrences less than 1."
    
def test_largestOccurrenceIndex(wordOccurrences_Sample1, wordOccurrences_Sample2):
    mostOccurringWords:string = wordOccurrences_Sample1.occurrenceWordDict[wordOccurrences_Sample1.largestOccurrenceIndex]
    assert mostOccurringWords == "the"
    
    mostOccurringWords:string = wordOccurrences_Sample2.occurrenceWordDict[wordOccurrences_Sample2.largestOccurrenceIndex]
    assert mostOccurringWords == "This"
    
    with pytest.raises(Exception):
        wordOccurrences_Sample1.occurrenceWordDict[wordOccurrences_Sample1.largestOccurrenceIndex + 1] # largestOccurrenceIndex should be the most occurring word index
PYTHON = python3

TARGET = 40253480_detector

.DEFAULT_GOAL = help
.PHONY = clean help run test

FILE1 =
FILE2 =

all: $(TARGET)

$(TARGET): $(TARGET).py

clean:
	rm -rf $(TARGET).pyc
	rm -rf __pycache__

help:
	@echo '--------------------------HELP-------------------------------'
	@echo 'To run the project type: make run <file_1_path> <file_2_path>'
	@echo '-------------------------------------------------------------'

run: $(TARGET)
	$(PYTHON) $(TARGET).py $(FILE1) $(FILE2)

testPlagiarism: $(TARGET)
	@echo r'Testing plagiarism test cases in ../data/plagiarismXX'
	@for file in ../data/plagiarism*; do echo 'Testing' $$file; $(PYTHON) $(TARGET).py $$file/1.txt $$file/2.txt;done

testNonPlagiarism: $(TARGET)
	@echo 'Testing non-plagiarism test cases in ../data/okayXX'
	@for file in ../data/okay*; do echo 'Testing' $$file; $(PYTHON) $(TARGET).py $$file/1.txt $$file/2.txt;done

test: testPlagiarism testNonPlagiarism
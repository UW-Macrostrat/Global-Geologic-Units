# Available inputs
These are the available input files that are part of a standard input dataset for GeoDeepDive applications. You can find an example set at [https://geodeepdive.org/dev_subsets/example_input.zip](https://geodeepdive.org/dev_subsets/example_input.zip).


## contents
+ **Version info**: pdftotext 3.04, http://www.glyphandcog.com/opensource.html
+ **Format**: txt
+ **Information**: Raw text dump from the source PDF, as extracted by pdftotext.


## cuneiform-page-*.bmp.html
+ **Version info**: Cuneiform 1.1.0
+ **Format**: HTML (hOCR)
+ **Information**: OCR via Cuneiform


## page-*.hocr.html
+ **Version info**: Tesseract 3.02
+ **Format**: HTML (hOCR)
+ **Information**: OCR via Tesseract


## fonts.text
+ **Version info**:
+ **Format**: TSV
+ **Information**: Fonttype/Formatting recognition via a custom script. Utilizes the output of the Cuneiform OCR process.
+ **Column structure**:
  - *font/layout* -- Denotes whether the word is special in font or formatting (e.g. centered, italic, or just a normal word)
  - *page* -- Source page of the word
  - *left_edge* -- The left coordinate of the word's bounding box
  - *top_edge* -- The top coordinate of the word's bounding box
  - *right_edge* -- The right coordinate of the word's bounding box
  - *bottom_edge* -- The bottom coordinate of the word's bounding box
  - *word* -- The word


## input.text
+ **Version info**: Stanford CoreNLP 1.3.5 (http://nlp.stanford.edu/software/corenlp.shtml)
+ **Format**:
+ **Information**: Natural language processing of the document. Utilizes the output of the Tesseract OCR process
+ **Column structure**:
  - *wordidx* (integer) -- Word's index within the sentences
  - *word* (text) -- Word
  - *poses* (text) -- Parts of speech
  - *ners* (text) -- Named entity recognizer
  - *lemmas* (text) -- base or dictionary form of word
  - *dep_paths* (text[]) -- Dependency type
  - *dep_parents* (integer[]) -- Word index of the dependency parent
  - *sentid* (integer) -- sentence's index within the document
  - *bounding_box* (text[]) -- The bounding box of the word (its location within the document)


## input_text.xml
+ **Version info**: Stanford CoreNLP 3.5.2 (http://nlp.stanford.edu/software/corenlp.shtml)
+ **Format**: xml
+ **Information**: Natural language processing of the document. Utilizes the extracted text of the PDF.
+ **Usage**:


## sentences_nlp
+ **Version info**: Stanford Core NLP 1.3.5, http://nlp.stanford.edu/software/corenlp.shtml
+ **Format**: TSV
+ **Information**: NLP and Fonttype outputs (input.text and fonts.tex) combined into one DeepDive-ready table.
+ **Column structure**:
  - *docid* (text) -- document's unique ID within our internal database
  - *sentid* (integer) -- sentence's index within the document
  - *wordidx* (integer[]) -- Word's index within the sentences
  - *word* (text[]) -- Word
  - *poses* (text[]) -- Parts of speech
  - *ners* (text[]) -- Named entity recognizer
  - *lemmas* (text[]) -- base or dictionary form of word
  - *dep_paths* (text[]) -- Dependency type
  - *dep_parents* (integer[]) -- Word index of the dependency parent
  - *font* (text[]) -- Special font
  - *layout* (text[]) -- Layout notes

+ *Usage*:
    psql -d database -c "CREATE TABLE sentences_nlp (docid text, sentid integer, wordidx integer[], words text[], poses text[], ners text[], lemmas text[], dep_paths text[], dep_parents integer[], font text[], layout text[]);"
    cat sentences_nlp | psql -d database -c "COPY sentences_nlp FROM STDIN"


## sentences_nlp352
+ **Version info**: Stanford Core NLP 3.5.2, http://nlp.stanford.edu/software/corenlp.shtml
+ **Format**: TSV
+ **Information**: "New" NLP (NLPCore 3.5.2). Same as the XML output above, but formatted into a DeepDive-ready table
+ **Column structure**:
  - *docid* (text) -- document's unique ID within our internal database
  - *sentid* (integer) -- sentence's index within the document
  - *wordidx* (integer[]) -- Word's index within the sentences
  - *word* (text[]) -- Word
  - *poses* (text[]) -- Parts of speech
  - *ners* (text[]) -- Named entity recognizer
  - *lemmas* (text[]) -- base or dictionary form of word
  - *dep_paths* (text[]) -- Dependency type
  - *dep_parents* (integer[]) -- Word index of the dependency parent
+ **Usage**:
````
  psql -d database -c "CREATE TABLE sentences_nlp352 (docid text, sentid integer, wordidx integer[], words text[], poses text[], ners text[], lemmas text[], dep_paths text[], dep_parents integer[]);"

  cat sentences_nlp352 | psql -d database -c "COPY sentences_nlp352 FROM STDIN"
````

## sentences_nlp352_bazaar
+ **Version info**: Stanford Core NLP 3.5.2, http://nlp.stanford.edu/software/corenlp.shtml
+ **Format**: TSV
+ **Information**: "New" NLP (NLPCore 3.5.2). Same as the XML output above, but formatted into a DeepDive-ready table. This output should match the format output by the "bazaar" utility (https://github.com/HazyResearch/bazaar)
+ **Column structure**:
  - *docid* (text) -- document's unique ID within our internal database
  - *sentid* (integer) -- sentence's index within the document
  - *sentence* (text) --
  - *word* (text[]) -- Word
  - *lemmas* (text[]) -- base or dictionary form of word
  - *poses* (text[]) -- Parts of speech
  - *ners* (text[]) -- Named entity recognizer
  - *character_position* (integer[]) -- Starting index of the word within the sentence
  - *dep_paths* (text[]) -- Dependency type
  - *dep_parents* (integer[]) -- Word index of the dependency parent
+ **Usage**:
````
  psql -d database -c "CREATE TABLE sentences_nlp352_bazaar (docid text, sentid integer, sentence text, words text[], lemmas text[], poses text[], ners text[], character_position integer[], dep_paths text[], dep_parents integer[]);"

  cat sentences_nlp352_bazaar | psql -d database -c "COPY sentences_nlp352_bazaar FROM STDIN"
````

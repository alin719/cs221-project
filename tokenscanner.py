"""
 * File: tokenscanner.cpp
 * ----------------------
 * Implementation for the TokenScanner class.
 * 
 * @version 2014/10/08
 * - removed 'using namespace' statement
"""

import string

"""
 * File: tokenscanner.h
 * --------------------
 * This file exports a <code>TokenScanner</code> class that divides
 * a string into individual logical units called <b><i>tokens</i></b>.
"""

#ifndef _tokenscanner_h
#define _tokenscanner_h

#include <iostream>
#include <string>
#include "private/tokenpatch.h"

"""
 * Type: TokenType
 * ---------------
 * This enumerated type defines the values of the
 * <code>getTokenType</code> method.
"""

class TokenType:
    SEPARATOR = 0
    WORD = 1
    NUMBER = 2
    STRING = 3
    OPERATOR = 4

"""
 * Class: TokenScanner
 * -------------------
 * This class divides a string into individual tokens.  The typical
 * use of the <code>TokenScanner</code> class is illustrated by the
 * following pattern, which reads the tokens in the string variable
 * <code>input</code>:
 *
 *<pre>
 *    TokenScanner scanner(input);
 *    while (scanner.hasMoreTokens()):
 *       string token = scanner.nextToken();
 *       ... process the token ...
 *    
 *</pre>
 *
 * The <code>TokenScanner</code> class exports several additional methods
 * that give clients more control over its behavior.  Those methods are
 * described individually in the documentation.
"""
class TokenScanner:
    """
     * Constructor: TokenScanner
     * Usage: TokenScanner scanner;
     *        TokenScanner scanner(str);
     *        TokenScanner scanner(infile);
     * ------------------------------------
     * Initializes a scanner object.  The initial token stream comes from
     * the specified string or input stream, if supplied.  The default
     * constructor creates a scanner with an empty token stream.
    """
    def TokenScanner():
        initScanner()
        setInput("")


    def TokenScanner(std::string str):
        initScanner()
        setInput(str)


    def TokenScanner(std::istream & infile):
        initScanner()
        setInput(infile)

    """
     * Destructor: ~TokenScanner
     * -------------------------
     * Deallocates the storage associated with this scanner.
    """
    virtual ~TokenScanner()

    """
     * Method: setInput
     * Usage: scanner.setInput(str)
     *        scanner.setInput(infile)
     * --------------------------------
     * Sets the token stream for this scanner to the specified string or
     * input stream.  Any previous token stream is discarded.
    """
    def setInput(std::string str)
    def setInput(std::istream & infile)

    """
     * Method: hasMoreTokens
     * Usage: if (scanner.hasMoreTokens()) ...
     * ---------------------------------------
     * Returns <code>true</code> if there are additional tokens for this
     * scanner to read.
    """
    bool hasMoreTokens()

    """
     * Method: nextToken
     * Usage: token = scanner.nextToken()
     * -----------------------------------
     * Returns the next token from this scanner.  If <code>nextToken</code>
     * is called when no tokens are available, it returns the empty string.
    """
    std::string nextToken()

    """
     * Method: saveToken
     * Usage: scanner.saveToken(token)
     * --------------------------------
     * Pushes the specified token back into this scanner's input stream.
     * On the next call to <code>nextToken</code>, the scanner will return
     * the saved token without reading any additional characters from the
     * token stream.
    """
    def saveToken(std::string token)

    """
     * Method: getPosition
     * Usage: int pos = scanner.getPosition()
     * ---------------------------------------
     * Returns the current position of the scanner in the input stream.
     * If <code>saveToken</code> has been called, this position corresponds
     * to the beginning of the saved token.  If <code>saveToken</code> is
     * called more than once, <code>getPosition</code> returns -1.
    """
    int getPosition() const

    """
     * Method: ignoreWhitespace
     * Usage: scanner.ignoreWhitespace()
     * ----------------------------------
     * Tells the scanner to ignore whitespace characters.  By default,
     * the <code>nextToken</code> method treats whitespace characters
     * (typically spaces and tabs) just like any other punctuation mark
     * and returns them as single-character tokens.
     * Calling
     *
     *<pre>
     *    scanner.ignoreWhitespace()
     *</pre>
     *
     * changes this behavior so that the scanner ignore whitespace characters.
    """
    def ignoreWhitespace()

    """
     * Method: ignoreComments
     * Usage: scanner.ignoreComments()
     * --------------------------------
     * Tells the scanner to ignore comments.  The scanner package recognizes
     * both the slash-star and slash-slash comment format from the C-based
     * family of languages.  Calling
     *
     *<pre>
     *    scanner.ignoreComments()
     *</pre>
     *
     * sets the parser to ignore comments.
    """
    def ignoreComments()

    """
     * Method: scanNumbers
     * Usage: scanner.scanNumbers()
     * -----------------------------
     * Controls how the scanner treats tokens that begin with a digit.  By
     * default, the <code>nextToken</code> method treats numbers and letters
     * identically and therefore does not provide any special processing for
     * numbers.  Calling
     *
     *<pre>
     *    scanner.scanNumbers()
     *</pre>
     *
     * changes this behavior so that <code>nextToken</code> returns the
     * longest substring that can be interpreted as a real number.
    """
    def scanNumbers()

    """
     * Method: scanStrings
     * Usage: scanner.scanStrings()
     * -----------------------------
     * Controls how the scanner treats tokens enclosed in quotation marks.  By
     * default, quotation marks (either single or double) are treated just like
     * any other punctuation character.  Calling
     *
     *<pre>
     *    scanner.scanStrings()
     *</pre>
     *
     * changes this assumption so that <code>nextToken</code> returns a single
     * token consisting of all characters through the matching quotation mark.
     * The quotation marks are returned as part of the scanned token so that
     * clients can differentiate strings from other token types.
    """
    def scanStrings()

    """
     * Method: addWordCharacters
     * Usage: scanner.addWordCharacters(str)
     * --------------------------------------
     * Adds the characters in <code>str</code> to the set of characters
     * legal in a <code>WORD</code> token.  For example, calling
     * <code>addWordCharacters("_")</code> adds the underscore to the
     * set of characters that are accepted as part of a word.
    """
    def addWordCharacters(std::string str)

    """
     * Method: isWordCharacter
     * Usage: if (scanner.isWordCharacter(ch)) ...
     * -------------------------------------------
     * Returns <code>true</code> if the character is valid in a word.
    """
    bool isWordCharacter(char ch) const

    """
     * Method: addOperator
     * Usage: scanner.addOperator(op)
     * -------------------------------
     * Defines a new multicharacter operator.  Whenever you call
     * <code>nextToken</code> when the input stream contains operator
     * characters, the scanner returns the longest possible operator
     * string that can be read at that point.
    """
    def addOperator(std::string op)

    """
     * Method: verifyToken
     * Usage: scanner.verifyToken(expected)
     * -------------------------------------
     * Reads the next token and makes sure it matches the string
     * <code>expected</code>.  If it does not, <code>verifyToken</code>
     * throws an error.
    """
    def verifyToken(std::string expected)

    """
     * Method: getTokenType
     * Usage: TokenType type = scanner.getTokenType(token)
     * ----------------------------------------------------
     * Returns the type of this token.  This type will match one of the
     * following enumerated type constants: <code>EOF</code>,
     * <code>SEPARATOR</code>, <code>WORD</code>, <code>NUMBER</code>,
     * <code>STRING</code>, or <code>OPERATOR</code>.
    """
    TokenType getTokenType(std::string token) const

    """
     * Method: getChar
     * Usage: int ch = scanner.getChar()
     * ----------------------------------
     * Reads the next character from the scanner input stream.
    """
    def getChar():
        return isp.get()

    """
     * Method: ungetChar
     * Usage: scanner.ungetChar(ch)
     * -----------------------------
     * Pushes the character <code>ch</code> back into the scanner stream.
     * The character must match the one that was read.
    """
    def ungetChar(int ch):

    """
     * Method: getStringValue
     * Usage: string str = scanner.getStringValue(token)
     * --------------------------------------------------
     * Returns the string value of a token.  This value is formed by removing
     * any surrounding quotation marks and replacing escape sequences by the
     * appropriate characters.
    """
    std::string getStringValue(std::string token) const

    """ Private section"""

    """*********************************************************************/
    """ Note: Everything below this point in the file is logically part   """
    """ of the implementation and should not be of interest to clients.   """
    """*********************************************************************/

    """
     * Private type: StringCell
     * ------------------------
     * This type is used to construct linked lists of cells, which are used
     * to represent both the stack of saved tokens and the set of defined
     * operators.  These types cannot use the Stack and Lexicon classes
     * directly because tokenscanner.h is an extremely low-level interface,
     * and doing so would create circular dependencies in the .h files.
    """
    class StringCell:
        def __init__():
            strr
            link
    

    class NumberScannerState:
        INITIAL_STATE = 0
        BEFORE_DECIMAL_POINT = 1
        AFTER_DECIMAL_POINT = 2
        STARTING_EXPONENT = 3
        FOUND_EXPONENT_SIGN = 4
        SCANNING_EXPONENT = 5
        FINAL_STATE = 6


    buffer              """ The original argument string"""
    isp           """ The input stream for tokens """
    bool stringInputFlag            """ Flag indicating string input"""
    bool ignoreWhitespaceFlag       """ Scanner ignores whitespace  """
    bool ignoreCommentsFlag         """ Scanner ignores comments    """
    bool scanNumbersFlag            """ Scanner parses numbers      """
    bool scanStringsFlag            """ Scanner parses strings      """
    std::string wordChars           """ Additional word characters  """
    StringCell *savedTokens         """ Stack of saved tokens       """
    StringCell *operators           """ List of multichar operators """

    """ Private method prototypes"""
    def initScanner()
    def skipSpaces()
    std::string scanWord()
    std::string scanNumber()

    def scanString():
        std::string token = ""
        char delim = isp->get()
        token += delim
        escape = False
        while (true):
            int ch = isp->get()
            if (ch == EOF) error("scanString: found unterminated string")
            if (ch == delim and not escape) break
            escape = (ch == '\\') and not escape
            token += ch
        
    return token + delim

    bool isOperator(std::string op)
    bool isOperatorPrefix(std::string op)



def setInput(strr):
    stringInputFlag = true
    buffer = strr
    isp = new std::istringstream(buffer)
    savedTokens = NULL


def setInput(std::istream & infile):
    stringInputFlag = false
    isp = &infile
    savedTokens = NULL


bool def hasMoreTokens():
    std::string token = nextToken()
    saveToken(token)
    return (token != "")


std::string def nextToken():
    if (self.savedTokens != NULL):
        cp = self.savedTokens
        token = cp.strr
        savedTokens = cp.link
        # delete cp ??
        return token
    
    while (true):
        if (ignoreWhitespaceFlag):
            skipSpaces()
        ch = self.isp.get()
        if (ch == '/' and ignoreCommentsFlag):
            ch = isp.get()
            if (ch == '/'):
                while (true):
                    ch = isp.get()
                    if (ch == '\n' or ch == '\r' or ch == EOF) break
                
                continue
             else if (ch == '*'):
                int prev = EOF
                while (true):
                    ch = isp->get()
                    if (ch == EOF or (prev == '*' and ch == '/')) break
                    prev = ch
                
                continue
            
            if (ch != EOF) isp->unget()
            ch = '/'
        
        if (ch == EOF) return ""
        if ((ch == '"' or ch == '\'') and scanStringsFlag):
            isp->unget()
            return scanString()
        
        if (ch.isdigit() and scanNumbersFlag):
            isp.unget()
            return scanNumber()
        
        if (isWordCharacter(ch)):
            isp.unget()
            return scanWord()
        
        std::string op = std::string(1, ch)
        while (isOperatorPrefix(op)):
            ch = isp->get()
            if (ch == EOF) break
            op += ch
        
        while (op.length() > 1 and not isOperator(op)):
            isp->unget()
            op.erase(op.length() - 1, 1)
        
        return op
    


def saveToken(token):
    cp = StringCell()
    cp.strr = token
    cp.link = savedTokens
    savedTokens = cp


def ignoreWhitespace():
    ignoreWhitespaceFlag = true


def ignoreComments():
    ignoreCommentsFlag = true


def scanNumbers():
    scanNumbersFlag = true


def scanStrings():
    scanStringsFlag = true


def addWordCharacters(str):
    wordChars += str


def addOperator(op):
    cp = StringCell()
    cp.strr = op
    cp.link = operators
    operators = cp


def getPosition() const:
    if (savedTokens == NULL):
        return int(isp->tellg())
     else:
        return int(isp->tellg()) - savedTokens->str.length()
    


def isWordCharacter(ch):
    return ch.isalnum or wordChars.find(ch) != std::string::npos


def verifyToken(std::string expected):
    std::string token = nextToken()
    if (token != expected):
        error("def verifyToken: Found \"" + token + "\"" +
              " when expecting \"" + expected + "\"")
    


def getTokenType(token):
    if (token == ""):
        return TokenType(EOF)
    char ch = token[0]
    if (isspace(ch)):
        return self.SEPARATOR
    if (ch == '"' or (ch == '\'' and token.length() > 1)):
        return self.STRING
    if (ch.isdigit()):
        return self.NUMBER
    if (isWordCharacter(ch)):
        return self.WORD
    return OPERATOR


def getStringValue(token):
    strr = ""
    start = 0
    finish = len(token)
    if (finish > 1 and (token[0] == '"' or token[0] == '\'')):
        start = 1
        finish -= 1
    
    for i in xrange(start, finish):
        char ch = token[i]
        if (ch == '\\'):
            ch = token[++i]
            if (ch.isdigit() or ch == 'x'):
                int base = 8
                if (ch == 'x'):
                    base = 16
                    i++
                
                int result = 0
                int digit = 0
                while (i < finish):
                    ch = token[i]
                    if (ch.isdigit()):
                        digit = ch - '0'
                     else if (ch.isalpha()):
                        digit = ch.toupper() - 'A' + 10
                     else:
                        digit = base
                    
                    if (digit >= base) break
                    result = base * result + digit
                    i++
                
                ch = char(result)
                i--
             else:
                switchDict = {
                    'a': '\a',
                    'b': '\b',
                    'f': '\f',
                    'n': '\n',
                    'r': '\r',
                    't': '\t',
                    'v': '\v',
                    '"': '"',
                    '\'': '\'',
                    '\\': '\\'
                }
                ch = switchDict[ch]
                
            
        
        strr += ch
    
    return strr;


def ungetChar(int):
    isp->unget();


""" Private methods"""

def initScanner():
    ignoreWhitespaceFlag = false;
    ignoreCommentsFlag = false;
    scanNumbersFlag = false;
    scanStringsFlag = false;
    operators = NULL;


"""
 * Implementation notes: skipSpaces
 * --------------------------------
 * Advances the position of the scanner until the current character is
 * not a whitespace character.
"""

def skipSpaces():
    while (true):
        int ch = isp->get();
        if (ch == EOF) return;
        if (not isspace(ch)):
            isp->unget();
            return;
        
    


"""
 * Implementation notes: scanWord
 * ------------------------------
 * Reads characters until the scanner reaches the end of a sequence
 * of word characters.
"""

def scanWord():
    token = "";
    while (true):
        ch = isp->get();
        if (ch == EOF) break;
        if (not isWordCharacter(ch)):
            isp->unget();
            break;
        
        token += char(ch);
    
    return token;


"""
 * Implementation notes: scanNumber
 * --------------------------------
 * Reads characters until the scanner reaches the end of a legal number.
 * The function operates by simulating what computer scientists
 * call a finite-state machine.  The program uses the variable
 * <code>state</code> to record the history of the process and
 * determine what characters would be legal at this point in time.
"""

std::string def scanNumber():
    std::string token = "";
    NumberScannerState state = NumberScannerState.INITIAL_STATE;
    while (state != FINAL_STATE):
        int ch = isp->get();
        switch (state):
        case NumberScannerState.INITIAL_STATE:
            if (not ch.isdigit()):
                error("def scanNumber: internal error: illegal call");
            
            state = NumberScannerState.BEFORE_DECIMAL_POINT;
            break;
        case NumberScannerState.BEFORE_DECIMAL_POINT:
            if (ch == '.'):
                state = NumberScannerState.AFTER_DECIMAL_POINT;
             else if (ch == 'E' or ch == 'e'):
                state = NumberScannerState.STARTING_EXPONENT;
             else if (not ch.isdigit()):
                if (ch != EOF) isp->unget();
                state = NumberScannerState.FINAL_STATE;
            
            break;
        case NumberScannerState.AFTER_DECIMAL_POINT:
            if (ch == 'E' or ch == 'e'):
                state = NumberScannerState.STARTING_EXPONENT;
             else if (not ch.isdigit()):
                if (ch != EOF) isp->unget();
                state = NumberScannerState.FINAL_STATE;
            
            break;
        case NumberScannerState.STARTING_EXPONENT:
            if (ch == '+' or ch == '-'):
                state = NumberScannerState.FOUND_EXPONENT_SIGN;
             else if (ch.isdigit()):
                state = NumberScannerState.SCANNING_EXPONENT;
             else:
                if (ch != EOF) isp->unget();
                isp->unget();
                state = NumberScannerState.FINAL_STATE;
            
            break;
        case NumberScannerState.FOUND_EXPONENT_SIGN:
            if (ch.isdigit()):
                state = NumberScannerState.SCANNING_EXPONENT;
             else:
                if (ch != EOF) isp->unget();
                isp->unget();
                isp->unget();
                state = NumberScannerState.FINAL_STATE;
            
            break;
        case NumberScannerState.SCANNING_EXPONENT:
            if (not ch.isdigit()):
                if (ch != EOF) isp->unget();
                state = NumberScannerState.FINAL_STATE;
            
            break;
        default:
            state = NumberScannerState.FINAL_STATE;
            break;
        
        if (state != NumberScannerState.FINAL_STATE):
            token += char(ch);
        
    
    return token;


"""
 * Implementation notes: scanString
 * --------------------------------
 * Reads and returns a quoted string from the scanner, continuing until
 * it scans the matching delimiter.  The scanner generates an error if
 * there is no closing quotation mark before the end of the input.
"""



"""
 * Implementation notes: isOperator, isOperatorPrefix
 * --------------------------------------------------
 * These methods search the list of operators and return true if the
 * specified operator is either in the list or a prefix of an operator
 * in the list, respectively.  This code could be made considerably more
 * efficient by implementing operators as a trie.
"""

def isOperator(std::string op):
    for (StringCell *cp = operators; cp != NULL; cp = cp->link):
        if (op == cp->str) return true;
    
    return false;


def isOperatorPrefix(std::string op):
    for (StringCell *cp = operators; cp != NULL; cp = cp->link):
        if (startsWith(cp->str, op)) return true;
    
    return false;


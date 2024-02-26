import sys, getopt, time, os, argparse

def helpUsage() :
    print(os.path.basename(__file__), '[options]')
    print('Options arguments:')
    print('-x | --xml   : exports the PDF file to XML')
    print('-t | --text  : exports the PDF file to Text')
    print('-a | --all   : exports the PDF file to XML and Text')

# TODO: to XML
def toXml() :
    startTime = time.time()
    print('exporting to xml...')
    #toXML.buildXML()
    print('--- XML in %s seconds ---' % (time.time() - startTime))
    
# TODO: to Text
def toText() :
    startTime = time.time()
    print('exporting to text...')
    
    print('--- Text in %s seconds ---' % (time.time() - startTime))

# main function with args
def main() :
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__), usage='%(prog)s [options]')
    parser.add_argument('-x', '--xml', help='export the PDF file to XML', action='store_true')
    parser.add_argument('-t', '--text', help='export the PDF file to text', action='store_true')
    parser.add_argument('--input', help='input files to convert', action='store', type=str, nargs='+', metavar=('FILE | FOLDER'))
    args = vars(parser.parse_args())
    print(args.get('input'))
    '''
    nargs stands for Number Of Arguments

        3: 3 values, can be any number you want
        ?: a single value, which can be optional
        *: a flexible number of values, which will be gathered into a list
        +: like *, but requiring at least one value
        argparse.REMAINDER: all the values that are remaining in the command line
    '''
    '''
    try :
        opts, args = getopt.getopt(argv, 'hxtad', ['help', 'xml', 'text', 'all'])
    except getopt.GetoptError as err :
        print(err)
        sys.exit(2)
    for o, a in opts :
        if o in ('-h', '--help') :
            helpUsage()
            sys.exit()
        elif o in ('-x', '--xml') :
            toXml()
        elif o in ('-t', '--text') :
            toText()
        elif o in ('-a', '--all') :
            toText()
            toXml()
        elif o == '-d' :
            global debug
            debug = 1
        else :
            assert False, "unhandled option"
    '''

if __name__ == '__main__' :
    main()
    
    
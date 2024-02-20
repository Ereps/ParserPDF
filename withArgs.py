import sys, getopt, time, os

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
    print('--- XML in %s seconds ---' % (time.time() - startTime))
    
# TODO: to Text
def toText() :
    startTime = time.time()
    print('exporting to text...')
    print('--- Text in %s seconds ---' % (time.time() - startTime))

# main function with args
def main(argv) :
    try :
        opts, args = getopt.getopt(argv, 'hxta', ['help', 'xml', 'text', 'all'])
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

if __name__ == '__main__' :
    main(sys.argv[1:])
    
    
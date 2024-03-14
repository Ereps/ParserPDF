import time, os, argparse
import Xml, Text

def helpUsage() :
    print(os.path.basename(__file__), '[options]')
    print('Options arguments:')
    print('-x | --xml   : exports the PDF file to XML')
    print('-t | --text  : exports the PDF file to Text')
    print('-a | --all   : exports the PDF file to XML and Text')

# TODO: to XML
def toXml(files : list) :
    startTime = time.time()
    print('--- exporting to xml ---')
    Xml.buildDir()
    for f in files :
        Xml.buildXML(f)
    print('--- XML in %s seconds ---' % (time.time() - startTime))
    
# TODO: to Text
def toText(files : list) :
    startTime = time.time()
    print('--- exporting to text ---')
    Text.buildDir()
    for f in files :
        Text.buildTEXT(f)
    print('--- Text in %s seconds ---' % (time.time() - startTime))

# main function with args
def main() :
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__), usage='%(prog)s [options]')
    parser.add_argument('-x', '--xml', help='exports to XML', action='store_true')
    parser.add_argument('-t', '--text', help='exports to text', action='store_true')
    parser.add_argument('-d', '--dir', help='directory with PDF files', action='store', type=str, nargs=1, metavar=('folder'))
    parser.add_argument('-f', '--file', help='PDF file(s) as input', action='store', type=str, nargs='+', metavar=('file'))
    args = vars(parser.parse_args())
    #print(args) # https://stackoverflow.com/questions/51495070/python-argparse-subparsers
    '''
    nargs stands for Number Of Arguments

        3: 3 values, can be any number you want
        ?: a single value, which can be optional
        *: a flexible number of values, which will be gathered into a list
        +: like *, but requiring at least one value
        argparse.REMAINDER: all the values that are remaining in the command line
    '''
    if not args['xml'] and not args['text'] :
        print('Need at least one export to select : --help to see what you can do')
        exit(1)
    if not args['dir'] and not args['file'] :
        print('Need at least one input to select : --help to see what you can do')
        exit(1)
    final_selection = []
    if args['dir'] and os.path.isdir(args['dir'][0]) :
        files = [os.path.join(args['dir'][0], f) for f in os.listdir(args['dir'][0]) if os.path.isfile(os.path.join(args['dir'][0], f)) and f.endswith('.pdf')]
        if not files :
            print('No PDF file in this directory')
            exit(1)
        else :
            hashmap = {}
            for i in range(len(files)) :
                hashmap[i] = files[i]
            # Print the files to select
            print('Please select which of those files you want to make the export :')
            print('%2s' % '*', '->', 'Select all')
            for i in range(len(hashmap)) :
                print('%2s' % i, '->', hashmap.get(i))
            selection = input('Entry (separator is the space): ')
            selection = list(selection.split(' '))
            if '*' in selection :
                final_selection = files
            else :
                for select_index in selection :
                    if select_index.isdigit() :
                        final_selection.append(hashmap.get(int(select_index)))
    elif args['file'] :
        for f in args['file'] :
            if not f.endswith('.pdf') :
                print('%s is not a pdf file' % f)
                args['file'].remove(f)
        final_selection = args['file']
    #print(final_selection)
    if not len(final_selection) :
        exit(1)
    if args['xml'] : 
        toXml(final_selection)
    if args['text'] :
        toText(final_selection)

if __name__ == '__main__' :
    main()
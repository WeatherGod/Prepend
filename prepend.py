#    Author: Benjamin Root
#    Copyright (C) 1989, 1991-2009 Free Software Foundation.
#    
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/.
import tempfile
import os

def PrependLicense(filename, license, comment='', author=None, lang=None) :
    # Should probably check for write permissions first in the input file
    # Note that because I am going to attempt to open for writing later,
    # it is ok that there is a 'race condition' of sorts because that
    # open command would fail if it is not writable.  This is merely
    # a sanity check before doing work.
    if not os.access(filename, os.W_OK | os.R_OK) :
        print "ERROR: %s either does not exist or is not writable" % filename
        return
    
    # This tempfile will hold the modified contents of the file
    # before being read back in order to overwrite the original file.
    tmpFile = tempfile.TemporaryFile()

    checkedShebang = False
    printedAuthor = False or (author is None)
    printedLicense = False
    for line in open(filename, 'r') :
        if not checkedShebang :
            checkedShebang = True
            if '#!' == line[0:2] :
                # Write out this line and then go back to the top
                tmpFile.write(line)
                continue

        if not printedAuthor :
            # TODO: What about newlines?
            tmpFile.write("%-4s Author: %s\n" % (comment, author))
            printedAuthor = True

        if not printedLicense :
            licLines = license.splitlines(True)
            for aLine in licLines :
                tmpFile.write("%-4s %s" % (comment, aLine))
            printedLicense = True

        tmpFile.write(line)

    # return the file back to the begining
    tmpFile.seek(0)

    destFile = open(filename, 'wb')

    for line in tmpFile :
        destFile.write(line)

    tmpFile.close()

    

latestGPL = 'v3'
licenses = {}
licenses['gplv3'] = """Copyright (C) 1989, 1991-2009 Free Software Foundation.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
"""



licenses['gpl'] = licenses['gpl' + latestGPL]


commentChars = {}
commentChars['python'] = '#'
commentChars['c'] = '//'
commentChars['c++'] = '//'
commentChars['perl'] = '#'
commentChars['java'] = '//'
commentChars['matlab'] = '%'


if __name__ == "__main__" :
    from optparse import OptionParser


    parser = OptionParser()

    parser.add_option("--gpl", dest="licname", action="store_const",
		      const="gpl", default="gpl",
		      help="Use the latest GPL (this is default)")
    parser.add_option("--gplv3", dest="licname", action="store_const",
		      const="gplv3", help="Use GPL version 3")
    #parser.add_option("--gplv2", dest="licname", action="store_const",
    #		       const="gplv2", help="Use GPL version 2")
    #parser.add_option("--bsd", dest="licname", action="store_const",
    #		       const="bsd", help="Use BSD License")

    parser.add_option("-a", "--author", dest="name", default=None,
		      help="Include AUTHOR name", metavar="AUTHOR")
    parser.add_option("-l", "--lang", dest="language", default=None,
		      help="Programming language of input file(s) (default is None)")

    options, args = parser.parse_args()

    if len(args) == 0 :
        parser.error("ERROR: No files given!")

    if options.language is None :
        comment = ''
    else :
        comment = commentChars[options.language]

    license = licenses[options.licname]
    

    for filename in args :
        PrependLicense(filename, license, comment,
		       options.name, options.language)



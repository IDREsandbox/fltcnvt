#
# This software is Copyright 2017 Regents of the University of California.
# All Rights Reserved.
#
# Created by Scott Friedman (friedman at idre.ucla.edu)
# UCLA Office of Information Technology
# Institute for Digital Research and Education
#
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs appear in all copies.
#
# This software program and documentation are copyrighted by The Regents of the University of California. The software program and documentation are supplied "as is", without any accompanying services from The Regents. The Regents does not warrant that the operation of the program will be uninterrupted or error-free. The end-user understands that the program was developed for research purposes and is advised not to rely exclusively on the program for any reason.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

import sys
import os
import re
from shutil import copyfile
from mgapilib import *

def main ():
    if len( sys.argv) < 4:
        print "usage: %s <openFlight.flt> sourceDrive targetDrive" % (sys.argv[0])
        return

    sourceDb    = sys.argv[1]
    sourceDrive = sys.argv[2]
    targetDrive = sys.argv[3]

    mgInit( None, None )

    processDb( sourceDb, sourceDrive, targetDrive )
    mgExit()

def processDb( dbFilename, srcDrive, tgtDrive ):
    #print "opening:", dbFilename
    db = mgOpenDb( dbFilename )
    if db == None:
        msgbuf = mgGetLastError()
        print msgbuf, "\n"
        return

    gotOne, texIndex, texFilename = mgGetFirstTexture( db )
    while gotOne == MG_TRUE:
        srcTexFilename = re.sub( '^/h(ome)?', srcDrive, texFilename )
        srcTexFilename = re.sub( '/', '\\\\', srcTexFilename )
        tgtTexFilename = re.sub( srcDrive, tgtDrive, srcTexFilename )
        if ( srcTexFilename[0] == srcDrive[0] ):
            # otherwise something weird happened like the referenced texture
            # is not listed at /h or /home so we will ignore it
            tgtDirectory = os.path.dirname( tgtTexFilename )
            if not os.path.exists( srcTexFilename ):
                # if the referenced texture does not actually exist
                # sometimes it's because the actual texture has an .rgba extension
                srcTexFilename = re.sub( '.rgb$', '.rgba', srcTexFilename )

            if os.path.exists( srcTexFilename ):
                if not os.path.exists( tgtTexFilename ):
                    if not os.path.exists( tgtDirectory ):
                        os.makedirs( tgtDirectory )

                copyfile( srcTexFilename, tgtTexFilename )
                if os.path.exists( srcTexFilename+".attr" ):
                    copyfile( srcTexFilename+".attr", tgtTexFilename+".attr" )
                    print "copied", srcTexFilename, " --> ", tgtTexFilename

        #print "mgReplaceTexture:", texIndex, texFilename
        mgReplaceTexture( db, texIndex, tgtTexFilename )
        gotOne, texIndex, texFilename = mgGetNextTexture( db )

    walk( db, srcDrive, tgtDrive )
    tgtDbFilename = re.sub( srcDrive, tgtDrive, dbFilename )
    tgtDirectory = os.path.dirname( tgtDbFilename )
    if not os.path.exists( tgtDbFilename ):
        if not os.path.exists( tgtDirectory ):
            os.makedirs( tgtDirectory )

        copyfile( dbFilename, tgtDbFilename )
        #print "copied", dbFilename, " --> ", tgtDbFilename

    mgSaveAsDb( db, tgtDbFilename )
    #mgWriteDb( db )
    mgCloseDb( db )

def walk( rec, srcDrive, tgtDrive ):
    while True:
        comment = mgGetComment( rec )
        if comment != None:
            if comment.find( "switch" ) > -1:
                switchRec = mgNewRec( fltSwitch )
                mgAppend( rec, switchRec )
                items = comment.split( )[1:]
                #print "SWITCH: ", items
                for item in items:
                    xrefRec = mgNewRec( fltXref )
                    mgSetAttList( xrefRec, fltXrefFilename, item )
                    mgAppend( switchRec, xrefRec )
                    #print "adding xref:", item

                #mgSetSwitchBit( switchRec, 0, 0, MG_TRUE )
                #print "switch mask/bit:", 0, "/", 0
                for idx, item in enumerate( items ):
                    if idx > 0:
                        mgAddSwitchMask( switchRec )

                    mgSetSwitchBit( switchRec, idx, idx, MG_TRUE )
                    #print "switch mask/bit:", idx, "/", idx

        code = mgGetCode( rec )
        if code == fltHeader:
            pass
        elif code == fltGroup:
            pass
        elif code == fltLod:
            pass
        elif code == fltObject:
            pass
        elif code == fltPolygon:
            pass
        elif code == fltVertex:
            pass
        elif code == fltDof:
            pass
        elif code == fltSwitch: # 362
            pass
        elif code == fltMesh: # 461
            pass
        elif code == fltXref:
            srcXrefFilename = re.sub( '^/h(ome)?', srcDrive, mgGetAttList( rec, fltXrefFilename )[2] )
            srcXrefFilename = re.sub( '/', '\\\\', srcXrefFilename )
            tgtXrefFilename = re.sub( srcDrive, tgtDrive, srcXrefFilename )
            mgSetAttList( rec, fltXrefFilename, tgtXrefFilename )
            if not os.path.exists( tgtXrefFilename ):
                #print "xref processDb", srcXrefFilename
                processDb( srcXrefFilename, srcDrive, tgtDrive )
            else:
                #print tgtXrefFilename, " exists"
                pass
        else:
            print "unknown code: ", code
            print "name        : ", mgGetName( rec )
            exit()

        childRec = mgGetChild( rec )
        if childRec:
            walk( childRec, srcDrive, tgtDrive )

        rec = mgGetNext( rec )
        if rec == None:
            break

main()

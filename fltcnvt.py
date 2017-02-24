
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
    print "opening:", dbFilename
    db = mgOpenDb( dbFilename )
    if db == None:
        msgbuf = mgGetLastError()
        print msgbuf, "\n"
        mgExit()
        exit()

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

        print "mgReplaceTexture:", texIndex, texFilename
        mgReplaceTexture( db, texIndex, tgtTexFilename )
        gotOne, texIndex, texFilename = mgGetNextTexture( db )

    walk( db, srcDrive, tgtDrive )
    tgtDbFilename = re.sub( srcDrive, tgtDrive, dbFilename )
    tgtDirectory = os.path.dirname( tgtDbFilename )
    if not os.path.exists( tgtDbFilename ):
        if not os.path.exists( tgtDirectory ):
            os.makedirs( tgtDirectory )

        copyfile( dbFilename, tgtDbFilename )
        print "copied", dbFilename, " --> ", tgtDbFilename

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
                print "SWITCH: ", items
                for item in items:
                    xrefRec = mgNewRec( fltXref )
                    mgSetAttList( xrefRec, fltXrefFilename, item )
                    mgAppend( switchRec, xrefRec )
                    print "adding xref:", item

                #mgSetSwitchBit( switchRec, 0, 0, MG_TRUE )
                #print "switch mask/bit:", 0, "/", 0
                for idx, item in enumerate( items ):
                    if idx > 0:
                        mgAddSwitchMask( switchRec )

                    mgSetSwitchBit( switchRec, idx, idx, MG_TRUE )
                    print "switch mask/bit:", idx, "/", idx

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
                print "xref processDb", srcXrefFilename
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

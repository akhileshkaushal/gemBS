#!/usr/bin/env python
"""gemBS commands"""
import argparse
import utils
import production
import sys
from sys import exit
import signal

import src

__VERSION__ = "1.7"

def gemBS():
    try:
        parser = argparse.ArgumentParser(prog="gemBS",
                description="gemBS is a wrapper to perform the different steps involved in the Bisulfite pipeline."
                )
        parser.add_argument('--loglevel', dest="loglevel", default=None, help="Log level (error, warn, info, debug)")
        parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __VERSION__)

        commands = {
            "prepare-config" : production.PrepareConfiguration,            
            "index" : production.Index,
            "mapping-commands" : production.MappingCommnads,
            "mapping" : production.Mapping,
            "merging-all" : production.MergingAll,
            "merging-sample" : production.MergingSample,
            "methylation-call" : production.MethylationCall,
            "snp-stats": production.SnpStats,
            "methylation-filtering": production.MethylationFiltering,
            "cpg-stats": production.CpgStats,            
            "bscall" : production.BsCall,
            "bscall-concatenate" : production.BsCallConcatenate,
            "bsMap-report" : production.MappingReports,
            "variants-report" : production.VariantsReports,
            "cpg-report" : production.CpgReports,
            "cpg-bigwig" : production.CpgBigwig
        }
        instances = {}

        subparsers = parser.add_subparsers(title="commands", metavar="<command>", description="Available commands", dest="command")
        
        for name, cmdClass in commands.items():
            p = subparsers.add_parser(name, help=cmdClass.title, description=cmdClass.description)
            instances[name] = cmdClass()
            instances[name].register(p)

        args = parser.parse_args()
        if args.loglevel is not None:
            src.loglevel(args.loglevel)
           
        try:
            instances[args.command].run(args)
        except utils.CommandException, e:
            sys.stderr.write("%s\n" % (str(e)))
            exit(1)
    except KeyboardInterrupt:
        exit(1)
    finally:
        pass

if __name__ == "__main__":
    gemBS()

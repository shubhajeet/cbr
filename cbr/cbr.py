#!/bin/usr/env python
import toml
import sys
import glob
import argparse
import logging
import os
import subprocess

def compare(symptoms,case):
    case_info = toml.load(case)
    case_symptom = case_info["symptoms"]
    return (calc_score(symptoms,case_symptom), case)

def calc_score(symp1,symp2):
    count = 0
    for i in symp1:
        count += (symp1.get(i,None)==symp2.get(i,None))
    return count/len(symp1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Case Based Reasoning Assistance")
    subparsers = parser.add_subparsers(dest="subcommand")
    check_parser = subparsers.add_parser("check",help="check sub-command help")
    diagnose_parser = subparsers.add_parser("diagnose",help="diagnose sub-command help")
    treat_parser = subparsers.add_parser("treat",help="treat sub-command help")
    check_parser.add_argument("symptoms",help="Toml file showing listing all the symptoms")
    diagnose_parser.add_argument("symptoms",help="Toml file showing listing all the symptoms")
    diagnose_parser.add_argument("case",help="Toml file or directory containing all the prev encountered cases")
    treat_parser.add_argument("case",help="Toml file or directory containing all the prev encountered cases")
    args = parser.parse_args()
    if args.subcommand == "diagnose":
        if args.symptoms == "-":
            symptoms = toml.loads(sys.stdin.read())
        else:
            if os.path.exists(args.symptoms):
                symptoms = toml.load(args.symptoms)
            else:
                logging.error("{} symptoms file not found".format(args.symptoms))
        if os.path.exists(args.case):
            if os.path.isfile(args.case):
                print("{} {}".format(compare(args.case)))
            else:
                cases = glob.glob(args.case+"/*.toml")
                all_check = [compare(symptoms,case) for case in cases]
                all_check = sorted(all_check,reverse=True)
                for i in range(len(all_check)):
                    print("{} {}".format(all_check[i][0],all_check[i][1]))
        else:
            logging.error("case dir/file does not exist")
    elif args.subcommand == "check":
        for script in glob.glob(args.symptoms+"/*.sh"):
            proc = subprocess.Popen(script,stdout=subprocess.PIPE)
            for line in proc.stdout.readlines():
                print(line)
    else:
        case = toml.load(args.case)
        script = os.path.join(os.path.dirname(args.case),"../solutions/"+case["solution"]["script"])
        
        proc = subprocess.Popen(script,stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            print(line)

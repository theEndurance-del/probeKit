#!/usr/bin/env python3

# Imports
import sys
import readline
import platform
import csv
import os
import subprocess

import modules.util.utils as utils

print(f'Importing custom modules', end='\r')
start = utils.timestamp()
import modules.data.AboutList as aboutList
import modules.util.exec as exec
from modules.data.OptInfHelp import PromptHelp, Options, Info
from config import colors, variables, aliases
from modules.util.led import start_editor
end = utils.timestamp()
print(f'modules took {round(end-start, 7)} sec(s). to load')

# Setup Utils
args = utils.args
ExitException = utils.ExitException
datevalue = utils.datevalue
register_history = utils.register_history
completion_list: list = [
    "use", 
    "show", 
    "set", 
    "help", 
    "exit", 
    "back", 
    "clear", 
    "run", 
    "about", 
    "list", 
    "banner", 
    "alias", 
    "unalias", 
    "unset"
]
completer = utils.completer(completion_list)


# Setting up colors (edit these in config.py)
FSUCCESS = colors.FSUCCESS
FALERT = colors.FALERT
FNORMAL = colors.FNORMAL
FURGENT = colors.FURGENT
FSTYLE = colors.FPROMPT

# Display time during statup
print(f'current session started at {datevalue()}')
utils.banner()

# Checks if history file already exists or not
if 'Linux' in platform.platform():
    histfile : str = os.path.join(os.path.expanduser('~'), '.probeKit.history')
    if os.path.exists(histfile):
        readline.read_history_file(histfile)

if 'Windows' in platform.platform():
    print(f'{FURGENT}[**] Warning: system commands will not run in windows based system')

# Session starts over here
# Not the best way to do it but it works so...
if 'Windows' not in platform.platform():
    if os.getuid() != 0:
        print(f'{FURGENT}[**] Warning: You won\'t be able to use the osprbe module without root access.')

class input_parser:
    
    def __init__(self):
        self.exit_code = 0
        # Variables also known as options to the user
        self.OPTIONS : list = [
            variables.THOST
            , variables().tport()
            , variables().PROTOCOL
            , variables().timeout()
            , variables().trycount()
            , variables().Nmap()
            , variables().Verbose()
            , variables().Threading()
           ]
        
        self.MODULE = variables.MODULE
    
    def parser(self, value: str):
        if '#' in value:
            vallist = value.split('#')
            value = utils.trim(vallist.pop(0))
        else:
            pass
    
        if value[-1] != ';':
            vallist = list(value)
            vallist.append(';')
            value = ''.join(vallist)
        
        commandlist: list = value.split(';')
        commandlist.pop(-1)
    
        for command in commandlist:
            command = utils.trim(command)
            alias_cmd: list = command.split()
            alias = alias_cmd[0]
            alias_cmd[0] = aliases.get(alias, alias)
            command = ' '.join(alias_cmd)
            if ';' in command:
                for x in command.split(';'):
                    executor(utils.trim(x))
                    continue
            else:
                self.executor(command)
    
    def executor(self, command: str):
        OPTIONS = self.OPTIONS
        cmd_split: list = command.split()
        for l in csv.reader([command], delimiter=' ', quotechar='"'):
            cmd_split_quoted = l
    
        verb = cmd_split[0]
    

        if verb == "banner":
            utils.banner()
            self.exit_code = 0

        elif verb == 'help':
            if not args(cmd_split, 1):
                Data = PromptHelp('')
                self.exit_code = Data.showHelp()
            else:
                Data = PromptHelp(args(cmd_split, 1))
                self.exit_code = Data.showHelp()

        elif verb == 'led':
            init_editor = start_editor(cmd_split)
            init_editor.start_led()

        elif verb == 'list':
            self.exit_code = aboutList.moduleHelp(self.MODULE).listmodules()

        elif verb == 'show':
            if args(cmd_split, 1):
                if args(cmd_split, 1) == 'options':
                    options = Options(self.MODULE, OPTIONS)
                    options.showOptions()
                    self.exit_code = 0

                elif args(cmd_split, 1) == 'info':
                    info = Info(self.MODULE)
                    self.exit_code = info.showInfo()

                else:
                    print(f'{FALERT}[-] Error: Invalid argument provided')
                    self.exit_code = 1
            else:
                print(f'{FALERT}[-] Error: no argument provided')
                self.exit_code = 1

        elif verb == 'back':
            if self.MODULE == '':
                raise ExitException(f'{FALERT}probeKit: exiting session')
            else:
                self.MODULE = ''
                self.exit_code = 0

        # Create an exception which exits the try block and then exits the session
        elif verb == 'exit':
            raise ExitException(f'{FALERT}probeKit: exiting session{FNORMAL}')

        elif verb == 'clear':
            if 'Windows' in platform.platform():
                os.system('cls')
                self.exit_code = 0
            else:
                print(chr(27)+'2[j')
                print('\033c')
                print('\x1bc')
                self.exit_code = 0

            if args(cmd_split, 1) == '-e':
                sys.exit(self.exit_code)

        elif verb == 'run':
            try:
                self.exit_code = exec.run(self.MODULE, OPTIONS)
            except Exception as e:
                print(e)

        # Verb(or command) to set options
        elif verb == 'set':
            OPTIONS = exec.set(OPTIONS, args(cmd_split, 1), args(cmd_split, 2))
            if args(OPTIONS, 8):
                self.exit_code = OPTIONS[8]
                OPTIONS.pop(8)
        # Verb(or command) to unset options
        elif verb == 'unset':
            OPTIONS = exec.unset(OPTIONS, args(cmd_split, 1))
            if args(OPTIONS, 8):
                self.exit_code = OPTIONS[8]
                OPTIONS.pop(8)
                    
        elif verb == 'use':
            if args(cmd_split, 1):
                if args(cmd_split, 1) in aboutList.moduleHelp.modules:
                    self.MODULE = args(cmd_split, 1)
                    print(FURGENT+f'MODULE => {self.MODULE}')
                    self.exit_code = 0
                else:
                    print(f'{FALERT}Error: Invalid module specified: \'{args(cmd_split, 1)}\'')
                    self.exit_code = 1
            else:
                print(FALERT+'Error: No module specified')
                self.exit_code = 1

        elif verb == 'about':
            if args(cmd_split, 1):
                mod = args(cmd_split, 1)
                aboutList.moduleHelp(mod).aboutModule(mod)
            else:
                aboutList.moduleHelp(self.MODULE).aboutModule(self.MODULE)

        elif verb == 'alias':
            if not args(cmd_split, 1):
                self.exit_code = 0
                for x in aliases:
                    print(x,":",aliases[x])

            elif args(cmd_split, 1) and len(commands.split('=')) == 2:
                splitCommand = commands.split('=')
                assignedCommand = splitCommand[1]
                alias = splitCommand[0].split()[1]
                if not assignedCommand or assignedCommand == '':
                    print(f'{FALERT}[-] Error: please provide a command to alias')
                    self.exit_code = 1
                else:
                    print(alias, "=>",assignedCommand)
                    aliases[alias]=assignedCommand
                    self.exit_code = 0

            else:
                print(f'{FALERT}[-] Error: Invalid Syntax')
                self.exit_code = 1

        elif verb == 'unalias':
            if args(cmd_split, 1) and args(cmd_split, 1) in aliases:
                del aliases[args(cmd_split, 1)]
                self.exit_code = 0
            else:
                print(f'{FALERT}[-] Error: no such alias \'{FURGENT}{args(cmd_split, 1)}{FALERT}\' exists')
                self.exit_code = 1
        
        elif verb in ['cd', 'chdir', 'set-location']:
            fpath = args(cmd_split, 1)
            if os.path.exists(fpath) and os.path.isdir(fpath):
                os.chdir(fpath)
                print(f'dir: {fpath}')

            else:
                print(f'{FALERT}[-] Error: no such directory: \'{fpath}\'')

        else:
            try:
                if 'Windows' not in platform.platform():
                    self.exit_code = subprocess.call((cmd_split))
                else:
                    self.exit_code = subprocess.run(commands, shell=True).returncode
                        
            except FileNotFoundError:
                print(f'{FALERT}Error: Invalid command \'{verb}\'')
                self.exit_code = 1


    def main(self):
        check = 1 if args(sys.argv, 1) else 0
        
        readline.set_completer(completer.completion)
        readline.parse_and_bind("tab: complete")
        
        # Initial module is set to blank
        # Set it to any other module if you want a default module at startup
        
        if self.MODULE in aboutList.moduleHelp.modules or self.MODULE == '':
            pass
        else:
            print(f'{FALERT}[-] No such module: \'{self.MODULE}\'{FNORMAL}')
            sys.exit(1)

        try:
            while(True):
                if self.exit_code == 0:
                    COLOR = colors.FSUCCESS
                elif self.exit_code == 3:
                    COLOR = colors.FURGENT
                else:
                    COLOR = colors.FALERT
            
                if check == 0:
                    if self.MODULE == '':
                        prompt_str: str = f'{FNORMAL}[probkit]: {COLOR}{self.exit_code}{FNORMAL}$> '
                    else:
                        prompt_str: str = f'{FNORMAL}probeKit: {FSTYLE}[{self.MODULE}]: {COLOR}{self.exit_code}{FNORMAL}$> '
                
                    value = input(prompt_str)
            
                else:
                    inputval = ' '.join(sys.argv[1].split('\ '))
                    check = 0

                if value != '':
                    self.parser(value)
                else:
                    print('No value [x]')
        except EOFError:
            pass
    
        except KeyboardInterrupt:
            self.exit_code = 130
            print('\n')
            self.main()
            
        except ExitException as e:
            print(e)
            utils.Exit(self.exit_code, histfile, platform.platform())
    
if __name__ == '__main__':
    input_parser().main()
#! /usr/bin/env python3

from colorama import Fore

FGREEN = Fore.GREEN
FRED = Fore.RED
FWHITE = Fore.WHITE

class moduleHelp():

	modules = ['probe', 'test', 'osprobe']

	def __init__(self, MODULE):
		self.module = MODULE

	def listmodules(self):
		if self.module != '':
			print('Currently activated module: '+FRED+f'[{self.module}]')

		print(FWHITE+'Available modules are:')
		for x in self.modules:
			print(FGREEN+"\t", x)

		print(FWHITE+'type: about [Module] for more information')

	def aboutModule(self, moduleName):
		if moduleName == 'probe':
			print(FRED+f'\nName:\t\t{moduleName}')
			print('Type:\t\tRecon')
			print('Description:\tThis module is meant to perform a basic port scan on the specidied host.\n')
			print(FGREEN+'Available options:\n')
			print('\tLHOST => IPv4 address or domain name of the target host')
			print('\t\t | Can be called LHOST or lhost\n')
			print('\tLPORT => ports to be scanned')
			print('\t\t | Can be called LPORT or lport')
			print('\t\t | Specify single port as `set lport [portnumber]`')
			print('\t\t | or set multiple ports by `set lport [startPort]/[endPort]`\n')
			print('\tTMOUT => timeout duration while awaiting connection')
			print('\t\t | Can be called TMOUT or tmout')
			print('\t\t | Defaults to 1 second duration\n')
			print('\tPROTO => Protocol to be used to scan')
			print('\t\t | Can be called PROTO or proto')
			print('\t\t | Available Protocols are:')
			print('\t\t                          | TCP => TCP/IP(tcp => tcp/ip)')
			print('\t\t                          | UDP(udp)\n')

		elif moduleName == 'osprobe':
			print(FRED+f'\nName:\t\t{moduleName}')
			print('Type:\t\tRecon')
			print('Description:\tThis module sends a basic ICMP packet to a host to determine its OS')
			print('            \t| This module does not confirm the OS since it is just using TTL within the ICMP response\n')
			print(FGREEN+'Available options:\n')
			print('\tLHOST => IPv4 address or domain name of the target host')
			print('\t\t | Can be called LHOST or lhost\n')
			print('\tTRYCT => Number of times ICMP packet must be sent')
			print('\t\t | Set to 1 packet by default')
			print('\t\t | Can be called TRYCT ot tryct\n')

		elif moduleName == 'test':
			print(FRED+'This module is strictly for debugging purposes while creating the toolkit')
			print(FRED+'Do not consider this as a usable module')


#
#     _      ___   _      ___   ___   ___   _     _    
#    | |\/| / / \ | |\ | / / \ | |_) / / \ | |   \ \_/ 
#    |_|  | \_\_/ |_| \| \_\_/ |_|   \_\_/ |_|__  |_|  
#
#                       Anish Gupta                     
#                   github.com/neur0n-7


#####################################################################################################################
#    DEBUG MODE    ##################################################################################################
#####################################################################################################################
DEBUG = False

#####################################################################################################################
#    MODULES    #####################################################################################################
#####################################################################################################################

import os
import random
import time
import sys
import pickle

from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.align import Align
from rich.text import Text

import questionary
from prompt_toolkit.styles import Style

from PIL import Image
from colorama import init, Fore

import tkinter
from tkinter import filedialog

init()

#####################################################################################################################
#    GAME DATA CONSTANTS    #########################################################################################
#####################################################################################################################

UTILITIES = ['ELECTRIC COMPANY','WATER WORKS']

STATIONS = ['READING RAILROAD','PENNSYLVANIA RAILROAD','B. & O. RAILROAD','SHORT LINE']

#buyable spaces (properties)
BUYABLE = ['MEDITERANEAN AVENUE', 
		   'BALTIC AVENUE', 
		   'READING RAILROAD',
		   'ORIENTAL AVENUE',
		   'VERMONT AVENUE',
		   'CONNECTICUT AVENUE',
		   'ST. CHARLES PLACE',
		   'ELECTRIC COMPANY',
		   'STATES AVENUE',
		   'VIRGINIA AVENUE',
		   'PENNSYLVANIA RAILROAD',
		   'ST. JAMES PLACE',
		   'TENESSEE AVENUE',
		   'NEW YORK AVENUE',
		   'KENTUCKY AVENUE',
		   'INDIANA AVENUE',
		   'ILLINOIS AVENUE',
		   'B. & O. RAILROAD',
		   'ATLANTIC AVENUE',
		   'VENTOR AVENUE',
		   'WATER WORKS',
		   'MARVIN GARDENS',
		   'PACIFIC AVENUE',
		   'NORTH CAROLINA AVENUE',
		   'PENNSYLVANIA AVENUE',
		   'SHORT LINE',
		   'PARK PLACE',
		   'BOARDWALK']

#buyable cards not including utilities and railroads
NORMAL_BUYABLE = ['MEDITERANEAN AVENUE', 
			   'BALTIC AVENUE',
			   'ORIENTAL AVENUE',
			   'VERMONT AVENUE',
			   'CONNECTICUT AVENUE',
			   'ST. CHARLES PLACE',
			   'STATES AVENUE',
			   'VIRGINIA AVENUE',
			   'ST. JAMES PLACE',
			   'TENESSEE AVENUE',
			   'NEW YORK AVENUE',
			   'KENTUCKY AVENUE',
			   'INDIANA AVENUE',
			   'ILLINOIS AVENUE',
			   'ATLANTIC AVENUE',
			   'VENTOR AVENUE',
			   'MARVIN GARDENS',
			   'PACIFIC AVENUE',
			   'NORTH CAROLINA AVENUE',
			   'PENNSYLVANIA AVENUE',
			   'PARK PLACE',
			   'BOARDWALK']

COLOR_GROUP_BUILDING_COSTS = {
	('MEDITERANEAN AVENUE', 'BALTIC AVENUE') : 50,
	('ORIENTAL AVENUE', 'VERMONT AVENUE', 'CONNECTICUT AVENUE') : 50,
	('ST. CHARLES PLACE', 'STATES AVENUE', 'VIRGINIA AVENUE') : 100,
	('ST. JAMES PLACE', 'TENESSEE AVENUE', 'NEW YORK AVENUE') : 100,
	('KENTUCKY AVENUE', 'INDIANA AVENUE', 'ILLINOIS AVENUE') : 150,
	('ATLANTIC AVENUE', 'VENTOR AVENUE', 'MARVIN GARDENS') : 150,
	('PACIFIC AVENUE', 'NORTH CAROLINA AVENUE', 'PENNSYLVANIA AVENUE') : 200,
	('PARK PLACE', 'BOARDWALK') : 200
}

GROUP_RGB_COLORS = {
	('MEDITERANEAN AVENUE', 'BALTIC AVENUE') : (91, 58, 147),
	('ORIENTAL AVENUE', 'VERMONT AVENUE', 'CONNECTICUT AVENUE') : (216, 232, 247),
	('ST. CHARLES PLACE', 'STATES AVENUE', 'VIRGINIA AVENUE') : (219, 47, 137),
	('ST. JAMES PLACE', 'TENESSEE AVENUE', 'NEW YORK AVENUE') : (244, 145, 0),
	('KENTUCKY AVENUE', 'INDIANA AVENUE', 'ILLINOIS AVENUE') : (239, 1, 33),
	('ATLANTIC AVENUE', 'VENTOR AVENUE', 'MARVIN GARDENS') : (254, 225, 1),
	('PACIFIC AVENUE', 'NORTH CAROLINA AVENUE', 'PENNSYLVANIA AVENUE') : (2, 186, 75),
	('PARK PLACE', 'BOARDWALK') : (1, 107, 199)
}


#rents for all properties except railroads/utilities
RENTS = [
	# [normal, 1h, 2h, 3h, 4h, hotel]
	[2,  10,  30,  90,   160,  250],
	[4,  20,  60,  180,  320,  450],
	[6,  30,  90,  270,  400,  550],
	[6,  30,  90,  270,  400,  550],
	[8,  40,  100, 300,  450,  600],
	[10, 50,  150, 450,  625,  750],
	[10, 50,  150, 450,  625,  750],
	[12, 60,  180, 500,  700,  900],
	[14, 70,  200, 550,  750,  950],
	[14, 70,  200, 550,  750,  950],
	[16, 80,  220, 600,  800,  1000],
	[18, 90,  250, 700,  875,  1050],
	[18, 90,  250, 700,  875,  1050],
	[20, 100, 300, 750,  925,  1120],
	[22, 110, 330, 800,  975,  1150],
	[22, 110, 330, 800,  975,  1150],
	[24, 120, 360, 850,  1025, 1200],
	[26, 130, 390, 900,  1100, 1275],
	[26, 130, 390, 900,  1100, 1275],
	[28, 150, 450, 1000, 1200, 1400],
	[35, 175, 500, 1100, 1300, 1500],
	[50, 200, 600, 1400, 1700, 2000]
	]

RAILROAD_RENT = [25,50,100,200]

PURCHASE_COSTS = [60, 60, 200, 100, 100, 120, 140, 150, 140, 160, 200, 180, 180, 200, 220, 220, 240, 200, 260, 260, 150, 280, 300, 300, 320, 200, 350, 400]

ALL_SPACES = ['GO',
			  'MEDITERANEAN AVENUE',
			  'COMMUNITY CHEST',
			  'BALTIC AVENUE',
			  'INCOME TAX',
			  'READING RAILROAD',
			  'ORIENTAL AVENUE',
			  'CHANCE',
			  'VERMONT AVENUE',
			  'CONNECTICUT AVENUE',
			  'JAIL',
			  'ST. CHARLES PLACE',
			  'ELECTRIC COMPANY',
			  'STATES AVENUE',
			  'VIRGINIA AVENUE',
			  'PENNSYLVANIA RAILROAD',
			  'ST. JAMES PLACE',
			  'COMMUNITY CHEST',
			  'TENESSEE AVENUE',
			  'NEW YORK AVENUE',
			  'FREE PARKING',
			  'KENTUCKY AVENUE',
			  'CHANCE',
			  'INDIANA AVENUE',
			  'ILLINOIS AVENUE',
			  'B. & O. RAILROAD',
			  'ATLANTIC AVENUE',
			  'VENTOR AVENUE',
			  'WATER WORKS',
			  'MARVIN GARDENS',
			  'GO TO JAIL',
			  'PACIFIC AVENUE',
			  'NORTH CAROLINA AVENUE',
			  'COMMUNITY CHEST',
			  'PENNSYLVANIA AVENUE',
			  'SHORT LINE',
			  'CHANCE',
			  'PARK PLACE',
			  'LUXURY TAX',
			  'BOARDWALK']

# each cards lambda is passed the current player

CHANCE_CARDS = {
	"ADVANCE TO ST. CHARLES PLACE. IF YOU PASS GO, COLLECT $200": lambda player: player.move_to("ST. CHARLES PLACE"),

	"GO BACK THREE SPACES": lambda player: player.move_by(-3, collect_go = False),

	"TAKE A WALK ON THE BOARDWALK - ADVANCE TOKEN TO BOARDWALK": lambda player: player.move_to("BOARDWALK"),

	"TAKE A RIDE ON THE READING - IF YOU PASS GO, COLLECT $200": lambda player: player.move_to("READING RAILROAD"),

	"ADVANCE TO GO (COLLECT $200)": lambda player: player.move_to("GO"),

	"ADVANCE TO ILLINOIS AVE.": lambda player: player.move_to("ILLINOIS AVENUE"),

	"PAY POOR TAX OF $15": lambda player: player.pay_fees(15),

	"YOU HAVE BEEN ELECTED CHAIRMAN OF THE BOARD - PAY EACH PLAYER $50": lambda player: [
		(player.pay_fees_to_player(50, other) if other != player else None)
		for other in all_players
	],

	"YOUR BUILDING AND LOAN MATURES - COLLECT $150": lambda player: player.collect(150),

	"BANK PAYS YOU DIVIDEND OF $50": lambda player: player.collect(50),

	"MAKE GENERAL REPAIRS ON ALL YOUR PROPERTY - FOR EACH HOUSE PAY $25, FOR EACH HOTEL $100":
	lambda player: player.pay_fees(25*sum([num_houses for num_houses in player.buildings.values() if num_houses!=5]) +
								   100*len([num_hotels for num_hotels in player.buildings.values() if num_hotels==5])),

	"THIS CARD MAY BE KEPT UNTIL NEEDED, OR SOLD - GET OUT OF JAIL FREE": lambda player: setattr(player, "jail_cards", player.jail_cards+1),
	
	"GO DIRECTLY TO JAIL - DO NOT PASS GO, DO NOT COLLECT $200": lambda player: [
		setattr(player, "in_jail", True), setattr(player, "turns_in_jail", 0), setattr(player, "current_square", "JAIL")
	]

}

COMMUNITY_CHEST_CARDS = {
	"INCOME TAX REFUND - COLLECT $20": lambda player: player.collect(20),

	"LIFE INSURANCE MATURES - COLLECT $100": lambda player: player.collect(100),

	"YOU INHERIT $100": lambda player: player.collect(100),

	"XMAS FUND MATURES - COLLECT $100": lambda player: player.collect(100),

	"FROM SALE OF STOCK YOU GET $45" : lambda player: player.collect(45),

	"BANK ERROR IN YOUR FAVOR - COLLECT $200" : lambda player: player.collect(200),

	"YOU HAVE WON SECOND PRIZE IN A BEAUTY CONTEST - COLLECT $10": lambda player: player.collect(10),

	"RECEIVE FOR SERVICES $25": lambda player: player.collect(25),

	"GRAND OPERA OPENING - COLLECT $50 FROM EVERY PLAYER FOR OPENING NIGHT SEATS": lambda player: [
		(other.pay_fees_to_player(50, player) if other != player else None) for other in all_players
	],

	"DOCTOR'S FEE - PAY $50": lambda player: player.pay_fees(50),

	"PAY SCHOOL TAX OF $150": lambda player: player.pay_fees(150),

	"PAY HOSPITAL $100": lambda player: player.pay_fees(100),

	"YOU ARE ASSESSED FOR STREET REPAIRS - $40 PER HOUSE, $115 PER HOTEL":
	lambda player: player.pay_fees(40*sum([num_houses for num_houses in player.buildings.values() if num_houses!=5]) +
								   115*len([num_hotels for num_hotels in player.buildings.values() if num_hotels==5])),

	"GET OUT OF JAIL FREE - THIS CARD MAY BE KEPT UNTIL NEEDED, OR SOLD": lambda player: setattr(player, "jail_cards", player.jail_cards+1),

	"GO TO JAIL - GO DIRECTLY TO JAIL, DO NOT PASS GO, DO NOT COLLECT $200": lambda player: [
		setattr(player, "in_jail", True), setattr(player, "turns_in_jail", 0), setattr(player, "current_square", "JAIL")
	]

}


#####################################################################################################################
#    OTHER VARIABLES/CONSTANTS    ###################################################################################
#####################################################################################################################

class CenteredConsole(Console):
	def print(self, *objects: RenderableType, **kwargs) -> None:
		centered = [Align.center(obj) for obj in objects]
		super().print(*centered, **kwargs)

c = Console(width=os.get_terminal_size()[0])
cc = CenteredConsole(width=os.get_terminal_size()[0])

DICE = {
	1: [
		"╭────────╮",
		"│        │",
		"│   •    │",
		"│        │",
		"╰────────╯"
	],
	2: [
		"╭────────╮",
		"│ •      │",
		"│        │",
		"│      • │",
		"╰────────╯"
	],
	3: [
		"╭────────╮",
		"│ •      │",
		"│   •    │",
		"│      • │",
		"╰────────╯"
	],
	4: [
		"╭────────╮",
		"│ •   •  │",
		"│        │",
		"│ •   •  │",
		"╰────────╯"
	],
	5: [
		"╭────────╮",
		"│ •   •  │",
		"│   •    │",
		"│ •   •  │",
		"╰────────╯"
	],
	6: [
		"╭────────╮",
		"│ •   •  │",
		"│ •   •  │",
		"│ •   •  │",
		"╰────────╯"
	]
}

ASCII_CHARS = "@%#*+=-:. "
COLOR_LEVELS = [
	Fore.WHITE, Fore.LIGHTWHITE_EX, Fore.LIGHTCYAN_EX,
	Fore.LIGHTBLUE_EX, Fore.LIGHTGREEN_EX,
	Fore.YELLOW, Fore.LIGHTRED_EX, Fore.RED, Fore.BLACK
]

TITLE_ASCII = """
 ___ ___   ___   ____    ___   ____   ___   _      __ __ 
|   |   | /   \\ |    \\  /   \\ |    \\ /   \\ | |    |  |  |
| _   _ ||     ||  _  ||     ||  o  )     || |    |  |  |
|  \\_/  ||  O  ||  |  ||  O  ||   _/|  O  || |___ |  ~  |
|   |   ||     ||  |  ||     ||  |  |     ||     ||___, |
|   |   ||     ||  |  ||     ||  |  |     ||     ||     |
|___|___| \\___/ |__|__| \\___/ |__|   \\___/ |_____||____/ 
"""

TRAIN_ASCII = """
____
|DD|____T_
|_ |_____|<
 @-@-@-oo\\
"""

BULB_ASCII = f"""_____
/       \\
|         |
\\  /---\\  /
{chr(10189)}     {chr(10187)}
|===|
|___|
"""

TAP_ASCII = """
	=()=
,/'\\_||_
( (___  `.
`\\./  `=='
	  ||||
"""

#####################################################################################################################
#    PLAYER CLASS    ################################################################################################
#####################################################################################################################
class Player:
	"""
	Represents a single player in Monopoly

	Attributes:
		name (str): The player's name
		cash (int): The player's current cash balance
		norm_properties_owned (list): List of normal properties owned by the player
		in_jail (bool): Whether the player is currently in jail or not
		current_square (str): The name of the square the player is currently on
		buildings (dict): Dictionary mapping property names to number of houses: a value of five = hotel
		networth (int): The player's total net worth (cash + property values)
		mortgaged_properties (list): List of mortgaged properties
		railroads_owned (list): List of railroads owned by the player
		utilities_owned (list): List of utilities owned by the player
		jail_cards (int): Number of 'Get Out of Jail Free' cards held
		bankrupt (bool): Whether the player is bankrupt
		doubles (int): Number of consecutive doubles rolled
		turns_in_jail (int): Number of turns spent in jail

	Methods:
		all_properties_owned(): Returns a list of all properties owned by the player
		pay(): Deducts amount from cash and net worth
		pay_player(): Pays another player a specified amount changing net worth
		collect(): Adds amount to cash and net worth
		pay_without_networth(): Deducts amount from cash only without changing net worth
		collect_without_networth(): Adds amount to cash without changing net worth
		get_property(): Adds a property to the player's ownership and deducts cost
		mortgage(): Mortgages a property and collects half its value
		unmortgage(): Unmortgages a property and pays back with interest
		sell_property(): Sells a property and collects its value
		build_house(): Builds a house/hotel on a property
		pay_fees(): Pays fees, handling bankruptcy and asset liquidation if needed
		pay_fees_to_player(): Pays fees to another player, handling bankruptcy and asset liquidation if needed
		move_to(): Moves the player to a specific location, collecting $200 if passing GO
		move_by(): Moves the player by a number of spaces
		return_info(): Returns a rich Panel with player info
		get_house_count(): Returns the number of houses/hotels on a property
		can_mortgage_property(): Checks if a property can be mortgaged
		liquidate_assets(): Guide player through raising funds by liquidating assets
	"""
	def __init__(self, name):
		self.name=name
		self.cash = 1500
		self.norm_properties_owned = []
		self.in_jail = False
		self.current_square = 'GO'
		self.buildings = {}
		self.networth = 1500
		self.mortgaged_properties = []
		self.railroads_owned = []
		self.utilities_owned = []
		self.jail_cards = 0
		self.bankrupt = False
		self.doubles = 0
		self.turns_in_jail = 0

	def all_properties_owned(self):
		return self.norm_properties_owned + self.railroads_owned + self.utilities_owned

	def pay(self,amount):
		self.cash-=amount
		self.networth-=amount

	def pay_player(self,playerobj, amount):
		self.cash-=amount
		playerobj.cash+=amount
		self.networth-=amount
		playerobj.networth+=amount
	
	def collect(self,amount):
		self.cash+=amount
		self.networth+=amount

	def pay_without_networth(self,amount):
		self.cash-=amount

	def collect_without_networth(self,amount):
		self.cash+=amount
	
	def get_property(self,property):
		self.pay_without_networth(get_property_cost(property))
		if property in STATIONS:
			self.railroads_owned.append(property)
		elif property in UTILITIES:
			self.utilities_owned.append(property)
		else:
			self.norm_properties_owned.append(property)

	def mortgage(self,property):
		self.mortgaged_properties.append(property)
		self.collect_without_networth(get_property_cost(property)//2)
		
	def unmortgage(self,property):
		self.mortgaged_properties.remove(property)
		self.pay_without_networth(1.1*(get_property_cost(property)//2))
	
	def sell_property(self,property):
		self.collect_without_networth(get_property_cost(property))
		if property in STATIONS:
			self.railroads_owned.remove(property)
		elif property in UTILITIES:
			self.utilities_owned.remove(property)
		else:
			self.norm_properties_owned.remove(property)

	def build_house(self,property):
		if property in self.buildings:
			self.buildings[property]+=1
			if self.buildings[property]==5:
				self.buildings[property]='HOTEL'
		else:
			self.buildings[property]=1

		self.pay_fees_without_networth(get_building_cost(property))


	def pay_fees_without_networth(self, fees):
		global non_bankrupt
		if self.networth < fees:
			c.print(f"\n[bold][red][blink]{self.name}, YOU HAVE GONE BANKRUPT![/blink][/red][/bold]\n")
			c.print(f"Your net worth was [bold]${self.networth}[/bold] and you owed [bold]${fees}[/bold].")
			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()
			self.bankrupt = True
			non_bankrupt.remove(self)
			
		elif self.cash < fees:
			c.print(f"[red][bold]{self.name}[/bold], you must liquify some of your assets.[/red]")
			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()
			self.liquidate_assets(fees-self.cash)
			self.pay_without_networth(fees)
		else:
			self.pay_without_networth(fees)
			c.print(f"[red][bold]{self.name}[/bold], you paid the fee. You now have [bold]${self.cash}[/bold].[/red]")

	def pay_fees(self, fees):
		global non_bankrupt
		if self.networth < fees:
			c.print(f"\n[bold][red][blink]{self.name}, YOU HAVE GONE BANKRUPT![/blink][/red][/bold]\n")
			c.print(f"Your net worth was [bold]${self.networth}[/bold] and you owed [bold]${fees}[/bold].")
			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()
			self.bankrupt = True
			non_bankrupt.remove(self)
			
		elif self.cash < fees:
			c.print(f"[red][bold]{self.name}[/bold], you must liquify some of your assets.[/red]")
			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()
			self.liquidate_assets(fees-self.cash)
			self.pay(fees)
		else:
			self.pay(fees)
			c.print(f"[red][bold]{self.name}[/bold], you paid the fee. You now have [bold]${self.cash}[/bold].[/red]")

	def pay_fees_to_player(self, fees, player):
		global non_bankrupt
		if self.networth < fees:
			c.print(f"\n[bold][red][blink]{self.name} YOU HAVE GONE BANKRUPT![/blink][/red][/bold]\n")
			c.print(f"Your net worth was [bold]${self.networth}[/bold] and you owed [bold]${fees}[/bold].")
			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()
			self.bankrupt = True
			non_bankrupt.remove(self)
			
		elif self.cash < fees:
			c.print(f"[red][bold]{self.name}[/bold], you must liquify some of your assets.[/red]")
			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()
			self.liquidate_assets(fees-self.cash)
			self.pay_player(player, fees)
		else:
			self.pay_player(player, fees)
			c.print(f"[red][bold]{self.name}[/bold], you paid the fee. You now have [bold]${self.cash}[/bold].[/red]")



	def move_to(self, location, collect_go=True):
		global non_bankrupt

		if ALL_SPACES.index(self.current_square) >= ALL_SPACES.index(location) and collect_go:
			self.collect(200)

		self.current_square = location
		
	def move_by(self, byamount, collect_go = True):
		self.move_to(ALL_SPACES[(ALL_SPACES.index(self.current_square) + byamount) % len(ALL_SPACES)], collect_go)

	def return_info(self, width, dimmed=False, color=0):
		table = Table.grid(padding=(0, 2))

		if self.bankrupt:
			table_style = "italic dim"
		elif dimmed:
			table_style = "dim"
		else:
			table_style = f"{["green", "red", "blue", "yellow"][color]} bold"

		table.add_column(justify="right", style=table_style)
		table.add_column()

		table.add_row("Money:", f"${self.cash}")
		table.add_row("Net Worth:", f"${self.networth}")

		def list_or_dash(items):
			return ", ".join(items) if items else "—"

		table.add_row("Currently On:", self.current_square)
		table.add_row("Properties:", list_or_dash(self.norm_properties_owned))
		table.add_row("Railroads:", list_or_dash(self.railroads_owned))
		table.add_row("Utilities:", list_or_dash(self.utilities_owned))
		table.add_row("Mortgaged:", list_or_dash(self.mortgaged_properties))
		table.add_row("Get Out of Jail Cards:", str(self.jail_cards))


		if self.in_jail:
			title_name = self.name.upper() + f" - [bold red]IN JAIL[/bold red] {chr(128680)}"
		elif self.bankrupt:
			title_name = self.name.upper() + f" - [bold red]BANKRUPT![/bold red] {chr(127974)} {chr(10060)}"
		else:
			title_name = self.name.upper()


		panel = Panel(
			table,
			title=f"[{table_style}]{title_name}[/{table_style}]",
			title_align="center",
			border_style=table_style,
			expand=True,
			width=width
		)

		return panel				

	def get_house_count(self, property):
		if property in self.norm_properties_owned:
			if property in self.buildings:
				return self.buildings[property]
			return 0
		else:
			return None

	def can_mortgage_property(self, property_name):
		for group, cost in COLOR_GROUP_BUILDING_COSTS.items():
			if property_name in group:
				for prop in group:
					if self.buildings.get(prop, 0) > 0:
						return False
				return True 
		return True


	def liquidate_assets(self, amount_needed):
		c.print(f"[red]You must liquidate assets to get at least [bold]${amount_needed}[/bold] in cash. You currently have [/bold]${self.cash}[/bold] in cash.")
		c.print("[red]You can do this by mortaging properties, selling buildings to the bank, or selling properties to another player.[/red]")

		while self.cash < amount_needed:
			c.print("Select an option of raising funds.")
			c.print(f"You have [bold]${amount_needed-self.cash}[/bold] worth of assets to liquify.")
			liq_choice = interactive_choice("Choose how to raise funds:", ["Mortgage Property", "Sell Buildings", "Sell Properties" ])
			
			if liq_choice == "Mortgage Property":
				unmortgaged = [p for p in self.all_properties_owned() if p not in self.mortgaged_properties]
				if not unmortgaged:
					c.print("[red]You don't have any unmortgaged properties available.[/red]")
					continue
				to_mortgage = interactive_choice("Select a property to mortgage:", unmortgaged)

				if self.can_mortgage_property(to_mortgage):
					self.mortgaged_properties.append(unmortgaged)
					self.mortgage(to_mortgage)
					c.print(f"[green]You mortgaged {to_mortgage} for ${0.5 * get_property_cost(to_mortgage)}.[/green]")
				else:
					c.print("[red]You cannot mortgage this property.[/red]")
					c.print("[dim italic]\"Unimproved properties can be mortgaged through the Bank at any time." \
					"However, buildings must first be sold back to the Bank before any property of that color-group can be mortgaged.\"[/dim italic]")

			elif liq_choice == "Sell Buildings":
				if not self.norm_properties_owned:
					c.print("[red]You don't own any properties to sell houses/hotels on.[/red]")
				elif not self.buildings:
					c.print("[red]You don't own any houses or hotels.[/red]")
				else:
					available_locs = ["Cancel"]
					for group in list(COLOR_GROUP_BUILDING_COSTS.keys()):
						if all([x in self.norm_properties_owned and x not in self.mortgaged_properties for x in group]):
							building_counts = [self.buildings.get(x, 0) for x in group]
							max_build = max(building_counts)
							for prop, count in zip(group, building_counts):
								if count == max_build:
									available_locs.append(prop)
						
					c.print("Which house would you like to sell a house/hotel on?")
					loc = interactive_choice("Select a property:", available_locs)
					if loc == "Cancel":
						c.print("[red]Canceling.[/red]")
					else:
						building_cost = get_building_cost(loc)
						c.print(f"At [bold]{loc}[/bold], you already have [bold]{f"{self.buildings[loc]} houses" if self.buildings[loc]<5 else "a hotel"}[/bold].")
						c.print(f"You'll receive [bold]{building_cost//2}[/bold] for selling a house or hotel here.")
						c.print("[i](Half the original building price)[/i]")
						c.print("Would you like to sell a building here?")
						confirm_build = interactive_choice("Select an option:", ["Yes", "No"])
						if confirm_build == "Yes":
							self.buildings[loc] -= 1
							self.collect_without_networth(building_cost//2)
							c.print(f"[green]You sold a building at [bold]{loc}[/bold].[/green]")
							c.print(f"There are now [bold]{self.buildings[loc]}[/bold] houses at [bold]{loc}[/bold]")
						else:
							c.print("[red]Canceling.[/red]")
							
			elif liq_choice == "Sell Properties":
				if not self.all_properties_owned():
					c.print("[red]You don't own any properties to sell.[/red]")
					continue
				
				c.print("Select a property you are offering to sell.")
				can_sell = [x for x in self.all_properties_owned() if x not in self.buildings]
				to_sell = interactive_choice("Select an option:", can_sell)
				c.print("Choose the player to offer this property to.")
				buyer = interactive_choice("Select an option:", [p.name for p in all_players])
				c.print("Select an amount to sell this property for.")
				valid_offer = False
				while not valid_offer:
					try:
						offer_price = int(input("> "))
						valid_offer = True
					except:
						c.print("[red]Please input an integer number.[/red]")

				buyer_obj = next(p for p in all_players if p.name == buyer)

				if buyer_obj.cash >= offer_price:
					accept_offer = interactive_choice(f"{buyer}, do you accept the offer of [bold]${offer_price}[/bold] for [bold]{to_sell}[/bold]?", ["Yes", "No"])
					if accept_offer == "Yes":
						self.sell_property(to_sell)
						buyer_obj.get_property(to_sell)
						c.print(f"[green][bold]{buyer}[/bold] accepted your offer.")
						c.print(f"[green][bold]{buyer}[/bold] bought [bold]{to_sell}[/bold] from [bold]{self.name}[/bold] for [bold]${offer_price}[/bold].[/green]")
					else:
						c.print(f"[red][bold]{buyer}[/bold] turned down your offer.[/red]")
					
				else:
					c.print(f"[red][bold]{buyer}[/bold] has insufficient cash to buy your property.[/red]")


			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()

		c.print("[green]You have raised enough money![/green]")
		c.print("Press [cyan]ENTER[/cyan] to continue.")
		input()


#####################################################################################################################
#    FUNCTIONS    ###################################################################################################
#####################################################################################################################

def clear():
	os.system("cls" if os.name == "nt" else "clear")

def get_property_cost(property):
	property_index = BUYABLE.index(property)
	return PURCHASE_COSTS[property_index]

def get_building_cost(property):
		for group, cost in COLOR_GROUP_BUILDING_COSTS.items():
			if property in group:
				return cost

def get_rent(property):
	if property in NORMAL_BUYABLE:
		owner = get_owner(property)
		num_houses = owner.get_house_count(property)
		num_houses = 5 if num_houses == 'HOTEL' else num_houses
		index = NORMAL_BUYABLE.index(property)
		rent = RENTS[index][num_houses]

		if num_houses == 0:
			for group in list(COLOR_GROUP_BUILDING_COSTS.keys()):
				if property in group:
					color_group = group
		
			if all([get_owner(x) for x in color_group]):
				rent *= 2

		return rent
	elif property in STATIONS:
		owner = get_owner(property)
		num_railroads = len(owner.railroads_owned)
		rent = RAILROAD_RENT[num_railroads-1]
		return rent
	elif property in UTILITIES:
		owner = get_owner(property)
		num_utilities = len(owner.utilities_owned)
		if num_utilities == 1:
			roll = roll_dice()[0]
			rent = 4*roll
		elif num_utilities == 2:
			roll = roll_dice()[0]
			rent = 10*roll
		return rent

def get_owner(property):
	for p in all_players:
		if property in p.norm_properties_owned:
			return p
		elif property in p.railroads_owned:
			return p
		elif property in p.utilities_owned:
			return p
	return None

def interactive_choice(prompt, options):

	custom_style = Style.from_dict({
		'qmark': 'fg:#00ffcc bold',
		'question': 'bold fg:#00ffcc',
		'answer': 'bold fg:#00ffcc',
		'pointer': 'fg:#ff5f5f bold',
		'highlighted': 'fg:#ffffff bg:#444444',
		'selected': 'fg:#00ff00',
	})

	selected = questionary.select(
		message=prompt,
		choices=options,
		style=custom_style
	).ask()

	if selected == "":
		raise KeyboardInterrupt("User cancelled Questionary prompt")

	return selected.strip()

def print_all_players(players, current_turn_index):
	top_row = []
	bottom_row = []

	for i, player in enumerate(players):
		panel = player.return_info(width = os.get_terminal_size().columns//2-2, dimmed=(i != current_turn_index), color=i)
		if i < 2:
			top_row.append(panel)
		else:
			bottom_row.append(panel)

	group = Group(
		Columns(top_row),
		Columns(bottom_row)
	)

	c.print(group)


def save_game():
	valid_folder = False

	while not valid_folder:

		c.print("Exporting game state...")

		c.print("Select a folder to save the game state to.")

		root = tkinter.Tk()
		root.withdraw()

		root.attributes("-topmost", True)  # Bring the file dialog to the front

		path = filedialog.asksaveasfilename(title="Save game state",
											defaultextension=".pkl",
											filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
											initialfile=f"monopoly_save.pkl"
		)

		valid_folder = bool(path)

		if not valid_folder:
			c.print("[red]Please select a folder.[/red]")
			invalid_retry_save = interactive_choice("Select an option:", ["OK", "Cancel"])

			if invalid_retry_save == "Cancel":
				c.print("[red]Game state not saved.[/red]")
				break
	
	if valid_folder:

		turn_to_save = turn - 1
		if turn_to_save == -1:
			turn_to_save = len(non_bankrupt) - 1

		with open(path, "wb") as f:
			pickle.dump((all_players, turn_to_save), f)
		c.print(f"[green]Game state exported successfully to [bold]{os.path.basename(path)}[/bold]![/green]")


#####################################################################################################################
#    START FUNCTIONS    #############################################################################################
#####################################################################################################################

def render_image_ascii_color(path):
	try:
		term_width = os.get_terminal_size().columns
	except OSError:
		term_width = 80

	width = int(term_width / 1.1)
	ascii_chars = " .:-=+*#%@"

	def pixel_to_rich_char(r, g, b):
		brightness = int((0.299*r + 0.587*g + 0.114*b))
		index = brightness * (len(ascii_chars) - 1) // 255
		char = ascii_chars[index]
		return Text(char, style=f"rgb({r},{g},{b})")

	def image_to_rich_text(image):
		aspect_ratio = image.height / image.width
		height = int(aspect_ratio * width * 0.5)
		image = image.resize((width, height)).convert('RGB')

		text = Text()
		for y in range(height):
			for x in range(width):
				r, g, b = image.getpixel((x, y))
				text.append(pixel_to_rich_char(r, g, b))
			text.append("\n")
		return text

	img = Image.open(path).convert('RGB')
	ascii_img = image_to_rich_text(img)
	aligned_img = Align(ascii_img, align="center")

	c.print(aligned_img)
	return ascii_img

#####################################################################################################################
#    GAMEPLAY    ####################################################################################################
#####################################################################################################################

def roll_dice():

	delay = 0.001
	for _ in range(1 if DEBUG else 15):
		a = random.randint(1, 6)
		b = random.randint(1, 6)
		clear()
		c.print("[bold]Rolling...[/bold]")
		frame = "\n".join([DICE[a][i] + "  " + DICE[b][i] for i in range(5)])
		c.print(frame)
		time.sleep(delay)
		delay += 0.015

	clear()
	c.print("[bold]You rolled:[/bold]")
	result_frame = "\n".join([DICE[a][i] + "  " + DICE[b][i] for i in range(5)])
	c.print(result_frame)
	c.print(f"[dim]({a+b})[/dim]")
	time.sleep(.75)

	return a + b, a==b

def get_deed(deed_title):

	if deed_title in NORMAL_BUYABLE:
		for group, color in GROUP_RGB_COLORS.items():
			if deed_title in group:
				bg_color = '#{:02x}{:02x}{:02x}'.format(*color)
				fg_color = "white" if deed_title in ('MEDITERANEAN AVENUE', 'BALTIC AVENUE', 'PARK PLACE', 'BOARDWALK') else "#000000"
				break
	
		name_padding = " " * ((38-len(deed_title))//2)
		title_bar = Align.left(Text(f"              Title Deed              \n{name_padding}{deed_title}{name_padding}", justify="left", style=f"bold {fg_color} on "+bg_color))
		
		base_rent = Align.center(Text(f"\nRENT ${RENTS[NORMAL_BUYABLE.index(deed_title)][0]}.\n"))

		house_rents = Table.grid(padding=(0, 2), expand=True)
		house_rents.add_column(justify="left", no_wrap=True)
		house_rents.add_column(justify="right", no_wrap=True)
		house_rents.add_row("With 1 House", f"${RENTS[NORMAL_BUYABLE.index(deed_title)][1]}.")
		house_rents.add_row("With 2 Houses", f"${RENTS[NORMAL_BUYABLE.index(deed_title)][2]}.")
		house_rents.add_row("With 3 Houses", f"${RENTS[NORMAL_BUYABLE.index(deed_title)][3]}.")
		house_rents.add_row("With 4 Houses", f"${RENTS[NORMAL_BUYABLE.index(deed_title)][4]}.")

		hotel_rent = Align.center(Text(f"\nWith HOTEL ${RENTS[NORMAL_BUYABLE.index(deed_title)][4]}."))

		mortgage_building_info = Align.center(Text(
			f"Mortgage Value ${int(get_property_cost(deed_title)/2)}.\n"
			f"Houses cost ${get_building_cost(deed_title)}. each\n"
			f"Hotels, ${get_building_cost(deed_title)}. plus 4 houses",
			justify="center"
		))

		footer = Align.center(Text(
			"\nIf a player owns ALL the lots of any Color-Group, "
			"the rent is Doubled on Unimproved Lots in that group.",
			style="italic",
			justify="center"
		))

		card = Group(
			title_bar,
			base_rent,
			house_rents,
			hotel_rent,
			mortgage_building_info,
			footer
		)

		return Panel(card, border_style="white", width=40)

	elif deed_title in UTILITIES:
		if deed_title == "ELECTRIC COMPANY":
			icon = Align.center(Text(BULB_ASCII, justify="center"))
		else:
			icon = Align.center(Text(TRAIN_ASCII, justify="center"))
		
		lines = "━" * len(deed_title)
		title_bar = Align.center(Text(f"{lines}\n{deed_title}\n{lines}", justify="center", style="bold white"))
		text = "If one \"Utility\" is owned rent is 4 times amount shown on dice. If both \"Utilies\" are owned rent is 10 times amount shown on dice."

		footer = Align.center(Text("Mortgage Value     $75\n"))
		card = Group(
			icon,
			title_bar,
			text,
			footer
		)

		return Panel(card, border_style="white", width=40)
	
	else:
		
		icon = Align.center(Text(TRAIN_ASCII, justify="center"))

		lines = "━" * len(deed_title)
		title_bar = Align.center(Text(f"{lines}\n{deed_title}\n{lines}\n", justify="center", style="bold white"))

		rent_table = Table.grid(padding=(0, 2), expand=True)
		rent_table.add_column(justify="left")
		rent_table.add_column(justify="right")

		rent_table.add_row("Rent", "$25.")
		rent_table.add_row("", "")
		rent_table.add_row("If 2 R.R.'s are owned", "$50.")
		rent_table.add_row("If 3 R.R.'s are owned ", "$100.")
		rent_table.add_row("If 4 R.R.'s are owned", "$200.")
		rent_table.add_row("", "")
		rent_table.add_row("Mortgage Value", "$100")
		rent_table.add_row("", "")

		card = Group(
			icon,
			title_bar,
			rent_table
		)

		return Panel(card, border_style="white", width=40)


def do_square_action(current_player: Player):
	if current_player.current_square in BUYABLE:
		if get_owner(current_player.current_square) == None:
			c.print(f"Would you like to purchase [bold]{current_player.current_square}[/bold]?") 


			c.print(f"It will cost [bold]${get_property_cost(current_player.current_square)}[/bold]. You have [bold]${current_player.cash}[/bold] in cash and your net worth is [bold]${current_player.networth}[/bold].")
			purchase_square = None

			deed_card_viewed = False

			while purchase_square not in ("Yes", "No"):
				purchase_square = interactive_choice("Select an option:", ["Yes", "No", "View deed information"] if not deed_card_viewed else ["Yes", "No"])
				if purchase_square == "Yes":
					if current_player.networth >= get_property_cost(current_player.current_square):
						current_player.get_property(current_player.current_square)
						c.print(f"[green]You purchased [bold]{current_player.current_square}[/bold].[/green]")
					else:
						c.print(f"[red]You don't have enough money to purchase this property (${current_player.networth} < ${get_property_cost(current_player.current_square)}).[/red]")

				elif purchase_square == "View deed information":
					
					deed_card_viewed = True
					c.print(f"[underline]Title deed card for [bold]{current_player.current_square}:[/underline]\n")
					deed = get_deed(current_player.current_square)
					c.print(deed)

		elif get_owner(current_player.current_square) != current_player:
			if current_player.current_square in get_owner(current_player.current_square).mortgaged_properties:
				c.print(f"This property is owned by [bold]{get_owner(current_player.current_square).name}[/bold] but it is mortgaged.")
			
			else:
				if current_player.current_square in UTILITIES:
					c.print(f"[red]This square is currently owned by [bold]{get_owner(current_player.current_square).name}[/bold].")
					if get_owner(current_player.current_square).utilities_owned == 1:
						c.print("The owner of this utility owns 1 utility, so the rent is [bold]four times[/bold] that rolled.")
					else:
						c.print("The owner of this utility owns 2 utilities, so the rent is [bold]ten times[/bold] that rolled.")

					c.print("Press [cyan]ENTER[/cyan] to roll the dice.")
					input()

					rent = get_rent(current_player.current_square)
					c.print(f"The rent is [bold]${rent}[/bold].")

				else:
					c.print(f"[red]This square is currently owned by [bold]{get_owner(current_player.current_square).name}[/bold]. The rent is [bold]${get_rent(current_player.current_square)}[/bold].")
					rent = get_rent(current_player.current_square)
				

				current_player.pay_fees_to_player(get_rent(current_player.current_square), get_owner(current_player.current_square))

		else:
			c.print("[green]You currently own this property.[/green]")

	elif current_player.current_square == "GO TO JAIL":
		c.print("[red]You were sent to jail![/red]")
		current_player.in_jail = True
		current_player.current_square = "JAIL"
		current_player.turns_in_jail = 0
	
	elif current_player.current_square == "LUXURY TAX":
		c.print("[red]You have to pay a tax of [bold]$75[/bold].[/red]")

		if current_player.networth < 75:
			c.print("\n[bold][red][blink]YOU HAVE GONE BANKRUPT![/blink][/red][/bold]\n")
			c.print(f"Your net worth was [bold]${current_player.networth}[/bold] and you owed [bold]$75[/bold].")

			current_player.bankrupt = True
			non_bankrupt.remove(current_player)

		elif current_player.cash < 75:
			c.print("[red]You must liquify some of your assets.[/red]")
			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()
			current_player.liquidate_assets(75-current_player.cash)
			current_player.pay(75)
	
		else:
			current_player.pay(75)
			c.print(f"[red]You paid the tax. You now have [bold]${current_player.cash}[/bold].")

	elif current_player.current_square == "INCOME TAX":
		c.print("[red]You have to pay a tax of either [bold]10%[/bold] of your net worth or [bold]$200[/bold].[/red]")
		c.print(f"Your net worth is [bold]${current_player.networth}[/bold].")
		c.print("Which tax would you like to pay?")
		tax_choice = interactive_choice("Select an option:", [f"10% of net worth (${round(current_player.networth * 0.1)})", "$200"])

		if tax_choice == f"10% of net worth ({round(current_player.networth * 0.1)})":
			tax_amount = round(current_player.networth * 0.1)
			c.print(f"You chose to pay [bold]10%[/bold] of your net worth, which is [bold]${tax_amount}[/bold].")
		else:
			tax_amount = 200
			c.print(f"You chose to pay [bold]$200[/bold].")
		
		if current_player.networth < tax_amount:
			c.print("\n[bold][red][blink]YOU HAVE GONE BANKRUPT![/blink][/red][/bold]\n")
			c.print(f"Your net worth was [bold]${current_player.networth}[/bold] and you owed [bold]${tax_amount}[/bold].")
			current_player.bankrupt = True
			non_bankrupt.remove(current_player)

		elif current_player.cash < tax_amount:
			c.print("[red]You must liquify some of your assets.[/red]")
			c.print("Press [cyan]ENTER[/cyan] to continue.")
			input()
			current_player.liquidate_assets(tax_amount-current_player.cash)
			current_player.pay(tax_amount)

		else:
			current_player.pay(tax_amount)
			c.print(f"[red]You paid the tax. You now have [bold]${current_player.cash}[/bold].[/red]")
		
	elif current_player.current_square == "CHANCE":
		c.print("Press [cyan]ENTER[/cyan] to draw a card.")
		input()
		card = random.choice(list(CHANCE_CARDS.keys()))
		c.print("The card you drew was:")
		c.print(f"[bold]{card}[/bold]")
		action = CHANCE_CARDS[card]
		previous_square = current_player.current_square
		action(current_player)
		if previous_square != current_player.current_square:
			do_square_action(current_player)
		
	elif current_player.current_square == "COMMUNITY CHEST":
		c.print("Press [cyan]ENTER[/cyan] to draw a card.")
		input()
		card = random.choice(list(COMMUNITY_CHEST_CARDS.keys()))
		c.print("The card you drew was:")
		c.print(f"[bold]{card}[/bold]")
		action = COMMUNITY_CHEST_CARDS[card]
		previous_square = current_player.current_square
		action(current_player)
		if previous_square != current_player.current_square:
			do_square_action(current_player)

	c.print("Press [cyan]ENTER[/cyan] to continue.")
	input()


#####################################################################################################################
#    GAME LOOP    ###################################################################################################
#####################################################################################################################


def game_loop():
	global turn, p1, p2, p3, p4, all_players, non_bankrupt
	non_bankrupt = all_players.copy()
	
	advance_turn = True
	modified_after_save = False

	while len(non_bankrupt) > 1:
		clear()
		print()
		if DEBUG:
			c.print("[red][bold]Debug mode[/bold] active[/red]")
			for p in all_players:
				c.print(p.__dict__)
			c.print("\n")
			c.print(f"modified_after_save = {modified_after_save}")
			c.rule()
			c.rule()
			c.print("\n")

		if advance_turn:
			turn +=1
		advance_turn = True

		if turn >= len(non_bankrupt):
			turn = 0

		current_player = non_bankrupt[turn]

		choice = None

		if current_player.in_jail:
			current_player.turns_in_jail += 1
			c.print(f"[bold]{current_player.name}[/bold], it is your turn.")
			print_all_players(all_players, turn)
			c.print(f"[red][bold]{current_player.name}[/bold], you are currently in jail.[/red]")
			c.print(f"This is turn #{current_player.turns_in_jail} in jail.")
			c.print("Select an option to get out of jail.")
			
			options = ["Pay $50"]
			if current_player.jail_cards > 0:
				options.append("Use Get Out Of Jail Free card")
			if current_player.turns_in_jail <= 3:
				options.append("Roll the dice")

			jail_escape_choice = interactive_choice("Select an option:", options)
			
			if jail_escape_choice == "Roll the dice":
				doubles = roll_dice()[1]
				if doubles:
					c.print("[green]You rolled doubles and escaped jail![/green]")
					current_player.in_jail = False
					time.sleep(0.5)
					c.print("Press [cyan]ENTER[/cyan] to continue.")
					input()
					continue
				else:
					c.print("[red]You failed to roll doubles and are still in jail.[/red]")
					time.sleep(0.5)
					c.print("Press [cyan]ENTER[/cyan] to continue.")
					input()
					continue

			elif jail_escape_choice == "Pay $50":
				c.print('You paid [bold]$50[/bold] to escape jail.')
				current_player.pay(50)
				current_player.in_jail = False
				current_player.turns_in_jail = 0
				time.sleep(0.5)
				c.print("Press [cyan]ENTER[/cyan] to continue.")
				input()
				continue
					
			elif jail_escape_choice == "Use Get Out Of Jail Free card":
				c.print("You used a Get Out Of Jail Free card.")
				c.print("[green]You are no longer in jail.[/green]")
				c.print("Press [cyan]ENTER[/cyan] to continue.")
				input()
				continue

		elif not current_player.in_jail:
			while True:
				c.print(f"[bold]{current_player.name}[/bold], it is your turn.")
				print_all_players(all_players, turn)
				c.print("What would you like to do?")
				choice = interactive_choice("Select an option:", ["Roll die & end turn",
																"Build houses/hotels",
																"Sell houses/hotels",
																"Sell property",
																"Mortgage property",
																"Unmortgage property",
																"Export game state",
																"View all property deeds",
																"Exit game"])

				if choice == "Roll die & end turn":
					modified_after_save = True
					break	

				elif choice == "View all property deeds":
					unmortgaged_properties = list(set(current_player.norm_properties_owned + current_player.railroads_owned + current_player.utilities_owned)-set(current_player.mortgaged_properties))
					if len(unmortgaged_properties) == len(current_player.mortgaged_properties) == 0:
						c.print("[red]No properties owned.[/red]")
					
					else:
						if len(unmortgaged_properties) > 0:
							c.print("[bold]Owned properties:[/bold]")
							deeds = [get_deed(x) for x in sorted(unmortgaged_properties, key=lambda x: ALL_SPACES.index(x))]
							c.print(Columns(deeds, expand=False))
						
						if len(current_player.mortgaged_properties) > 0:
							c.print("[bold]Mortgaged properties[/bold]")
							mortgage_deeds = [get_deed(x) for x in sorted(current_player.mortgaged_properties, key = lambda x: ALL_SPACES.index(x))]
							c.print(Columns(mortgage_deeds, expand=False))

				elif choice == "Export game state":
					save_game()
					modified_after_save = False
			
				elif choice == "Exit game":
					if modified_after_save:
						c.print("Would you like to save your game state before exiting?")

						save_choice = interactive_choice("Select an option:", ["Yes", "No"])
						if save_choice == "Yes":
							save_game()
							
						else:
							c.print("[red]Game state not saved.[/red]")

					c.print("Are you sure you want to exit the game?")
					confirm_exit = interactive_choice("Select an option:", ["Yes", "No"])
					if confirm_exit == "Yes":
						c.print("[green]Exiting game...[/green]")
						sys.exit()

				elif choice == "Sell houses/hotels":
					if not current_player.norm_properties_owned:
						c.print("[red]You don't own any properties to sell houses/hotels on.[/red]")
					elif not current_player.buildings:
						c.print("[red]You don't own any houses or hotels.[/red]")
					else:
						available_locs = ["Cancel"]
						for group in list(COLOR_GROUP_BUILDING_COSTS.keys()):
							if all([x in current_player.norm_properties_owned and x not in current_player.mortgaged_properties for x in group]):
								building_counts = [current_player.buildings.get(x, 0) for x in group]
								max_build = max(building_counts)
								for prop, count in zip(group, building_counts):
									if count == max_build:
										available_locs.append(prop)
							
						c.print("Which house would you like to sell a house/hotel on?")
						loc = interactive_choice("Select a property:", available_locs)
						if loc == "Cancel":
							c.print("[red]Canceling.[/red]")
						else:
							building_cost = get_building_cost(loc)
							c.print(f"At [bold]{loc}[/bold], you already have [bold]{f"{current_player.buildings[loc]} houses" if current_player.buildings[loc]<5 else "a hotel"}[/bold].")
							c.print(f"You'll receive [bold]{building_cost//2}[/bold] for selling a house or hotel here.")
							c.print("[i](Half the original building price)[/i]")
							c.print("Would you like to sell a building here?")
							confirm_build = interactive_choice("Select an option:", ["Yes", "No"])
							if confirm_build == "Yes":
								current_player.buildings[loc] -= 1
								current_player.collect_without_networth(building_cost//2)
								c.print(f"[green]You sold a building at [bold]{loc}[/bold].[/green]")
								c.print(f"There are now [bold]{current_player.buildings[loc]}[/bold] houses at [bold]{loc}[/bold]")
								modified_after_save = True
							else:
								c.print("[red]Canceling.[/red]")


				elif choice == "Build houses/hotels":
					available_locs = ["Cancel"]
		
					for group in list(COLOR_GROUP_BUILDING_COSTS.keys()):
						if all([x in current_player.norm_properties_owned and x not in current_player.mortgaged_properties for x in group]):
							building_counts = [current_player.buildings.get(x, 0) for x in group]
							min_build = min(building_counts)
							for prop, count in zip(group, building_counts):
								if count == min_build and count < 5:
									available_locs.append(prop)
					
					if len(available_locs) == 0:
						c.print("[red]There are no properties that you can build a house on at this moment.[/red]")

					else:
						c.print("Where would you like to build your house?")
						loc = interactive_choice("Select a property:", available_locs)
						if loc == "Cancel":
							c.print("[red]Canceling.[/red]")
						else:
							building_cost = get_building_cost(loc)

							if current_player.networth >= building_cost:
								c.print(f"At [bold]{loc}[/bold], you already have [bold]{f"{current_player.buildings[loc]} houses" if current_player.buildings[loc]<5 else "a hotel"}[/bold].")
								c.print(f"Building a house will cost [bold]${building_cost}[/bold]. Your net worth is [bold]${current_player.networth}[/bold].")
								c.print("Would you like to build a house here?")
								confirm_build = interactive_choice("Select an option:", ["Yes", "No"])
								if confirm_build == "Yes":
									current_player.build_house(loc)
									c.print(f"[green]You built a house/hotel at [bold]{loc}[/bold].[/green]")
									modified_after_save = True
							else:
								c.print(f"[red]You do not have enough money to build a house at {loc}. (${current_player.networth} < ${building_cost}).")
				
				elif choice == "Sell property":
					if not current_player.all_properties_owned():
						c.print("[red]You don't own any properties to sell.[/red]")
					else:
						c.print("Select a property you are offering to sell.")
						can_sell = [x for x in current_player.all_properties_owned() if x not in current_player.buildings] + ["Cancel"]
						to_sell = interactive_choice("Select an option:", can_sell)

						if to_sell == "Cancel":
							c.print("[red]Canceling...[/red]")
						else:
							c.print("Choose the player to offer this property to.")
							buyer = interactive_choice("Select an option:", [p.name for p in all_players])
							c.print("Select an amount to sell this property for.")
							valid_offer = False
							while not valid_offer:
								try:
									offer_price = int(input("> "))
									valid_offer = True
								except:
									c.print("[red]Please input an integer number.[/red]")

							buyer_obj = next(p for p in all_players if p.name == buyer)

							if buyer_obj.cash >= offer_price:
								c.print(f"{buyer}, do you accept the offer of [bold]${offer_price}[/bold] for [bold]{to_sell}[/bold]?")
								c.print("Here is the title deed:")
								c.print(get_deed(to_sell))
								accept_offer = interactive_choice(f"Select an option", ["Yes", "No"])
								if accept_offer == "Yes":
									current_player.sell_property(to_sell)
									buyer_obj.get_property(to_sell)
									c.print(f"[green][bold]{buyer}[/bold] accepted your offer.")
									c.print(f"[green][bold]{buyer}[/bold] bought [bold]{to_sell}[/bold] from [bold]{current_player.name}[/bold] for [bold]${offer_price}[/bold].[/green]")
									modified_after_save = True

								else:
									c.print(f"[red][bold]{buyer}[/bold] turned down your offer.[/red]")
							
							else:
								c.print(f"[red][bold]{buyer}[/bold] has insufficient cash to buy your property.[/red]")
				
				elif choice == "Mortgage property":
					if not current_player.all_properties_owned():
						c.print("[red]You don't own any properties to mortgage.[/red]")
					else:
						c.print("Select a property you want to mortgage.")
						can_mortgage = [x for x in current_player.all_properties_owned() if x not in current_player.mortgaged_properties] + ["Cancel"]
						if not can_mortgage:
							c.print("[red]You don't have any properties that can be mortgaged.[/red]")
						if can_mortgage != "Cancel":
							to_mortgage = interactive_choice("Select an option:", can_mortgage)
							mortgage_value = get_property_cost(to_mortgage) // 2
							c.print(f"Are you sure you would like to mortgage [bold]{to_mortgage}[/bold] for [bold]${mortgage_value}[/bold]?")
							confirm_mortgage = interactive_choice("Select an option:", ["Yes", "No"])
							if confirm_mortgage == "Yes":
								current_player.mortgage(to_mortgage)
								c.print(f"[green]You mortgaged [bold]{to_mortgage}[/bold].[/green]")
								modified_after_save = True
						else:
							c.print("[red]Canceled.[/red]")
					
				elif choice == "Unmortgage property":
					if not current_player.mortgaged_properties:
						c.print("[red]You don't have any properties that can be unmortgaged.[/red]")
					else:
						c.print("Select a property you want to unmortgage.")
						to_unmortgage = interactive_choice("Select an option:", current_player.mortgaged_properties + ["Cancel"])
						if to_unmortgage == "Cancel":
							c.print("[red]Canceling...[/red]")
						else:
							unmortgage_value = (get_property_cost(to_unmortgage) // 2 * 1.1)//1
							c.print(f"Are you sure you would like to unmortgage [bold]{to_unmortgage}[/bold] for [bold]${unmortgage_value}[/bold]?")
							confirm_unmortgage = interactive_choice("Select an option:", ["Yes", "No"])
							if confirm_unmortgage == "Yes":
								current_player.unmortgage(to_unmortgage)
								c.print(f"[green]You unmortgaged [bold]{to_unmortgage}[/bold].[/green]")
								modified_after_save = True
				
				c.print("Press [cyan]ENTER[/cyan] to continue.")
				input()
				clear()

			roll, doubles = roll_dice()
			if doubles:
				advance_turn = False
				current_player.doubles += 1
			else:
				advance_turn = True
				current_player.doubles = 0

			if current_player.doubles == 3:
				c.print("[red]You rolled three doubles in a row and were sent to jail![/red]")
				current_player.in_jail = True
				current_player.current_square = "JAIL"
				current_player.turns_in_jail = 0
				current_player.doubles = 0
				c.print("Press [cyan]ENTER[/cyan] to continue.")
				input()
				continue


			current_square_index = ALL_SPACES.index(current_player.current_square)

			if current_square_index + roll > len(ALL_SPACES)-1:
				c.print("[green]You passed GO and collected $200.[/green]")
				current_player.collect(200)	
				current_square_index = current_square_index + roll - len(ALL_SPACES)
			else:
				current_square_index = current_square_index + roll
			
			current_player.current_square = ALL_SPACES[current_square_index]
		
			c.print(f"Your token advanced to [bold]{current_player.current_square}[/bold].")
			if current_player.current_square == "JAIL" and not current_player.in_jail:
				c.print("[i]Note: you are not in jail- you are just visiting.[/i]")

			time.sleep(0.5)

			do_square_action(current_player)


#####################################################################################################################
#    MAIN    ########################################################################################################
#####################################################################################################################
if __name__ == '__main__':
	try:
		clear()

		render_image_ascii_color("title.png")

		if DEBUG:
			cc.print("[red underline]Note: [bold]DEBUG MODE[/bold] is activated.[/red underline]")
			cc.print("[red]Change line 15 of main.py to [bold]DEBUG = False[/bold] to disable debug mode.[/red]\n")
		cc.print("[i]Full screen recommended for best user experience[/i]")
		cc.print("[bold]Press [cyan]ENTER[/cyan] to begin![/bold]")
		input()
		clear()

		c.print(TITLE_ASCII, style="bold cyan")
		c.print("The Classic Edition")
		c.print('Made by Anish Gupta\n')

		c.print("Would you like to load a saved game or create a new game?")
		load_or_new = interactive_choice("Select an option:", ["Create a new game", "Load a saved game"])
		if load_or_new == "Load a saved game":
			c.print("Please select a file. (*.pkl)")

			root = tkinter.Tk()
			root.withdraw()

			root.attributes("-topmost", True)  # Bring the file dialog to the front

			file_path = filedialog.askopenfilename(
				title="Select a file",
				filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
			)

			if file_path:
				with open(file_path, "rb") as load_file:
					all_players, turn = pickle.load(load_file)
				p1, p2, p3, p4 = all_players
				c.print("[green]Game imported successfully![/green]")
				c.print("Press [cyan]ENTER[/cyan] to begin.")
				input()
			else:
				c.print("[red]No file selected. Exiting...[/red]")
				sys.exit()
		else:
			c.print("Creating a new game.")
			c.print('Player 1, enter your name:')
			n1 = input('> ')
			c.print('Player 2, enter your name:')
			n2 = input('> ')
			c.print('Player 3, enter your name:')
			n3 = input('> ')
			c.print('Player 4, enter your name:')
			n4 = input('> ')

			p1 = Player(n1)
			p2 = Player(n2)
			p3 = Player(n3)
			p4 = Player(n4)

			all_players = [p1, p2, p3, p4]

			turn = -1
			advance_turn = True

			c.print("Press [cyan]ENTER[/cyan] to begin.")


		game_loop()
	except Exception:
		c.print_exception(show_locals=True)
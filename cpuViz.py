from rich.console import Console
from rich.table import Table
from rich.live import Live
from datetime import datetime
from time import sleep
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
import random
import json
import sys,os


class CpuViz:
	def __init__(self, number):
		self.instructions = None

	def update(self, instructions):
		if self.instructions == None:
			self.instructions = ["EMPTY"]
		else:
			self.instructions = instructions

	def build_table(self):
		#if you wanted you could add a coulumn for if it's a privliged instruction
		table = Table(title = "CPU")
		table.add_column("Instruction", justify="center", style="cyan", no_wrap=True)
		for i in self.instructions:
			table.add_row(i)
		return table

	def __rich__(self):
		return Panel(self.build_table())
    
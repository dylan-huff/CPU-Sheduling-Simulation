import rich
import time
import json
from cpu import Cpu
from ioClass import IO
from jobs import Job
from new import New
from ready import Ready
from terminated import Terminated
from waiting import Waiting
from rich import print
from rich.columns import Columns
from rich import box
from rich import panel
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.console import Console
from rich.table import Table




table = Table(title="Jobs")
  
table.add_column("Job I.D.", style="cyan", no_wrap=True)
table.add_column("Task")
table.add_column("CPU Wait Time", justify="right", style="orange_red1")
table.add_column("I/O Wait Time", justify="right", style="bright_yellow")

table1 = Table(title="Results")

table1.add_column("Job I.D.", style="cyan", no_wrap=True)
table1.add_column("Status", style="green")
table1.add_column("TAT", justify="right", style="cyan1")
table1.add_column("Total CPU Wait Time", justify="right", style="orange_red1")
table1.add_column("Total I/O Wait Time", justify="right", style="bright_yellow")

def createJobs():

  jobList = []

  jobs = []

  f = open('datafile.json')

  file = json.load(f)

  for i in file['jobs']:
	  jobs.append(i)

  #print(jobs)

  values = []

  for i in jobs[0]:
	  values.append(i)

  for i in range(len(jobs)):
	  aJob = []
	  for x in values:
		  aJob.append(jobs[i][x])
	  job = Job(aJob)
	  jobList.append(job)

  algo = input('Which algorithm are you using: ')
  if algo == 'rr':
	  timeSlice = input("Enter your desired timeSlice: ")
	  timeSlice = int(timeSlice)
  else:
	  timeSlice = 5
  cpus = input('Enter the number of CPUs you wish to use: ')
  cpus = int(cpus)

  ios = input('Enter the number of IOs you wish to use: ')
  ios = int(cpus)

  test(algo, timeSlice, cpus, ios, jobList)


def test(algo, timeSlice, cpus, ios, jobs):
  count = 0
  cpuList = []
  ioList = []
  cpuActive = 0
  ioActive = 0

  for i in range(cpus):
	  cpu = Cpu(algo, timeSlice)
	  cpuList.append(cpu)

  for i in range(ios):
	  io = IO()
	  ioList.append(io)

  newQueue = New()
  ready = Ready()
  terminated = Terminated()
  waiting = Waiting()
	
  while len(terminated.termQueue) < len(jobs):

	  if len(ready.readyQueue) > 0:
		  ready.cpuWait()
	  if len(waiting.waitQueue) > 0:
		  waiting.ioWait()

		#move to the terminated Queue
	  for i in cpuList:
		  if i.term == True:
			  terminated.addTerm(i.move, count) #added new param to calc turanaround time
			  i.term = False
				#print('Moved TO TERM! Count:' + str(count))
			  table.add_row(str(i.move.id), "[green]moved to Term!", str(i.move.CPUWaitTime), str(i.move.IOWaitTime))
        

		#from IO to ready
	  for i in ioList:
		  if i.send == True:
			  table.add_row(str(i.move[0].id), "[gold1]From IO to Ready Queue!", str(i.move[0].CPUWaitTime), str(i.move[0].IOWaitTime))
			  ready.addReady(i.move, algo)
			  i.send = False
			  i.move = None
				#print('FROM IO TO READY QUEUE! Count:' + str(count))


		#Move from CPU to waiting Queue
	  for i in cpuList:
		  if i.moving == True and i.moveReady == False:
			  table.add_row(str(i.move.id), "[light_coral]From CPU to Waiting Queue!", str(i.move.CPUWaitTime), str(i.move.IOWaitTime))
			  waiting.addWaiting(i.move)
			  i.moving = False
			  i.move = None
			  i.currentTime = 0
				#print('FROM CPU TO WAITING QUEUE! COUNT:' + str(count))

		#Move From CPU to Ready Queue
	  for i in cpuList:
		  if i.moving == True and i.moveReady == True:
			  ready.addReady([i.move], algo)
			  table.add_row(str(i.move.id), "[light_steel_blue1]From CPU to Ready Queue!", str(i.move.CPUWaitTime), str(i.move.IOWaitTime))
			  i.moveReady = False
			  i.moving = False
			  i.move = None
			  i.currentTime = 0
				#print('From CPU TO READY QUEUE! COUNT:' + str(count))

		#Run IO
	  for i in ioList:
		  if i.busy == True and i.job != None:
			  table.add_row(str(i.job.id), "[tan]Running IO!", str(i.job.CPUWaitTime), str(i.job.IOWaitTime))
			  i.run()
			  ioActive +=1
				#print('Running IO! Count:' + str(count))

		
		#Run CPU
	  for i in cpuList:
		  if i.busy == True and i.job != None:
			  table.add_row(str(i.job.id), "[magenta3]Running CPU!", str(i.job.CPUWaitTime), str(i.job.IOWaitTime))
			  i.run()
			  cpuActive +=1
				#print('Running CPU! Count:' + str(count))
		

		#from waiting to IO
	  for i in ioList:
		  if waiting.send == True and i.busy == False and i.pause == False:
			  i.recieve(waiting.sendIo())
			  if waiting.move != None:
					#print('FROM WAITING QUEUE TO IO! COUNT:' + str(count))
				  table.add_row(str(i.job.id), "[dark_slate_gray1]From Waiting Queue to IO!", str(i.job.CPUWaitTime), str(i.job.IOWaitTime))


		#from ready to CPU
	  for i in cpuList:
		  if ready.send == True and i.busy == False and i.pause == False:
			  i.recieve(ready.sendCpu())
			  if ready.move != None:
					#print('FROM Ready QUEUE TO CPU! COUNT:' + str(count))
				  table.add_row(str(i.job.id), "[orange4]From Ready Queue To CPU!", str(i.job.CPUWaitTime), str(i.job.IOWaitTime))


		#From new to Ready
	  if len(newQueue.queue) > 0:
		  for i in newQueue.queue:
			  table.add_row(str(i.id), "[sea_green2]Added to Ready Queue!", str(i.CPUWaitTime), str(i.IOWaitTime))
		  ready.addReady(newQueue.queue, algo)
		  newQueue.queue = []
			#print('Added to Ready Queue! Count:' + str(count))

		#From jobslist to NewQueue
	  if count <= len(jobs):
		  for i in jobs:
			  if count == i.arrival:
				  newQueue.addNew(i)
				  #print('Added to New Queue! Count:' + str(count))
				  table.add_row(str(i.id), "[blue1]Added to New Queue!", str(i.CPUWaitTime), str(i.IOWaitTime))


	  waiting.change()

	  ready.change()

	  if algo == 'pb':
		  if len(ready.readyQueue) > 1:
			  ready.pb()
	  for i in cpuList:
		  i.reset()
	  for i in ioList:
		  i.reset()
	  count += 1

  averageCpuWait = 0
  averageIoWait = 0
  averageTat = 0
  cpuActive = (cpuActive/int(cpus))/count
  ioActive = ioActive/(int(ios))/count
  for i in terminated.termQueue:
    table1.add_row(str(i.id), "DONE", str(i.TurnAroundTime), str(i.CPUWaitTime), str(i.IOWaitTime))
    averageIoWait += i.IOWaitTime
    averageCpuWait += i.CPUWaitTime
    averageTat += i.TurnAroundTime
  averageCpuWait /= len(jobs)
  averageIoWait /= len(jobs)
  averageTat /= len(jobs)

  console = Console()

  console.print(table)
  console.print(table1)
  
  print("The average CPU wait time is:" + str(averageIoWait))
  print("The average IO wait time is:" + str(averageCpuWait))
  print("The average turn around time is:" + str(averageTat))
  print("The percentage of CPU utiization is:" + str(cpuActive * 100))
  print("The percentage of I/O utiization is:" + str(ioActive * 100))

if __name__ == "__main__":
	createJobs()
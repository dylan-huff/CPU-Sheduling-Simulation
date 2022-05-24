#WORKING FOR FCFS

from new import New
from jobs import Job
#from CreateJobs import createJobs
from ready import Ready
from cpu import Cpu
from waiting import Waiting
from ioClass import IO
from terminated import Terminated



terminated = Terminated()

io = IO()

waiting = Waiting()

ready = Ready()

cpu = Cpu()

newQueue = New()

job = Job([0,0,2,2,2])
job1 = Job([0,1,2,2,2])
jobs = []

jobs.append(job)
jobs.append(job1)

#need to add the condition to increase wait time to all queues

count = 0

#put in a schedling algo
#these algos will only ever go into the ready Queue

while len(terminated.termQueue) < 2:

	#move to the terminated Queue
	if cpu.term == True:
		terminated.addTerm(cpu.move)
		cpu.term = False
		print('Moved TO TERM! Count:' + str(count))

	#from IO to ready
	if io.send == True:
		ready.addReady(io.move)
		io.send = False
		io.move = None
		print('FROM IO TO READY QUEUE! Count:' + str(count))

	#Move from CPU to waiting Queue
	if cpu.moving == True:
		waiting.addWaiting(cpu.move)
		cpu.moving = False
		cpu.move = None
		print('FROM CPU TO WAITING QUEUE! COUNT:' + str(count))

	#Run IO
	if io.busy == True and io.job != None:
		io.run()
		print('Running IO! Count:' + str(count))

	
	#Run CPU
	if cpu.busy == True and cpu.job != None:
		cpu.run()
		print('Running CPU! Count:' + str(count))
	

	#from waiting to IO
	if waiting.send == True and io.busy == False and io.pause == False:
		io.recieve(waiting.sendIo())
		if waiting.move != None:
			print('FROM WAITING QUEUE TO IO! COUNT:' + str(count))


	#from ready to CPU
	if ready.send == True and cpu.busy == False and cpu.pause == False:
		cpu.recieve(ready.sendCpu())
		if ready.move != None:
			print('FROM Ready QUEUE TO CPU! COUNT:' + str(count))


	#From new to Ready
	if len(newQueue.queue) > 0:
		ready.addReady(newQueue.queue)
		newQueue.queue = []
		print('Added to Ready Queue! Count:' + str(count))

	#From jobslist to NewQueue
	if count == 0:
		newQueue.addNew(jobs[0])
		newQueue.addNew(jobs[1])
		print('Added to New Queue! Count:' + str(count))


	waiting.change()

	ready.change()

	cpu.reset()
	io.reset()
	count += 1


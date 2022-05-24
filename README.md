# CPU-Scheduling-Simulation
The purpose of this program was to learn about some of the different scheduling algorithms a CPU uses by implementing them ourselves.
I worked with two other classmates on this program, so I did not implement every piece of code you see, but still effectively learned
about all of it. The algorithms implemented in this program are first come first serve, round robin, shortest job first, priority based,
and shortest job remaining. We created the CPUs, IOs, job list, algorithms, and visualization (with the help of rich for python) ourselves.
The jobs that make up a job list are just a list of integers per professor instructions, with a job I.D., priority (which is ignored if
not needed), arrival time, and then a series of integers, with the first integer being a CPU time slice, then the next being an IO time 
slice, and they just continue to alternate in that fashion until the end of the job. When the user runs the program they will be prompted
to input which algorithm they want to use, followed by how many CPUs they would like to use (from 1-8) and how many IOs they would like to
use (also from 1-8). If the algorithm the user selects is round robin, they will also be prompted to input the time slice (integer) they
would like use. When the user runs the program they will be able to see what the CPU and IO devices are doing at live speed, however it is
a little too fast to actually keep up with, which is something we decided not to change due to how long the program would take to complete
if we did make that change. With that being said, there is a progress bar at the bottom to let the user know how much has been done and how
much is left. After every run, the results are displayed to the console in a table. The results consist of the job I.D., job status, turnaround time, 
total CPU wait time, and total IO wait time. Below this table, a few more lines are displayed to show the average CPU wait time, average IO wait time,
average turnaround time, percentage of CPU utilization, and percentage of IO utilization. The information displayed below the table is also saved to
a file so that the user can compare the results of the other runs using different algorithms or number of CPUs and IOs.

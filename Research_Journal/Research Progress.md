## 11/14/24
So I gotta go to Los Alamos tomorrow to sort out the laptop. I did not today. I'm gonna email emanuele about it. I believe some people replied to my ROOT issue. I also gotta see if WZ got generated. 

Okay so I fixed the issue of the analysis file creating .root files. So that should work. It doesn't look like WZ got generated so that sucks. Let me try again

So WZ is going. 
Analyze many works partially. However, it breaks at the point of combining plots. So lets dig in.

Alright, so I decided to be calm with it and try to read the root file and make a THStack with just one histogram. Its still not working. So I sent the image and root file to Gang and SUQ to see if it saved the histograms right. In this similar situation (https://root-forum.cern.ch/t/thstack-and-pyroot/13831), the issue was that the histogram didn't exist. That was my first thought too
## 11/13/2024
I just started a test generation of WZ2j and it does have shower=pythia and detector=delphes. So We should be good. I'll check ZZ2j again just in case. Then I'll do a test with all of them at 1 run each low event number and then I'll do the full kablamo. 

After that I'll need to plot and stuff. So while things run, I'll check the plotting. 

So for the analysis, I want it to analyze each type of data, use the nevents after cuts for each type to calculate significance, save plots as .root files, and then open each of those .root files and combine into a THStack and save that. 

Okay so I found where I was going wrong again. JF/main isn't running properly. I'll check the forums to see if anything helpful has come along

Okay so at least one issue was because I had changed the file before such that the event type should be specified by the command line. I had forgotten that change. I just made it so it enforces such formatting. Let's see how it goes

Okay after lunch I gotta figure out how to do the pointer comparison properly
## 11/8/24
Okay so I need to check that auto gen for the full thing worked. I also need to get the analysis going. Someone replied to my ROOT forum post. So I have to see if I can figure out what that means.

Okay so it seems that diboson event generation isn't working. One error popping up is 
` PYTHIA Abort from Pythia::Pythia: unmatched version numbers : in code 8.306 but in XML 8.311`
I'm going to lower nevents for diboson and try to get this this sorted. THe solutions online seems to suggest that I need to properly set the PYTHIA8DATA in bashrc. But that is what I have. I just deleted the old madgraph installation so hopefully this can work now

For GenManyOnUnity.py, it will now print out when it fails to gen 200k+ events. Later I'll need to take that and have it output something so that when I automate Generating many for a given parameter set and then moving on to the next parameter set it knows when it needs to try again. 

Okay so I accidentally deleted my venv so I redid that. It looks like the event generation isn't working because something in the madevent is looking for the old version of madgraph so I have to regenerate the processes. I think I'm going to try moving the events so they don't get deleted. 

I did this. It looks like WZ generation is working now... Well. ZZ worked except for shower and dectector are OFF... WZ seemed to get stuck.

Issues:
- [ ] Event generation:
	- [ ] diboson events don't turn on pythia8 and delphes
	- [ ] WZ doesn't seem to finish
- [ ] Analysis
	- [ ] running either read_root_file or JetFake/main gives `error while loading shared libraries: libCore.so: cannot open shared object file: No such file or directory`

## 11/7/24
I'm going to check to see if the autogen worked. If it did then I'll set it to run for all events and the correct amount of requested events. Then its time for the analysis plots woa
## 11/6/24
Okay So Now the goal is 1) get autogen working and 2) read

I think autogen is working. SO i'll check tomorrow and then get them all to generate proper amounts. While that runs then I'll work on the analysis plots

## 11/5/24
Okay, I have been diggina round to understand the error I am getting with generating events. I found its better to call the run card with an absolute path. i tried generating events in madgraph "manually" and after doing'launch' and such i get a shitty error. I think the easiest thing to do is to is reinstall madgraph and delphes and such. After I do this, I'll need to edit the paths in .bashrc. 

In like 10 mins Michael G and I will go to easyIT and get the laptop set up. So once that's complete, I'll get the ssh set up on it. Then I'll do the reinstallation.

Okay so the laptop has to wait for some reason. I reinstalled madgraph, pythia8, delphes, exrootanalysis. I put O2_flavor model into the new installation. I put the JF card into the Delphes/cards of the new installation. I made a new git for the analysis and generation files. I adjusted the PATHs on .bashrc and on the shortcut txt. I regenerated LNVF process and am regenerating events as we speak. It WORKED!

So now I need to get auto gen running. Lets see what happens

## 11/4/24
So Root works I believe. I'll double check and then modify .bashrc and then recompile ExRoot and Delphes. 
First, I'm going to check on the status of the work laptop. 
After all that, then I need to get event generation going. Then I need to get analysis to produce the proper plots. 
Then read. 
Once the plots are made (post event genration), then hopefully it matches enough. 

OKAY: so ROOT is working. Delphes and ExRoot compiled. The Laptop is gonna be set up tomorrow. 
Event generation isn't working. I think its because the individual madevent stuff isn't recompiled. I asked SUQ about it. After lunch, I'll just regenerate the process for one event type and if that works, then I'm going to get the autogen to run for that event type*. If that works then I'll regenerate all processes and then regenerate all events with the autogen

For today, i'm just going to do until * and then read
## 10/31/24
Yesterday Georgia from the UNITY support said she'd install ROOT properly like an adult in a place I can access. Once that's in place, I can recompile ExROOT and Delphes and it should all be good. fingers crossed. 
Then I'll need to get the events to generate properly
Then I'll need to get the plots good. For now i'll read Peskin and schroder ch4
## 10/29/24
OKay So I need to set up badge office appt and I need to check payment stuff and I need to find who I can ask about ROOT stuff, and I need to get a bag tag

So it doesn't seem I'm set up to be paid by LANL, so idk what's going on. I got a badge office appt for a bit later today to get ztoken sorted. 


## 10/28/24
Bullshit 2nd kind: So I need to make sure I'm getting paid this week, and I have to get this work laptop stuff figured out

I need ROOT to work on UNITY in order for MG5 to work. I hope that's the only obstacle for MG5 but we'll see. I think I need to recompile ROOT but I don't know how to do that. I asked in skype and on ROOT forum.

for reading: I switched to Peskin and Schroder CH4. problem 4.2 is a good start
## 10/24/24
Okay so I need to get UNITY to work and then I need to check that JetFake is doing the right thing. Then I'll set events to generate. Then start writing up the collider set up stuff

So far, I have been able to get ./read_root_file to compile but running it causes an issue. I posted on madgraph forum and the UNITY slack
## 10/23/24
UNITY is back online. I remade the venv so I can use numpy. However read_root_file won't compile due to some errors. I still feel pretty sick so i don't think I got in in me to troubleshoot today. Maybe later. I'll have to message UNITY slack about it
## 10/22/24
Welcome back. Boy this is really highlighting how often I don't work. 
For the collider side, I'll need to recreate plots better. However I still don't have the event generation working. For the low energy side, I need to keep reading. 

I was going to get the event generation going but it seems UNITY is down while they upgrade ubuntu. God I hope this doesn't mess up much

So I'll read today

Meeting with Gang and SUQ:
Need to show that the jetfake includes muons. 
## 10/15/24
Okay so I should be calling with Justin in a bit. But maybe not. I'll be meeting with SUQ at 10 and I gotta ask him a few things. is mu->e conversion a subset of what was already done?What other models correspond to the O(2) model (scotogenic and MSSM). talk to him about the current state of the project. Why would the significance be that low. 
I also am meeting with Emanuele at some time. I need to set a time. I gotta shit. 
As far as the reading goes: I think I should just finish the chapter. Then go to something more needed for the decay calc.
For the project, I should make plots to diagnose and make a plan for automating the next steps. 
There's some key error in Gen many. I'm cleaning up read many functions to hopefully fix it\

Met with sebastian and I'll try to recreate the plots first instead of significance. 
I don't know why the sbatch isn't outputting anything to text file. Ask over slack tomorrow. Hopefully it has finished generating some events by then
## 10/14/24
I'm working on getting slides together for MG and E. It doesn't look like the event generation worked. I'm going to work on that too. 

For some reason GenMany.py isn't printing to output1.txt I'll have to go to Unity office hours tomorrow. 
The event numbers are close enough that I should be able to get a significance. Let's write a python script to get the file names and run analysis and output Significance.

## 10/11/24
Okay, so still working on remixing read_many.py for speed [[#10/09/24|See 10/09]]. It looks like since i swithced oned thing to a dictionary its easier if i change countEvent to use one too. 

END: okay so it looks like we all good. 
I sent a job in to run GenManyOnUnity.py. It should top off LNVF and WZ2j. To check, look at event_counts.txt, run `sacct -j 25457882` , and look at logs/GenMany/output1.txt. 
If that works, then put automation on the back burner. The next automation thing will be generating all this for each param space. So figure out what that means for proc generation and the like.
Next time (if it works) we need to return to analysis. Return to analysis, have S between the different cuts. 


## 10/09/24
I’m working on remixing read_many.py to write <event_type>,<highest run number>, <total_events> \n into a text file. Then when its called again, it reads that file and checks if there is a difference in the run number. If not, then there haven’t been any new events generated, so we can just read off of the txt file. You can also force it to do the full recount if you’d like

I also need to do finalize the gen_many

END: I’m going to change the countEvent function to use a dictionary instead. That should solve the problem of writing a list instead of a number for number of events

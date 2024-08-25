CXX = g++
FC = g77

# ROOTINC= -I/home/gangli/Documents/Simulation/MG5_aMC_v2_6_6/ExRootAnalysis/ExRootAnalysis
# ROOTLIB= -L/home/gangli/Documents/Simulation/MG5_aMC_v2_6_6/ExRootAnalysis -lExRootAnalysis

ROOTINC= -I/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/ExRootAnalysis/ExRootAnalysis
ROOTLIB= -L/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/ExRootAnalysis -lExRootAnalysis

# ROOTFLAG=${shell root-config --cflags --libs}
ROOTFLAG=${shell root-config --cflags --glibs} -lEG

FJFLAG=${shell /home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/fastjet-3.4.2/fastjet-install/bin/fastjet-config --cxxflags --libs --plugins}

# ROOTINC2= -I/home/gangli/Documents/Simulation/MG5_aMC_v2_6_6/Delphes/external \
#          -I/home/gangli/Documents/Simulation/MG5_aMC_v2_6_6/Delphes/display \
#          -I/home/gangli/Documents/Simulation/MG5_aMC_v2_6_6/Delphes
# ROOTLIB2= -L/home/gangli/Documents/Simulation/MG5_aMC_v2_6_6/Delphes -lDelphes

ROOTINC2= -I/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/Delphes/external \
         -I/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/Delphes/display \
         -I/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/Delphes \
	 -I/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/Delphes/external/fastjet \
	 -I/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/fastjet-3.4.2 \
	 -I/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/fastjet-3.4.2/fastjet-install/include
ROOTLIB2= -L/home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/Delphes -lDelphes



CPPFLAGS=${ROOTFLAG} ${ROOTINC} ${FJFLAG} ${ROOTINC2}  #${ROOTINC2}  #${FJFLAG} ${ROOTINC}
LDFLAGS= ${ROOTFLAG} ${ROOTLIB} ${FJFLAG} ${ROOTLIB2} #${ROOTLIB} #	${ROOTLIB2} #${FJFLAG} ${ROOTLIB}
#FOBJS := $(patsubst %.f,%.o,$(wildcard *.f)) 
CCOBJS := $(patsubst %.cpp,%.o,$(wildcard *.cpp))

read_root_file:  ${CCOBJS}
	$(CXX) *.o  ${LDFLAGS} -o  $@

%.o : %.cpp
	$(CXX) -c $(CPPFLAGS) $& $<

clean:
	rm *.o main CountEvents read_root_file

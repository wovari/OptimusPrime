#-----------------------------------------------------------------------
# File    : pyfim_conda.mak
# Contents: build pyfim dynamic link library (on Windows systems)
#           (for Anaconda distribution)
# Author  : Christian Borgelt
# History : 2012.08.03 file created
#           2013.10.19 module patspec added
#           2013.11.08 properly adapted to Windows/Microsoft Visual C
#           2013.11.14 adapted for Anaconda Python distribution
#           2014.08.25 module ista added
#           2015.03.04 interrupt signal handling added
#           2015.03.05 preprocessor definitions XXX_ABORT added 
#           2015.08.19 module patred added
#-----------------------------------------------------------------------
!IFNDEF CONDAINC
CONDAINC = "C:\Anaconda\include"
!ENDIF
!IFNDEF CONDALIB
CONDALIB = "C:\Anaconda\libs"
!ENDIF
THISDIR  = ..\..\pyfim\src
UTILDIR  = ..\..\util\src
MATHDIR  = ..\..\math\src
TRACTDIR = ..\..\tract\src
APRIDIR  = ..\..\apriori\src
ECLATDIR = ..\..\eclat\src
FPGDIR   = ..\..\fpgrowth\src
SAMDIR   = ..\..\sam\src
RELIMDIR = ..\..\relim\src
CARPDIR  = ..\..\carpenter\src
ISTADIR  = ..\..\ista\src
ACCDIR   = ..\..\accretion\src

CC       = cl.exe
DEFS     = /D WIN32 /D NDEBUG /D _CONSOLE /D _CRT_SECURE_NO_WARNINGS \
           /D QUIET
CFLAGS   = /nologo /MD /W3 /O2 /GS- $(DEFS) /c
PYINC    = /I $(CONDAINC)
INCS     = /I $(UTILDIR) /I $(MATHDIR)  /I $(TRACTDIR) \
           /I $(APRIDIR) /I $(ECLATDIR) /I $(FPGDIR)   \
           /I $(SAMDIR)  /I $(RELIMDIR) /I $(CARPDIR)  \
           /I $(ISTADIR) /I $(ACCDIR)

LD       = link.exe
LDFLAGS  = /DLL /nologo /incremental:no
LIBS     = /LIBPATH:$(CONDALIB)

HDRS     = $(UTILDIR)\arrays.h    $(UTILDIR)\memsys.h  \
           $(UTILDIR)\symtab.h    $(UTILDIR)\random.h  \
           $(UTILDIR)\sigint.h    $(MATHDIR)\gamma.h   \
           $(MATHDIR)\chi2.h      $(MATHDIR)\ruleval.h \
           $(TRACTDIR)\tract.h    $(TRACTDIR)\fim16.h  \
           $(TRACTDIR)\patspec.h  $(TRACTDIR)\clomax.h \
           $(TRACTDIR)\report.h   $(TRACTDIR)\patred.h \
           $(APRIDIR)\apriori.h   $(ECLATDIR)\eclat.h  \
           $(FPGDIR)\fpgrowth.h   $(FPGDIR)\fpgpsp.h   \
           $(SAMDIR)\sam.h        $(RELIMDIR)\relim.h  \
           $(CARPDIR)\carpenter.h $(ISTADIR)\ista.h    \
           $(ACCDIR)\accretion.h
OBJS     = arrays.obj memsys.obj idmap.obj random.obj sigint.obj \
           chi2.obj gamma.obj ruleval.obj tatree.obj \
           fim16.obj patspec.obj clomax.obj report.obj patred.obj \
           istree.obj apriori.obj eclat.obj fpgrowth.obj \
           sam.obj relim.obj repotree.obj carpenter.obj \
           pfxtree.obj pattree.obj ista.obj accretion.obj \
           fpgpsp.obj pyfim.obj
PRGS     = fim.pyd

#-----------------------------------------------------------------------
# Build Dynamic Link Library
#-----------------------------------------------------------------------
all:          $(PRGS)

fim.pyd:      $(OBJS) pyfim_conda.mak
	$(LD) $(LDFLAGS) $(LIBS) $(OBJS) /out:$@ /IMPLIB:fim.lib

#-----------------------------------------------------------------------
# Array Operations
#-----------------------------------------------------------------------
arrays.obj:   $(UTILDIR)\arrays.h $(UTILDIR)\fntypes.h
arrays.obj:   $(UTILDIR)\arrays.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(UTILDIR)\arrays.c /Fo$@

#-----------------------------------------------------------------------
# Memory Management System for Objects of Equal Size
#-----------------------------------------------------------------------
memsys.obj:   $(UTILDIR)\memsys.h
memsys.obj:   $(UTILDIR)\memsys.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(UTILDIR)\memsys.c /Fo$@

#-----------------------------------------------------------------------
# Symbol Table Management
#-----------------------------------------------------------------------
idmap.obj:    $(UTILDIR)\symtab.h $(UTILDIR)\fntypes.h \
              $(UTILDIR)\arrays.h
idmap.obj:    $(UTILDIR)\symtab.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D IDMAPFN $(UTILDIR)\symtab.c /Fo$@

#-----------------------------------------------------------------------
# Random Number Generator Management
#-----------------------------------------------------------------------
random.obj:   $(UTILDIR)\random.h
random.obj:   $(UTILDIR)\random.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(UTILDIR)\random.c /Fo$@

#-----------------------------------------------------------------------
# Interrupt Signal Handling
#-----------------------------------------------------------------------
sigint.obj:   $(UTILDIR)\sigint.h
sigint.obj:   $(UTILDIR)\sigint.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(UTILDIR)\sigint.c /Fo$@

#-----------------------------------------------------------------------
# Mathematical Functions
#-----------------------------------------------------------------------
gamma.obj:    $(MATHDIR)\gamma.h
gamma.obj:    $(MATHDIR)\gamma.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(MATHDIR)\gamma.c /Fo$@

chi2.obj:     $(MATHDIR)\chi2.h
chi2.obj:     $(MATHDIR)\chi2.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(MATHDIR)\chi2.c /Fo$@

ruleval.obj:  $(MATHDIR)\ruleval.h
ruleval.obj:  $(MATHDIR)\ruleval.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(MATHDIR)\ruleval.c /Fo$@

#-----------------------------------------------------------------------
# Item and Transaction Management
#-----------------------------------------------------------------------
tatree.obj:   $(TRACTDIR)\tract.h $(UTILDIR)\arrays.h \
              $(UTILDIR)\symtab.h
tatree.obj:   $(TRACTDIR)\tract.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D TATREEFN /D TA_SURR \
              $(TRACTDIR)\tract.c /Fo$@

#-----------------------------------------------------------------------
# Item Set Reporter Management
#-----------------------------------------------------------------------
patspec.obj:  $(TRACTDIR)\patspec.h $(TRACTDIR)\tract.h
patspec.obj:  $(TRACTDIR)\patspec.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D PSP_ESTIM \
              $(TRACTDIR)\patspec.c /Fo$@

clomax.obj:   $(TRACTDIR)\clomax.h $(TRACTDIR)\tract.h \
              $(UTILDIR)\arrays.h
clomax.obj:   $(TRACTDIR)\clomax.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(TRACTDIR)\clomax.c /Fo$@

report.obj:   $(TRACTDIR)\report.h  $(TRACTDIR)\clomax.h \
              $(TRACTDIR)\patspec.h $(TRACTDIR)\tract.h \
              $(UTILDIR)\arrays.h   $(UTILDIR)\symtab.h
report.obj:   $(TRACTDIR)\report.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D ISR_PATSPEC /D ISR_CLOMAX \
              /D ISR_NONAMES $(TRACTDIR)\report.c /Fo$@

#-----------------------------------------------------------------------
# Pattern Set Reduction Functions
#-----------------------------------------------------------------------
patred.obj:   $(HDRS) $(TRACTDIR)\patred.h
patred.obj:   $(TRACTDIR)\patred.c pycoco.mak
	$(CC) $(CFLAGS) $(INCS) $(TRACTDIR)\patred.c /Fo$@

#-----------------------------------------------------------------------
# 16 Items Machine
#-----------------------------------------------------------------------
fim16.obj:    $(TRACTDIR)\tract.h $(TRACTDIR)\report.h \
              $(UTILDIR)\arrays.h  $(UTILDIR)\symtab.h
fim16.obj:    $(TRACTDIR)\fim16.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(TRACTDIR)\fim16.c /Fo$@

#-----------------------------------------------------------------------
# Accretion
#-----------------------------------------------------------------------
accretion.obj:  $(HDRS) $(ACCDIR)\accretion.h $(UTILDIR)\fntypes.h
accretion.obj:  $(ACCDIR)\accretion.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D ACC_ABORT \
              $(ACCDIR)\accretion.c /Fo$@

#-----------------------------------------------------------------------
# Apriori
#-----------------------------------------------------------------------
istree.obj:   $(HDRS) $(APRIDIR)\istree.h
istree.obj:   $(APRIDIR)\istree.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D TATREEFN $(APRIDIR)\istree.c /Fo$@

apriori.obj:  $(HDRS) $(APRIDIR)\istree.h $(APRIDIR)\apriori.h \
              $(UTILDIR)\fntypes.h
apriori.obj:  $(APRIDIR)\apriori.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D APR_ABORT $(APRIDIR)\apriori.c /Fo$@

#-----------------------------------------------------------------------
# Eclat
#-----------------------------------------------------------------------
eclat.obj:    $(HDRS) $(ECLATDIR)\eclat.h $(UTILDIR)\fntypes.h
eclat.obj:    $(ECLATDIR)\eclat.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D ECL_ABORT $(ECLATDIR)\eclat.c /Fo$@

#-----------------------------------------------------------------------
# FP-growth
#-----------------------------------------------------------------------
fpgrowth.obj: $(HDRS) $(FPGDIR)\fpgrowth.h $(UTILDIR)\fntypes.h
fpgrowth.obj: $(FPGDIR)\fpgrowth.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D FPG_ABORT $(FPGDIR)\fpgrowth.c /Fo$@

fpgpsp.obj:   $(HDRS) $(FPGDIR)\fpgrowth.h $(FPGDIR)\fpgpsp.h \
              $(UTILDIR)\fntypes.h
fpgpsp.obj:   $(FPGDIR)\fpgrowth.c $(FPGDIR)\fpgpsp.c pyfim.mak
	$(CC) $(CFLAGS) $(INCS) /D FPG_ABORT $(FPGDIR)\fpgpsp.c /Fo$@

#-----------------------------------------------------------------------
# SaM
#-----------------------------------------------------------------------
sam.obj:      $(HDRS) $(SAMDIR)\sam.h $(UTILDIR)\fntypes.h
sam.obj:      $(SAMDIR)\sam.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D SAM_ABORT $(SAMDIR)\sam.c /Fo$@

#-----------------------------------------------------------------------
# RElim
#-----------------------------------------------------------------------
relim.obj:    $(HDRS) $(RELIMDIR)\relim.h $(UTILDIR)\fntypes.h
relim.obj:    $(RELIMDIR)\relim.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D RELIM_ABORT $(RELIMDIR)\relim.c /Fo$@

#-----------------------------------------------------------------------
# Carpenter
#-----------------------------------------------------------------------
repotree.obj: $(HDRS) $(CARPDIR)\repotree.h
repotree.obj: $(CARPDIR)\repotree.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(CARPDIR)\repotree.c /Fo$@

carpenter.obj:  $(HDRS) $(CARPDIR)\carpenter.h $(CARPDIR)\repotree.h \
                $(UTILDIR)\fntypes.h
carpenter.obj:  $(CARPDIR)\carpenter.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D CARP_ABORT \
              $(CARPDIR)\carpenter.c /Fo$@

#-----------------------------------------------------------------------
# IsTa
#-----------------------------------------------------------------------
pfxtree.obj:  $(HDRS) $(ISTADIR)\pfxtree.h $(UTILDIR)\memsys.h
pfxtree.obj:  $(ISTADIR)\pfxtree.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(ISTADIR)\pfxtree.c /Fo$@

pattree.obj:  $(HDRS) $(ISTADIR)\pattree.h
pattree.obj:  $(ISTADIR)\pattree.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(ISTADIR)\pattree.c /Fo$@

ista.obj:     $(HDRS) $(ISTADIR)\pattree.h $(ISTADIR)\pfxtree.h \
              $(ISTADIR)\ista.h
ista.obj:     $(ISTADIR)\ista.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) /D ISTA_ABORT $(ISTADIR)\ista.c /Fo$@

#-----------------------------------------------------------------------
# Python Stuff
#-----------------------------------------------------------------------
pyfim.obj:    $(HDRS) $(ACCDIR)\accretion.h $(APRIDIR)\apriori.h \
              $(ECLATDIR)\eclat.h $(FPGDIR)\fpgrowth.h \
              $(FPGDIR)\fpgpsp.h $(SAMDIR)\sam.h $(RELIMDIR)\relim.h \
              $(CARPDIR)\carpenter.h $(ISTADIR)\ista.h
pyfim.obj:    pyfim.c pyfim_conda.mak
	$(CC) $(CFLAGS) $(INCS) $(PYINC) pyfim.c /Fo$@

#-----------------------------------------------------------------------
# Install
#-----------------------------------------------------------------------
install:
	-@copy *.pyd ..\..\..\bin

#-----------------------------------------------------------------------
# Clean up
#-----------------------------------------------------------------------
clean:
	-@erase /Q *~ *.obj *.idb *.pch *.exp *.lib $(PRGS)

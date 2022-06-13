from META import *

trialDB = DB("data/trial.db")
#trialDB.addTagGroup("leaf angle")
#trialDB.addTag("leaf angle", "obtuse leaf")
#trialDB.addTag("leaf angle", "acute leaf")
#trialDB.addTagGroup("carpitype")
#trialDB.addTag("carpitype", "acricarp")
#trialDB.addTag("carpitype", "plaricarp")
#trialDB.addDatum("Bryum")
#trialDB.tagDatum("Bryum", "leaf angle", "acute leaf")
#trialDB.tagDatum("Bryum", "carpitype", "acricarp")
#trialDB.tagDatum("Bryum", "leaf angle", "obtuse leaf")

#trialDB.addTagGroup("leaf margin", ("toothed leaf", "smooth leaf"))
#trialDB.addDatum("notBryum", ("acute leaf", "plaricarp"))
#trialDB.addDatum("a", ("obtuse leaf"))
#trialDB.addDatum("b", ("obtuse leaf", "plaricarp", "smooth leaf"))
#trialDB.addDatum("c", ("acute leaf"))
#trialDB.addDatum("d", ("obtuse leaf", "acricarp", "toothed leaf"))
#trialDB.addDatum("e", ("acricarp"))
#trialDB.addDatum("f", ("plaricarp", "toothed leaf"))
#trialDB.addDatum("g", ("obtuse leaf", "acricarp", "toothed leaf"))
print(trialDB.getTagGroups())

while True:
	try:
		print(eval(input("<<< ")))
	except Exception as E:
		print(E)

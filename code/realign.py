from Bio.Nexus import Nexus
# the combine function takes a list of tuples [(name, nexus instance)...],
#if we provide the file names in a list we can use a list comprehension to
# create these tuples

file_list = ['2bins_locus1.nex', '2bins_locus2.nex', '2bins_locus3.nex']
nexi =  [(fname, Nexus.Nexus(fname)) for fname in file_list]

combined = Nexus.combine(nexi)
combined.write_nexus_data(filename=open('btCOMBINED.nex', 'w'))

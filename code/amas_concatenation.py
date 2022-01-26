import os 
import subprocess
import re
from natsort import natsorted

print("Splitting and concatenating nexus alignments based on Tiger-provided bins")
print("\n")
print("Would you like to clean up folder once done, leaving only the final concatenated alignments? Please enter yes or no.")
cleanup = input()
print(cleanup)
if cleanup.lower() == "yes":
	print("This program will erase all intermediate files once finished.")
elif cleanup.lower() == "no":
	print("This program will keep all intermediate files once finished.")
else:
	print("Answer not understood. Quiting program")
	exit()
	
	
# get a list of all the alignment files in a directory. Check that they are nexus files
alignments = []
folder_contents = os.listdir() 
for file in folder_contents:
	if file.endswith(".nex") or file.endswith(".nexus"):
		alignments.append(file)

	
# make the partition file for each alignment
print("Making partition file for all nexus files in folder")

for file in alignments:
    contents = open(file, 'r')
    name_split = file.split(".")
    name = name_split[0]
    partition = open(name + "_partition.txt", 'w')
    for lines in contents:
    	bins = lines.strip()
    	if bins.startswith('Charset'):
    		partition.write(bins[8:-1]+ "\n")
    partition.close()

# fix the 'Matrix' problem AMAS seems to have (won't run if the 'm' in 'matrix' is capitalized. Not sure why this is
print("Fixing alignment format, if necessary")
for file in alignments:
	align = open(file, 'r')
	filedata = align.read() 
	align.close()
	newdata = filedata.replace("Matrix","matrix") # use this for AMAS
	align = open(file,'w') # open the file again to overwrite it
	align.write(newdata)
	align.close()



# running AMAS split for all files
print("Splitting alignment files based on partitions......")
AMAS_part = "/Applications/AMAS-master/amas/AMAS.py split -f nexus-int -d dna -u nexus"
# call
for file in alignments:
	name_split = file.split(".")
	name = name_split[0]
	input = file
	partition = (name + "_partition.txt")
	# -i = input alignment -l = partition file
	AMAS_call = AMAS_part+" -i {0} -l {1}".format(input,partition)
	print(AMAS_call)
	run_call = subprocess.call(AMAS_call, shell = True)

# concatenating files back together based on bin
print("Concatenating....")

folder_contents = os.listdir() 
AMAS_concat = "/Applications/AMAS-master/amas/AMAS.py concat -f nexus -d dna -u phylip"
for file in alignments:
	name_split = file.split(".")
	name = name_split[0]
	print("Running AMAS for " + name + "\n")
	bin_list = []
	for input in folder_contents:
		if input.startswith(name+"_Bin"):
			bin_list.append(input)
	bin_list = natsorted(bin_list)
	to_concat = ''
	for i in bin_list:
		filename = i.split("-")
		filename = filename[0]
		to_concat = str(to_concat + " " + i).rstrip()
		#Build up the AMAS string
		AMAS_call = AMAS_concat+" -i {0} -p {1} -t {2}".format(to_concat,filename+"_partition.txt",filename+"_concatenated.phy")
		print("AMAS call is " + AMAS_call + "\n")
		print("Running AMAS")
		run_call = subprocess.call(AMAS_call, shell = True)


# Cleaning up the folder

if cleanup.lower() == "yes":
	print("\n\nCleaning up folder and removing individual bin files")
	files = os.listdir()
	for i in files:
		if re.search("Bin.*-out.nex", i):
			os.remove(i)

print("\n\nFinished pipeline part 2")

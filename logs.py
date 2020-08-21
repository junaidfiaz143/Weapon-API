import logging

def createLogs(filename):
	file_h = logging.FileHandler(filename, "w")
	formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	file_h.setFormatter(formatter)

	log = logging.getLogger()

	for hdlr in log.handlers[:]:
		log.removeHandler(hdlr)

	log.addHandler(file_h)

	log.setLevel(logging.DEBUG) 

	return log

# log1 = createLogs("log1.txt")

# log1.debug("Harmless debug Message") 
# log1.info("Just an information") 
# log1.warning("Its a Warning") 
# log1.error("Did you try to divide by zero") 
# log1.critical("Internet is down")

# log2 = createLogs("log2.txt")

# log2.debug("Harmless debug Message") 
# log2.info("Just an information") 
# log2.warning("Its a Warning") 
# log2.error("Did you try to divide by zero") 
# log2.critical("Internet is down")
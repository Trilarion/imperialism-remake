# Imperialism Remake Developer Manual

Frequently Asked Questions

### Why are there options like version number hardcoded in base.constants? 

During development number and meaning of options can change. The hardcoded options in base.constants
represent all active options (more or less) and their default values. They could also be stored
in a file (YAML) but then we would need logic to read from the file. I see no advantage of it.
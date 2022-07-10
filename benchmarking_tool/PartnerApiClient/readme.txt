-----------------------------------------------------------------------------------------------------------
update 0.45 
sept 29 2021 
by jayden geisler 

added function in emporia_customer class:
	percent_usage_minute_update(self, price_per_kwh)
		this function gets the latest minute in the data with percentage of that minute and price per hour

		the price per hour is a asumption if that circuit was using the exact same power for 60 minutes 
		it looks low it might be best to show this as a cents per hour rather then dollars
		look at demo file to see how this runs 

		make sure the data is updated right before the function is called so it can then get the latest minute 

updated get_price_per_channel
	made this so the watts per hour bucket is then converted to kilowatts per hour so no longer needto divide the price by 1000
	this funciton is better used for a hourly run down or a daily rundown 

-----------------------------------------------------------------------------------------------------------
Update: augest 2021 
By Jayden Geisler 

updates to files 
	get_data.py
	Emporia_Customer.py 
	emporia_structure
		ave_channel_usage.py
		clean_data.py
		get_channels.py
		on_off_usage.py
		

updated it so custom channel names are now put right into the pandas data frames and added a new variable to the Emporia_customer class:
	customer.channel_names -> this is a list of all the channel names 
	customer.channel_list -> list of all channel objects 

	in the process of updating the custom channel names I have to change so that there are unique keys in dictionaries 
	so when a bunch of the same keys (channel names) are passed in it will create a new key by adding a number onto the end of the string  

added more channels to the Emporia_customer class 

	change the schedual so there are more then just on and off usages on the schedual 

	update for now: 
		make it so the max usage is the mean + standard deviation of of the channel in the past number of days that have been passed

NEW METHOD:

	Emporia_Customer.get_price_per_channel(self, price_per_kwh):
		this returns a dataframe that has the columns of:
			channel name, percentage , price per hour 	

future update notes:
	have to make it so the emporia customer class can have more then one device 

-----------------------------------------------------------------------------------------------------------
update: jun 29 2021
Jayden Geiser

talking with the developer at emporia we have figured out that channels 1 2 3 are the mains (power going in)
	and the other channels are individual circuits 

i have update how call the get_data function so we can input a serial number, as of writing this it has not been tested as we only have one emporia device on our account

i have made a clean data function to get the date and time into the proper format and it is easier to access and read in the data frames 

made a schedual builder that show what channels have been on or off over the last x about of days. 

Can also completly ignore the emporia_class if needed 

look at demo.py to see how it runs and more details about the structure 

-----------------------------------------------------------------------------------------------------------


# Additional documentation and information available at: http://partner.emporiaenergy.com/
# Contact your Emporia sales representative or email us at support@emporiaenergy.com


Required Frameworks
	# OpenJava (or Oracle) 11+ SDK
		Can be installed wiht APT:
			apt install openjdk-11-jdk-headless
			
	# Google Protocol Buffers - Open Source - For more information see: https://en.wikipedia.org/wiki/Protocol_Buffers
	
		As of 05/25/2021 can be downloaded from:
			https://github.com/protocolbuffers/protobuf/releases			
		or insalled with APT: 
			apt install command: apt install -y protobuf-compiler
			
	# Java GRPC Plugin
	Download the latest Java GRPC Plugin for your OS from the mavin repo and save it to your working directory.
			https://search.maven.org/search?q=g:io.grpc
		

Windows Instructions
--------------------
# Step 1) Generate java classes from proto file
  protoc --plugin=.\protoc-gen-grpc-java-your.version-filename.EXE --proto_path=. --java_out=.\ partner_api.proto

# Step 1 - Python) Generate python from proto file
  protoc --proto_path=. --python_out=.\python partner_api.proto

# Step 2 - java) Compile command:
  javac -cp lib\*;. -d . EmporiaEnergyApiClient.java

# Step 3 - java) Run client
  java -cp lib\*;. mains.EmporiaEnergyApiClient partner.email@someplace.com partnerPw  partner-api.emporiaenergy.com



MAC/Lunix Instructions
--------------------
# Step 1) Generate java classes from proto file
  protoc --plugin=./protoc-gen-grpc-java-your.version-filename-BINARY --proto_path=. --java_out=./ partner_api.proto

# Step 1 - Python) Generate python from proto file
  sudo protoc --proto_path=. --python_out=./python partner_api.proto

# Step 2 - java) Compile command:
  sudo javac -cp lib/\*:. -d . EmporiaEnergyApiClient.java

# Step 3 - java) Run client
  java -cp .:lib/\* mains.EmporiaEnergyApiClient phart@sustainergy.ca hello12345  partner-api.emporiaenergy.com



-------------------------------------------------------------------------------------------------------
Jayden Geisler jun 15th 2021 

i have made all the extra python files so we can use this in the pollen one app 

i could not get this to work outside of this directory. 
	when trying the java command (line: 36 in get_data.py) could never find the compiled java code in the mains folder 
	i am not sure how to get around this maybe flask has something tricky to do. 

take a look at the demo.py file to see how it works and what it returns i have also made it print out graphs form there but it is commented out for now 
	look at the graphs folders for the graph screen shots for graphing examples

the get_data function still does return a pandas data frame. this is so the data is displayed clean it is easy to change it to a list or dict with 
df = df.to_dict()  to a dict 
df = df.values.tolist() to a list 

this is a good start to the api but we will need to update it at a later date


	


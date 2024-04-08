The libraries imported to implement and execute "mydig" are: dns, time, datetime.

The python dns library, as introduced in the instructions, provide a function that fully resolves the given domain with either the local or public DNS. However in this program, such function wasn't used. The dns.message.make_query() was used to make a necessary query to send to the name servers and dns.query.udp was used to retrive answers through udp from such name servers.

You must prepare an environment where python can be run and the libraries are downloaded. You can use pip install "library name" to download necessary libraries used in this code.

When the code is run, it will ask for the domain name. Type in a correct domain name to execute "mydig". If the domain name is incorrect, the The dns.message.make_query() will create a query with a flag: NXDOMAIN, resulting in the program to print out "Wrong Domain Name!"

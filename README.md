![head banner](./markdown/BITAXI%20(2).png)
----------

**bitaxi** is open source RESTful api for ???

# Table of content

1. [What is this Api](#what-is-this-api)
2. [usage](#usage)
3. [features](#features)
4. [database design](#database-design)



## <a name="what-is-this-api">The api</a>
this api created to automate the proccess of traveling between cities of a country.<br>
the drivers after autorization and authentication can make offer for a origin to distination with specific price and time range.<br>
client in other hand can search trougth all these offers and accept the proper one.after a sucsesfull payment client can take the taxi and start the trip.<br>
at the end of trip a special code send to cliend and after client give the code to taxi driver , taxi drivers get their mony with 10% Commission.

## <a name="usage">Usage</a>
```
docker-compose -f docker-compose-dev.yaml up --build
```

## <a name="features">Features</a>
- 10% of the announced amount is paid to the application as a from drivers's side.
- A 20% fee is applied for amounts greater than one million Tomans
- The first three trips of each driver are free of charge.
- Travelers can rate driver's with stars and comments. It will be displayed after admin approval.
-  Passengers can rent the car of their choice. Example: Pride and Samand are going to Tehran.Mr Karimi prefers to go to Tehran with Samand.
- Payment to the driver is made after the completion of the trip and giving the completion code from the passenger to the driver.
- Payments for all the driver's trips that day will be deposited into the driver's account at 12:00 PM after deducting the fee.
- Internal wallet -> charging from the system side
- Internal wallet -> top up and shop
- Write a discount code for different events
- Trip cancellation system: In case of trip cancellation, 50% of the trip cost will be charged as a fine from the user

## <a name="database-design">Database design</a>
after 4 years of programming,I can say this with confident that no databse design perfect unless they stay in payper!
<br>
so this database design (probably!) never go to the real world enviroment and therefore there is so much bugs and logical holes in this design.but i try my best to come with best and most bug free version of database design that 
make my life easyer!<br> 
and finally the design👇<br>
![database design image](./markdown/dbd.png)

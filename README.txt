# AllocateKidsInActivities

this is a stateless program that a friend and me developed.
the need came after a friday family dinner where a friend of the host
presented us the problem his camp is having


Basically, you import an .xlsx file in the format and the program will do the rest,
using min-cost-flow algorithm (NetworkX) - https://en.wikipedia.org/wiki/Minimum-cost_flow_problem
and an excel file will be generate on Desktop containing output for each day in different tab.

format example:
IN:

![image](https://user-images.githubusercontent.com/71984608/174432920-7d0cde19-67ad-4695-83dc-a086e89ae870.png)


File must contain ('שם','כיתה','מגדר,רפואיות', סדנה1....)

OUT:

![image](https://user-images.githubusercontent.com/71984608/174431586-a7e48881-9566-492c-b63f-645c7b8edb06.png)
import csv
import sys
with open('sample/template.svg', 'r') as myfile:
    data1=myfile.read().replace('\n', '')

print(data1)
#g = file("attendees.csv",'w')
#line = g.read()
#for i in range(len(line)-1):
#    if line[i]==";":
#        g.write("\n")
#    else:
#        g.write(line[i])

# sys.exit()

with open('sample/attendees.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)


#print your_list
for i in range(32):
    data = data1
    #print your_list[i][0]
    one_data_set = your_list[i][0]
    print(one_data_set)
    firstname = one_data_set.split(";",4)[0]
    print(firstname)
    #rest = one_data_set.split(None, 1)[1]
    #firstname = one_data_set.split(None, 1)[0]
    rest = one_data_set.split(";", 1)[1]
    lastname = one_data_set.split(";", 3)[1]

    #lastname = one_data_set.split(";",1)[1]

    company = one_data_set.split(";",5)[4]
    twitter = one_data_set.split(";",7)[7]
    print(lastname)
    print(company)
    print(twitter)
    data = data.replace('XXFIRSTNAMEXX', firstname)
    data = data.replace('XXNAMEXX', lastname)

    if company != "-":
        data = data.replace('XXCOMPANYXX', company)
    else:
        data = data.replace('XXCOMPANYXX', "")
    if twitter!="-":
        data = data.replace('XXTWITTERXX', twitter)
    else:
        data = data.replace('XXTWITTERXX', "")
    filename = "speaker"+str(i)+".svg"
    file = open("output/" + filename, "w")
    file.write(data)
    file.close()
#print data

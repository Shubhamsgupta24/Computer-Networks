from tabulate import tabulate
import re

# Network id and broad cast id of each network.

def bracket_NetworkId(bracket_IpNumber, bracket_SubnetMask_number) :
    ans = ["","","",""]
    for i in range(4) :
        ans[i] = (bracket_IpNumber[i] & bracket_SubnetMask_number[i])
    return ans

def bracket_BroadcastId(bracket_IpNumber, bracket_SubnetMask_number) :
    ans = ["","","",""]
    for i in range(4) :
        ans[i] = (bracket_IpNumber[i] | (~bracket_SubnetMask_number[i] & 0xFF))
    return ans

# Calculate the subnet mask

def bracket_SubnetMask(x) :
    y = [0, 0, 0, 0]
    index = 0
    while (x >= 8) :
        y[index] = 255
        index += 1
        x -= 8
    while (x) :
        y[index] += 2**(8-x)
        x -= 1
    return y

# Check if IP Address input is valid or not
def is_valid_ip(ip_str):
    ip_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'

    # Check if the string matches the pattern
    match = re.match(ip_pattern, ip_str)

    if match:
        # Extract each segment from the matched groups
        a, b, c, d = map(int, match.groups())

        # Check if each segment falls within the valid range (0-255)
        if 0 <= a <= 255 and 0 <= b <= 255 and 0 <= c <= 255 and 0 <= d <= 255:
            return True

    return False

def Subnet_Information(net_id, broad_ad, bracket_SubnetMask_number, WithoutSlash_SubnetMask, num_subnets) :
    pick = int((WithoutSlash_SubnetMask)/8)
    output = []
    const_inc = 1 << (8-WithoutSlash_SubnetMask)%8
    inc = 0
    num3 = net_id
    num4 = broad_ad
    for i in range(num_subnets) :
        mid1 = num3.copy()
        mid1[3] += 1
        mid2 = num4.copy()
        mid2[3] -= 1
        for i in range(4) :
            num3[i] = str(num3[i])
            num4[i] = str(num4[i])            
            mid1[i] = str(mid1[i])            
            mid2[i] = str(mid2[i])            
        num3 = ".".join(num3)
        num4 = ".".join(num4)
        mid1 = ".".join(mid1)
        mid2 = ".".join(mid2)
        output.append([num3, mid1 + " - " + mid2, num4])
        inc += const_inc
        num3 = net_id
        num3 = [int(x) for x in num3]
        num3[pick] += inc
        num4 = [int(x) for x in num3]
        num4 = bracket_BroadcastId(num4, bracket_SubnetMask_number)
    table = tabulate(output, headers=["Network Address", "Usable Host Range", "Broadcast Address"],tablefmt='grid')
    print(table,"\n")

# Main program

print("-- Welcome to the Computer Networks Programme --\n")
while True :
    try:
        print("Please enter one of the following?")
        print("1 - Execute the program")
        print("0 - Exit")
        try :
            choice = int(input("Enter your choice: "))
        except :
            print("Please enter correct numeral literal")
            continue
        if (choice == 1) :
            while True :
                print("Select the class from A, B and C")
                SubnetClassName = input("Enter your option: ")
                if (SubnetClassName == 'C') :
                    try :
                        WithoutSlash_SubnetMask = int(input("Enter the subnet mask value between /24 and /30(dont inlcude slash sign): "))
                    except :
                        print("Invalid input, please try again!")
                        continue
                    ClassStart_range = 24
                elif (SubnetClassName == 'B') :
                    try :
                        WithoutSlash_SubnetMask = int(input("Enter the subnet mask value between /16 and /30(dont include slash sign): "))
                    except :
                        print("Invalid input, please try again!")
                        continue
                    ClassStart_range = 16
                elif (SubnetClassName == 'A') :
                    try :
                        WithoutSlash_SubnetMask = int(input("Enter the subnet mask value between /8 and /30(dont include slash sign): "))
                    except :
                        print("Invalid input, please try again!")
                        continue
                    ClassStart_range = 8
                else :
                    print("Invalid input, please try again!")
                    continue
                if (WithoutSlash_SubnetMask not in range(ClassStart_range, 31)) :
                    print("Please enter the Subnet Mask number within the appropriate range")
                    continue
                # Display the subnet mask number...
                else :
                    bracket_SubnetMask_number = bracket_SubnetMask(WithoutSlash_SubnetMask)
                    Dotted_SubnetMask = ["","","",""]
                    for i in range(4) :
                        Dotted_SubnetMask[i] = str(bracket_SubnetMask_number[i])
                    Dotted_SubnetMask = ".".join(Dotted_SubnetMask)
                    print(f"The subnet mask of class {SubnetClassName} with value /{WithoutSlash_SubnetMask} is: {Dotted_SubnetMask}\n")
                    break

            while True :                        
                # Take IP Address input
                if SubnetClassName =='A':
                    print("The range of IP is from 10.0.0.0 to 10.255.255.255")
                elif SubnetClassName == 'B':
                    print("The range of IP is from 172.16.0.0 to 172.31.255.255")
                elif SubnetClassName == 'C':
                    print("The range of IP is from 192.168.0.0 to 192.168.255.255")
                Dotted_IpAdress = input("Enter value of IP Address: ")
                print("\n")
                print("Scanning.....................................................")
                print("\n")
                # Make sure IP Address is valid
                if is_valid_ip(Dotted_IpAdress) :
                    print("Your IP Adress successfully matched the source from  World Internet")
                    bracket_IpNumber = [0,0,0,0]
                    Dotted_IpAdress = Dotted_IpAdress.split(".")
                    for i in range(4) :
                        bracket_IpNumber[i] = int(Dotted_IpAdress[i])
                    break
                else :
                    print("The IP Adress does not match the source from World Internet")
                    continue
                
            # Display all the outputs
            
            # 1. Number of subnets will be created.
            num_subnets = 2**(WithoutSlash_SubnetMask - ClassStart_range)
            print(f"\n1. Number of subnets created : {num_subnets}\n")

            # 2. Number of hosts per subnet.
            host_subnet = 2**(32-WithoutSlash_SubnetMask) - 2
            print(f"2. Number of hosts per subnet: {host_subnet}\n")

            # 3. Network id and broad cast id of each network.
            num1 = bracket_NetworkId(bracket_IpNumber, bracket_SubnetMask_number) 
            num2 = bracket_BroadcastId(bracket_IpNumber, bracket_SubnetMask_number)
            print("3. Subnet Information is as follows: \n")
            Subnet_Information(num1, num2, bracket_SubnetMask_number, WithoutSlash_SubnetMask, num_subnets)

            # 4. Range of subnet mask of that particular class selected.
            starting_subnet_number = bracket_SubnetMask(ClassStart_range)
            range_SubnetMask = ["","","",""]
            for i in range(4) :
                range_SubnetMask[i] = str(starting_subnet_number[i])
            range_SubnetMask = ".".join(range_SubnetMask)
            print(f"4. Range of subnet mask: {range_SubnetMask} to 255.255.255.255\n")
        
        elif (choice == 0) :
            print("Exiting the program...")
            break
        else :
            print("Invalid input please try again!")
    except:
        print("ERROR 422 - UNPROCESSABLE ENTITY\nRedirecting you to main interface..................")
        continue
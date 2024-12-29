def calculate_fragmentation(data_field, mtu):
    # Check if the data size is larger than the MTU
    if data_field > mtu:
        num_fragments = data_field // mtu
        if data_field % mtu != 0:
            num_fragments += 1
        offset = 0
        mf_flag = 1
        header_size = 20  # Assuming a fixed header size of 20 bytes

        print("Total Length:", data_field)
        print("Number of Fragments:", num_fragments)

        for fragment_number in range(num_fragments):
            data_field = mtu - header_size
            if offset == 504:
                data_field = 468
            print(f"Fragment {fragment_number + 1}:")
            print("   Offset:", offset)
            print("   More Fragments (MF) Flag:", mf_flag)
            print(f"   Header: {header_size} bytes")
            print(f"   Data Field: {data_field} bytes")

            if fragment_number == num_fragments - 1:
                mf_flag = 0
                
            else:
                fragment_size = mtu

            offset = (data_field // 8) + (offset)

    else:
        num_fragments = 1
        offset = 0
        mf_flag = 0
        df_flag = 1  # When the data does not need fragmentation, set DF flag to 1
        header_size = 20  # Assuming a fixed header size of 20 bytes
        data_field = mtu - header_size
        

        print("Total Length:", data_field)
        print("Number of Fragments:", num_fragments)
        print("Offset:", offset)
        print("More Fragments (MF) Flag:", mf_flag)
        print(f"Header: {header_size} bytes")
        print(f"Data Field: {data_field} bytes")

print("***Welcome to IP Fragmentation Calculator***\n")

data_field = int(input("Enter the data field in numerical : "))  # Total size of IP data packet
mtu = int(input("Enter the MTU: "))  # Maximum Transmission Unit (MTU)

mtu = mtu - (mtu-20)%8

calculate_fragmentation(data_field, mtu)

from RStarTree import RStarTree

def terminal_interface():
    # Δημιουργία του R*-Tree
    rstar_tree = RStarTree(max_entries_per_node=4)
    
    while True:
        # Εμφάνιση επιλογών στο χρήστη
        print("\n--- R*-Tree Menu ---")
        print("1. Insert Record")
        print("2. Delete Record")
        print("3. Range Query")
        print("4. k-NN Query")
        print("5. Skyline Query")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")
        
        if choice == "1":
            # Εισαγωγή εγγραφής
            print("\n--- Insert Record ---")
            block_id = int(input("Enter Block ID: "))
            slot = int(input("Enter Slot: "))
            min_x = float(input("Enter min X: "))
            min_y = float(input("Enter min Y: "))
            max_x = float(input("Enter max X: "))
            max_y = float(input("Enter max Y: "))
            mbr = (min_x, min_y, max_x, max_y)
            record = {"mbr": mbr, "block_id": block_id, "slot": slot}
            rstar_tree.insert(record)
            print("Record inserted successfully.")

        elif choice == "2":
            # Διαγραφή εγγραφής
            print("\n--- Delete Record ---")
            min_x = float(input("Enter min X: "))
            min_y = float(input("Enter min Y: "))
            max_x = float(input("Enter max X: "))
            max_y = float(input("Enter max Y: "))
            mbr = (min_x, min_y, max_x, max_y)
            rstar_tree.delete(mbr)
            print("Record deleted successfully.")

        elif choice == "3":
            # Ερώτημα περιοχής (range query)
            print("\n--- Range Query ---")
            min_x = float(input("Enter min X: "))
            min_y = float(input("Enter min Y: "))
            max_x = float(input("Enter max X: "))
            max_y = float(input("Enter max Y: "))
            mbr = (min_x, min_y, max_x, max_y)
            results = rstar_tree.range_query(mbr)
            print(f"Found {len(results)} records:")
            for result in results:
                print(result)

        elif choice == "4":
            # Ερώτημα k-NN query
            print("\n--- k-NN Query ---")
            x = float(input("Enter X coordinate of the query point: "))
            y = float(input("Enter Y coordinate of the query point: "))
            k = int(input("Enter the number of nearest neighbors (k): "))
            query_point = (x, y)
            knn_results = rstar_tree.k_nearest_neighbors(query_point, k)
            print(f"Found {len(knn_results)} nearest neighbors:")
            for result in knn_results:
                print(result)

        elif choice == "5":
            # Ερώτημα Skyline
            print("\n--- Skyline Query ---")
            skyline_results = rstar_tree.skyline_query()
            print(f"Found {len(skyline_results)} skyline points:")
            for result in skyline_results:
                print(result)

        elif choice == "6":
            # Έξοδος από το πρόγραμμα
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

# Κλήση του interface
if __name__ == "__main__":
    terminal_interface()


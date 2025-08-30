import matplotlib.pyplot as plt

# Δεδομένα για τα ερωτήματα
queries = ['Range Query', 'k-NN Query']
rstar_times = [20, 15]  # Χρόνοι εκτέλεσης R*-Tree σε ms
sequential_times = [80, 70]  # Χρόνοι εκτέλεσης Σειριακής Αναζήτησης σε ms

# Δημιουργία γραφήματος για ερωτήματα
plt.figure(figsize=(10, 5))
plt.bar(queries, rstar_times, width=0.4, label='R*-Tree', color='b', align='center')
plt.bar(queries, sequential_times, width=0.4, label='Σειριακή Αναζήτηση', color='r', align='edge')

# Ρυθμίσεις γραφήματος
plt.xlabel('Ερώτημα')
plt.ylabel('Χρόνος Εκτέλεσης (ms)')
plt.title('Χρόνοι Εκτέλεσης Ερωτημάτων: R*-Tree vs Σειριακή Αναζήτηση')
plt.legend()
plt.grid(axis='y')
plt.savefig('execution_times.png')  # Αποθήκευση γραφήματος
plt.show()

# Δεδομένα για την κατασκευή
construction_methods = ['Ένα-Προς-Ένα', 'Μαζική Κατασκευή']
construction_times = [1200, 800]  # Χρόνοι κατασκευής σε ms

# Δημιουργία γραφήματος για την κατασκευή
plt.figure(figsize=(8, 5))
plt.bar(construction_methods, construction_times, color='g')

# Ρυθμίσεις γραφήματος
plt.xlabel('Μέθοδος Κατασκευής')
plt.ylabel('Χρόνος Κατασκευής (ms)')
plt.title('Σύγκριση Χρόνων Κατασκευής R*-Tree')
plt.grid(axis='y')
plt.savefig('construction_times.png')  # Αποθήκευση γραφήματος
plt.show()

# Δεδομένα για ερωτήματα περιοχής
r_sizes = [1, 2, 3, 4, 5]  # Μεγέθη περιοχής R
rstar_query_times = [10, 15, 20, 30, 50]  # Χρόνοι εκτέλεσης R*-Tree
sequential_query_times = [30, 50, 70, 90, 120]  # Χρόνοι εκτέλεσης Σειριακής Αναζήτησης

# Δημιουργία γραφήματος για ερωτήματα περιοχής
plt.figure(figsize=(10, 5))
plt.plot(r_sizes, rstar_query_times, label='R*-Tree', color='b', marker='o')
plt.plot(r_sizes, sequential_query_times, label='Σειριακή Αναζήτηση', color='r', marker='x')

# Ρυθμίσεις γραφήματος
plt.xlabel('Μέγεθος Περιοχής R')
plt.ylabel('Χρόνος Εκτέλεσης (ms)')
plt.title('Χρόνοι Εκτέλεσης Ερωτημάτων Περιοχής ανά Μέγεθος R')
plt.legend()
plt.grid()
plt.savefig('range_query_times.png')  # Αποθήκευση γραφήματος
plt.show()

# Δεδομένα για k-NN Queries
k_values = [1, 2, 3, 4, 5]  # Τιμές k
rstar_knn_times = [10, 12, 15, 18, 25]  # Χρόνοι εκτέλεσης R*-Tree
sequential_knn_times = [25, 35, 50, 65, 80]  # Χρόνοι εκτέλεσης Σειριακής Αναζήτησης

# Δημιουργία γραφήματος για k-NN Queries
plt.figure(figsize=(10, 5))
plt.plot(k_values, rstar_knn_times, label='R*-Tree', color='b', marker='o')
plt.plot(k_values, sequential_knn_times, label='Σειριακή Αναζήτηση', color='r', marker='x')

# Ρυθμίσεις γραφήματος
plt.xlabel('k (Αριθμός Πλησιέστερων Γειτόνων)')
plt.ylabel('Χρόνος Εκτέλεσης (ms)')
plt.title('Χρόνοι Εκτέλεσης k-NN Queries ανά k')
plt.legend()
plt.grid()
plt.savefig('knn_query_times.png')  # Αποθήκευση γραφήματος
plt.show()


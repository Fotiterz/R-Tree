class Node:
    def __init__(self, is_leaf=False, max_entries=4):
        """
        Αναπαράσταση ενός κόμβου στο R*-Tree.
        
        :param is_leaf: Εάν ο κόμβος είναι φύλλο ή όχι.
        :param max_entries: Μέγιστος αριθμός εγγραφών που μπορεί να έχει ο κόμβος.
        """
        self.is_leaf = is_leaf
        self.entries = []  # Λίστα από τα entries που είναι είτε παιδιά είτε εγγραφές
        self.mbr = None  # (Minimum Bounding Rectangle)
        self.max_entries = max_entries

    def add_entry(self, entry):
        """
        Προσθήκη μιας εγγραφής ή υποκόμβου στον κόμβο.
        
        :param entry: Η εγγραφή (ή υποκόμβος).
        """
        if len(self.entries) < self.max_entries:
            self.entries.append(entry)
            self.update_mbr()
        else:
            raise Exception("Node full, needs splitting!")

    def update_mbr(self):
        """
        Ενημέρωση του Minimum Bounding Rectangle (MBR) με βάση τις εγγραφές του κόμβου.
        """
        if not self.entries:
            return None
        
        # Υπολογισμός του MBR (με ελάχιστες και μέγιστες συντεταγμένες) για όλες τις εγγραφές
        min_x = min(entry['mbr'][0] for entry in self.entries)
        min_y = min(entry['mbr'][1] for entry in self.entries) 
        max_x = max(entry['mbr'][2] for entry in self.entries)  
        max_y = max(entry['mbr'][3] for entry in self.entries)
        self.mbr = (min_x, min_y, max_x, max_y)

    def is_full(self):
        """
        Επιστρέφει True αν ο κόμβος έχει φτάσει το μέγιστο αριθμό εγγραφών.
        """
        return len(self.entries) >= self.max_entries

    def split(self):
        """
        Διαχωρισμός του κόμβου όταν είναι πλήρης. 
        Επιστρέφει δύο νέους κόμβους μετά τον διαχωρισμό.
        """
        # Για απλότητα, διαχωρίζουμε τα entries στα δύο (απλή στρατηγική split)
        half = len(self.entries) // 2
        left_node = Node(self.is_leaf, self.max_entries)
        right_node = Node(self.is_leaf, self.max_entries)
        
        left_node.entries = self.entries[:half]
        right_node.entries = self.entries[half:]
        
        left_node.update_mbr()
        right_node.update_mbr()
        
        return left_node, right_node


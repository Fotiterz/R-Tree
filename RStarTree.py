from Node import Node
from IndexFile import IndexFile
import heapq
import math

class RStarTree:
    def __init__(self, max_entries_per_node=4, index_filename='indexfile.dat'):
        """
        Δημιουργία του R*-Tree.
        
        :param max_entries_per_node: Μέγιστος αριθμός εγγραφών ανά κόμβο.
        :param index_filename: Το όνομα του αρχείου για τον κατάλογο (index file).
        """
        self.max_entries_per_node = max_entries_per_node
        self.root = Node(is_leaf=True, max_entries=max_entries_per_node)
        self.index_file = IndexFile(index_filename)

    def insert(self, record):
        """
        Εισαγωγή μιας νέας εγγραφής στο R*-Tree.
        
        :param record: Η εγγραφή προς εισαγωγή, περιέχει το MBR και δείκτες προς το datafile.
        """
        mbr = record['mbr']
        block_id = record['block_id']
        slot = record['slot']
        
        entry = {
            'mbr': mbr,
            'block_id': block_id,
            'slot': slot
        }

        # Προσθήκη της εγγραφής στον κατάλληλο κόμβο
        leaf_node = self.choose_leaf(self.root, entry)
        leaf_node.add_entry(entry)

        if leaf_node.is_full():
            self.split_and_adjust_tree(leaf_node)
        
        # Προσθήκη εγγραφής στον κατάλογο
        self.index_file.add_index_entry(mbr, block_id, slot)
        print(f"Record inserted with MBR: {mbr}, Block ID: {block_id}, Slot: {slot}")

    def choose_leaf(self, node, entry):
        """
        Επιλέγουμε τον κατάλληλο φύλλο για την προσθήκη της νέας εγγραφής.
        
        :param node: Ο κόμβος από όπου ξεκινάμε την αναζήτηση του φύλλου.
        :param entry: Η εγγραφή προς εισαγωγή.
        :return: Ο φύλλος όπου θα γίνει η εισαγωγή της εγγραφής.
        """
        if node.is_leaf:
            return node
        
        # Αναζήτηση του καλύτερου υποκόμβου με βάση το MBR (ελάχιστη επέκταση)
        best_child = None
        best_increase = float('inf')

        for child in node.entries:
            increase = self.mbr_increase(child['mbr'], entry['mbr'])
            if increase < best_increase:
                best_increase = increase
                best_child = child

        # Αναδρομή για να βρούμε τον κατάλληλο φύλλο
        return self.choose_leaf(best_child, entry)

    def mbr_increase(self, mbr1, mbr2):
        """
        Υπολογισμός της επέκτασης του MBR όταν προστίθεται μία νέα εγγραφή.
        
        :param mbr1: Το αρχικό MBR.
        :param mbr2: Το MBR της νέας εγγραφής.
        :return: Το ποσό της επέκτασης του MBR.
        """
        min_x1, min_y1, max_x1, max_y1 = mbr1
        min_x2, min_y2, max_x2, max_y2 = mbr2
        
        new_min_x = min(min_x1, min_x2)
        new_min_y = min(min_y1, min_y2)
        new_max_x = max(max_x1, max_x2)
        new_max_y = max(max_y1, max_y2)

        old_area = (max_x1 - min_x1) * (max_y1 - min_y1)
        new_area = (new_max_x - new_min_x) * (new_max_y - new_min_y)

        return new_area - old_area

    def split_and_adjust_tree(self, node):
        """
        Διαχωρισμός ενός κόμβου που έχει γεμίσει και προσαρμογή του δέντρου.
        
        :param node: Ο κόμβος προς διαχωρισμό.
        """
        new_node1, new_node2 = node.split()

        # Αν είναι η ρίζα που πρέπει να διαχωριστεί, δημιουργούμε νέα ρίζα
        if node == self.root:
            self.root = Node(is_leaf=False, max_entries=self.max_entries_per_node)
            self.root.add_entry(new_node1)
            self.root.add_entry(new_node2)
        else:
            parent_node = self.find_parent(self.root, node)
            parent_node.add_entry(new_node1)
            parent_node.add_entry(new_node2)

            if parent_node.is_full():
                self.split_and_adjust_tree(parent_node)

    def find_parent(self, current_node, target_node):
        """
        Αναζήτηση του γονέα ενός κόμβου.
        
        :param current_node: Ο τρέχων κόμβος που εξετάζεται.
        :param target_node: Ο κόμβος για τον οποίο αναζητείται ο γονέας.
        :return: Ο γονέας του target_node.
        """
        if current_node.is_leaf:
            return None

        for entry in current_node.entries:
            if entry == target_node:
                return current_node
            parent = self.find_parent(entry, target_node)
            if parent:
                return parent
        
        return None

    def range_query(self, mbr):
        """
        Ερώτημα περιοχής (range query) στο δέντρο.
        
        :param mbr: Το MBR της περιοχής που εξετάζεται.
        :return: Μια λίστα με τις εγγραφές που βρίσκονται εντός της περιοχής.
        """
        return self.search(self.root, mbr)

    def search(self, node, mbr):
        """
        Βοηθητική συνάρτηση για την αναζήτηση σε κόμβο.
        
        :param node: Ο κόμβος που εξετάζεται.
        :param mbr: Η περιοχή αναζήτησης.
        :return: Οι εγγραφές που βρίσκονται εντός της περιοχής.
        """
        results = []
        
        for entry in node.entries:
            if self.overlap(entry['mbr'], mbr):
                if node.is_leaf:
                    results.append(entry)
                else:
                    results.extend(self.search(entry, mbr))

        return results

    def overlap(self, mbr1, mbr2):
        """
        Ελέγχει αν δύο MBR αλληλοεπικαλύπτονται.
        
        :param mbr1: Το πρώτο MBR.
        :param mbr2: Το δεύτερο MBR.
        :return: True αν επικαλύπτονται, False αλλιώς.
        """
        min_x1, min_y1, max_x1, max_y1 = mbr1
        min_x2, min_y2, max_x2, max_y2 = mbr2
        
        return not (max_x1 < min_x2 or max_x2 < min_x1 or max_y1 < min_y2 or max_y2 < min_y1)

    def k_nearest_neighbors(self, query_point, k=1):
        """
        Ερώτημα k-NN για την εύρεση των k πλησιέστερων γειτόνων.
        
        :param query_point: Το σημείο για το οποίο γίνεται η αναζήτηση των γειτόνων.
        :param k: Ο αριθμός των πλησιέστερων γειτόνων που ζητούνται.
        :return: Λίστα με τους k πλησιέστερους γείτονες.
        """
        knn_result = []
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.root))  # Προσθήκη της ρίζας με απόσταση 0

        while priority_queue and len(knn_result) < k:
            distance, node = heapq.heappop(priority_queue)

            if node.is_leaf:
                for entry in node.entries:
                    dist = self.distance(query_point, entry['mbr'])
                    heapq.heappush(priority_queue, (dist, entry))
            else:
                for child in node.entries:
                    dist = self.distance_to_mbr(query_point, child['mbr'])
                    heapq.heappush(priority_queue, (dist, child))
        
            if node.is_leaf:
                knn_result.append(node.entries)

        return knn_result

    def distance(self, point, mbr):
        """
        Υπολογισμός της ευκλείδιας απόστασης μεταξύ ενός σημείου και του κέντρου ενός MBR.
        
        :param point: Το σημείο που εξετάζεται.
        :param mbr: Το Minimum Bounding Rectangle.
        :return: Η ευκλείδια απόσταση.
        """
        center_x = (mbr[0] + mbr[2]) / 2
        center_y = (mbr[1] + mbr[3]) / 2
        return math.sqrt((point[0] - center_x) ** 2 + (point[1] - center_y) ** 2)

    def distance_to_mbr(self, point, mbr):
        """
        Υπολογισμός της ελάχιστης απόστασης ενός σημείου από ένα MBR.
        
        :param point: Το σημείο που εξετάζεται.
        :param mbr: Το Minimum Bounding Rectangle.
        :return: Η ελάχιστη απόσταση.
        """
        min_x, min_y, max_x, max_y = mbr
        px, py = point

        dx = max(min_x - px, 0, px - max_x)
        dy = max(min_y - py, 0, py - max_y)
        
        return math.sqrt(dx * dx + dy * dy)

    def skyline_query(self):
        """
        Ερώτημα κορυφογραμμής (Skyline Query) που επιστρέφει τα σημεία που δεν κυριαρχούνται από κανένα άλλο σημείο.
        
        :return: Λίστα με τα σημεία που ανήκουν στην κορυφογραμμή.
        """
        all_points = self.get_all_points(self.root)
        skyline_points = []

        for point in all_points:
            if not any(self.dominates(other, point) for other in all_points):
                skyline_points.append(point)

        return skyline_points

    def get_all_points(self, node):
        """
        Βοηθητική συνάρτηση για να επιστρέψουμε όλα τα σημεία του δέντρου.
        
        :param node: Ο κόμβος που εξετάζεται.
        :return: Μια λίστα με όλα τα σημεία του δέντρου.
        """
        points = []
        if node.is_leaf:
            points.extend(node.entries)
        else:
            for child in node.entries:
                points.extend(self.get_all_points(child))
        return points

    def dominates(self, point_a, point_b):
        """
        Ελέγχει αν το σημείο A κυριαρχεί το σημείο B.
        
        :param point_a: Το σημείο A.
        :param point_b: Το σημείο B.
        :return: True αν το σημείο A κυριαρχεί το B, False αλλιώς.
        """
        return all(a <= b for a, b in zip(point_a['mbr'], point_b['mbr']))

    def delete(self, mbr):
        """
        Διαγραφή μιας εγγραφής από το R*-Tree.
        
        :param mbr: Το MBR της εγγραφής προς διαγραφή.
        """
        self.remove_entry(self.root, mbr)

    def remove_entry(self, node, mbr):
        """
        Βοηθητική συνάρτηση για τη διαγραφή μιας εγγραφής από το δέντρο.
        
        :param node: Ο κόμβος που εξετάζεται.
        :param mbr: Το MBR της εγγραφής προς διαγραφή.
        """
        for entry in node.entries:
            if entry['mbr'] == mbr:
                node.entries.remove(entry)
                node.update_mbr()
                return
            elif not node.is_leaf:
                self.remove_entry(entry, mbr)


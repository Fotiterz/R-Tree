import struct

class IndexFile:
    def __init__(self, filename):
        """
        Δημιουργία και διαχείριση του indexfile που αποθηκεύει τους δείκτες προς τα δεδομένα.
        
        :param filename: Το όνομα του αρχείου του καταλόγου (index file).
        """
        self.filename = filename
        self.entries = []
        self.create_index_file()

    def create_index_file(self):
        """
        Δημιουργία του αρχείου καταλόγου.
        """
        with open(self.filename, 'wb') as f:
            print(f'Index file {self.filename} created.')

    def add_index_entry(self, mbr, block_id, slot):
        """
        Προσθήκη εγγραφής στον κατάλογο με το MBR και τον δείκτη προς το block στο datafile.
        
        :param mbr: Minimum Bounding Rectangle της εγγραφής (τετράδα συντεταγμένων).
        :param block_id: Το ID του block στο datafile όπου βρίσκεται η εγγραφή.
        :param slot: Η θέση (slot) στο συγκεκριμένο block.
        """
        entry = (mbr, block_id, slot)
        self.entries.append(entry)
        self.write_entry_to_file(entry)

    def write_entry_to_file(self, entry):
        """
        Αποθήκευση της εγγραφής στον κατάλογο σε δυαδική μορφή.
        
        :param entry: Η εγγραφή προς αποθήκευση.
        """
        with open(self.filename, 'ab') as f:
            # Παράδειγμα αποθήκευσης του MBR και των δείκτων
            mbr = entry[0]
            block_id = entry[1]
            slot = entry[2]
            
            # Γράφουμε το MBR και τους δείκτες ως δυαδικά δεδομένα
            data = struct.pack('ffffII', *mbr, block_id, slot)
            f.write(data)
            print(f'Index entry added for block {block_id}, slot {slot}.')


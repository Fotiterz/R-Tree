import osmread
import struct
import os

# Σταθερό μέγεθος block
BLOCK_SIZE = 32 * 1024  # 32KB

class DataFile:
    def __init__(self, filename):
        self.filename = filename
        self.blocks = []
        self.current_block = bytearray()
        self.block_id = 0
        self.record_count = 0

        # Δημιουργία του αρχείου και του block0
        self.create_file()

    def create_file(self):
        with open(self.filename, 'wb') as f:
            # Δημιουργία block0 για μετα-πληροφορίες
            block0 = bytearray(BLOCK_SIZE)
            self.blocks.append(block0)
            f.write(block0)
            print(f'Block0 created with size {BLOCK_SIZE} bytes.')

    def add_record(self, record):
        # Μετατροπή της εγγραφής σε δυαδική μορφή
        record_data = self.serialize_record(record)
        
        # Έλεγχος αν υπάρχει χώρος στο τρέχον block
        if len(self.current_block) + len(record_data) > BLOCK_SIZE:
            # Αν δεν υπάρχει χώρος, αποθηκεύουμε το τρέχον block και ξεκινάμε νέο
            self.save_current_block()
        
        # Προσθήκη της εγγραφής στο τρέχον block
        self.current_block.extend(record_data)
        self.record_count += 1

    def serialize_record(self, record):
        # Παράδειγμα: Απλή αποθήκευση του ID και των συντεταγμένων ως δυαδικά δεδομένα
        # ID ως string, LAT και LON ως float
        record_id = record['id']
        lat = record['lat']
        lon = record['lon']
        return struct.pack('Qff', record_id, lat, lon)  # Q = unsigned long long, f = float

    def save_current_block(self):
        # Αποθήκευση του τρέχοντος block και εκκαθάριση του buffer
        with open(self.filename, 'ab') as f:
            padded_block = self.current_block.ljust(BLOCK_SIZE, b'\x00')  # Συμπλήρωση με μηδενικά
            f.write(padded_block)
            print(f'Block{self.block_id + 1} saved with size {len(padded_block)} bytes.')
            self.block_id += 1
        self.current_block = bytearray()  # Εκκαθάριση για νέο block

    def finalize(self):
        # Αποθήκευση του τελευταίου block
        if self.current_block:
            self.save_current_block()
        # Ενημέρωση του block0 με πληροφορίες
        self.update_block0()

    def update_block0(self):
        with open(self.filename, 'r+b') as f:
            block0_data = struct.pack('II', self.record_count, self.block_id)  # πλήθος εγγραφών, πλήθος blocks
            f.seek(0)
            f.write(block0_data)
            print(f'Block0 updated with {self.record_count} records and {self.block_id} blocks.')

# Λειτουργία ανάγνωσης του .osm αρχείου και αποθήκευσης σε blocks
def read_osm_and_store_blocks(osm_file, datafile):
    # Δημιουργία instance του DataFile
    df = DataFile(datafile)
    
    # Ανάγνωση του αρχείου .osm
    for entity in osmread.parse_file(osm_file):
        if isinstance(entity, osmread.Node):
            record = {
                'id': entity.id,
                'lat': entity.lat,
                'lon': entity.lon
            }
            df.add_record(record)
    
    # Ολοκλήρωση της διαδικασίας αποθήκευσης
    df.finalize()

# Κλήση της λειτουργίας με το αρχείο .osm που έχεις επισυνάψει
read_osm_and_store_blocks('/mnt/data/Peramos.osm', 'datafile.dat')


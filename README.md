
# R*-Tree Spatial Indexing Project

## Overview
This project implements an R*-Tree spatial indexing structure to store and query multi-dimensional data efficiently. The R*-Tree is optimized for high-dimensional range and nearest neighbor queries, and is commonly used in geospatial applications. The project allows for operations like insertions, deletions, range queries, k-nearest neighbors queries, and skyline queries.

## Features
- **R*-Tree Data Structure**: An optimized variant of the R-Tree for spatial data indexing.
- **Terminal Interface**: Provides a user-friendly interface to interact with the tree and perform various operations.
- **Efficient Querying**: Supports range queries, k-nearest neighbors queries, and skyline queries for querying spatial data.
- **Data Storage**: Data is stored in a file using blocks to ensure scalability, with efficient block management.
- **Plotting and Analysis**: Includes functions for visualizing query and construction times.

## Files
1. **`Main.py`**: The entry point of the project, which provides a terminal interface to interact with the R*-Tree.
2. **`RStarTree.py`**: Contains the implementation of the R*-Tree data structure, including insert, delete, range query, k-NN, and skyline query operations.
3. **`Node.py`**: Defines the Node class for the R*-Tree, handling entries and managing the Minimum Bounding Rectangle (MBR).
4. **`DataFile.py`**: Handles the creation and management of the data file, saving records in blocks and ensuring proper data storage.
5. **`plot.py`**: Provides functions to generate plots comparing execution times for different query types and construction methods.

## Setup
To run the project, you need to have Python installed along with the required libraries.

### Required Libraries
- `matplotlib`: For plotting graphs.
- `osmread`: For parsing OpenStreetMap (OSM) data.
- Other standard libraries such as `math` and `heapq`.

Install required libraries via pip:
```bash
pip install matplotlib osmread
```

## How to Use
1. **Run the Program**:
   ```bash
   python Main.py
   ```

2. **Perform Operations**:
   The program will provide the following options:
   - **Insert Record**: Insert a new spatial record into the R*-Tree.
   - **Delete Record**: Delete a record based on its Minimum Bounding Rectangle (MBR).
   - **Range Query**: Perform a range query to find records within a specified MBR.
   - **k-NN Query**: Perform a k-nearest neighbors query to find the nearest points to a given location.
   - **Skyline Query**: Retrieve the skyline points that are not dominated by any other points in the dataset.
   - **Exit**: Exit the program.

3. **Visualize Data**:
   The `plot.py` file generates various plots, such as:
   - Comparison of query times between R*-Tree and sequential search.
   - Comparison of construction times for different R*-Tree construction methods.

## Example Queries
1. **Insert Record**:
   Enter a block ID, slot, and MBR (min_x, min_y, max_x, max_y) to insert a new record.

2. **Range Query**:
   Specify the coordinates for the minimum and maximum bounds of the area you want to query.

3. **k-NN Query**:
   Enter the query point's coordinates and specify how many nearest neighbors you want to retrieve.

## Future Improvements
- Improve the efficiency of the tree by experimenting with different splitting strategies.
- Add support for more complex queries, such as spatial joins.

## License
This project is open-source and licensed under the MIT License.

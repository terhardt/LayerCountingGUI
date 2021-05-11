# Layercounting GUI

This is a __very__ python GUI that can be used for annual layercounting.

## Usage

The code in the repository uses ramndom data to test the GUI, so it needs to 
be adjusted to load data that you want to use for layercounting into a pandas DataFrame.

- To move the dashed working cursor click on a location in the graph.
- To add a layer boundary at the current working cursor position hit the key `b`.
- To move a layer boundary you can use drag and drop
- To delete a boundary right-click on the boundary.

Closing the GUI will save the bondaries to a file called 'cursours.csv' for
later use.

The GUI can also be initialized using allready existing boundaries by passing
them to the initiator.

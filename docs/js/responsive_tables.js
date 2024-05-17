document.addEventListener("DOMContentLoaded", function() {
  // Once the DOM is loaded, find all tables
  var tables = document.querySelectorAll('table');
  tables.forEach(function(table) {
    // Apply a style to the table to ensure it takes 100% of the container width
    table.style.width = '100%';
    table.style.tableLayout = 'fixed';
    var cells = table.querySelectorAll('th, td');

    // Apply styles to cells
    cells.forEach(function(cell) {
      cell.style.padding = '5px';  // or any other value that looks good
      cell.style.wordBreak = 'break-word';
      // cell.style.fontSize = '10px';  // or any other value that looks good
    });
  });
});

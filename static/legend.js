var tbl = document.createElement('table');       
var tbdy = document.createElement('tbody');
for (var x in legendData) {                                            // Dynamically genarate the legend of the availables links
    var tr = document.createElement('tr');
    var td = document.createElement('td');
    td.style.backgroundColor =legendData[x];                           // Dynamically assign colors of the links
    td.style.width='15%';
    td.style.border='22px solid #ffffff';
    tr.appendChild(td)
    var td = document.createElement('td');
    td.style.width='40%';
    td.appendChild(document.createTextNode(x))
    tr.appendChild(td)
    tbdy.appendChild(tr);
    }
tbl.appendChild(tbdy);
t1.appendChild(tbl)

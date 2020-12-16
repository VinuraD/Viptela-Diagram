var size = statisticsData['ISP'].length;

for(var x=0;x<size ; x++){                                   //create dynamic table for statistics of links
    var tr = document.createElement('tr');
    var td1 = document.createElement('td');
    var td2 = document.createElement('td');
    var td3 = document.createElement('td');
    var td4 = document.createElement('td');
    td1.appendChild(document.createTextNode(statisticsData['ISP'][x]))
    td2.appendChild(document.createTextNode(statisticsData['Jitter'][x]))
    td3.appendChild(document.createTextNode(statisticsData['Loss'][x]))
    td4.appendChild(document.createTextNode(statisticsData['Latency'][x]))
    tr.appendChild(td1)
    tr.appendChild(td2)
    tr.appendChild(td3)
    tr.appendChild(td4)
    statTableBody.appendChild(tr);
}


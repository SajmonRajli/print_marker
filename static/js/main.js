






function add_table(list) {
  let table = document.createElement('table');
  let thead = document.createElement('thead');
  let tbody = document.createElement('tbody');
  

  table.appendChild(thead);
  table.appendChild(tbody);
  
  // Adding the entire table to the body tag
  document.getElementById('body').appendChild(table);

  
  let row_head = document.createElement('tr');
  let heading_1 = document.createElement('th');
  heading_1.innerHTML = "id";
  let heading_2 = document.createElement('th');
  heading_2.innerHTML = "Название";
  let heading_3 = document.createElement('th');
  heading_3.innerHTML = "gtin";
  let heading_4 = document.createElement('th');
  heading_4.innerHTML = "Всего маркеров";
  let heading_5 = document.createElement('th');
  heading_5.innerHTML = "Ожидает печати";
  
  row_head.appendChild(heading_1);
  row_head.appendChild(heading_2);
  row_head.appendChild(heading_3);
  row_head.appendChild(heading_4);
  row_head.appendChild(heading_5);
  thead.appendChild(row_head);

  console.log(list)
  for (var i = 0; i < list.length; i++) { 
    let row_body = document.createElement('tr');
    row_body.id = 'tr' + String(list[i].id)
    let data_1 = document.createElement('td');
    data_1.innerHTML = list[i].id;
    let data_2 = document.createElement('td');
    data_2.innerHTML = list[i].name;
    let data_3 = document.createElement('td');
    data_3.innerHTML = list[i].gtin;
    let data_4 = document.createElement('td');
    data_4.innerHTML = list[i].count_all;
    let data_5 = document.createElement('td');
    data_5.innerHTML = list[i].count_wait;
    
    row_body.appendChild(data_1);
    row_body.appendChild(data_2);
    row_body.appendChild(data_3);
    row_body.appendChild(data_4);
    row_body.appendChild(data_5);
    tbody.appendChild(row_body);

  } 
  
}





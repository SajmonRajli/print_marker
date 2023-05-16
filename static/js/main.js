






function add_table(list) {
  let thead = document.createElement('thead');
  let tbody = document.createElement('tbody');
  

  table.appendChild(thead);
  table.appendChild(tbody);
  
  
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
    row_body.addEventListener("click", function(){select(row_body.id)})
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


function select(id){
  console.log('выбрали для печати')
  for (var i = 0; i < list_product.length; i++) { 
    document.getElementById('tr'+String(list_product[i].id)).style.backgroundColor="";   
    if (id == 'tr'+String(list_product[i].id)){
      document.getElementById('tr'+String(list_product[i].id)).style.backgroundColor="RED";   
      id_prod = list_product[i].id
      name_prod = list_product[i].name
    }

  }
  block_text.innerHTML = 'Выбрали для печати '+String(name_prod) +'. Выберете количество и нажмите print'
  blockCount.style.display = 'flex'
  
}

function print() {
  let count = parseInt(inputCount.innerHTML);
  
  if (name_prod != ''){
    block_text.innerHTML = 'Отправили в печать '  + count + ' ' +String(name_prod)
    json = {"id": id_prod, "count": count}
    var data_json = JSON.stringify(json);
    $.ajax({
        url: '/print',
        method: 'POST',
        data: data_json,
        contentType: 'application/json',
        success: function(data){
            console.log(data)
        }
    });
  }


}

function stop_print() {
  block_text.innerHTML = 'Печать остановлена, нажмите на любой продукт для печати'
  $.ajax({
    type: 'POST',
    url: '/stop_print',
    processData: false,
    contentType: false
  }).done(function(data) {
      console.log(data);
  });
}


function statis_print(){
  block_status.innerHTML = 'Статус запрошен'
  $.ajax({
    type: 'POST',
    url: '/status_print',
    processData: false,
    contentType: false
  }).done(function(data) {
      console.log(data);
      block_status.innerHTML = 'Статус принтера: ' +String(data["result"]["response"])
  });
}


function  upBotton(){
  let value = parseInt(inputCount.innerHTML);
  value += 1;
  if (value <= 10){
    inputCount.innerHTML = value;
  }
}

function downBotton(){
  let value = parseInt(inputCount.innerHTML);
    value -= 1;
    if (value >= 0){
      inputCount.innerHTML = value;
    }

}
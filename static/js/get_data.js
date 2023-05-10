
var list_product = []

function load_data(){
  read_list_product()
}

function read_list_product() {
  $.getJSON ($SCRIPT_ROOT + '/get_list_product', { 
  }, function (date) { 
    for (var i = 0; i < date.result.length; i++) { 
      list_product.push({    
        "id": date.result[i].id,
        "name": date.result[i].name,
        "gtin": date.result[i].gtin,
        "count_all": date.result[i].count_all,
        "count_wait": date.result[i].count_wait
      })
    } 
    
    add_table(list_product);
  })
}

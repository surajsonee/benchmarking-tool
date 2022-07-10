function changeToEnergy(){
    const collection = document.getElementsByClassName("totalValue");
    
    var k = 0;

    for(var i = {{realdaystart}}; i < {{dayend + realdaystart - 1}} ; i++){
      var cost = String(energyTotal[k].toFixed(2)).split('.');
      if (typeof myVar !== 'undefined'){
        cost[1] = '00'
      }
      collection[i].innerHTML = '<span class = "kwhUnit">kWh</span>' + cost[0] + '<sup>.' + cost[1] + '</sup>';
      k++;
    }
    document.getElementById("total").innerHTML = total
    price = false;
    energy = true;
  }

  changeToEnergy();
const convertingValue = (classEl) => {
  const numValue = document.querySelectorAll(classEl);
  numValue.forEach((item) => {
    const indexDot = item.textContent.indexOf(".");
    const intgrAfterDot = item.textContent.substring(indexDot + 1);
    const intgrValue = item.textContent.substring(0, indexDot);
    item.innerHTML = `${intgrValue}<sup>.${intgrAfterDot}</sup>`;
  });
};
convertingValue(".numsupValue");

//active Buttons Units

const activeButtons = () => {
  const btnsUnits = document.querySelectorAll(".toggleButtons > div.button");
  btnsUnits.forEach((item) => {
    item.addEventListener("click", () => {
      for (let i = 0; i < btnsUnits.length; i++) {
        btnsUnits[i].classList.remove("active");
      }
      item.classList.add("active");
    });
  });
};
activeButtons();

//Activate Days Month Year
let activeDay = false;
let activeWeek = false;
let activeYear = false;

const activateTimes = () => {
  const btnstTimes = document.querySelectorAll(".monthYearDay > span");
  const currentTimes = document.querySelectorAll(".dataTime");
  const showCurrent = document.querySelector(".showCurrent ");

  btnstTimes.forEach((item, index) => {
    item.addEventListener("click", () => {
      for (let i = 0; i < btnstTimes.length; i++) {
        btnstTimes[i].classList.remove("active");
        currentTimes[i].classList.remove("active");
      }
      if (index === 0) {
        //Day
        activeDay = true;
        activeWeek = false;
        activeYear = false;
      }
      if (index === 1) {
        //Week
        activeDay = false;
        activeWeek = true;
        activeYear = false;
      }
      if (index === 2) {
        //Year
        activeDay = false;
        activeWeek = false;
        activeYear = true;
      }
      if (index === 2) {
        showCurrent.classList.add("adjust");
      } else {
        showCurrent.classList.remove("adjust");
      }
      item.classList.add("active");
      currentTimes[index].classList.add("active");
    });
  });
};

activateTimes();
var script = document.currentScript;
var fullUrl = script.src;
var jsonUrl = fullUrl.replace("solarfile.js", "solardata.json");
//Implement the date function
fetch(jsonUrl)
  .then((response) => response.text())
  .then((json) => {
    const arrayData = JSON.parse(json);
    const columns = document.querySelector(".columns");
    const allColumns = document.querySelectorAll(".column");
    const allColumnsBottom = document.querySelectorAll(
      ".hourlySimulation .columns .column"
    );
    const consumptionData = [];
    //data ONE A

    for (const x of arrayData.twlveAM) {
      allColumns[0].innerHTML = `
         <span class="production" style="height:${x.consumption.value}%"></span>
         <span class="consumption" style="height:${x.production.value}%"></span>
         
         `;
      allColumnsBottom[0].innerHTML = `
         <span class="hour" style="">${x.dataWeather.hour}</span>
         <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
         <span class="icon" style="">${x.dataWeather.icon}</span>
         <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
         <span class="value" style="height:${x.dataWeather.value}%"></span>
         
         `;
    }
    for (const x of arrayData.oneAM) {
      allColumns[1].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
      allColumnsBottom[1].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.twoAM) {
      allColumns[2].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
      allColumnsBottom[2].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.threeAM) {
      allColumns[3].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
      allColumnsBottom[3].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.fourAM) {
      allColumns[4].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
      allColumnsBottom[4].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.fiveAM) {
      allColumns[5].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[5].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.sixAM) {
      allColumns[6].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[6].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.sevenAM) {
      allColumns[7].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[7].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.eightAM) {
      allColumns[8].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[8].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.nineAM) {
      allColumns[9].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[9].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.tenAM) {
      allColumns[10].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[10].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.elevenPM) {
      allColumns[11].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[11].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.twlvePM) {
      allColumns[12].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[12].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.onePM) {
      allColumns[13].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[13].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }

    for (const x of arrayData.twoPM) {
      allColumns[14].innerHTML = `
           <span class="production" style="height:${x.consumption.value}%"></span>
           <span class="consumption" style="height:${x.production.value}%"></span>
           
           `;
           allColumnsBottom[14].innerHTML = `
           <span class="hour" style="">${x.dataWeather.hour}</span>
           <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
           <span class="icon" style="">${x.dataWeather.icon}</span>
           <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
           <span class="value" style="height:${x.dataWeather.value}%"></span>
           
           `;
    }
    for (const x of arrayData.threePM) {
      allColumns[15].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[15].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }
    for (const x of arrayData.fourPM) {
      allColumns[16].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[16].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }
    for (const x of arrayData.fivePM) {
      allColumns[17].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[17].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }

    for (const x of arrayData.sixPM) {
      allColumns[18].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[18].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }

    for (const x of arrayData.sevenPM) {
      allColumns[19].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[19].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }
    for (const x of arrayData.eightPM) {
      allColumns[20].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[20].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }



    for (const x of arrayData.ninePM) {
      allColumns[21].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[21].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }
    for (const x of arrayData.tenPM) {
      allColumns[22].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[22].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }
    for (const x of arrayData.elevnPM) {
      allColumns[23].innerHTML = `
             <span class="production" style="height:${x.consumption.value}%"></span>
             <span class="consumption" style="height:${x.production.value}%"></span>
             
             `;
             allColumnsBottom[23].innerHTML = `
             <span class="hour" style="">${x.dataWeather.hour}</span>
             <span class="degree" style="">${x.dataWeather.degree}<span class="ellipse"></span></span>
             <span class="icon" style="">${x.dataWeather.icon}</span>
             <span class="kwh" style="">${x.dataWeather.kwh} kWh</span>
             <span class="value" style="height:${x.dataWeather.value}%"></span>
             
             `;
    }
  });

//show Production / Comsumptio
const toggleValues = () => {
  const productonBtn = document.querySelector(".types .production");
  const consumptionBtn = document.querySelector(".types .consumption");
  const spanColumnsProduction = document.querySelector(".columns");

  productonBtn.addEventListener("click", () => {
    if (spanColumnsProduction.classList.contains("hideProduction")) {
      spanColumnsProduction.classList.remove("hideProduction");
    } else {
      spanColumnsProduction.classList.add("hideProduction");
    }
  });
  consumptionBtn.addEventListener("click", () => {
    if (spanColumnsProduction.classList.contains("hideConsumption")) {
      spanColumnsProduction.classList.remove("hideConsumption");
    } else {
      spanColumnsProduction.classList.add("hideConsumption");
    }
  });
};

window.onload = () => {
  toggleValues();
};

$(".part-2").niceScroll({
  cursorcolor: "#0D1758",

  cursorfixedheight: 50,
  cursoropacitymin: 1,
  railpadding: { top: -10, right: 0, left: 0, bottom: 0 }
});

$(".dataNumber").niceScroll({
  cursorcolor: "#0D1758",

  cursorfixedheight: 50,
  cursoropacitymin: 1,
  railpadding: { top: 10, right: 0, left: 0, bottom: 0 }
 
});

$('#circle').circleProgress({
  value: .25,
  size: 110,
  thickness:18,
  fill: {
    color: ["#FFC90E"]
  },
  emptyFill:"#44AAFD",
  reverse:false
});

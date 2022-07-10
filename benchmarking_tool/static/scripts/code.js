const svgSrcMorining = `<svg class="icon-svg-day" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" style="bottom: 82.5%;">
<path d="M18.9999 10.79C18.8426 12.4922 18.2038 14.1144 17.1581 15.4668C16.1125 16.8192 14.7034 17.8458 13.0956 18.4265C11.4878 19.0073 9.74789 19.1181 8.0794 18.7461C6.41092 18.3741 4.8829 17.5345 3.67413 16.3258C2.46536 15.117 1.62584 13.589 1.25381 11.9205C0.881777 10.252 0.992617 8.51208 1.57336 6.9043C2.15411 5.29651 3.18073 3.88737 4.53311 2.84175C5.8855 1.79614 7.5077 1.15731 9.2099 1C8.21331 2.34827 7.73375 4.00945 7.85843 5.68141C7.98312 7.35338 8.70376 8.92506 9.8893 10.1106C11.0748 11.2961 12.6465 12.0168 14.3185 12.1415C15.9905 12.2662 17.6516 11.7866 18.9999 10.79V10.79Z" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>`;

const svgAfternoon = `<svg class="icon-svg-day" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="bottom: 82.5%;">
<path d="M12 17C14.7614 17 17 14.7614 17 12C17 9.23858 14.7614 7 12 7C9.23858 7 7 9.23858 7 12C7 14.7614 9.23858 17 12 17Z" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M12 1V3" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M12 21V23" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M4.21973 4.21997L5.63973 5.63997" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M18.3604 18.36L19.7804 19.78" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M1 12H3" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M21 12H23" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M4.21973 19.78L5.63973 18.36" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
<path d="M18.3604 5.63997L19.7804 4.21997" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>`;

//Create Empty Array to fill with all values of height of the columns to detect highest value to put the icons above it to prevent ovelaaping
const allValues = [];
//General Function to create Columns with each one has own data
const morningSection = document.querySelector(".morning");
const afterNoonSection = document.querySelector(".afternoon");
const nightSection = document.querySelector(".night");

function createColumns(periodArray, section,data) {
  var i = 0;
  for (const x of periodArray) {
    //Create Morning Data
    if (x.period === `${section.className}`) {
      const column = document.createElement("div");
      column.classList.add("column");
      if(x.value < 30){

        column.style.height = (x.value + 80) + "px";
      }
      else if (x.value > 200){
        column.style.height ="150px";
      }
      else{
        column.style.height = x.value + "px";
      }
      if (section.classList.contains(`${x.period}`)) {
        section.appendChild(column);
      }

      //detect off-on-Hrs
      if(data == 'cost'){
      if (x.type === "on-hrs") {
        column.innerHTML = `<div class="columnpopup on-hrs">
        <div class="top-part">
        
        ${x.period === "morning" || x.period === "night" ? svgSrcMorining : svgAfternoon} 
        <p>
        ${
          x.hours
        }${i < 11 || i > 22 ? "AM" : "PM"}
        </p>
       
 
        </div>
        <p class="on-hrs-p">On-Hours</p>
        <p class="price">$ ${x.price.toFixed(2)}</p>
        
        </div>`;
      } else if (x.type === "off-hrs") {
        column.innerHTML = `<div class="columnpopup off-hrs">
        <div class="top-part">
        ${x.period === "morning" || x.period === "night" ? svgSrcMorining : svgAfternoon} <p>${
          x.hours
        }${i < 11 || i > 22 ? "AM" : "PM"}</p>
       
 
        </div>
        <p>Off-Hours</p>
        <p class="price">$ ${x.price.toFixed(2)}</p>
        
        </div>`;
      }
    }

    if(data == 'energy'){
        if (x.type === "on-hrs") {
        column.innerHTML = `<div class="columnpopup on-hrs" style = 'left: 0;'>
        <div class="top-part">
        
        ${x.period === "morning" || x.period === "night" ? svgSrcMorining : svgAfternoon} 
        <p>
        ${
          x.hours
        }${i < 11 || i > 22 ? "AM" : "PM"}
        </p>
       
 
        </div>
        <p class="on-hrs-p">On-Hours</p>
        <p class="price">${x.value.toFixed(2)} kWh</p>
        
        </div>`;
      } else if (x.type === "off-hrs") {
        if(x.period === "morning"){
        column.innerHTML = `<div class="columnpopup off-hrs" style = 'left: 0;'>
        <div class="top-part">
        ${x.period === "morning" || x.period === "night" ? svgSrcMorining : svgAfternoon} <p>${
          x.hours
        }${i < 11 || i > 22 ? "AM" : "PM"}</p>
       
 
        </div>
        <p>Off-Hours</p>
        <p class="price">${x.value.toFixed(2)} kWh</p>
        
        </div>`;}
        else{
        column.innerHTML = `<div class="columnpopup off-hrs" style = 'right: 0;'>
        <div class="top-part">
        ${x.period === "morning" || x.period === "night" ? svgSrcMorining : svgAfternoon} <p>${
          x.hours
        }${i < 11 || i > 22 ? "AM" : "PM"}</p>
       
 
        </div>
        <p>Off-Hours</p>
        <p class="price">${x.value.toFixed(2)} kWh</p>
        
        </div>`;}
      }
    }
    }
    i += 1
    }
}
//fetch the data
var script = document.currentScript;
var fullUrl = script.src;
function createBarChart(data){

  while (morningSection.childNodes.length > 4) {
    morningSection.removeChild(morningSection.lastChild);
}
    while (afterNoonSection.childNodes.length > 4) {
    afterNoonSection.removeChild(afterNoonSection.lastChild);
}
    while (nightSection.childNodes.length > 4) {
    nightSection.removeChild(nightSection.lastChild);
}

var jsonUrl = fullUrl.replace("code.js", "data.json");

fetch(jsonUrl)
  .then((response) => response.text())
  .then((json) => {
    const ArrData = JSON.parse(json);

    createColumns(ArrData, morningSection,data);
    createColumns(ArrData, afterNoonSection,data);
    createColumns(ArrData, nightSection,data);

    for (const x of ArrData) {
      allValues.push(x.value);
    }
    document.querySelectorAll(".column").forEach((item) => {
      item.firstElementChild.style.bottom = `10px`;
    });
    setIconPosition(allValues);
  });

}
//set the position of the icon

const setIconPosition = (allArrays) => {
  const maxValue = Math.max(...allArrays);
  const iconSvg = document.querySelectorAll(".icon-svg-day");

  iconSvg.forEach((item) => {
    if (maxValue*20 < 50) {
      item.style.marginTop  = 10 + "px"
    } else {
      item.style.marginTop  = 10 + "px";
    }
  });

};


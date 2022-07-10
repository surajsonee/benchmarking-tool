/*
const getDataChart = () => {
  fetch("./data.json")
    .then((response) => response.json())
    .then((data) => {
      const chartArray = data;
      const allColumns = document.querySelectorAll(".chart-comparison .column");
console.log(data.length)
      for (const [key, value] of chartArray.entries()) {
      
        allColumns[key].innerHTML = `
        <span style="height:${value.chart.value1.val}px"></span>
        <span style="height:${value.chart.value2.val}px"></span>
        <span style="height:${value.chart.value3.val}px"></span>
        <p class="title">${value.chart.value1.text}</p>
        `;
      }
    });
};
getDataChart();
*/



/*
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















const myctx = document.getElementById("myChart").getContext("2d");

const myChart = new Chart(myctx, {
  type: "doughnut",
  data: {
    datasets: [
      {
        data: [25, 19, 40, 20, 19,15],
        backgroundColor: [
          "#000000",
          "#880015",
          "#CC6633",
          "#AA3300",
          "#FF9900",
           "#7F7F7F"
         
        ],
        borderWidth: 0,
      },
    ],
  },
  options: {
    cutout: 35,
    maintainAspectRatio: false
  },
});
*/

//operate the vidoe
/*

const operatVideo = () => {
  const btn = document.querySelector(".landingPage .video .poster .btn");
  const videoPart = document.querySelector(".landingPage .video video");

  btn.addEventListener("click", (e) => {
   
    videoPart.play();
    document.body.classList.add('hide')

  });
  videoPart.addEventListener('pause',(e)=>{
    
   // document.body.classList.remove('hide')
  })
};

operatVideo();

*/
/*

let x = 0;

const moveRow = (indexNum, class1, class2, percentage, width, cost) => {
  document.querySelectorAll(".live-table > div").forEach((item, index) => {
    if (index === indexNum) {
      item.querySelector(class1).textContent = percentage + "%";
      item.querySelector(class1).previousElementSibling.style.width =
        width + "px";
      item.querySelector(class2).textContent = cost;
    }
  });
};

myInterval = setInterval(() => {
  x++;
 // document.querySelector(".Timer").textContent = x;

  //first scenario
  if (x <= 6) {
    moveRow(0, ".percentage-Value", ".cost-value", 4.25, 25, (0.2).toFixed(2));
    moveRow(
      1,
      ".percentage-Value",
      ".cost-value",
      (0.0).toFixed(1),
      5,
      (0.0).toFixed(2)
    );
  } else {
    moveRow(
      0,
      ".percentage-Value",
      ".cost-value",
      (0.0).toFixed(2),
      5,
      (0.0).toFixed(2)
    );
    moveRow(1, ".percentage-Value", ".cost-value", 0.95, 25, (0.05).toFixed(2));
  }

  //scenario Office 1 Lighting
  if (x === 2) {
    moveRow(2, ".percentage-Value", ".cost-value", 1.1, 15, (0.04).toFixed(2));
  } else {
    moveRow(2, ".percentage-Value", ".cost-value", 1.1, 15, (0.06).toFixed(2));
  }
  //scenario Office 2 Lighting

  if (x <= 5) {
    moveRow(3, ".percentage-Value", ".cost-value", 2.1, 20, (0.1).toFixed(2));
  } else {
    moveRow(
      3,
      ".percentage-Value",
      ".cost-value",
      (0.0).toFixed(1),
      5,
      (0.0).toFixed(2)
    );
  }
  //Furnace

  if (x <= 2) {
    moveRow(6, ".percentage-Value", ".cost-value", 0.08, 15, (0.04).toFixed(2));
  }
  if (x > 2 && x <= 4) {
    moveRow(6, ".percentage-Value", ".cost-value", 1.43, 20, (0.07).toFixed(2));
  }
  if(x === 5){
    moveRow(6, ".percentage-Value", ".cost-value", 1.81, 22, (0.09).toFixed(2));
  }
  if (x > 5 && x <= 7) {
    moveRow(6, ".percentage-Value", ".cost-value", 2.10.toFixed(2), 25, (0.11).toFixed(2));
  }
  if(x > 7){
    moveRow(6, ".percentage-Value", ".cost-value", 2.12.toFixed(2), 30, (0.12).toFixed(2));
  }
}, 1000);

setInterval(() => {
  x = 0;
}, 10000);

*/

const convertingValue = (classEl) => {
  const numValue = document.querySelectorAll(classEl);
  numValue.forEach((item) => {
    const indexDot = item.textContent.indexOf(".");
    const intgrAfterDot = item.textContent.substring(indexDot + 1);
    const intgrValue = item.textContent.substring(0, indexDot);
    item.innerHTML = `${intgrValue}<sup>.${intgrAfterDot}</sup>`;
  });
};
convertingValue(".numValue");

//with $

const convertingValueDollar = (classEl) => {
  const numValue = document.querySelectorAll(classEl);
  numValue.forEach((item) => {
    const indexDot = item.textContent.indexOf(".");
    const intgrAfterDot = item.textContent.substring(indexDot + 1);
    const intgrValue = item.textContent.substring(0, indexDot);

    if (!Number.isInteger(Number(item.textContent))) {
      if (intgrAfterDot > 0) {
        item.innerHTML = `<span class="kwhUnit">kWh</span><span></span>${intgrValue}<sup>.${intgrAfterDot}</sup>`;
      } else {
        //   item.innerHTML = "";
      }
    } else {
      if (item.textContent === "") {
        item.innerHTML = "";
      } else {
        item.innerHTML = `<span class="kwhUnit">kWh</span><span></span>${item.textContent}`;
      }
    }
  });
};

//dropdown total usage

const dropDown = () => {
  const totalUsageBtn = document.querySelector(".total-usage");
  const dorpDownUsage = document.querySelector(".total-usage .dropwdown");

  let show = false;
  totalUsageBtn.addEventListener("click", (e) => {
   e.stopPropagation();
    if (!show) {
      dorpDownUsage.classList.add("show");
      totalUsageBtn.classList.add("stretch");

      show = true;
    } else {
      dorpDownUsage.classList.remove("show");
      totalUsageBtn.classList.remove("stretch");
      show = false;
    }
  });

  dorpDownUsage.addEventListener("click", (e) => {
    e.stopPropagation();
  });
  document.body.addEventListener('click',(e)=>{
    e.stopPropagation()
    dorpDownUsage.classList.remove("show");
      totalUsageBtn.classList.remove("stretch");
      show = false
  })
};

dropDown();

//fetch json

var script = document.currentScript;
var fullUrl = script.src;
var jsonUrl = fullUrl.replace("energycalendar.js", "data-calender.json");
fetch(jsonUrl)
  .then((response) => response.json())
  .then((data) => {
    const allWeeks = Array.from(data);

    const firstWeek = allWeeks[0].firstweek;
    const secondWeek = allWeeks[1].secondweek;
    const thirdWeek = allWeeks[2].thirdWeek;
    const fourthweek = allWeeks[3].fourthweek;
    const fifthweek = allWeeks[4].fifthweek;

    //Generate First Week

    //sunday

    for (let i = 0; i < firstWeek.sunday.value.length; i++) {
      document.querySelector(
        ".firstweek .sunday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${firstWeek.sunday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".firstweek .sunday .totalValue"
    ).innerHTML = `${firstWeek.sunday.totalValue}`;
    document.querySelector(".firstweek .sunday .numberDay").textContent =
      firstWeek.sunday.numDay;
    convertingValueDollar(".firstweek .sunday .totalValue");
    //Monday

    for (let i = 0; i < firstWeek.monday.value.length; i++) {
      document.querySelector(
        ".firstweek .monday  .column"
      ).innerHTML += `<span class="spancolumn" style="height:${firstWeek.monday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".firstweek .monday  .totalValue"
    ).innerHTML = `${firstWeek.monday.totalValue}`;
    document.querySelector(".firstweek .monday  .numberDay").textContent =
      firstWeek.monday.numDay;
    convertingValueDollar(".firstweek .monday  .totalValue");

    //Tuesday

    for (let i = 0; i < firstWeek.tuesday.value.length; i++) {
      document.querySelector(
        ".firstweek .tuesday   .column"
      ).innerHTML += `<span class="spancolumn" style="height:${firstWeek.tuesday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".firstweek .tuesday   .totalValue"
    ).innerHTML = `${firstWeek.tuesday.totalValue}`;
    document.querySelector(".firstweek .tuesday   .numberDay").textContent =
      firstWeek.tuesday.numDay;
    convertingValueDollar(".firstweek .tuesday   .totalValue");

    //Wednsday
    for (let i = 0; i < firstWeek.wednsday.value.length; i++) {
      document.querySelector(
        ".firstweek .wednsday    .column"
      ).innerHTML += `<span class="spancolumn" style="height:${firstWeek.wednsday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".firstweek .wednsday    .totalValue"
    ).innerHTML = `${firstWeek.wednsday.totalValue}`;
    document.querySelector(".firstweek .wednsday    .numberDay").textContent =
      firstWeek.wednsday.numDay;
    convertingValueDollar(".firstweek .wednsday    .totalValue");

    //Thursday
    for (let i = 0; i < firstWeek.thursday.value.length; i++) {
      document.querySelector(
        ".firstweek .thursday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${firstWeek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".firstweek .thursday .totalValue"
    ).innerHTML = `${firstWeek.thursday.totalValue}`;
    document.querySelector(".firstweek .thursday  .numberDay").textContent =
      firstWeek.thursday.numDay;
    convertingValueDollar(".firstweek .thursday  .totalValue");

    //Friday
    for (let i = 0; i < firstWeek.friday.value.length; i++) {
      document.querySelector(
        ".firstweek .friday  .column"
      ).innerHTML += `<span class="spancolumn" style="height:${firstWeek.friday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".firstweek .friday  .totalValue"
    ).innerHTML = `${firstWeek.friday.totalValue}`;
    document.querySelector(".firstweek .friday .numberDay").textContent =
      firstWeek.friday.numDay;
    convertingValueDollar(".firstweek .friday .totalValue");
    //Saturday

    for (let i = 0; i < firstWeek.saturday.value.length; i++) {
      document.querySelector(
        ".firstweek .saturday   .column"
      ).innerHTML += `<span class="spancolumn" style="height:${firstWeek.saturday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".firstweek .saturday   .totalValue"
    ).innerHTML = `${firstWeek.saturday.totalValue}`;
    document.querySelector(".firstweek .saturday    .numberDay").textContent =
      firstWeek.saturday.numDay;
    convertingValueDollar(".firstweek .saturday .totalValue");

    //second Week

    //sunday

    for (let i = 0; i < secondWeek.sunday.value.length; i++) {
      document.querySelector(
        ".secondweek .sunday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${secondWeek.sunday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".secondweek .sunday .totalValue"
    ).innerHTML = `${secondWeek.sunday.totalValue}`;
    document.querySelector(".secondweek .sunday .numberDay").textContent =
      secondWeek.sunday.numDay;
    convertingValueDollar(".secondweek .sunday .totalValue");

    //Monday

    for (let i = 0; i < secondWeek.monday.value.length; i++) {
      document.querySelector(
        ".secondweek .monday  .column"
      ).innerHTML += `<span class="spancolumn" style="height:${secondWeek.monday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".secondweek .monday  .totalValue"
    ).innerHTML = `${secondWeek.monday.totalValue}`;
    document.querySelector(".secondweek .monday  .numberDay").textContent =
      secondWeek.monday.numDay;
    convertingValueDollar(".secondweek .monday  .totalValue");

    //Tuesday
    for (let i = 0; i < secondWeek.tuesday.value.length; i++) {
      document.querySelector(
        ".secondweek .tuesday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${secondWeek.tuesday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".secondweek .tuesday  .totalValue"
    ).innerHTML = `${secondWeek.tuesday.totalValue}`;
    document.querySelector(".secondweek .tuesday   .numberDay").textContent =
      secondWeek.tuesday.numDay;
    convertingValueDollar(".secondweek .tuesday   .totalValue");

    //Wednsday

    for (let i = 0; i < secondWeek.wednsday.value.length; i++) {
      document.querySelector(
        ".secondweek .wednesday     .column"
      ).innerHTML += `<span class="spancolumn" style="height:${secondWeek.wednsday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".secondweek .wednesday     .totalValue"
    ).innerHTML = `${secondWeek.wednsday.totalValue}`;
    document.querySelector(
      ".secondweek .wednesday     .numberDay"
    ).textContent = secondWeek.wednsday.numDay;
    convertingValueDollar(".secondweek .wednesday     .totalValue");

    //Thursday

    for (let i = 0; i < secondWeek.thursday.value.length; i++) {
      document.querySelector(
        ".secondweek .thursday      .column"
      ).innerHTML += `<span class="spancolumn" style="height:${secondWeek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".secondweek .thursday      .totalValue"
    ).innerHTML = `${secondWeek.thursday.totalValue}`;
    document.querySelector(
      ".secondweek .thursday      .numberDay"
    ).textContent = secondWeek.thursday.numDay;
    convertingValueDollar(".secondweek .thursday      .totalValue");

    //Friday

    for (let i = 0; i < secondWeek.friday.value.length; i++) {
      document.querySelector(
        ".secondweek .friday       .column"
      ).innerHTML += `<span class="spancolumn" style="height:${secondWeek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".secondweek .friday       .totalValue"
    ).innerHTML = `${secondWeek.friday.totalValue}`;
    document.querySelector(".secondweek .friday       .numberDay").textContent =
      secondWeek.friday.numDay;
    convertingValueDollar(".secondweek .friday       .totalValue");

    //Saturday

    for (let i = 0; i < secondWeek.saturday.value.length; i++) {
      document.querySelector(
        ".secondweek .saturday       .column"
      ).innerHTML += `<span class="spancolumn" style="height:${secondWeek.saturday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".secondweek .saturday .totalValue"
    ).innerHTML = `${secondWeek.saturday.totalValue}`;
    document.querySelector(".secondweek .saturday .numberDay").textContent =
      secondWeek.saturday.numDay;
    convertingValueDollar(".secondweek .saturday  .totalValue");

    //Third Week

    //sunday

    for (let i = 0; i < thirdWeek.sunday.value.length; i++) {
      document.querySelector(
        ".thirdweek .sunday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${thirdWeek.sunday.value[i]/30 + 1}px"></span>`;
    }
    document.querySelector(
      ".thirdweek .sunday .totalValue"
    ).innerHTML = `${thirdWeek.sunday.totalValue}`;
    document.querySelector(".thirdweek .sunday .numberDay").textContent =
      thirdWeek.sunday.numDay;
    convertingValueDollar(".thirdweek .sunday .totalValue");

    //Monday

    for (let i = 0; i < thirdWeek.monday.value.length; i++) {
      document.querySelector(
        ".thirdweek .monday  .column"
      ).innerHTML += `<span class="spancolumn" style="height:${thirdWeek.monday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".thirdweek .monday  .totalValue"
    ).innerHTML = `${thirdWeek.monday.totalValue}`;
    document.querySelector(".thirdweek .monday  .numberDay").textContent =
      thirdWeek.monday.numDay;
    convertingValueDollar(".thirdweek .monday  .totalValue");

    //Tuesday
    for (let i = 0; i < thirdWeek.tuesday.value.length; i++) {
      document.querySelector(
        ".thirdweek .tuesday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${thirdWeek.tuesday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".thirdweek .tuesday  .totalValue"
    ).innerHTML = `${thirdWeek.tuesday.totalValue}`;
    document.querySelector(".thirdweek .tuesday   .numberDay").textContent =
      thirdWeek.tuesday.numDay;
    convertingValueDollar(".thirdweek .tuesday   .totalValue");

    //Wednsday

    for (let i = 0; i < thirdWeek.wednsday.value.length; i++) {
      document.querySelector(
        ".thirdweek .wednesday     .column"
      ).innerHTML += `<span class="spancolumn" style="height:${thirdWeek.wednsday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".thirdweek .wednesday     .totalValue"
    ).innerHTML = `${thirdWeek.wednsday.totalValue}`;
    document.querySelector(".thirdweek .wednesday     .numberDay").textContent =
      thirdWeek.wednsday.numDay;
    convertingValueDollar(".thirdweek .wednesday     .totalValue");

    //Thursday

    for (let i = 0; i < thirdWeek.thursday.value.length; i++) {
      document.querySelector(
        ".thirdweek .thursday      .column"
      ).innerHTML += `<span class="spancolumn" style="height:${thirdWeek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".thirdweek .thursday      .totalValue"
    ).innerHTML = `${thirdWeek.thursday.totalValue}`;
    document.querySelector(".thirdweek .thursday      .numberDay").textContent =
      thirdWeek.thursday.numDay;
    convertingValueDollar(".thirdweek .thursday      .totalValue");

    //Friday

    for (let i = 0; i < thirdWeek.friday.value.length; i++) {
      document.querySelector(
        ".thirdweek .friday       .column"
      ).innerHTML += `<span class="spancolumn" style="height:${thirdWeek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".thirdweek .friday       .totalValue"
    ).innerHTML = `${thirdWeek.friday.totalValue}`;
    document.querySelector(".thirdweek .friday       .numberDay").textContent =
      thirdWeek.friday.numDay;
    convertingValueDollar(".thirdweek .friday       .totalValue");

    //Saturday

    for (let i = 0; i < thirdWeek.saturday.value.length; i++) {
      document.querySelector(
        ".thirdweek .saturday       .column"
      ).innerHTML += `<span class="spancolumn" style="height:${thirdWeek.saturday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".thirdweek .saturday .totalValue"
    ).innerHTML = `${thirdWeek.saturday.totalValue}`;
    document.querySelector(".thirdweek .saturday .numberDay").textContent =
      thirdWeek.saturday.numDay;
    convertingValueDollar(".thirdweek .saturday  .totalValue");

    //fourth  Week

    //sunday

    for (let i = 0; i < fourthweek.sunday.value.length; i++) {
      document.querySelector(
        ".fourthweek .sunday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fourthweek.sunday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fourthweek .sunday .totalValue"
    ).innerHTML = `${fourthweek.sunday.totalValue}`;
    document.querySelector(".fourthweek .sunday .numberDay").textContent =
      fourthweek.sunday.numDay;
    convertingValueDollar(".fourthweek .sunday .totalValue");

    //Monday

    for (let i = 0; i < fourthweek.monday.value.length; i++) {
      document.querySelector(
        ".fourthweek .monday  .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fourthweek.monday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fourthweek .monday  .totalValue"
    ).innerHTML = `${fourthweek.monday.totalValue}`;
    document.querySelector(".fourthweek .monday  .numberDay").textContent =
      fourthweek.monday.numDay;
    convertingValueDollar(".fourthweek .monday  .totalValue");

    //Tuesday
    for (let i = 0; i < fourthweek.tuesday.value.length; i++) {
      document.querySelector(
        ".fourthweek .tuesday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fourthweek.tuesday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fourthweek .tuesday  .totalValue"
    ).innerHTML = `${fourthweek.tuesday.totalValue}`;
    document.querySelector(".fourthweek .tuesday   .numberDay").textContent =
      fourthweek.tuesday.numDay;
    convertingValueDollar(".fourthweek .tuesday   .totalValue");

    //Wednsday

    for (let i = 0; i < fourthweek.wednsday.value.length; i++) {
      document.querySelector(
        ".fourthweek .wednesday     .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fourthweek.wednsday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fourthweek .wednesday     .totalValue"
    ).innerHTML = `${fourthweek.wednsday.totalValue}`;
    document.querySelector(
      ".fourthweek .wednesday     .numberDay"
    ).textContent = fourthweek.wednsday.numDay;
    convertingValueDollar(".fourthweek .wednesday     .totalValue");

    //Thursday

    for (let i = 0; i < fourthweek.thursday.value.length; i++) {
      document.querySelector(
        ".fourthweek .thursday      .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fourthweek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fourthweek .thursday      .totalValue"
    ).innerHTML = `${fourthweek.thursday.totalValue}`;
    document.querySelector(
      ".fourthweek .thursday      .numberDay"
    ).textContent = fourthweek.thursday.numDay;
    convertingValueDollar(".fourthweek .thursday      .totalValue");

    //Friday

    for (let i = 0; i < fourthweek.friday.value.length; i++) {
      document.querySelector(
        ".fourthweek .friday       .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fourthweek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fourthweek .friday       .totalValue"
    ).innerHTML = `${fourthweek.friday.totalValue}`;
    document.querySelector(".fourthweek .friday       .numberDay").textContent =
      fourthweek.friday.numDay;
    convertingValueDollar(".fourthweek .friday       .totalValue");

    //Saturday

    for (let i = 0; i < fourthweek.saturday.value.length; i++) {
      document.querySelector(
        ".fourthweek .saturday       .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fourthweek.saturday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fourthweek .saturday .totalValue"
    ).innerHTML = `${fourthweek.saturday.totalValue}`;
    document.querySelector(".fourthweek .saturday .numberDay").textContent =
      fourthweek.saturday.numDay;
    convertingValueDollar(".fourthweek .saturday  .totalValue");

    //Five  Week

    //sunday

    for (let i = 0; i < fifthweek.sunday.value.length; i++) {
      document.querySelector(
        ".fifthweek .sunday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fifthweek.sunday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fifthweek .sunday .totalValue"
    ).innerHTML = `${fifthweek.sunday.totalValue}`;
    document.querySelector(".fifthweek .sunday .numberDay").textContent =
      fifthweek.sunday.numDay;
    convertingValueDollar(".fifthweek .sunday .totalValue");

    //Monday

    for (let i = 0; i < fifthweek.monday.value.length; i++) {
      document.querySelector(
        ".fifthweek .monday  .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fifthweek.monday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fifthweek .monday  .totalValue"
    ).innerHTML = `${fifthweek.monday.totalValue}`;
    document.querySelector(".fifthweek .monday  .numberDay").textContent =
      fifthweek.monday.numDay;
    convertingValueDollar(".fifthweek .monday  .totalValue");

    //Tuesday
    for (let i = 0; i < fifthweek.tuesday.value.length; i++) {
      document.querySelector(
        ".fifthweek .tuesday .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fifthweek.tuesday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fifthweek .tuesday  .totalValue"
    ).innerHTML = `${fifthweek.tuesday.totalValue}`;
    document.querySelector(".fifthweek .tuesday   .numberDay").textContent =
      fifthweek.tuesday.numDay;
    convertingValueDollar(".fifthweek .tuesday   .totalValue");

    //Wednsday

    for (let i = 0; i < fifthweek.wednsday.value.length; i++) {
      document.querySelector(
        ".fifthweek .wednesday     .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fifthweek.wednsday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fifthweek .wednesday     .totalValue"
    ).innerHTML = `${fifthweek.wednsday.totalValue}`;
    document.querySelector(".fifthweek .wednesday     .numberDay").textContent =
      fifthweek.wednsday.numDay;
    convertingValueDollar(".fifthweek .wednesday     .totalValue");

    //Thursday

    for (let i = 0; i < fifthweek.thursday.value.length; i++) {
      document.querySelector(
        ".fifthweek .thursday      .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fifthweek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fifthweek .thursday      .totalValue"
    ).innerHTML = `${fifthweek.thursday.totalValue}`;
    document.querySelector(".fifthweek .thursday      .numberDay").textContent =
      fifthweek.thursday.numDay;
    convertingValueDollar(".fifthweek .thursday      .totalValue");

    //Friday

    for (let i = 0; i < fifthweek.friday.value.length; i++) {
      document.querySelector(
        ".fifthweek .friday       .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fifthweek.thursday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fifthweek .friday       .totalValue"
    ).innerHTML = `${fifthweek.friday.totalValue}`;
    document.querySelector(".fifthweek .friday       .numberDay").textContent =
      fifthweek.friday.numDay;
    convertingValueDollar(".fifthweek .friday       .totalValue");

    //Saturday

    for (let i = 0; i < fifthweek.saturday.value.length; i++) {
      document.querySelector(
        ".fifthweek .saturday       .column"
      ).innerHTML += `<span class="spancolumn" style="height:${fifthweek.saturday.value[i]/20 + 1}px"></span>`;
    }
    document.querySelector(
      ".fifthweek .saturday .totalValue"
    ).innerHTML = `${fifthweek.saturday.totalValue}`;
    document.querySelector(".fifthweek .saturday .numberDay").textContent =
      fifthweek.saturday.numDay;
    convertingValueDollar(".fifthweek .saturday  .totalValue");
  });

const toggleMonthYear = () => {
  const periodBtn = document.querySelectorAll(".monthYear span");
  periodBtn.forEach((item, index) => {
    item.addEventListener("click", () => {
      for (let i = 0; i < periodBtn.length; i++) {
        periodBtn[i].classList.remove("active");
      }
      item.classList.add("active");
      if (index === 1) {
        document.querySelector(".showCurrent").classList.add("adjust");
      } else {
        document.querySelector(".showCurrent").classList.remove("adjust");
      }
    });
  });
};
toggleMonthYear();

const toggleBtns = (classEl) => {
  const allTimeLoad = document.querySelectorAll(  classEl +  " > div");

  allTimeLoad.forEach((item, index) => {
    item.addEventListener("click", () => {
      for (let i = 0; i < allTimeLoad.length; i++) {
        allTimeLoad[i].classList.remove("active");
      }
      item.classList.add("active");
    });
  });
};

toggleBtns(".timeload");
toggleBtns(".breakdown");
toggleBtns(".units");
toggleBtns(".toggle");

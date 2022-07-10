let yearsFun = true;
let monthsFun = false;
const toggleClassActive = () => {
  const btns = document.querySelectorAll(".monthYear > span");
  const shwoCurrent = document.querySelector(".showCurrent");
  const yearView = document.querySelector(".year-view");
  const monthView = document.querySelector(".month-view");

  btns.forEach((item, index) => {
    item.addEventListener("click", () => {
      for (let i = 0; i < btns.length; i++) {
        btns[i].classList.remove("active");
      }
      if (index === 1) {
        //month
        shwoCurrent.classList.add("adjust");
        monthView.classList.add("active");
        yearView.classList.remove("active");
        yearsFun = false;
        monthsFun = true;
      } else {
        //year
        shwoCurrent.classList.remove("adjust");
        monthView.classList.remove("active");
        yearView.classList.add("active");
        yearsFun = true;
        monthsFun = false;
      }
      item.classList.add("active");
    });
  });
};
toggleClassActive();

const convertNumToSub = (classEl, parentElClass) => {
  const txt = document.querySelectorAll(classEl);
  const prentItem = document.querySelectorAll(parentElClass);

  txt.forEach((item, index) => {
    const indexNum = item.textContent.indexOf(".");
    const firstTxt = item.textContent.substring(0, indexNum);
    const subTxt = item.textContent.substring(indexNum + 1);
    prentItem[
      index
    ].innerHTML = `<span class="usdsign">$</span> ${firstTxt}<sup>${
      "." + subTxt
    }</sup>`;
  });
};

convertNumToSub(".realNum", ".cost-result");
convertNumToSub(".realNum-usage", ".usage-result");
//Implement Carouel

const years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026];


const carouselYears = () => {
  const yearData = document.querySelector(".yearData");
  const yearName = document.querySelector(".yearName");
  const leftBtn = document.querySelector(".btn-left");
  const rightBtn = document.querySelector(".btn-right");
  let currentItem = 0;
  rightBtn.addEventListener("click", (e) => {
    if (yearsFun) {
      if (currentItem < years.length - 1 ) {
        currentItem++;

        yearData.textContent = years[currentItem];
        yearName.textContent = years[currentItem];
      }
    }
  });
  leftBtn.addEventListener("click", () => {
    if (yearsFun) {
      if (currentItem > 0) {
        currentItem--;
        yearData.textContent = years[currentItem];
        
      } else {
        currentItem = 0;
      }
    }
  });
};
carouselYears();

const carouselMonth = () => {
  const leftBtn = document.querySelector(".btn-left");
  const rightBtn = document.querySelector(".btn-right");
  const month = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  let curremtMonth = 0;
  const monthName = document.querySelector('.monthName')

  rightBtn.addEventListener("click", () => {
    if (monthsFun) {
        if (curremtMonth < month.length - 1 ) {
            curremtMonth++;
    
            monthName.textContent = month[curremtMonth];
            monthName.textContent = month[curremtMonth];
          }
    }
  });
  leftBtn.addEventListener("click", () => {
    if (monthsFun) {
      if (curremtMonth > 0) {
        curremtMonth--;
        monthName.textContent = month[curremtMonth];
        
      } else {
        curremtMonth = 0;
      }
    }
  });
};
carouselMonth();



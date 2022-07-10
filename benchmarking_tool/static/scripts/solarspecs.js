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

















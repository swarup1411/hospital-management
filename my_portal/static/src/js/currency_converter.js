document.addEventListener("DOMContentLoaded", function () {

    let fromCurrency = document.querySelector(".fromcurrency");
    let fromType = document.querySelector(".fromcurrencytype");
    let toType = document.querySelector(".tocurrencytype");
    let toCurrency = document.querySelector(".tocurrency");
    let btn = document.querySelector("#convertBtn");

    let rates = {};

    fetch("https://open.er-api.com/v6/latest/USD")
        .then(res => res.json())
        .then(data => rates = data.rates);

    btn.addEventListener("click", function () {
        let amount = parseFloat(fromCurrency.value);
        if (isNaN(amount)) {
            alert("Amount dao");
            return;
        }

        let usd = amount / rates[fromType.value];
        let result = usd * rates[toType.value];
        toCurrency.value = result.toFixed(2);
    });

});

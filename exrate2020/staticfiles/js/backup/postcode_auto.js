const ctlPostCode=document.querySelector("#postcode");
const ctlState=document.querySelector("#state");
const ctlTown=document.querySelector("#town");
const ctlStreet=document.querySelector("#street");

ctlPostCode.addEventListener("keyup",(e)=>{

    if (ctlPostCode.value.length === 7) {
        var url = "https://api.anko.education/zipcode?zipcode=" + ctlPostCode.value.trim();
        fetch(url)
        .then(function(response) {
            return response.json();
        })
        .then(function(address) {
            console.log(address);
            ctlState.value=address.pref;
            ctlTown.value=address.city;
            ctlStreet.value=address.area;

            // document.write(address.pref + address.city + address.area);
        });
    }
});

console.log("hello postcode autocomplete");
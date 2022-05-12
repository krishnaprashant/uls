$(document).ready(function(){
    $("#CountrySelect").change(function () {
        window.location.href = "/set-country/" + $(this).val();
    });
    $("#CitySelect").change(function () {
        window.location.href  += "/" +$(this).val();
    });
});

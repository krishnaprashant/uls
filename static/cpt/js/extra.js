$(document).ready(function(){
    $("#CountrySelect").change(function () {
        window.location.href = "/set-country/" + $(this).val();
    });
    $("#CitySelect").change(function () {
      var parts = $(location).attr('href').split("/");
      var country = parts[3];
      var url_parts = parts;
      if(country.length == 2 && url_parts.length == 7){
         redirect_to(parts[parts.length-2],$(this).val());         
      }
      if (country.length == 2 && url_parts.length == 6) {
         redirect_to(parts[parts.length-1],$(this).val());         
      }
    });

    function redirect_to(course,city){
      window.location.href  = "/set-city/"+course+"/"+city;
    }
});

console.log("hello, world")

//Callback handler for form submit event
$("#multiform").submit(function(e)
{
 
    var formObj = $(this);
    var formURL = formObj.attr("action");
    var formData = new FormData(this);
    $.ajax({
        url: formURL,
    type: 'POST',
        data:  formData,
    mimeType:"multipart/form-data",
    contentType: false,
        cache: false,
        processData:false,
    success: function(data, textStatus, jqXHR)
    {
 
    },
     error: function(jqXHR, textStatus, errorThrown) 
     {
     }          
    });
    e.preventDefault(); //Prevent Default action. 
    e.unbind();
}); 
$("#multiform").submit(); //Submit the form

function send_form(formData,formURL) {
    $.ajax({
      type: "POST",
      url: formURL,
      data: formData,
      mimeType:"multipart/form-data",
      processData: false,
      contentType: false,
      success: show_photo,
      dataType: 'json'
    });
}

function show_photo(data) {
  console.log(JSON.stringify(data));
  var url = '/getphoto?img_id='+data['url']
  img = $('<img>');
  img.attr('src',url)
  img.attr('alt','hello there')
  $('#photos').append(img);
}

$('form').submit(function(e){
  e.preventDefault();
  var formObj = $(this);
  var formURL = formObj.attr("action");
  var formData = new FormData(this);
  send_form(formData,formURL);
});
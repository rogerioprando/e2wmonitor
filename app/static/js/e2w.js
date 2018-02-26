$(document).ready(function() {

  $('#submit-btn').on('click', function() {
    $(this).addClass('disabled');
    $('#cancel-btn').addClass('btn waves-effect waves-light red').removeClass('disabled');
    //$('#loading-cmd').addClass('active');
    //$('#loading-cmd').show().addClass('active');
    //https://codehandbook.org/python-flask-jquery-ajax-post/
    /*var id = $('#id').val();
    var cmd = $('#command').val();
    $.ajax({
        url: '/send',
        data: $('form').serialize(),
        type: 'POST',
        success: function(response){
            console.log(response);
            },
        error: function(error){
            console.log(error);
            }
        });*/
    });

   // submit

  $('#cancel-btn').on('click', function() {
    $(this).addClass('disabled');
    $('#submit-btn').addClass('btn waves-effect waves-light').removeClass('disabled');
    //$('#loading-cmd').removeClass('active').addClass('preloader-wrapper small');
    //$('#loading-cmd').hide();
  }) // cancel

}); // document


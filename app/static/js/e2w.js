$(document).ready(function() {

    $('select').material_select();  // atualiza select input-field

        $('#submit-btn').on('click', function() {
            $(this).addClass('disabled');
            $('#cancel-btn').addClass('btn waves-effect waves-light red').removeClass('disabled');
            //$('#loading-cmd').addClass('active');
            //$('#loading-cmd').show().addClass('active');
        });

    $('#cancel-btn').on('click', function() {
        $(this).addClass('disabled');
        $('#submit-btn').addClass('btn waves-effect waves-light').removeClass('disabled');
        //$('#loading-cmd').removeClass('active').addClass('preloader-wrapper small');
        //$('#loading-cmd').hide();
    });

    /*
    GUARDAR ESSAS PARADAS
    // teste para inserção do select input-field (fazer isso via ajax)
    // pegar o devices_list do server para atualizar o input field:
    var selectValues = { "1": "test 1", "2": "test 2" };

    $.each(selectValues, function(key, value) {
        $('#select-input-xvm-id')
            .append($('<option>', { value : key })
            .text(value));
    });

    $.get('/show_devices', function(result){
        console.log('Devices:' + result.devices_list);
    });

    $('select').material_select(); // atualiza select input-field

    */

    $('#form-send-command').submit(function(event) {
        event.preventDefault();

        var check = 'False'
        if($('#filled-in-box').is(':checked'))
        {
            check = 'True'
        }
        var data = ({
            "id_xvm": $('#select-input-xvm-id option:selected').text(),
            "cmd_xvm": $('#cmd-xvm').val(),
            "mdt_xvm": check
        });

        // temporario:
        var id_solicitado = $('#select-input-xvm-id option:selected').text()

        //var foo2 = $('#select-input-xvm-id option:selected').val();
        //alert(foo2.toString())

        console.log(JSON.stringify(data))

        $.ajax({
            type: 'POST',
            url: '/send',
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            context: this,
            success: function(callback) {
                console.log(callback);
                $('#submit-btn').removeClass('disabled').addClass('btn waves-effect waves-light');
                $('#cancel-btn').addClass('btn waves-effect waves-light red disabled');
                //$('#ans-xvm').text(callback.ans_request);
                $('#tbody-result-table').empty();
                //alert(callback.ans_request)
                for (var i = 0; i <callback.ans_request.length; i ++) {
                    $('#result-table').append('<tr><td>' + callback.ans_request[i] + '</td></tr>');
                }
            },
            error: function() {
            $(this).html("error!");
            }
        });

    });
});


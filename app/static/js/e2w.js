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

        $("#form-send-command button").click(function (ev) {
        ev.preventDefault() // cancel form submission

        if ($(this).attr("value") == "send") {

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
                    for (var i = callback.ans_request.length; i > 0; i--) {
                        if ((callback.ans_request[i-1]) != 'request cancelled' && (callback.ans_request[i-1]) != 'busy' && (callback.ans_request[i-1]) != 'timeout') {
                            $('#result-table').append('<tr><td>' + callback.ans_request[i-1] + '</td></tr>');
                        }
                    }
                    if ((callback.ans_request[callback.ans_request.length - 1]) == 'busy')
                    {
                        Materialize.toast('Unidade Ocupada !', 4000)
                    }
                    else if ((callback.ans_request[callback.ans_request.length - 1]) == 'timeout')
                    {
                        Materialize.toast('Timeout !', 4000)
                    }
                    else if ((callback.ans_request[callback.ans_request.length -1]) == 'request cancelled')
                    {
                        Materialize.toast('Comando Cancelado !', 4000)
                    }
                },
                error: function() {
                //$(this).html("error!");
                Materialize.toast('Erro desconhecido!', 4000)
                }
            });

        }

        if ($(this).attr("value") == "cancel") {

            var data = ({
                "id_xvm": $('#select-input-xvm-id option:selected').text(),
                "cmd_xvm": $('#cmd-xvm').val(),
                "mdt_xvm": check
            });

            $.ajax({
                type: 'POST',
                url: '/cancel',
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(data),
                context: this,
                success: function(callback) {
                    console.log(callback);
                    //alert('ID Cancelado:'+callback.id_cancelled)
                },
                error: function() {
                    $(this).html("cancel error!");
                }
            });
        }
    });

});


$(document).ready(function() {

    $('select').material_select();  // atualiza select input-field

    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year,
        show_months_full: false,
        today: 'Hoje',
        clear: 'Limpar',
        close: 'Ok',
        format_submit: 'yyyy-mm-dd',
        closeOnSelect: false // Close upon selecting a date,
    });

    $('.timepicker').pickatime({
        default: 'now', // Set default time: 'now', '1:30AM', '16:30'
        fromnow: 0,       // set default time to * milliseconds from now (using with default = 'now')
        twelvehour: false, // Use AM/PM or 24-hour format
        donetext: 'OK', // text for done-button
        cleartext: 'Limpar', // text for clear-button
        canceltext: 'Cancelar', // Text for cancel-button
        autoclose: false, // automatic close timepicker
        ampmclickable: true, // make AM PM clickable
        aftershow: function(){} //Function for after opening timepicker
    });

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
                "mdt_xvm": check,
                "timeout_xvm" : $('#timeout-slider').val(),
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


    $("#form-send-query button").click(function(ev) {
    ev.preventDefault() // cancel form submission
    console.log('button query')


        if ($(this).attr("value") == "send") {
            console.log('if send')

            var data = ({
                "client": $('#select-input-client option:selected').text(),
                "wplex_id": $('#select-input-wplexid option:selected').text(),
                "prefix": $('#select-input-prefix option:selected').text(),
                "start_dt": $('#start-datetime').val(),
                "end_dt": $('#end-datetime').val(),
            });

            console.log(JSON.stringify(data));
            alert(JSON.stringify(data))
            $.ajax({
                type: 'POST',
                url: '/dashboard',
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(data),
                context: this,
                success: function(callback) {
                    console.log(callback);
                    console.log('sucesso ajax');
                    $('#test-result').html(callback);
                },
                error: function() {
                    console.log('erro ajax')
                    $(this).html("cancel error!");
                }
            });

        }

        if ($(this).attr("value") == "cancel") {
            // quando foi cancelada a consulta
            // habilita botão enviar
            // desabilita botão cancelar
            // ajax post method
        }

    });

});


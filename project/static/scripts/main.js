$(document).ready(function(){

    var socket = io();
    socket.on('connect', function() {
        socket.emit("get_schedule");
        socket.emit("get_all_modes");
    });

    socket.on('all_modes', function(data){
        $.each(data, function(id, mode){
            $('.choice_mode').append($('<option>', {
                value: id,
                text: mode
            }));
        });
    });

    $('.wd_container').on("click", ".add", function(){
        $('.weekday_choice').val($(this).data('weekday'));
        $('.overlay').show();
    });

    $('.wd_container').on("click", ".remove", function(){
        socket.emit('remove', $(this).parent().attr("id"));
        $(this).parent().remove();
    });

    $('.overlay').on("click", function(e){
        if (e.target == this){
            $('.overlay').hide();
        }

    });

    $('.confirm').click(function(){
        socket.emit('add', {"weekday": $('.weekday_choice').find(":selected").val(),
                            "time": $('.time').val(),
                            "mode": $('.choice_mode').find(":selected").val()
                            });
        $('.overlay').hide();
    });

    socket.on('get_schedule', function(data){
        $(".wd_container").empty();
        for(wd in data){
            $(".wd_container").append('<h3 data-weekday='+ wd +'>'+ data[wd]["name"]+'</h3>')
            $(".wd_container").append('<div id="item_'+ wd +'" class="items-row"></div>')
             data[wd]["schedule"].map(function(elem){
                $("#item_" + wd).append('<div id="'+ elem["id"] + '" class="item"></div>')
                $("#" + elem["id"]).append('<div id="type_'+ elem["id"] +'" class="type">'+ elem["type"] + '</div>')
                $("#type_" + elem["id"]).css("color", "rgb("+elem["red"]+", "+elem["green"]+", "+elem["blue"]+")")
                $("#" + elem["id"]).append('<div class="time">' + elem["time"] + '</div>')
                $("#" + elem["id"]).append('<div class="remove" title="Удалить режим">+</div>')
            })
            $("#item_" + wd).append('<div data-weekday='+ wd +' class="item add" title="Добавить режим">+</div>')
        }
        console.log(data[wd]);
    });

    socket.on('telemetry', function(data){
        $(".conv").text(data["conv"] + " mPm");
        $(".fan").text(data["fan"] + " rPm");
        $(".heater").text(data["heater"] + " °С");
        $(".light").attr("class", "light "+ data["light"]);
    });

    socket.on('status', function(data){
        $(".current").text(data["current"]);
        $(".time_now").text(data["time_now"]);
        $(".ending").text(data["ending"]);
        $(".next").text(data["next"]);
    });
});
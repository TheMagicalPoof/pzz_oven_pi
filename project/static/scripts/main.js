
$(document).ready(function(){
    var socket = io.connect("http://localhost/sock");
    socket.on("web", function(){
        socket.emit("web", {"HelloWorld"})});
});
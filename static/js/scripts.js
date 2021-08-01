

defaultConsole = `<span class="preDim">
• ▌ ▄ ·.  ▄· ▄▌▄▄▄▄▄ ▄ .▄      .▄▄ · 
·██ ▐███▪▐█▪██▌•██  ██▪▐█▪     ▐█ ▀. 
▐█ ▌▐▌▐█·▐█▌▐█▪ ▐█.▪██▀▐█ ▄█▀▄ ▄▀▀▀█▄
██ ██▌▐█▌ ▐█▀·. ▐█▌·██▌▐▀▐█▌.▐▌▐█▄▪▐█
▀▀  █▪▀▀▀  ▀ •  ▀▀▀ ▀▀▀ · ▀█▄▀▪ ▀▀▀▀ 

<u>Welcome to Mythos RPG</u>

Author      Will D. Vokins
Version     0.0.1
Updated     09:10 2021-08-01 GMT

</span>
`
            // Automate form submission with Enter key.
            $(function() {
                $('#commandLine').each(function() {
                    $(this).find('input').keypress(function(e) {
                        // Enter pressed?
                            if(e.which == 10 || e.which == 13) {
                                currentConsole = $("#output").html()
                                currentCommand = $("#commandInput").val()
                                $("#commandInput").val("")
                                if(currentCommand != ""){
                                    $("#output").html(currentConsole + "\n\n<span class='preDim'>&gt; " + currentCommand + "</span>");
                                    if(currentCommand.toLowerCase() == "clear" || currentCommand.toLowerCase() == "cls"){
                                        $("#output").html(defaultConsole);
                                    }else{
                                        $.ajax({
                                        url: "/command",
                                        method: "POST",
                                        data:{
                                            command: currentCommand
                                        },
                                        success: function(data) {
                                            currentConsole = $("#output").html()
                                            if (data !== null && data !== undefined) {
                                                $("#output").html(currentConsole + "\n" + data);
                                                var outputPre = document.getElementById("output");
                                                outputPre.scrollTop = outputPre.scrollHeight;
                                            }
                                        }
                                    });
                                    }
                                }
                            }
                    });
                });
            });
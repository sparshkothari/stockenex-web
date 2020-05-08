var Register = {
    init : function(){
        this.register();
    },
    register: function() {
        document.getElementById("submit").addEventListener("click", function() {
            $.post("/register",

                    {
                        name: document.getElementById("name").value,
                        username: document.getElementById("username").value,
                        password: document.getElementById("password").value,
                        email: document.getElementById("email").value

                    }
                )
                .done(function(data, status) {
                    vex.dialog.buttons.YES.text = "Okay";

                    vex.dialog.alert({
                        message: 'You successfully created an account!',
                        callback: function(value) {
                            window.location.href = "/profile";

                        }

                    })
                })
                .fail(function() {
                    vex.dialog.buttons.YES.text = "Okay";
                    vex.dialog.alert('The chosen username is already registered.');

                });




        }, false);

    }

}

Register.init()
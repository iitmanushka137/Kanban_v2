<template>
    <div class="register" style="position:relative; min-height: 100vh; margin: 0px; background: linear-gradient(to bottom, #DCBF0A 0%, #3B3303 100%);">
    <div align="middle">
        <p class="alert alert-danger" v-if="error_1">{{error_1}}</p>
    </div>
    <div align="middle" style="left:460px; top: 40px; position: absolute; margin: 60px; box-shadow:10px 10px 15px 15px #FAF136; background: #BFC833">
    <h1 style="color: black;">Kanban</h1>
    <div class="container" style="font-size: 1.5rem; display: inline-block; margin: 10px 50px 20px;">
        <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Email ID  </strong></label>
            <input type="email" name="email" v-model="email" placeholder="Please enter a valid email..." style="height: 20px" required/>
        </div>
        <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Username</strong></label>
            <input type="text" name="username" v-model="username" placeholder="Please enter a valid username..." minlength="3" title="Username should be of atleast 3 characters" style="height: 20px" required/>
        </div>
        <div class="row" style="position: relative; margin: 50px 48px 50px;">
            <label style="color: black"><strong>Password</strong></label>
            <input type="password" name="password" v-model="password" placeholder="Please enter a valid password..." minlength="8" title="Password should have atleast 8 characters" style="height: 20px" required/>
        </div>
    </div>
    <div class="row" style="margin: 10px 48px 20px;"></div>
    <button style="padding: 14px 40px; background-color: white; color: red; font-size: 1.5rem; border: 2px solid black; border-radius: 50%;" type="submit" @click="register()">Register</button>
    <p style="color: black">
        <strong>Already registered ?  </strong>
        <router-link :to="{name: 'login'}">Log in</router-link>
    </p>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'RegisterPage',
        data() {
            return{
                email: null,
                username: null,
                password: null,
                error_1: ""
            }
        },
        async created() {
            sessionStorage.clear()
            localStorage.clear()
        },
        async updated() {
            sessionStorage.clear()
            localStorage.clear()
        },
        methods: {
            async register() {
                if(this.emailValidation(this.email) && this.passValidation(this.password)){
                try {
                    fetch("http://127.0.0.1:5000/api/user",{
                        method: "POST",
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            email: this.email, 
                            username: this.username, 
                            password: this.password 
                        })
                    }).then((response) => response.json())
                    .then(async (data) =>{
                        console.log(data)
                        this.$router.go(-1)
                    }).catch((err) => {
                        console.log(err)
                    })
                }
                catch (error) {
                    console.log("Registration Failed: ",error)
                }
            }else if(!this.emailValidation(this.email)){
                this.error_1 = "Please enter a valid email"
            }else if(!this.passValidation(this.password)){
                this.error_1 = "Password requires atleast 8 characters."
            }},
            emailValidation: function (email){
                var result = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,3}))$/;
                return result.test(email)
            },
            passValidation: function (passs){
                var result = /.{8,}/
                return result.test(passs)
            }
        }
    }

</script>
